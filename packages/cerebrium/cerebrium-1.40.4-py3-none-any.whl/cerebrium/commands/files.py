import concurrent.futures
import concurrent.futures
import datetime
import math
import os
from typing import Dict

import bugsnag
import humanize
import requests
import typer
from rich import print
from rich.table import Table
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

from cerebrium.api import cerebrium_request
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.project import get_current_project_context

CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")

cli = typer.Typer()

from typing import Optional


def ls_files(path: Optional[str] = typer.Argument("/", help="Remote path to list contents")):
    """
        List contents of persistent storage. Run `cerebrium ls --help` for more information.\n
    \n
        Usage: cerebrium ls [OPTIONS] [REMOTE_PATH]\n
    \n
          List contents of persistent storage.\n
    \n
        Options:\n
          -h, --help          Show this message and exit.\n
    \n
        Examples:\n
          # List all files in the root directory\n
          cerebrium ls\n
    \n
          # List all files in a specific directory\n
          cerebrium ls sub_folder/\n
    """
    project_id = get_current_project_context()
    response = cerebrium_request(
        "GET", f"v2/projects/{project_id}/volumes/default/ls", {"dir": path}, requires_auth=True
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"There was an error listing your files: {response.text}. Please login again and, if the problem persists, contact support.",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    data = response.json()

    table = Table(show_header=True, header_style="bold yellow")

    table.add_column("Name", style="dim")
    table.add_column("Size", style="dim", width=15)
    table.add_column("Last Modified", width=20)

    if not data or len(data) == 0:
        print("[yellow]No files found.[/yellow]")
        raise typer.Exit(0)

    for item in data:
        name = item["name"]
        size = (
            humanize.naturalsize(item.get("size_bytes", 0))
            if not item["is_folder"]
            else "Directory"
        )
        last_modified = item["last_modified"]
        if last_modified == "0001-01-01T00:00:00Z":
            last_modified = "N/A"
        else:
            last_modified = datetime.datetime.fromisoformat(
                last_modified.replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M:%S")

        table.add_row(name, size, last_modified)

    print(table)


def upload_single_file(src, dest, project_id, part_size_mb=50, pbar=None):
    file_size = os.path.getsize(src)
    part_size = part_size_mb * 1024 * 1024
    part_count = math.ceil(file_size / part_size)

    response = cerebrium_request(
        "POST",
        f"v2/projects/{project_id}/volumes/default/cp/initialize",
        {"file_path": dest, "part_count": part_count},
        requires_auth=True,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to initiate file copy: {response.text}",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    data = response.json()
    upload_id = data["upload_id"]
    parts = data["parts"]

    tqdm.write(f"Uploading {src} to {dest} ...")

    if part_count == 0 and file_size == 0:
        tqdm.write(f"File {src} uploaded successfully to {dest}")
        return typer.Exit(0)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(8),
        retry=lambda e: isinstance(e, requests.HTTPError),
        retry_error_callback=lambda e: typer.Exit(1),
    )
    def upload_part(part) -> Dict[str, str]:
        part_number = part["part_number"]
        url = part["url"]
        with open(src, "rb") as file:
            file.seek((part_number - 1) * part_size)
            part_data = file.read(part_size)
        put_response = requests.put(url, data=part_data)
        uploaded_size = len(part_data)

        try:
            put_response.raise_for_status()
        except requests.HTTPError as e:
            tqdm.write(f"Failed to upload part {part_number}: {e}, retrying...")
            raise e

        if pbar:
            pbar.update(uploaded_size)

        return {"part_number": part_number, "etag": put_response.headers["ETag"]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        uploaded_parts = list(executor.map(upload_part, parts))

    response = cerebrium_request(
        "POST",
        f"v2/projects/{project_id}/volumes/default/cp/complete",
        {
            "upload_id": upload_id,
            "file_path": dest,
            "parts": uploaded_parts,
        },
        requires_auth=True,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to complete file copy: {response.text}",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    tqdm.write(f"File {src} uploaded successfully to {dest}")


def cp_file(
    src: str = typer.Argument(..., help="Path to the source file or directory to be uploaded."),
    dest: str = typer.Argument(
        None, help="Destination path on the server where the file(s) should be uploaded."
    ),
):
    """
        Copy contents to persistent storage. Run `cerebrium cp --help` for more information.\n
    \n
        Usage: cerebrium cp [OPTIONS] LOCAL_PATH REMOTE_PATH (Optional)\n
    \n
          Copy contents to persistent storage.\n
    \n
        Options:\n
          -h, --help          Show this message and exit.\n
    \n
        Examples:\n
          # Copy a single file\n
          cerebrium cp src_file_name.txt # copies to /src_file_name.txt\n
    \n
          cerebrium cp src_file_name.txt dest_file_name.txt # copies to /dest_file_name.txt\n
    \n
          # Copy a directory\n
          cerebrium cp dir_name # copies to the root directory\n
          cerebrium cp dir_name sub_folder/ # copies to sub_folder/\n
    """
    project_id = get_current_project_context()

    if dest is None:
        # Set the destination to the root directory or to a name based on the source
        if os.path.isdir(src):
            dest = "/"
        else:
            dest = f"/{os.path.basename(src)}"

    total_size = 0
    file_paths = []

    if os.path.isdir(src):
        for root, _, files in os.walk(src):
            for file_name in files:
                file_src = os.path.join(root, file_name)
                file_size = os.path.getsize(file_src)
                total_size += file_size
                file_dest = os.path.join(dest, os.path.relpath(file_src, src))
                file_paths.append((file_src, file_dest))
    else:
        file_size = os.path.getsize(src)
        total_size += file_size
        file_paths.append((src, dest))

    with tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        colour="#EB3A6F",
        ncols=100,
    ) as pbar:
        for file_src, file_dest in file_paths:
            upload_single_file(file_src, file_dest, project_id, pbar=pbar)


def human_readable_size(size, decimal_places=2):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0
    return f"{size:.{decimal_places}f} PB"


def download_single_file(src, dest, project_id):
    """
    Download a single file from persistent storage.

    Args:
        src (str): Remote path to the file to download
        dest (str): Local path where the file should be saved
        project_id (str): Project ID to use for the API request
    """
    response = cerebrium_request(
        "GET",
        f"v2/projects/{project_id}/volumes/default/download",
        {"file_path": src},
        requires_auth=True,
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to get download URL: {response.text}",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    try:
        download_url = response.json().get("url")
        if not download_url:
            cerebrium_log(
                level="ERROR",
                message="Failed to get download URL from response",
                prefix="",
            )
            bugsnag.notify(Exception("No download URL in response"))
            raise typer.Exit(1)
    except ValueError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to parse response: {e}",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)

    download_response = requests.get(download_url, stream=True)
    try:
        download_response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to download file.",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    total_size = int(download_response.headers.get("content-length", 0))

    tqdm.write(f"Downloading {src} to {dest} ...")

    with open(dest, "wb") as f:
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            colour="#EB3A6F",
            ncols=100,
        ) as pbar:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(len(chunk))

    tqdm.write(f"File {src} downloaded successfully to {dest}")


def download_file(
    src: str = typer.Argument(..., help="Remote path to the file to be downloaded."),
    dest: str = typer.Argument(
        None, help="Local destination path where the file should be saved."
    ),
):
    """
        Download a file from persistent storage. Run `cerebrium download --help` for more information.\n
    \n
        Usage: cerebrium download [OPTIONS] REMOTE_PATH [LOCAL_PATH]\n
    \n
          Download a file from persistent storage.\n
    \n
        Options:\n
          -h, --help          Show this message and exit.\n
    \n
        Examples:\n
          cerebrium download file_name.txt\n
    \n
          cerebrium download file_name.txt local_file_name.txt\n
    \n
          cerebrium download sub_folder/file_name.txt\n
    """
    project_id = get_current_project_context()

    if dest is None:
        dest = os.path.basename(src)

    download_single_file(src, dest, project_id)


def rm_file(
    remote_path: str = typer.Argument(..., help="Path to the file or directory to be removed.")
):
    """
        Remove a file or directory from persistent storage. Run `cerebrium rm --help` for more information.\n
    \n
        Usage: cerebrium rm [OPTIONS] REMOTE_PATH\n
    \n
          Remove a file or directory from persistent storage.\n
    \n
        Options:\n
          -h, --help          Show this message and exit.\n
    \n
        Examples:\n
          # Remove a specific file\n
          cerebrium rm /file_name.txt\n
          cerebrium rm /sub_folder/file_name.txt\n
    \n
          # Remove a directory and all its contents\n
          cerebrium rm /sub_folder/ # Note that it must end with a forward slash /\n
          cerebrium rm / # Removes all files in the root directory\n
    """
    project_id = get_current_project_context()
    response = cerebrium_request(
        "DELETE",
        f"v2/projects/{project_id}/volumes/default/rm",
        {"file_path": remote_path},
        requires_auth=True,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to remove file: {response.text}",
            prefix="",
        )
        bugsnag.notify(e)
        raise typer.Exit(1)

    print(f"[green]{remote_path} removed successfully.[/green]")
