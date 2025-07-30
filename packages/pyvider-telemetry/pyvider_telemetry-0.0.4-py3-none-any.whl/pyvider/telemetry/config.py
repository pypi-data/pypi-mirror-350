#
# config.py
#
"""
Configuration Models for Pyvider Telemetry (structlog-based).

This module defines the configuration objects used to set up and customize
the telemetry system, primarily focusing on logging behavior. It utilizes
the `attrs` library for creating structured and immutable configuration classes.

The configuration system supports:
- Environment variable-driven configuration
- Programmatic configuration with type safety
- Module-specific log level overrides
- Multiple output formats (JSON, key-value)
- Emoji customization options
- Service identification for multi-service environments
"""

import os
import sys
from typing import TYPE_CHECKING, Literal

from attrs import define, field

if TYPE_CHECKING:
    # Type checking imports to avoid circular dependencies
    pass

# Type alias for valid log level strings
LogLevelStr = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]

# Tuple of valid log levels for runtime validation
_VALID_LOG_LEVEL_TUPLE: tuple[LogLevelStr, ...] = (
    "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"
)

# Type alias for console formatter options
ConsoleFormatterStr = Literal["key_value", "json"]

# Tuple of valid formatter options for runtime validation
_VALID_FORMATTER_TUPLE: tuple[ConsoleFormatterStr, ...] = ("key_value", "json")


@define(frozen=True, slots=True)
class LoggingConfig:
    """
    Configuration for the Pyvider logging subsystem (structlog-based).

    This class defines all logging-specific configuration options, including
    log levels, output formatting, emoji features, and timestamp handling.

    Attributes:
        default_level: The default logging level for all loggers.
                      Can be overridden per module using module_levels.
        module_levels: A dictionary mapping module names to specific log levels.
                      Enables fine-grained control over logging verbosity.
        console_formatter: The formatter to use for console output.
                          "key_value" provides human-readable output,
                          "json" provides machine-parseable structured output.
        logger_name_emoji_prefix_enabled: If True, prepends context-aware emojis
                                        based on logger name patterns.
        das_emoji_prefix_enabled: If True, prepends Domain-Action-Status emojis
                                 based on semantic log fields.
        omit_timestamp: If True, timestamps will be omitted from log entries.
                       Useful for development or when external timestamping is used.

    Example:
        >>> config = LoggingConfig(
        ...     default_level="INFO",
        ...     module_levels={"auth": "DEBUG", "database": "ERROR"},
        ...     console_formatter="json",
        ... )
    """
    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=dict)
    console_formatter: ConsoleFormatterStr = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)


@define(frozen=True, slots=True)
class TelemetryConfig:
    """
    Main configuration object for Pyvider Telemetry (structlog-based).

    This is the top-level configuration class that encompasses all telemetry
    settings, including logging configuration and global system settings.

    Attributes:
        service_name: An optional service name to include in log entries.
                     Useful for identifying logs in multi-service environments.
                     Can also be set via OTEL_SERVICE_NAME or PYVIDER_SERVICE_NAME.
        logging: An instance of `LoggingConfig` for logging-specific settings.
                Provides fine-grained control over logging behavior.
        globally_disabled: If True, all telemetry (including logging) is disabled.
                          Useful for testing or environments where logging is not desired.

    Example:
        >>> config = TelemetryConfig(
        ...     service_name="my-service",
        ...     logging=LoggingConfig(default_level="INFO"),
        ...     globally_disabled=False,
        ... )
    """
    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)

    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """
        Creates a TelemetryConfig instance from environment variables.

        This method provides a convenient way to configure telemetry using
        environment variables, which is common in containerized and cloud
        environments.

        Environment Variables Used:
            Service Configuration:
                - OTEL_SERVICE_NAME or PYVIDER_SERVICE_NAME: For `service_name`.
                  OTEL_SERVICE_NAME takes precedence for OpenTelemetry compatibility.

            Logging Configuration:
                - PYVIDER_LOG_LEVEL: For `logging.default_level`.
                  Valid values: CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE, NOTSET
                - PYVIDER_LOG_CONSOLE_FORMATTER: For `logging.console_formatter`.
                  Valid values: key_value, json
                - PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED: For emoji prefix feature.
                  Valid values: true, false (case insensitive)
                - PYVIDER_LOG_DAS_EMOJI_ENABLED: For DAS emoji feature.
                  Valid values: true, false (case insensitive)
                - PYVIDER_LOG_OMIT_TIMESTAMP: For timestamp handling.
                  Valid values: true, false (case insensitive)
                - PYVIDER_LOG_MODULE_LEVELS: For per-module log levels.
                  Format: "module1:LEVEL1,module2:LEVEL2"
                  Example: "auth:DEBUG,database:ERROR,cache:WARNING"

            Global Configuration:
                - PYVIDER_TELEMETRY_DISABLED: For `globally_disabled`.
                  Valid values: true, false (case insensitive)

        Returns:
            A new TelemetryConfig instance configured from environment variables.

        Note:
            Invalid environment variable values fall back to defaults with
            warnings printed to stderr. This ensures the system remains
            functional even with misconfiguration.

        Example:
            >>> import os
            >>> os.environ["PYVIDER_SERVICE_NAME"] = "my-service"
            >>> os.environ["PYVIDER_LOG_LEVEL"] = "INFO"
            >>> config = TelemetryConfig.from_env()
            >>> assert config.service_name == "my-service"
            >>> assert config.logging.default_level == "INFO"
        """
        # Load service name with OpenTelemetry compatibility
        service_name_env: str | None = os.getenv(
            "OTEL_SERVICE_NAME", os.getenv("PYVIDER_SERVICE_NAME")
        )

        # Load and validate log level
        raw_default_log_level: str = os.getenv("PYVIDER_LOG_LEVEL", "DEBUG").upper()
        default_log_level: LogLevelStr

        match raw_default_log_level:
            case level if level in _VALID_LOG_LEVEL_TUPLE:
                default_log_level = level  # type: ignore[assignment]
            case _:
                print(
                    f"[Pyvider Config Warning] ⚙️➡️⚠️ Invalid PYVIDER_LOG_LEVEL "
                    f"'{raw_default_log_level}'. Defaulting to DEBUG.",
                    file=sys.stderr, flush=True
                )
                default_log_level = "DEBUG"

        # Load and validate console formatter
        raw_console_formatter: str = os.getenv(
            "PYVIDER_LOG_CONSOLE_FORMATTER", "key_value"
        ).lower()
        console_formatter: ConsoleFormatterStr

        match raw_console_formatter:
            case formatter if formatter in _VALID_FORMATTER_TUPLE:
                console_formatter = formatter  # type: ignore[assignment]
            case _:
                print(
                    f"[Pyvider Config Warning] ⚙️➡️⚠️ Invalid PYVIDER_LOG_CONSOLE_FORMATTER "
                    f"'{raw_console_formatter}'. Defaulting to 'key_value'.",
                    file=sys.stderr, flush=True
                )
                console_formatter = "key_value"

        # Load boolean configuration options
        logger_name_emoji_enabled_str: str = os.getenv(
            "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "true"
        ).lower()
        logger_name_emoji_prefix_enabled: bool = logger_name_emoji_enabled_str == "true"

        das_emoji_enabled_str: str = os.getenv(
            "PYVIDER_LOG_DAS_EMOJI_ENABLED", "true"
        ).lower()
        das_emoji_prefix_enabled: bool = das_emoji_enabled_str == "true"

        omit_timestamp_str: str = os.getenv("PYVIDER_LOG_OMIT_TIMESTAMP", "false").lower()
        omit_timestamp_bool: bool = omit_timestamp_str == "true"

        globally_disabled_str: str = os.getenv("PYVIDER_TELEMETRY_DISABLED", "false").lower()
        globally_disabled: bool = globally_disabled_str == "true"

        # Parse module-specific log levels
        module_levels = cls._parse_module_levels(
            os.getenv("PYVIDER_LOG_MODULE_LEVELS", "")
        )

        # Create logging configuration
        log_cfg = LoggingConfig(
            default_level=default_log_level,
            module_levels=module_levels,
            console_formatter=console_formatter,
            logger_name_emoji_prefix_enabled=logger_name_emoji_prefix_enabled,
            das_emoji_prefix_enabled=das_emoji_prefix_enabled,
            omit_timestamp=omit_timestamp_bool,
        )

        # Create and return main configuration
        return cls(
            service_name=service_name_env,
            logging=log_cfg,
            globally_disabled=globally_disabled
        )

    @staticmethod
    def _parse_module_levels(levels_str: str) -> dict[str, LogLevelStr]:
        """
        Parses a comma-separated string of module log level overrides.

        This method handles the parsing of the PYVIDER_LOG_MODULE_LEVELS
        environment variable, which allows setting different log levels
        for different modules or logger names.

        Args:
            levels_str: String in the format "module1:LEVEL1,module2:LEVEL2".
                       Whitespace around module names and levels is ignored.
                       Invalid entries are skipped with warnings.

        Returns:
            A dictionary mapping module names to LogLevelStr values.
            Only valid entries are included in the result.

        Example:
            >>> levels = TelemetryConfig._parse_module_levels("auth:DEBUG,db:ERROR")
            >>> assert levels == {"auth": "DEBUG", "db": "ERROR"}

            >>> # Invalid entries are skipped
            >>> levels = TelemetryConfig._parse_module_levels("auth:DEBUG,bad:INVALID")
            >>> assert levels == {"auth": "DEBUG"}
        """
        levels: dict[str, LogLevelStr] = {}

        if not levels_str.strip():
            return levels

        for item in levels_str.split(","):
            item = item.strip()
            if not item:
                continue

            parts: list[str] = item.split(":", 1)
            match len(parts):
                case 2:
                    module_name: str = parts[0].strip()
                    level_name_raw: str = parts[1].strip().upper()

                    # Validate module name
                    if not module_name:
                        print(
                            f"[Pyvider Config Warning] ⚙️➡️⚠️ Empty module name in "
                            f"PYVIDER_LOG_MODULE_LEVELS item '{item}'. Skipping.",
                            file=sys.stderr, flush=True
                        )
                        continue

                    # Validate and assign log level
                    match level_name_raw:
                        case level if level in _VALID_LOG_LEVEL_TUPLE:
                            levels[module_name] = level  # type: ignore[assignment]
                        case _:
                            print(
                                f"[Pyvider Config Warning] ⚙️➡️⚠️ Invalid log level '{level_name_raw}' "
                                f"for module '{module_name}' in PYVIDER_LOG_MODULE_LEVELS. Skipping.",
                                file=sys.stderr, flush=True
                            )

                case _:
                    print(
                        f"[Pyvider Config Warning] ⚙️➡️⚠️ Invalid item '{item}' in PYVIDER_LOG_MODULE_LEVELS. "
                        "Expected 'module:LEVEL' format. Skipping.",
                        file=sys.stderr, flush=True
                    )

        return levels

# 🐍⚙️
