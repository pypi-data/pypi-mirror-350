import os
import logging
from logging import FileHandler
import multiprocessing
from pathlib import Path
from typing import Dict, List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired
from dataclasses import field, dataclass
from functools import cached_property
import istari_digital_core

from istari_digital_client.env import env_bool, env_int, env_str, env_cache_root

logger = logging.getLogger("istari-digital-client.configuration")

JSON_SCHEMA_VALIDATION_KEYWORDS = {
    "multipleOf",
    "maximum",
    "exclusiveMaximum",
    "minimum",
    "exclusiveMinimum",
    "maxLength",
    "minLength",
    "pattern",
    "maxItems",
    "minItems",
}

ServerVariablesT = Dict[str, str]

BearerAuthSetting = TypedDict(
    "BearerAuthSetting",
    {
        "type": Literal["bearer"],
        "in": Literal["header"],
        "key": Literal["Authorization"],
        "value": str,
    },
)

AuthSettings = TypedDict(
    "AuthSettings",
    {
        "RequestAuthenticator": BearerAuthSetting,
    },
    total=False,
)


class HostSettingVariable(TypedDict):
    description: str
    default_value: str
    enum_values: List[str]


class HostSetting(TypedDict):
    url: str
    description: str
    variables: NotRequired[Dict[str, HostSettingVariable]]


@dataclass
class Configuration:
    registry_url: str | None = field(
        default_factory=env_str("ISTARI_REGISTRY_URL", default=None)
    )
    registry_auth_token: str | None = field(
        default_factory=env_str("ISTARI_REGISTRY_AUTH_TOKEN")
    )
    retry_enabled: bool | None = field(
        default_factory=env_bool("ISTARI_CLIENT_RETRY_ENABLED", default=True)
    )
    retry_max_attempts: int | None = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MAX_ATTEMPTS")
    )
    retry_min_interval_millis: int | None = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MIN_INTERVAL_MILLIS")
    )
    retry_max_interval_millis: int | None = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MAX_INTERVAL_MILLIS")
    )
    filesystem_cache_enabled: bool | None = field(
        default_factory=env_bool("ISTARI_CLIENT_FILESYSTEM_CACHE_ENABLED", default=True)
    )
    filesystem_cache_root: Path = field(
        default_factory=env_cache_root("ISTARI_CLIENT_FILESYSTEM_CACHE_ROOT")
    )
    filesystem_cache_clean_on_exit: bool = field(
        default_factory=env_bool(
            "ISTARI_CLIENT_FILESYSTEM_CACHE_CLEAN_BEFORE_EXIT", default=True
        )
    )
    retry_jitter_enabled: bool | None = field(
        default_factory=env_bool("ISTARI_CLIENT_RETRY_JITTER_ENABLED", default=True)
    )
    multipart_chunksize: int | None = field(
        default_factory=env_int("ISTARI_CLIENT_MULTIPART_CHUNKSIZE")
    )
    multipart_threshold: int | None = field(
        default_factory=env_int("ISTARI_CLIENT_MULTIPART_THRESHOLD")
    )
    server_index: Optional[int] = field(default=None)
    server_variables: Optional[ServerVariablesT] = field(default=None)
    server_operation_index: Optional[Dict[int, int]] = field(default_factory=lambda: {})
    server_operation_variables: Optional[Dict[int, ServerVariablesT]] = field(
        default_factory=lambda: {}
    )
    ignore_operation_servers: bool = field(default=False)
    ssl_ca_cert: Optional[str] = field(default=None)
    retries: Optional[int] = field(default=None)
    ca_cert_data: Optional[Union[str, bytes]] = field(default=None)
    debug: Optional[bool] = field(default=None)

    temp_folder_path: Optional[str] = field(init=False, default=None)
    logger: Dict[str, logging.Logger] = field(
        init=False,
        default_factory=lambda: {
            "package_logger": logging.getLogger("istari_digital_client.openapi_client"),
            "urllib3_logger": logging.getLogger("urllib3"),
        },
    )
    logger_format: str = field(
        init=False, default="%(asctime)s %(levelname)s %(message)s"
    )
    logger_stream_handler: Optional[logging.StreamHandler] = field(
        init=False, default=None
    )
    logger_file_handler: Optional[FileHandler] = field(init=False, default=None)
    logger_file: Optional[str] = field(init=False, default=None)
    verify_ssl: bool = field(init=False, default=True)
    cert_file: Optional[str] = field(init=False, default=None)
    key_file: Optional[str] = field(init=False, default=None)
    assert_hostname: Optional[bool] = field(init=False, default=None)
    tls_server_name: Optional[str] = field(init=False, default=None)
    connection_pool_maxsize: int = field(
        init=False, default=multiprocessing.cpu_count() * 5
    )
    proxy: Optional[str] = field(init=False, default=None)
    proxy_headers: Optional[Dict[str, str]] = field(init=False, default=None)
    safe_chars_for_path_param: str = field(init=False, default="")
    client_side_validation: bool = field(init=False, default=True)
    socket_options = None
    datetime_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S.%f%z")
    date_format: str = field(init=False, default="%Y-%m-%d")

    def __post_init__(self) -> None:
        self.server_index = (
            0
            if self.server_index is None and self.registry_url is None
            else self.server_index
        )
        os.environ["ISTARI_REGISTRY_URL"] = self.registry_url or ""
        logger.debug(
            "set os.environ['ISTARI_REGISTRY_URL'] to '%s'",
            os.environ.get("ISTARI_REGISTRY_URL"),
        )
        os.environ["ISTARI_REGISTRY_AUTH_TOKEN"] = self.registry_auth_token or ""
        logger.debug(
            "setting os.environ['ISTARI_REGISTRY_AUTH_TOKEN'] to '%s'",
            os.environ.get("ISTARI_REGISTRY_AUTH_TOKEN"),
        )

    def auth_settings(self) -> AuthSettings:
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth: AuthSettings = {}
        if self.registry_auth_token is not None:
            auth["RequestAuthenticator"] = {
                "type": "bearer",
                "in": "header",
                "key": "Authorization",
                "value": "Bearer " + self.registry_auth_token,
            }
        return auth

    @staticmethod
    def to_debug_report() -> str:
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return (
            "Python SDK Debug Report:\n" "OS: {env}\n" "Python Version: {pyversion}\n"
        )

    @staticmethod
    def get_host_settings() -> List[HostSetting]:
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                "url": "",
                "description": "No description provided",
            }
        ]

    def get_host_from_settings(
        self,
        index: Optional[int],
        variables: Optional[ServerVariablesT] = None,
        servers: Optional[List[HostSetting]] = None,
    ) -> str:
        """Gets host URL based on the index and variables
        :param index: array index of the host settings
        :param variables: hash of variable and the corresponding value
        :param servers: an array of host settings or None
        :return: URL based on host settings
        """
        if index is None:
            if not self.registry_url:
                raise ValueError(
                    "No server URL (registry_url) found and server_index is not defined."
                )
            return self.registry_url

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers))
            )

        url = server["url"]

        # go through variables and replace placeholders
        for variable_name, variable in server.get("variables", {}).items():
            used_value = variables.get(variable_name, variable["default_value"])

            if "enum_values" in variable and used_value not in variable["enum_values"]:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(
                        variable_name, variables[variable_name], variable["enum_values"]
                    )
                )

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @classmethod
    def from_native_configuration(
        cls: type["Configuration"], native: istari_digital_core.Configuration
    ) -> "Configuration":
        return Configuration(
            registry_url=native.registry_url,
            registry_auth_token=native.registry_auth_token,
            retry_enabled=native.retry_enabled,  # type: ignore[attr-defined]
            retry_max_attempts=native.retry_max_attempts,  # type: ignore[attr-defined]
            retry_min_interval_millis=native.retry_min_interval_millis,  # type: ignore[attr-defined]
            retry_max_interval_millis=native.retry_max_interval_millis,  # type: ignore[attr-defined]
            retry_jitter_enabled=native.retry_jitter_enabled,
            multipart_chunksize=native.multipart_chunksize,
            multipart_threshold=native.multipart_threshold,
        )

    @cached_property
    def native_configuration(self) -> istari_digital_core.Configuration:
        return istari_digital_core.Configuration(
            registry_url=self.registry_url,
            registry_auth_token=self.registry_auth_token,
            retry_enabled=self.retry_enabled,  # type: ignore[attr-defined]
            retry_max_attempts=self.retry_max_attempts,  # type: ignore[attr-defined]
            retry_min_interval_millis=self.retry_min_interval_millis,  # type: ignore[attr-defined]
            retry_max_interval_millis=self.retry_max_interval_millis,  # type: ignore[attr-defined]
            retry_jitter_enabled=self.retry_jitter_enabled,
            multipart_chunksize=self.multipart_chunksize,
            multipart_threshold=self.multipart_threshold,
        )


class ConfigurationError(ValueError):
    pass
