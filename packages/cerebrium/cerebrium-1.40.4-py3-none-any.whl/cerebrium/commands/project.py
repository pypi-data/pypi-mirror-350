import os
from typing import Annotated

import bugsnag
import typer
import yaml
from rich import box
from rich import print
from rich import print as console
from rich.panel import Panel
from rich.table import Table

from cerebrium.api import cerebrium_request
from cerebrium.files import CONFIG_PATH
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.project import get_current_project_context

project_app = typer.Typer(no_args_is_help=True)
CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")


@project_app.command("current")
def current():
    """
    Get the current project you are working in
    """
    print(f"projectId: {get_current_project_context()}")


@project_app.command("list")
def list_projects():
    """
    List all your projects
    """
    projects_response = cerebrium_request("GET", "v2/projects", {}, requires_auth=True)
    if projects_response is None:
        cerebrium_log(
            level="ERROR",
            message="There was an error getting your projects. Please login again and, if the problem persists, contact support.",
            prefix="",
        )
        bugsnag.notify(Exception("There was an error getting projects"))
        raise typer.Exit(1)

    if projects_response.status_code != 200:
        cerebrium_log(
            level="ERROR",
            message="There was an error getting your projects",
            prefix="",
        )
        bugsnag.notify(Exception("There was an error getting projects"))
        raise typer.Exit(1)

    if projects_response.status_code == 200:
        projects = projects_response.json()

        # Create the table
        table = Table(title="", box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("ID")
        table.add_column("Name")

        for project in projects:
            table.add_row(project["id"], project["name"])

        details = Panel.fit(
            table,
            title="[bold] Projects ",
            border_style="yellow bold",
            width=140,
        )
        console(details)

        print("")
        print(
            f"You can set your current project context by running 'cerebrium project set {projects[0]['id']}'"
        )


@project_app.command("set")
def set_project(
    project_id: Annotated[
        str,
        typer.Argument(
            help="The projectId of the project you would like to work in",
        ),
    ],
):
    """
    Set the project context you are working in.
    """
    # Check that project_id begins with p- or dev-p-
    if not project_id.startswith("p-") and not project_id.startswith("dev-p-"):
        print("Invalid Project ID. Project ID should start with 'p-'")
        bugsnag.notify(Exception("Invalid Project ID"))
        raise typer.Exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    key_name = ""
    if CEREBRIUM_ENV == "dev":
        key_name = "dev-"
    elif CEREBRIUM_ENV == "local":
        key_name = "local-"
    config[f"{key_name}project"] = project_id
    with open(CONFIG_PATH, "w", newline="\n") as f:
        yaml.dump(config, f)

    print(f"Project context successfully set to : {project_id}")
