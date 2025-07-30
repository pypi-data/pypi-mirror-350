import os

PIP_REQUIREMENTS_FILE = "requirements.txt"
CONDA_REQUIREMENTS_FILE = "conda_pkglist.txt"
APT_REQUIREMENTS_FILE = "pkglist.txt"
SHELL_COMMANDS_FILE = "shell_commands.sh"
PRE_BUILD_COMMANDS_FILE = "pre_build_commands.sh"

# Config file
DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".cerebrium", "config.yaml")
CONFIG_PATH = os.getenv("CEREBRIUM_CONFIG_PATH", DEFAULT_CONFIG_PATH)
