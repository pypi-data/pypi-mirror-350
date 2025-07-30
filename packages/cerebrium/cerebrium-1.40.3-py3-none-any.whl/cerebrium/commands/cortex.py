import cProfile
import os
import sys
from pstats import Stats
from typing import Annotated, Optional

import bugsnag
import toml
import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from cerebrium import api, __version__
from cerebrium.api import cerebrium_request
from cerebrium.config import (
    CerebriumConfig,
    ScalingConfig,
    HardwareConfig,
    DeploymentConfig,
    DependencyConfig,
    CustomRuntimeConfig,
    PartnerConfig,
)
from cerebrium.core import cli
from cerebrium.utils.check_cli_version import print_update_cli_message
from cerebrium.utils.deploy import package_app, get_function_names
from cerebrium.utils.display import confirm_partner_service_deployment
from cerebrium.utils.logging import cerebrium_log, console
from cerebrium.utils.project import get_current_project_context

_EXAMPLE_MAIN = """
def run(param_1: str, param_2: str, run_id):  # run_id is optional, injected by Cerebrium at runtime
    my_results = {"1": param_1, "2": param_2}
    my_status_code = 200 # if you want to return a specific status code

    return {"my_result": my_results, "status_code": my_status_code} # return your results
    
# To deploy your app, run:
# cerebrium deploy
"""


@cli.command("init")
def init(
    name: Annotated[str, typer.Argument(help="Name of the Cortex deployment.")],
    dir: Annotated[str, typer.Option(help="Directory to create the Cortex deployment.")] = "./",
):
    """
    Initialize an empty Cerebrium Cortex project.
    """
    path = os.path.join(dir, name)
    toml_path = os.path.join(path, "cerebrium.toml")
    main_path = os.path.join(path, "main.py")
    if dir != "./":
        console.print(f"Initializing Cerebrium Cortex project in new directory {name}")
    else:
        console.print(f"Initializing Cerebrium Cortex project in directory {path}")

    print_update_cli_message()

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        cerebrium_log(
            level="WARNING",
            message="Directory already exists. Please choose a different name.",
            prefix_separator="\t",
        )
        bugsnag.notify(Exception("Directory already exists error."))
        raise typer.Exit(1)

    if not os.path.exists(main_path):
        with open(main_path, "w", newline="\n") as f:
            f.write(_EXAMPLE_MAIN)

    scaling_config = ScalingConfig()
    hardware_config = HardwareConfig()
    dependency_config = DependencyConfig()
    deployment_config = DeploymentConfig(name=name)
    config = CerebriumConfig(
        scaling=scaling_config,
        hardware=hardware_config,
        deployment=deployment_config,
        dependencies=dependency_config,
        custom_runtime=None,
    )
    config.to_toml(toml_path)
    console.print("Cerebrium Cortex project initialized successfully!")
    console.print(f"cd {path} && cerebrium deploy to get started")


@cli.command(
    "deploy",
    help="""
Deploy a new Cortex app to Cerebrium. Run `cerebrium deploy --help` for more information.\n
    \n
Usage: cerebrium deploy [OPTIONS]\n
\n
  Deploy a Cortex app to Cerebrium.\n
\n
Options:\n
  --name TEXT                    Name of the App. Overrides the value in the TOML file if provided.\n
  --disable-syntax-check         Flag to disable syntax check.\n
  --log-level [DEBUG|INFO]       Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'.\n
  --config-file PATH             Path to the cerebrium config TOML file. You can generate a config using `cerebrium init`.\n
  -y, --disable-confirmation     Disable the confirmation prompt before deploying.\n
  --disable-animation            Disable TQDM loading bars and yaspin animations.\n
  --disable-build-logs           Disable build logs during a deployment.\n
  -h, --help                     Show this message and exit.\n
\n
Examples:\n
  # Deploy an app with the default settings\n
  cerebrium deploy\n
\n
  # Deploy an app with a custom name and disabled syntax check\n
  cerebrium deploy --name my_app --disable-syntax-check\n
    """,
)
def deploy(
    name: Annotated[
        Optional[str],
        typer.Option(
            "--name",
            help="Name of the App. Overrides the value in the TOML file if provided.",
        ),
    ] = None,
    disable_syntax_check: Annotated[
        bool, typer.Option(help="Flag to disable syntax check.")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
        ),
    ] = "INFO",
    config_file: Annotated[
        str,
        typer.Option(
            help="Path to the cerebrium config TOML file. You can generate a config using `cerebrium init`."
        ),
    ] = "./cerebrium.toml",
    disable_confirmation: Annotated[
        bool,
        typer.Option(
            "--disable-confirmation",
            "-y",
            help="Disable the confirmation prompt before deploying.",
        ),
    ] = False,
    disable_animation: Annotated[
        bool,
        typer.Option(
            "--disable-animation",
            help="Disable TQDM loading bars and yaspin animations.",
        ),
    ] = False,
    disable_build_logs: Annotated[
        bool,
        typer.Option("--disable-build-logs", help="Disable build logs during a deployment."),
    ] = False,
):
    print_update_cli_message()

    # Check user is logged in
    project_id = get_current_project_context()
    if not project_id:
        cerebrium_log(
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            color="red",
        )
        bugsnag.notify(Exception("User not logged in"))
        raise typer.Exit(1)

    with cProfile.Profile() as pr:
        # load config toml file
        log_level = log_level.upper()
        assert log_level in [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "INTERNAL",
        ], "Log level must be one of 'DEBUG' or 'INFO'"
        try:
            toml_config = toml.load(config_file)["cerebrium"]
        except FileNotFoundError:
            cerebrium_log(
                message="Could not find cerebrium.toml file. Please run `cerebrium init` to create one.",
                color="red",
            )
            bugsnag.notify(
                Exception(
                    "Could not find cerebrium.toml file. Please run `cerebrium init` to create one."
                )
            )
            raise typer.Exit(1)
        except KeyError:
            cerebrium_log(
                message="Could not find 'cerebrium' key in cerebrium.toml file. Please run `cerebrium init` to create one.",
                color="red",
            )
            raise typer.Exit(1)
        except Exception as e:
            bugsnag.notify(e)
            cerebrium_log(message=f"Error loading cerebrium.toml file: {e}", color="red")
            raise typer.Exit(1)

        deployment_section = toml_config.get("deployment", {})
        hardware_section = toml_config.get("hardware", {})
        config_error = False
        if not deployment_section:
            cerebrium_log(
                message="Deployment section is required in cerebrium.toml file. Please add a 'deployment' section.",
                level="ERROR",
            )
            config_error = True
        if "name" not in deployment_section:
            cerebrium_log(
                message="`deployment.name` is required in cerebrium.toml file. Please add a 'name' field to the 'deployment' section.",
                level="ERROR",
            )
            config_error = True
        if "gpu" in hardware_section:
            cerebrium_log(
                message="`hardware.gpu` field is deprecated. Please use `hardware.compute` instead.",
                level="ERROR",
            )
            config_error = True
        if "cuda_version" in deployment_section:
            cerebrium_log(
                message="`deployment.cuda_version` field is deprecated. Please use `deployment.docker_base_image_url` instead.",
                level="ERROR",
            )
            config_error = True
            # Check if the provider is Coreweave, if so print a V3 deprecation warning
        if hardware_section.get("provider", "aws") == "coreweave":
            cerebrium_log(
                message="Cortex V4 does not support Coreweave. Please consider updating your app to AWS.",
                level="ERROR",
            )
            config_error = True
        if config_error:
            raise typer.Exit(1)

        # Override name from TOML file if --name is provided
        if name:
            deployment_section["name"] = name

        deployment_config: DeploymentConfig = DeploymentConfig(**deployment_section)
        scaling_config: ScalingConfig = ScalingConfig(**toml_config.get("scaling", {}))
        hardware_config: HardwareConfig = HardwareConfig(**toml_config.get("hardware", {}))

        if "runtime" in toml_config and "custom" in toml_config["runtime"]:
            if "entrypoint" in toml_config["runtime"]["custom"]:
                if isinstance(toml_config["runtime"]["custom"]["entrypoint"], str):
                    toml_config["runtime"]["custom"]["entrypoint"] = toml_config["runtime"][
                        "custom"
                    ]["entrypoint"].split()
            if (
                "dockerfile_path" in toml_config["runtime"]["custom"]
                and toml_config["runtime"]["custom"]["dockerfile_path"] != ""
            ):
                if not os.path.exists(toml_config["runtime"]["custom"]["dockerfile_path"]):
                    cerebrium_log(
                        message="Dockerfile path does not exist. Please check the path in the toml file.",
                        color="red",
                    )
                    raise typer.Exit(1)
            custom_runtime_config = CustomRuntimeConfig(**toml_config["runtime"]["custom"])
        else:
            custom_runtime_config = None

        dependency_config: DependencyConfig = DependencyConfig(
            **toml_config.get("dependencies", {})
        )

        partner_config = None
        # Add partner config handling - it's the same as runtime.custom but instead its runtime.deepgram or runtime.rime
        if "runtime" in toml_config and "deepgram" in toml_config["runtime"]:
            partner_config = PartnerConfig(name="deepgram")
        if "runtime" in toml_config and "rime" in toml_config["runtime"]:
            partner_config = PartnerConfig(name="rime")

        config: CerebriumConfig = CerebriumConfig(
            scaling=scaling_config,
            hardware=hardware_config,
            deployment=deployment_config,
            dependencies=dependency_config,
            custom_runtime=custom_runtime_config,
            partner_services=partner_config,
        )

        # If partner config is present, we don't package the app - instead just call POST partner-services endpoint
        if partner_config is not None:
            payload = config.to_payload()

            if not disable_confirmation:
                if not confirm_partner_service_deployment(config):
                    sys.exit()

            console.print("Deploying partner service app...")

            payload["cliVersion"] = __version__
            project_id = get_current_project_context()
            setup_response = cerebrium_request(
                "POST", f"v2/projects/{project_id}/partner-apps", payload, requires_auth=True
            )

            if setup_response is None or setup_response.status_code != 200:
                default_error_message = "Error deploying partner app. Please check the dashboard or contact support if the issue persists."
                error_message = default_error_message

                if setup_response is not None:
                    try:
                        response_json = setup_response.json()
                        if isinstance(response_json, dict) and isinstance(
                            response_json.get("message"), str
                        ):
                            error_message = response_json["message"]
                    except Exception as e:
                        pass

                console.print(Text(error_message, style="red"))
                bugsnag.notify(Exception(error_message))
                raise typer.Exit(1)

            dashboard_url = f"{api.dashboard_url}/projects/{project_id}/apps/{project_id}-{config.deployment.name}"
            info_string = f"App Dashboard: {dashboard_url}"

            app_endpoint = setup_response.json()["internalEndpoint"]
            info_string += f"\n\nEndpoint:\n[bold red]POST[/bold red] {app_endpoint}"

            dashboard_info = Panel(
                info_string,
                title=f"[bold green] {config.deployment.name} is now live!  ",
                border_style="green",
                width=140,
            )
            console.print(Group(dashboard_info))

            return typer.Exit(0)

        build_status, setup_response = package_app(
            config,
            disable_build_logs,
            log_level,  # type: ignore
            disable_syntax_check,
            disable_animation,
            disable_confirmation,
        )
        if setup_response is None:
            message = "Error building app. Please check the dashboard or contact support if the issue persists."
            cerebrium_log(message=message, color="red")
            bugsnag.notify(Exception(message))
            raise typer.Exit(1)
        if build_status == "success":
            project_id = setup_response["projectId"]
            endpoint = setup_response["internalEndpoint"]
            dashboard_url = f"{api.dashboard_url}/projects/{project_id}/apps/{project_id}-{config.deployment.name}"
            info_string = f"App Dashboard: {dashboard_url}"

            # Loop over each function name and create the POST endpoint
            info_string += "\n\nEndpoints:"
            function_names = get_function_names(custom_runtime_config is not None)
            for method, function_name in function_names:
                info_string += f"\n[bold red]{method}[/bold red] {endpoint}/" + function_name

            dashboard_info = Panel(
                info_string,
                title=f"[bold green] {config.deployment.name} is now live!  ",
                border_style="green",
                width=140,
            )

            console.print(Group(dashboard_info))
        elif build_status in ["build_failure", "init_failure"]:
            bugsnag.notify(Exception("User build failed"))
            console.print(Text("Unfortunately there was an issue with your build", style="red"))
            raise typer.Exit(1)
    pr.disable()
    if log_level == "INTERNAL":
        stats = Stats(pr)
        stats.sort_stats("tottime").print_stats(10)
