import json
import os
import struct
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from typing import Literal, Any, cast, IO

import bugsnag
import jwt
import requests
import typer
import yaml
from rich import print
from tenacity import retry, stop_after_delay, wait_fixed
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from cerebrium.config import CerebriumConfig
from cerebrium.files import CONFIG_PATH
from cerebrium.types import JSON
from cerebrium.utils.files import detect_dev_folders
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.project import get_current_project_context
from cerebrium.utils.sync_files import make_cortex_dep_files
from cerebrium.utils.termination import _graceful_shutdown

CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")

if CEREBRIUM_ENV == "local":
    api_url_v2 = os.getenv("REST_API_URL", "http://localhost:4100")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://dev-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "207hg1caksrebuc79pcq1r3269")
    dashboard_url = "http://localhost:4100"
elif CEREBRIUM_ENV == "dev":
    api_url_v1 = os.getenv("REST_API_URL", "https://dev-rest-api.cerebrium.ai")
    api_url_v2 = os.getenv("REST_API_URL", "https://dev-rest.cerebrium.ai")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://dev-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "207hg1caksrebuc79pcq1r3269")
    dashboard_url = "https://dev-dashboard.cerebrium.ai"
else:
    api_url_v1 = os.getenv("REST_API_URL", "https://rest-api.cerebrium.ai")
    api_url_v2 = os.getenv("REST_API_URL", "https://rest.cerebrium.ai")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://prod-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "2om0uempl69t4c6fc70ujstsuk")
    dashboard_url = "https://dashboard.cerebrium.ai"


def is_logged_in() -> str | None:
    """
    Check if a user's JWT token has expired. If it has, make a request to Cognito with the refresh token to generate a new one.

    Returns:
        str: The new JWT token if the old one has expired, otherwise the current JWT token.
    """
    # Assuming the JWT token is stored in a config file
    if not os.path.exists(CONFIG_PATH):
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        bugsnag.notify(Exception("User not logged in"))
        return None

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f) or {}

    if config is None:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        bugsnag.notify(Exception("User not logged in"))
        return None

    key_name = "" if CEREBRIUM_ENV == "prod" else f"{CEREBRIUM_ENV}-"

    jwt_token: str = config.get(f"{key_name}accessToken", "")
    refresh_token: str = config.get(f"{key_name}refreshToken", "")
    if not jwt_token:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        bugsnag.notify(Exception("User not logged in"))
        return None

    # Decode the JWT token without verification to check the expiration time
    try:
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
    except Exception as e:
        cerebrium_log(level="ERROR", message=f"Failed to decode JWT token: {str(e)}", prefix="")
        bugsnag.notify(Exception("Failed to decode JWT token."))
        return None  # Check if the token has expired
    if datetime.fromtimestamp(payload["exp"]) < datetime.now():
        # Token has expired, request a new one using the refresh token
        response = requests.post(
            auth_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "refresh_token": refresh_token,
            },
            timeout=30,
        )
        if response.status_code == 200:
            new_jwt_token = response.json()["access_token"]
            # Update the config file with the new JWT token
            config[f"{key_name}accessToken"] = new_jwt_token
            with open(CONFIG_PATH, "w", newline="\n") as f:
                yaml.safe_dump(config, f)
            return new_jwt_token
        else:
            cerebrium_log(
                level="ERROR",
                message="Failed to refresh JWT token. Please login again.",
                prefix="",
            )
            bugsnag.notify(Exception("Failed to refresh JWT token."))
            return None
    else:
        # Token has not expired, return the current JWT token
        return jwt_token


@retry(stop=stop_after_delay(60), wait=wait_fixed(8))
def cerebrium_request(
    http_method: Literal["GET", "POST", "DELETE", "PATCH"],
    url: str,
    payload: dict[str, JSON] = {},
    requires_auth: bool = True,
    headers: dict[str, str] = {"ContentType": "application/json"},
    v1: bool = False,
) -> requests.Response:
    """
    Make a request to the Cerebrium API and check the response for errors.

    Args:
        http_method ('GET', 'POST', 'DELETE'): The HTTP method to use (GET, POST or DELETE).
        url (str): The url after the base url to use.
        payload (dict, optional): The payload to send with the request.
        requires_auth (bool): If the api call requires the user to be authenticated
        headers (dict, optional): By default, content-type is application/json so this is used to override
        v1 (bool, optional): If the request is to the v1 API. Defaults to False.

    Returns:
        dict: The response from the request.
    """
    if requires_auth:
        access_token = is_logged_in()
        if not access_token:
            sys.exit(1)

        payload["projectId"] = get_current_project_context()

    else:
        access_token = None

    url = f"{api_url_v1 if v1 else api_url_v2}/{url}"

    if access_token:
        headers["Authorization"] = f"{access_token}"

    data = None if payload is None else json.dumps(payload)
    if http_method == "POST":
        resp = requests.post(url, headers=headers, data=data, timeout=30)
    elif http_method == "GET":
        resp = requests.get(
            url,
            headers=headers,
            params=payload,
            timeout=30,
        )
    elif http_method == "DELETE":
        resp = requests.delete(url, headers=headers, params=payload, data=data, timeout=30)
    elif http_method == "PATCH":
        resp = requests.patch(url, headers=headers, params=payload, data=data, timeout=30)
    else:
        cerebrium_log(
            level="ERROR",
            message="Invalid HTTP method. Please use 'GET', 'POST', 'DELETE' or 'PATCH'.",
            prefix="",
        )
        bugsnag.notify(Exception("Invalid HTTP method."))
        sys.exit(1)

    if resp.status_code == 402:
        # Handle 402 Payment Required error
        message = resp.json().get(
            "message", "Payment required. Check your project plan or billing status."
        )
        cerebrium_log(
            level="ERROR",
            message=message,
            prefix="",
        )
        bugsnag.notify(Exception(message))
        sys.exit(1)

    return resp


# Define size limits
WARNING_SIZE_LIMIT = 1 * 1024 * 1024 * 1024  # 1GB in bytes
ERROR_SIZE_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB in bytes


def upload_cortex_files(
    build_id: str,
    cerebrium_config: CerebriumConfig,
    upload_url: str,
    zip_file_name: str,
    config: CerebriumConfig,
    file_list: list[str],
    source: Literal["serve", "cortex"] = "cortex",
    disable_animation: bool = False,
) -> bool:
    if file_list == []:
        cerebrium_log(
            level="ERROR",
            message="No files to upload.",
            prefix="Error uploading app to Cerebrium:",
        )
        raise typer.Exit(1)

    # Check for development folders in the root directory
    detected_dev_folders = detect_dev_folders(file_list)
    if detected_dev_folders:
        folders_str = ", ".join(f"'{folder}'" for folder in detected_dev_folders)
        cerebrium_log(
            level="WARNING",
            message=f"Development folder(s) {folders_str} detected in the root directory. "
            f"Including development folders is not recommended as they can significantly "
            f"increase upload size. They can be excluded in the cerebrium.toml file.",
            prefix="Warning:",
        )

    def add_utc_timestamp(zip_info: zipfile.ZipInfo, dt: datetime) -> None:
        # Convert the timezone-aware datetime to a Unix timestamp (UTC)
        timestamp = int(dt.timestamp())
        # Build the extra field: header ID 0x5455, data length 5, flag 1, then 4 bytes of timestamp.
        extra_field = struct.pack("<HHBI", 0x5455, 5, 1, timestamp)
        zip_info.extra = extra_field

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, zip_file_name)
            make_cortex_dep_files(working_dir=temp_dir, config=config)
            tmp_dep_files = os.listdir(temp_dir)
            with zipfile.ZipFile(zip_path, "w") as zip_file:
                print(f"Zipping {len(file_list)} file(s)...")

                # Process temporary dependency files.
                for f in tmp_dep_files:
                    full_path = os.path.join(temp_dir, f)
                    st = os.stat(full_path)
                    dt = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                    # Use the file name relative to the temp directory.
                    zi = zipfile.ZipInfo(f, date_time=time.gmtime(st.st_mtime)[:6])
                    add_utc_timestamp(zi, dt)
                    if os.path.isfile(full_path):
                        with open(full_path, "rb") as fp:
                            file_data = fp.read()
                        zip_file.writestr(zi, file_data)
                    elif os.path.isdir(full_path):
                        zip_file.writestr(zi, b"")

                # Process files from file_list.
                for f in file_list:
                    # Skip files already added from the temporary directory.
                    if f in tmp_dep_files:
                        continue
                    if os.path.isfile(f):
                        st = os.stat(f)
                        dt = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                        # Use the full relative path to preserve folder structure.
                        zi = zipfile.ZipInfo(f, date_time=time.gmtime(st.st_mtime)[:6])
                        add_utc_timestamp(zi, dt)
                        with open(f, "rb") as fp:
                            file_data = fp.read()
                        zip_file.writestr(zi, file_data)
                    elif os.path.isdir(f) and len(os.listdir(f)) == 0:
                        st = os.stat(f)
                        dt = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                        zi = zipfile.ZipInfo(f, date_time=time.gmtime(st.st_mtime)[:6])
                        add_utc_timestamp(zi, dt)
                        zip_file.writestr(zi, b"")

            # Check the zip file size
            zip_size = os.path.getsize(zip_path)
            if zip_size > ERROR_SIZE_LIMIT:
                cerebrium_log(
                    level="ERROR",
                    message="Your project zip file is over 2GB. Please use the cerebrium cp command to upload files instead.",
                    prefix="Error uploading app to Cerebrium:",
                )
                bugsnag.notify(Exception("Zip file is over 2GB"), severity="error")
                raise typer.Exit(1)
            elif zip_size > WARNING_SIZE_LIMIT:
                cerebrium_log(
                    level="WARNING",
                    message="Your project zip file is over 1GB. Your deployment should work but might encounter issues. Please consider using the cerebrium cp command if you encounter issues.",
                    prefix="Warning:",
                )
                bugsnag.notify(Exception("Zip file is over 1GB"), severity="warning")
            print("Uploading to Cerebrium...")

            with open(zip_path, "rb") as f:
                headers = {"Content-Type": "application/zip"}
                if not disable_animation:
                    with tqdm(
                        total=zip_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        colour="#EB3A6F",
                        ncols=100,
                    ) as pbar:
                        wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                        upload_response = requests.put(
                            upload_url,
                            headers=headers,
                            data=cast(IO[bytes], wrapped_f),
                            timeout=60,
                        )
                else:
                    upload_response = requests.put(
                        upload_url, headers=headers, data=f, timeout=60
                    )

            if upload_response.status_code != 200:
                bugsnag.notify(
                    Exception(f"Error uploading app to Cerebrium\n{upload_response.json()}")
                )
                cerebrium_log(
                    level="ERROR",
                    message=f"Error uploading app to Cerebrium\n{upload_response.json().get('message')}",
                    prefix="",
                )
                raise typer.Exit(1)
            if source == "cortex":
                print("Resources uploaded successfully.")
            return True

    except KeyboardInterrupt:
        _graceful_shutdown(
            app_name=cerebrium_config.deployment.name,
            build_id=build_id,
            is_interrupt=True,
        )
        raise typer.Exit(1)


# Function to get the logs from the API
def fetch_build_logs(app_name: str, build_id: str) -> dict[str, Any]:
    """
    Fetches the build logs from the API.

    Args:
        app_name (str): The app name.
        build_id (str): The build ID.

    Returns:
        dict: The response JSON containing the logs and build status.
    """
    project_id = get_current_project_context()

    response = cerebrium_request(
        "GET",
        f"v2/projects/{project_id}/apps/{project_id}-{app_name}/builds/{build_id}/logs",
        {},
    )

    if response is None or response.status_code != 200:
        error_message = (
            "Error streaming logs. Please check your internet connection. If this issue persists, please contact support."
            if response is None
            else f"Error streaming logs\n{response.json().get('message')}"
        )
        cerebrium_log(level="ERROR", message=error_message, prefix="")
        bugsnag.notify(Exception(error_message))
        raise typer.Exit(1)

    return response.json()
