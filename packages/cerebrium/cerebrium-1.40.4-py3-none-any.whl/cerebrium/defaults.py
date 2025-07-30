from sys import version_info

# Deployment
PYTHON_VERSION = f"{version_info.major}.{version_info.minor}"
DOCKER_BASE_IMAGE_URL = "debian:bookworm-slim"
INCLUDE = ["./*", "main.py", "cerebrium.toml"]
EXCLUDE = [".*"]
SHELL_COMMANDS = []
PRE_BUILD_COMMANDS = []
DISABLE_AUTH = False
ROLLOUT_DURATION_SECONDS = 0

# Custom Runtime
ENTRYPOINT = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
PORT = 8000
HEALTHCHECK_ENDPOINT = ""
READYCHECK_ENDPOINT = ""
DOCKERFILE_PATH = ""

# Hardware
CPU = 2.0
MEMORY = 12.0
COMPUTE = "CPU"
GPU_COUNT = 1
PROVIDER = "aws"
REGION = "us-east-1"

# Scaling
MIN_REPLICAS = 0
MAX_REPLICAS = 5
COOLDOWN = 30
REPLICA_CONCURRENCY = 1
RESPONSE_GRACE_PERIOD = 900  # 15 minutes
SCALING_METRIC = "concurrency_utilization"
SCALING_TARGET = 100
SCALING_BUFFER = 0
