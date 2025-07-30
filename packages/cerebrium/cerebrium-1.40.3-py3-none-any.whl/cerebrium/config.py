from abc import abstractmethod

from atom.api import Atom

from cerebrium.defaults import (
    COMPUTE,
    COOLDOWN,
    CPU,
    DISABLE_AUTH,
    DOCKER_BASE_IMAGE_URL,
    ENTRYPOINT,
    EXCLUDE,
    GPU_COUNT,
    HEALTHCHECK_ENDPOINT,
    READYCHECK_ENDPOINT,
    INCLUDE,
    MAX_REPLICAS,
    MEMORY,
    MIN_REPLICAS,
    PORT,
    PRE_BUILD_COMMANDS,
    PROVIDER,
    PYTHON_VERSION,
    REGION,
    REPLICA_CONCURRENCY,
    SHELL_COMMANDS,
    RESPONSE_GRACE_PERIOD,
    DOCKERFILE_PATH,
    SCALING_METRIC,
    SCALING_TARGET,
    SCALING_BUFFER,
    ROLLOUT_DURATION_SECONDS,
)


class TOMLConfig(Atom):
    @abstractmethod
    def __toml__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __json__(self) -> dict:
        raise NotImplementedError


class ScalingConfig(TOMLConfig):
    min_replicas: int = MIN_REPLICAS
    max_replicas: int = MAX_REPLICAS
    cooldown: int = COOLDOWN
    replica_concurrency: int = REPLICA_CONCURRENCY
    response_grace_period: int = RESPONSE_GRACE_PERIOD
    scaling_metric: str = SCALING_METRIC
    scaling_target: int = SCALING_TARGET
    scaling_buffer: int = SCALING_BUFFER
    roll_out_duration_seconds: int = ROLLOUT_DURATION_SECONDS

    def __toml__(self) -> str:
        return (
            "[cerebrium.scaling]\n"
            f"min_replicas = {self.min_replicas}\n"
            f"max_replicas = {self.max_replicas}\n"
            f"cooldown = {self.cooldown}\n"
            f"replica_concurrency = {self.replica_concurrency}\n"
            f"response_grace_period = {self.response_grace_period}\n"
            f'scaling_metric = "{self.scaling_metric}"\n'
            f"scaling_target = {self.scaling_target}\n"
            f"scaling_buffer = {self.scaling_buffer}\n"
            f"roll_out_duration_seconds = {self.roll_out_duration_seconds}\n\n"
        )

    def __json__(self) -> dict:
        return {
            "minReplicaCount": self.min_replicas,
            "maxReplicaCount": self.max_replicas,
            "cooldownPeriodSeconds": self.cooldown,
            "replicaConcurrency": self.replica_concurrency,
            "responseGracePeriodSeconds": self.response_grace_period,
            "scalingMetric": self.scaling_metric,
            "scalingTarget": self.scaling_target,
            "scalingBuffer": self.scaling_buffer,
            "rollOutDurationSeconds": self.roll_out_duration_seconds,
        }


class HardwareConfig(TOMLConfig):
    cpu: float = CPU
    memory: float = MEMORY
    compute: str = COMPUTE
    gpu_count: int = GPU_COUNT
    provider: str = PROVIDER
    region: str = REGION

    def __toml__(self) -> str:
        gpu_count_line = f"gpu_count = {self.gpu_count}\n" if self.compute != "CPU" else ""
        return (
            "[cerebrium.hardware]\n"
            f"cpu = {self.cpu}\n"
            f"memory = {self.memory}\n"
            f'compute = "{self.compute}"\n' + gpu_count_line + "\n"
        )

    def __json__(self) -> dict:
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "compute": self.compute,
            "gpuCount": self.gpu_count,
            "provider": self.provider,
            "region": self.region,
        }


class CustomRuntimeConfig(TOMLConfig):
    entrypoint: list[str] = ENTRYPOINT
    port: int = PORT
    healthcheck_endpoint: str = HEALTHCHECK_ENDPOINT
    readycheck_endpoint: str = READYCHECK_ENDPOINT
    dockerfile_path: str = DOCKERFILE_PATH

    def __toml__(self) -> str:
        return (
            "[cerebrium.runtime.custom]\n"
            f"entrypoint = {self.entrypoint}\n"
            f'port = "{self.port}"\n'
            f'healthcheck_endpoint = "{self.healthcheck_endpoint}"\n'
            f'readycheck_endpoint = "{self.readycheck_endpoint}"\n'
            f'dockerfile_path = "{self.dockerfile_path}"\n\n'
        )

    def __json__(self) -> dict:
        return {
            "entrypoint": (
                self.entrypoint
                if isinstance(self.entrypoint, list)
                else self.entrypoint.split()
            ),
            "port": self.port,
            "healthcheckEndpoint": self.healthcheck_endpoint,
            "readycheckEndpoint": self.readycheck_endpoint,
            "dockerfilePath": self.dockerfile_path,
        }


class DeploymentConfig(TOMLConfig):
    name: str
    python_version: str = PYTHON_VERSION
    docker_base_image_url: str = DOCKER_BASE_IMAGE_URL
    include: list[str] = INCLUDE
    exclude: list[str] = EXCLUDE
    shell_commands: list[str] = SHELL_COMMANDS
    pre_build_commands: list[str] = PRE_BUILD_COMMANDS
    disable_auth: bool = DISABLE_AUTH
    # TODO: Remove/Deprecate this in favor of scaling_config
    roll_out_duration_seconds: int = ROLLOUT_DURATION_SECONDS

    def __toml__(self) -> str:
        shell_commands = (
            f"shell_commands = {self.shell_commands}\n" if self.shell_commands else ""
        )

        return (
            "[cerebrium.deployment]\n"
            f'name = "{self.name}"\n'
            f'python_version = "{self.python_version}"\n'
            f'docker_base_image_url = "{self.docker_base_image_url}"\n'
            f"disable_auth = {str(self.disable_auth).lower()}\n"
            f"include = {self.include}\n"
            f"exclude = {self.exclude}\n" + shell_commands + "\n"
        )

    def __json__(self) -> dict:
        return {
            "name": self.name,
            "pythonVersion": self.python_version,
            "baseImage": self.docker_base_image_url,
            "include": self.include,
            "exclude": self.exclude,
            "shellCommands": self.shell_commands,
            "preBuildCommands": self.pre_build_commands,
            "disableAuth": self.disable_auth,
            "rollOutDurationSeconds": self.roll_out_duration_seconds,
        }


class DependencyConfig(Atom):
    pip: dict[str, str] = {}
    conda: dict[str, str] = {}
    apt: dict[str, str] = {}

    paths: dict[str, str] = {"pip": "", "conda": "", "apt": ""}

    def __toml__(self) -> str:
        pip_strings = (
            "[cerebrium.dependencies.pip]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.pip.items())
            + "\n"
            if self.pip
            else ""
        )
        conda_strings = (
            "[cerebrium.dependencies.conda]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.conda.items())
            + "\n"
            if self.conda != {}
            else ""
        )
        apt_strings = (
            "[cerebrium.dependencies.apt]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.apt.items())
            + "\n"
            if self.apt != {}
            else ""
        )
        if pip_strings or conda_strings or apt_strings:
            return pip_strings + conda_strings + apt_strings + "\n"
        return ""

    def __json__(self) -> dict:
        return {
            "pip": self.pip,
            "conda": self.conda,
            "apt": self.apt,
            "pip_file": self.paths["pip"],
            "conda_file": self.paths["conda"],
            "apt_file": self.paths["apt"],
        }


class PartnerConfig(TOMLConfig):
    name: str

    def __toml__(self) -> str:
        return "[cerebrium.partner.service]\n" f'name = "{self.name}"\n\n'

    def __json__(self) -> dict:
        return {"partnerName": self.name}


class CerebriumConfig(Atom):
    deployment: DeploymentConfig
    hardware: HardwareConfig
    scaling: ScalingConfig
    dependencies: DependencyConfig
    custom_runtime: CustomRuntimeConfig | None = None
    partner_services: PartnerConfig | None = None

    def to_toml(self, file: str = "cerebrium.toml") -> None:
        with open(file, "w", newline="\n") as f:
            f.write(self.deployment.__toml__())
            f.write(self.hardware.__toml__())
            f.write(self.scaling.__toml__())
            if self.custom_runtime is not None:
                f.write(self.custom_runtime.__toml__())
            f.write(self.dependencies.__toml__())

    def to_payload(self) -> dict:
        payload = {
            **self.deployment.__json__(),
            **self.hardware.__json__(),
            **self.scaling.__json__(),
        }
        if self.custom_runtime is not None:
            payload.update(self.custom_runtime.__json__())
            payload["runtime"] = "custom"
        elif self.partner_services is not None:
            payload["partnerService"] = self.partner_services.name
            payload["runtime"] = self.partner_services.name
        else:
            payload["runtime"] = "cortex"
        return payload
