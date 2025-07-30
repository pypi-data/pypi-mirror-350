import json
import os
import threading
from queue import Queue
from time import sleep

import bugsnag
import requests
import typer
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from cerebrium.api import cerebrium_request
from cerebrium.commands.logs import fetch_logs
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.project import get_current_project_context

run_app = typer.Typer(no_args_is_help=True)
console = Console()


def get_cerebrium_jwt(project_id):
    try:
        # Make a GET request to retrieve the API keys
        api_keys_response = cerebrium_request(
            "GET", f"v2/projects/{project_id}/api-keys", requires_auth=True
        )

        if api_keys_response is None or api_keys_response.status_code != 200:
            raise ValueError("Failed to retrieve API keys from the endpoint.")

        # Assuming the 'cerebrium_jwt' is among the items
        for key in api_keys_response.json():
            if key.get("source") == "cerebrium_jwt":
                jwt = key.get("apiKey")
                if jwt:
                    return jwt
        raise ValueError("cerebrium_jwt not found in the API keys.")

    except Exception as e:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to retrieve cerebrium_jwt from the endpoint: {e}",
            prefix="",
        )
        raise typer.Exit(1)


def get_api_base_url():
    env = os.environ.get("CEREBRIUM_ENV", "prod")
    if env == "dev":
        return "https://dev-api.cortex.cerebrium.ai"
    else:
        return "https://api.cortex.cerebrium.ai"


def get_run_status(project_id: str, app_id: str, run_id: str):
    run_response = cerebrium_request(
        "GET", f"v2/projects/{project_id}/apps/{app_id}/runs/{run_id}", {}, requires_auth=True
    )

    if run_response is None or run_response.status_code != 200:
        cerebrium_log(
            level="ERROR",
            message=f"Failed to retrieve run status for app {app_id} and run {run_id}.",
            prefix="",
        )
        raise typer.Exit(1)

    return run_response.json().get("item", {}).get("status", "unknown")


def display_run_status_and_logs(project_id: str, app_id: str, run_id: str):
    """
    Display run status and logs concurrently using Rich Live Layout.
    """
    stop_event = threading.Event()
    logs_queue = Queue()
    status_var = {"status": "Unknown"}  # Shared status variable
    last_log_timestamp = None

    layout = Layout()
    layout.split(
        Layout(name="status", size=3),
        Layout(name="logs", size=14),
    )

    def fetch_and_update_status():
        """
        Fetch and update the run status in the status_var.
        """
        try:
            while not stop_event.is_set():
                # Fetch the run status
                status = get_run_status(project_id, app_id, run_id)
                # Update the status variable
                status_var["status"] = status

                sleep(2)
        except KeyboardInterrupt:
            stop_event.set()
            console.print("\n[bold yellow]Stopped checking run status.[/bold yellow]")

    def fetch_logs_worker():
        """
        Fetch logs and add them to the logs queue.
        """
        nonlocal last_log_timestamp
        try:
            while not stop_event.is_set():
                logs_data, last_log_timestamp = fetch_logs(
                    project_id, app_id, run_id, last_log_timestamp
                )
                if logs_data:
                    for log_entry in logs_data:
                        logs_queue.put(log_entry)
                sleep(2)
        except KeyboardInterrupt:
            stop_event.set()
            console.print("\n[bold yellow]Stopped fetching logs.[/bold yellow]")

    # Start threads for fetching status and logs
    status_thread = threading.Thread(target=fetch_and_update_status, daemon=True)
    logs_thread = threading.Thread(target=fetch_logs_worker, daemon=True)

    status_thread.start()
    logs_thread.start()

    logs_buffer = []

    with Live(layout, refresh_per_second=4) as live:
        while not stop_event.is_set() or not logs_queue.empty():
            # Update status panel
            layout["status"].update(
                Panel(f"[bold blue]Run Status: {status_var['status']}[/bold blue]")
            )

            # Retrieve logs from the queue
            while not logs_queue.empty():
                log_entry = logs_queue.get()
                logs_buffer.append(log_entry)
                logs_queue.task_done()

            # Update logs panel
            if logs_buffer:
                table = Table(box=box.SIMPLE)
                table.add_column("Timestamp", style="cyan")
                table.add_column("Message", style="white")
                for log_entry in logs_buffer[-10:]:
                    timestamp = log_entry.get("timestamp", "")
                    log_line = log_entry.get("logLine", "").rstrip()
                    table.add_row(timestamp, log_line)
                layout["logs"].update(table)
            else:
                layout["logs"].update(Panel("[italic]Waiting for new logs...[/italic]"))

            # Refresh the live display
            live.update(layout)

            sleep(1)

    # Wait for both threads to complete
    status_thread.join()
    logs_thread.join()


@run_app.command()
def run(
    app_name_with_function: str = typer.Argument(
        ..., help="The name of the app and function in format 'app_name:function_name'"
    ),
    data: str = typer.Option(
        ..., "--data", "-d", help="Data to send to the application in JSON format"
    ),
    method: str = typer.Option(
        "POST", "--method", "-m", help="HTTP method to use for the request"
    ),
    webhook: str = typer.Option(
        None, "--webhook", help="URL to which the results should be sent"
    ),
    function_name: str = typer.Option(
        "run",
        "--function",
        "-f",
        help="Optional: The function name to call (alternative to using app_name:function_name format)",
    ),
):
    """
    Calls a user application with the specified data and method.
    Format: cerebrium run app_name:function_name --data '{"key": "value"}'
    """
    # Parse app_name and function_name from the argument
    if ":" in app_name_with_function:
        app_name, fn_name = app_name_with_function.split(":", 1)
    else:
        app_name = app_name_with_function
        fn_name = function_name

    # If function_name is still None, use "run" as default
    if not fn_name:
        fn_name = "run"
        console.print(f"[yellow]No function specified, using default: 'run'[/yellow]")

    project_id = get_current_project_context()
    jwt = get_cerebrium_jwt(project_id)

    if project_id is None:
        cerebrium_log(
            level="ERROR",
            message="No project found. Please run 'cerebrium project use PROJECT_ID' to set the current project.",
            prefix="",
        )
        raise typer.Exit(1)

    # Build the base URL
    base_url = f"{get_api_base_url()}/v4/{project_id}/{app_name}/{fn_name}"
    params = {}  # Synchronous call

    if webhook:
        params["webhook"] = webhook

    # Parse the data
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        cerebrium_log(level="ERROR", message="Invalid JSON data provided.", prefix="")
        raise typer.Exit(1)

    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    with console.status(
        f"[bold blue]Running {app_name} with function {fn_name}...[/bold blue]", spinner="dots"
    ):
        try:
            response = requests.request(
                method=method.upper(),
                url=base_url,
                headers=headers,
                json=json_data,
                params=params,
            )
        except requests.exceptions.RequestException as e:
            cerebrium_log(
                level="ERROR",
                message=f"There was an error making the request to the app {app_name}.\n{e}",
                prefix="",
            )
            bugsnag.notify(
                Exception("There was an error making the request to app"),
                meta_data={"app_name": app_name},
            )
            raise typer.Exit(1)

    # Handle the response
    if response.status_code == 200:
        result = response.json()

        # Pretty print the JSON response
        console.print(f"[bold]Response:[/bold]")
        console.print_json(json.dumps(result))

        # Get run_id from the response if available
        run_id = result.get("run_id")
        if run_id:
            # Determine environment for the dashboard URL
            env = os.environ.get("CEREBRIUM_ENV", "prod")
            dashboard_base = (
                "https://dev-dashboard.cerebrium.ai"
                if env == "dev"
                else "https://dashboard.cerebrium.ai"
            )

            # Construct the URL to view run logs
            logs_url = f"{dashboard_base}/projects/{project_id}/apps/{project_id}-{app_name}/runs?runId={run_id}"
            console.print(
                f"\n[bold blue]View run logs:[/bold blue] [link={logs_url}]here[/link]"
            )
    else:
        console.print(f"[bold red]Response code: {response.status_code}[/bold red]")
        try:
            message = response.json()
            console.print_json(json.dumps(message))
        except json.JSONDecodeError:
            console.print(response.text)
        cerebrium_log(
            level="ERROR",
            message=f"There was an error running the app {app_name}.\n{response.text}",
            prefix="",
        )
        bugsnag.notify(
            Exception("There was an error running app"),
            meta_data={"app_name": app_name},
        )
        raise typer.Exit(1)
