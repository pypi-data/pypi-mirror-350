import os
import time
import webbrowser

import bugsnag
import typer
import yaml
from yaspin import yaspin
from yaspin.spinners import Spinners

from cerebrium.api import cerebrium_request
from cerebrium.core import cli
from cerebrium.files import CONFIG_PATH
from cerebrium.utils.check_cli_version import print_update_cli_message
from cerebrium.utils.logging import cerebrium_log, console

CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")


@cli.command("login")
def login():
    """
    Authenticate user via oAuth and store token in ~/.cerebrium/config.yaml
    """

    print_update_cli_message()

    auth_response = cerebrium_request("POST", "device-authorization", {}, False, v1=True)
    if auth_response is None:
        cerebrium_log(
            level="ERROR",
            message="There was an error getting your device code. Please try again.\nIf the problem persists, please contact support.",
        )
        bugsnag.notify(Exception("There was an error getting your device code."))
        raise typer.Exit(1)
    auth_response = auth_response.json()["deviceAuthResponsePayload"]
    verification_uri = auth_response["verification_uri_complete"]

    console.print("You will be redirected to the following URL to authenticate:")
    console.print(verification_uri)
    webbrowser.open(verification_uri, new=2)

    start_time = time.time()
    with yaspin(Spinners.arc, text="Waiting for authentication...", color="magenta"):
        response = cerebrium_request(
            "POST", "token", {"device_code": auth_response["device_code"]}, False, v1=True
        )
        while time.time() - start_time < 60 and response.status_code == 400:  # 1 minutes
            time.sleep(0.5)
            response = cerebrium_request(
                "POST", "token", {"device_code": auth_response["device_code"]}, False, v1=True
            )
    if response.status_code == 200:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                config = yaml.safe_load(f) or {}
        else:
            config: dict[str, str] = {}

        key_name = ""
        if CEREBRIUM_ENV == "dev":
            console.print("Logging in with dev API key")
            key_name = "dev-"
        config[f"{key_name}accessToken"] = response.json()["accessToken"]
        config[f"{key_name}refreshToken"] = response.json()["refreshToken"]
        if CEREBRIUM_ENV == "local":
            console.print("Logging in with local API key")
            key_name = "local-"
        config[f"{key_name}accessToken"] = response.json()["accessToken"]
        config[f"{key_name}refreshToken"] = response.json()["refreshToken"]

        console.print("Logged in successfully.")
        with open(CONFIG_PATH, "w", newline="\n") as f:
            yaml.dump(config, f)

        projects_response = cerebrium_request("GET", "v2/projects", {}, True)
        assert projects_response is not None
        if projects_response.status_code != 200:
            return  # Early return to simplify the flow

        projects = projects_response.json()
        current_project_id = config.get(f"{key_name}project")

        if current_project_id and any(p["id"] == current_project_id for p in projects):
            console.print(f"Using existing project context ID: {current_project_id}")
        else:
            current_project = projects[0]["id"]
            config[f"{key_name}project"] = current_project
            if current_project_id:
                console.print(
                    f"Updated project context to ID: {current_project} (previous project not found)"
                )
            else:
                console.print(f"Current project context set to ID: {current_project}")

        with open(CONFIG_PATH, "w", newline="\n") as f:
            yaml.dump(config, f)
    else:
        try:
            console.print(auth_response.json()["message"])
            bugsnag.notify(Exception("Error logging in."))
        except Exception as e:
            console.print(auth_response.text)
            console.print("There was an error logging in. Please try again.")
            bugsnag.notify(e)


@cli.command("save-auth-config")
def save_auth_config(access_token: str, refresh_token: str, project_id: str):
    """
    Saves the access token, refresh token, and project ID to the config file.
    This function is a helper method to allow users to store credentials
    directly for the framework. Mostly used for CI/CD
    """
    # Use os.path.join for cross-platform path construction
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    # Check for missing values
    if not access_token:
        console.print("Access token is missing.")
        raise typer.Exit(1)
    if not refresh_token:
        console.print("Refresh token is missing.")
        raise typer.Exit(1)
    if not project_id:
        console.print("Project ID is missing.")
        raise typer.Exit(1)

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8", newline="\n") as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}

    key_name = ""
    if CEREBRIUM_ENV == "dev":
        console.print("Logging in with dev API key")
        key_name = "dev-"
    elif CEREBRIUM_ENV == "local":
        console.print("Logging in with local API key")
        key_name = "local-"

    config[f"{key_name}accessToken"] = access_token
    config[f"{key_name}refreshToken"] = refresh_token
    config[f"{key_name}project"] = project_id

    # Ensure that the newline character is consistent across platforms
    with open(CONFIG_PATH, "w", encoding="utf-8", newline="\n") as f:
        yaml.dump(config, f)
    console.print("Configuration saved successfully.")
