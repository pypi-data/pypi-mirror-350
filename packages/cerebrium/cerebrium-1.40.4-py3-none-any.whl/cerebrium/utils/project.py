import os

import bugsnag
import yaml

from cerebrium.files import CONFIG_PATH


class InvalidProjectIDError(Exception):
    pass


def is_valid_project_id(project_id: str) -> bool:
    """
    Validate that the project ID starts with 'p-' or 'dev-p-'
    """
    return project_id.startswith(("p-", "dev-p-"))


def get_current_project_context() -> str | None:
    """
    Get the current project context and project name
    """
    if os.getenv("CEREBRIUM_ENV") == "test":
        return "test-project"

    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                config = yaml.safe_load(f)
                env = os.getenv("CEREBRIUM_ENV", "prod")
                key_prefix = "" if env == "prod" else f"{env}-"
                project_id = config.get(f"{key_prefix}project")
                if project_id:
                    if is_valid_project_id(project_id):
                        return project_id
                    else:
                        raise InvalidProjectIDError(f"Invalid project ID: {project_id}")
        return None
    except Exception as e:
        bugsnag.notify(e)
        raise
