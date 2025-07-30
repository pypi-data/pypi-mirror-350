import os
import platform

import bugsnag
import jwt
import yaml

from cerebrium.files import CONFIG_PATH
from cerebrium.utils.project import get_current_project_context


def init_bugsnag():
    set_bugsnag_user()

    # Get OS & Project information
    os_info = {
        "os_type": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
    }
    project_id = get_current_project_context()

    bugsnag.add_metadata_tab("system", os_info)
    bugsnag.add_metadata_tab("project", {"project_id": project_id})


# Function to decode JWT and extract user info
def get_user_info_from_jwt(jwt_token: str):
    try:
        # Decode the JWT token without verification
        decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
        return decoded_token.get("sub") or decoded_token.get("username")
    except jwt.DecodeError:
        bugsnag.notify(Exception("Invalid JWT token"))
        return None


def set_bugsnag_user():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f) or {}

        if config is None:
            bugsnag.notify(Exception("User not logged in"))
        else:
            CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")
            key_name = "" if CEREBRIUM_ENV == "prod" else f"{CEREBRIUM_ENV}-"

            jwt_token: str = config.get(f"{key_name}accessToken", "")

            if jwt_token:
                user_id = get_user_info_from_jwt(jwt_token)

                if user_id:

                    def before_notify_callback(event):
                        event.set_user(id=user_id)

                    bugsnag.before_notify(before_notify_callback)
                else:
                    bugsnag.notify(Exception("Failed to extract user info from JWT"))
            else:
                bugsnag.notify(Exception("JWT token not found in config"))
