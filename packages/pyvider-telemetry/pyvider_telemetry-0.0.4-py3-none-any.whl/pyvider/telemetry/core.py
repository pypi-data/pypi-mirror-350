#
# core.py
#
"""
Pyvider Telemetry Core Setup (structlog-based).

This module contains the core logic for initializing and configuring the
`structlog` based logging system for Pyvider. It handles processor chains,
log level filtering, formatter selection, and global state management for telemetry.

This module is the heart of the telemetry system, responsible for:
- Setting up and configuring structlog with appropriate processors
- Managing thread-safe initialization and shutdown
- Building processor chains based on configuration
- Handling formatter selection (JSON vs key-value)
- Managing global state and configuration lifecycle
"""
import json
import logging as stdlib_logging
import os
import sys
import threading
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TextIO,
)

import structlog

from pyvider.telemetry.config import LoggingConfig, LogLevelStr, TelemetryConfig
from pyvider.telemetry.logger import base as logger_base_module
from pyvider.telemetry.logger.custom_processors import (
    TRACE_LEVEL_NUM,
    StructlogProcessor,
    add_das_emoji_prefix,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    filter_by_level_custom,
)

if TYPE_CHECKING:
    # Import for type checking only to avoid circular imports
    pass

# Module-level constants for logging infrastructure
_CORE_SETUP_LOGGER_NAME = "pyvider.telemetry.core_setup"
_PYVIDER_LOG_STREAM: TextIO = sys.stderr

def _set_log_stream_for_testing(stream: TextIO | None) -> None:  # pragma: no cover
    """
    Sets the global log stream, primarily for testing purposes.

    This function allows tests to redirect log output to capture and verify
    logging behavior without affecting stderr.

    Args:
        stream: The stream to use for logging output, or None to reset to stderr.

    Note:
        This is intended for testing only and should not be used in production code.
    """
    global _PYVIDER_LOG_STREAM
    _PYVIDER_LOG_STREAM = stream if stream is not None else sys.stderr

def _create_core_setup_logger(globally_disabled: bool = False) -> stdlib_logging.Logger:
    """
    Creates and configures a standard library logger for core setup messages.

    This logger is used specifically for telemetry system setup and teardown
    messages, separate from the main structlog-based logging system.

    Args:
        globally_disabled: If True, uses NullHandler to suppress all output.

    Returns:
        Configured stdlib logger for setup diagnostics.

    Note:
        This logger uses the standard library logging module to avoid
        circular dependencies during system initialization.
    """
    logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)

    # Clear any existing handlers to ensure clean state
    if logger.hasHandlers():
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

    # Configure handler based on disabled state
    handler: stdlib_logging.Handler
    match globally_disabled:
        case True:
            handler = stdlib_logging.NullHandler()
        case False:
            handler = stdlib_logging.StreamHandler(_PYVIDER_LOG_STREAM)
            formatter = stdlib_logging.Formatter(
                "[Pyvider Setup] %(levelname)s (%(name)s): %(message)s"
            )
            handler.setFormatter(formatter)

    # Set log level from environment with fallback
    level_str = os.getenv("PYVIDER_CORE_SETUP_LOG_LEVEL", "INFO").upper()
    level = getattr(stdlib_logging, level_str, stdlib_logging.INFO)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger

# Global state management for setup process
_core_setup_logger = _create_core_setup_logger()
_PYVIDER_SETUP_LOCK = threading.Lock()

# Level mapping for efficient numeric comparisons
_LEVEL_TO_NUMERIC: dict[LogLevelStr, int] = {
    "CRITICAL": stdlib_logging.CRITICAL,
    "ERROR": stdlib_logging.ERROR,
    "WARNING": stdlib_logging.WARNING,
    "INFO": stdlib_logging.INFO,
    "DEBUG": stdlib_logging.DEBUG,
    "TRACE": TRACE_LEVEL_NUM,
    "NOTSET": stdlib_logging.NOTSET,
}

class FormatterProcessor(Protocol):
    """Protocol for structlog formatter processors."""
    def __call__(self, logger_entry: Any) -> str: ...

def _create_service_name_processor(service_name: str | None) -> StructlogProcessor:
    """
    Factory function that creates a structlog processor for service name injection.

    This processor adds a static 'service_name' field to all log events when
    a service name is configured, enabling identification of logs from specific
    services in multi-service environments.

    Args:
        service_name: Service name to inject, or None to skip injection.

    Returns:
        Configured processor function that adds service_name to log events.

    Example:
        >>> processor = _create_service_name_processor("my-service")
        >>> # processor will add service_name="my-service" to all log events
    """
    def processor(
        _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict
    return processor

def _create_timestamp_processor(omit_timestamp: bool) -> list[StructlogProcessor]:
    """
    Creates timestamp-related processors based on configuration.

    This function builds a list of processors that handle timestamp generation
    and optionally removal. Timestamps are always generated first (for consistency)
    but can be removed later if configured to do so.

    Args:
        omit_timestamp: If True, adds processor to remove timestamps after generation.

    Returns:
        List of timestamp-related processors in correct order.

    Note:
        Timestamps are generated in local time with microsecond precision
        using the format "YYYY-MM-DD HH:MM:SS.ffffff".
    """
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False)
    ]

    if omit_timestamp:
        def pop_timestamp_processor(
            _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
        ) -> structlog.types.EventDict:
            """Remove timestamp from event_dict if omit_timestamp is enabled."""
            event_dict.pop("timestamp", None)
            return event_dict
        processors.append(pop_timestamp_processor)

    return processors

def _create_emoji_processors(config: LoggingConfig) -> list[StructlogProcessor]:
    """
    Creates emoji-related processors based on configuration flags.

    This function builds the emoji processing chain, which can include:
    - Logger name emoji prefixes (based on module/logger names)
    - Domain-Action-Status (DAS) emoji prefixes (based on semantic log fields)

    Args:
        config: Logging configuration with emoji settings.

    Returns:
        List of emoji processors to add to the processing chain.

    Note:
        Order matters - logger name emojis are applied before DAS emojis
        to ensure proper visual hierarchy in log output.
    """
    processors: list[StructlogProcessor] = []

    if config.logger_name_emoji_prefix_enabled:
        processors.append(add_logger_name_emoji_prefix)
    if config.das_emoji_prefix_enabled:
        processors.append(add_das_emoji_prefix)

    return processors

def _create_json_formatter_processors() -> list[Any]:
    """
    Creates JSON output formatter processors.

    Returns:
        List of processors for JSON output formatting.
    """
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json.dumps, sort_keys=False)
    ]

def _create_keyvalue_formatter_processors(output_stream: TextIO) -> list[Any]:
    """
    Creates key-value output formatter processors.

    Args:
        output_stream: Output stream for TTY detection and color support.

    Returns:
        List of processors for key-value output formatting.
    """
    processors: list[Any] = []

    # Remove logger_name from key-value output (it's redundant with emojis)
    def pop_logger_name_processor(
        _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Remove logger_name from key-value output to reduce redundancy."""
        event_dict.pop("logger_name", None)
        return event_dict
    processors.append(pop_logger_name_processor)

    # Add console renderer with TTY detection for colors
    is_tty = hasattr(output_stream, 'isatty') and output_stream.isatty()
    processors.append(
        structlog.dev.ConsoleRenderer(
            colors=is_tty,
            exception_formatter=structlog.dev.plain_traceback,
        )
    )

    return processors

def _create_formatter_processors(
    config: LoggingConfig, output_stream: TextIO
) -> list[Any]:
    """
    Creates output formatter processors based on configuration.

    This function builds the final stage of the processor chain that handles
    converting structured log events into their final output format.

    Args:
        config: Logging configuration with formatter settings.
        output_stream: Output stream for TTY detection and color support.

    Returns:
        List of formatter processors for the specified format.

    Raises:
        ValueError: If an unknown formatter type is specified.
    """
    match config.console_formatter:
        case "json":
            _core_setup_logger.info("📝➡️🎨 Configured JSON renderer.")
            return _create_json_formatter_processors()

        case "key_value":
            _core_setup_logger.info("📝➡️🎨 Configured Key-Value (ConsoleRenderer).")
            return _create_keyvalue_formatter_processors(output_stream)

        case unknown_formatter:
            # This should never happen due to config validation, but handle gracefully
            _core_setup_logger.warning(f"Unknown formatter: {unknown_formatter}")
            return _create_keyvalue_formatter_processors(output_stream)

def _build_core_processor_chain(config: TelemetryConfig) -> list[StructlogProcessor]:
    """
    Builds the core processor chain (excluding formatters) based on configuration.

    This function assembles the main processor chain in the correct order:
    1. Context merging and log level processing
    2. Filtering based on log levels
    3. Stack info and exception handling
    4. Timestamp processing
    5. Service name injection
    6. Emoji processing

    Args:
        config: Complete telemetry configuration.

    Returns:
        Ordered list of core processors (excludes formatters).

    Note:
        Order is critical - processors are applied sequentially and
        some depend on data added by previous processors.
    """
    log_cfg = config.logging

    # Base processors that are always included
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        add_log_level_custom,
        filter_by_level_custom(
            default_level_str=log_cfg.default_level,
            module_levels=log_cfg.module_levels,
            level_to_numeric_map=_LEVEL_TO_NUMERIC
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    # Add timestamp processors
    processors.extend(_create_timestamp_processor(log_cfg.omit_timestamp))

    # Add service name processor if configured
    if config.service_name is not None:
        processors.append(_create_service_name_processor(config.service_name))

    # Add emoji processors
    processors.extend(_create_emoji_processors(log_cfg))

    return processors

def _build_complete_processor_chain(config: TelemetryConfig) -> list[Any]:
    """
    Builds the complete processor chain including formatters.

    This function combines core processors with formatter processors
    to create the final processor chain for structlog configuration.

    Args:
        config: Complete telemetry configuration.

    Returns:
        Complete ordered list of processors including formatters.
    """
    core_processors = _build_core_processor_chain(config)
    output_stream = _PYVIDER_LOG_STREAM
    formatter_processors = _create_formatter_processors(config.logging, output_stream)

    # Combine core and formatter processors
    return core_processors + formatter_processors

def _apply_structlog_configuration(processors: list[Any]) -> None:
    """
    Applies the processor chain to structlog configuration.

    This function performs the final structlog configuration with the
    provided processor chain.

    Args:
        processors: Complete list of processors to configure.
    """
    output_stream = _PYVIDER_LOG_STREAM

    # Configure structlog with our processor chain
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=output_stream),
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

    stream_name = 'sys.stderr' if output_stream == sys.stderr else 'custom stream (testing)'
    _core_setup_logger.info(
        f"📝➡️✅ structlog configured. Wrapper: BoundLogger. Output: {stream_name}."
    )

def _configure_structlog_output(config: TelemetryConfig) -> None:
    """
    Configures structlog with the complete processor chain and output settings.

    This function orchestrates the structlog configuration by:
    1. Building the complete processor chain
    2. Applying the configuration to structlog

    Args:
        config: Complete telemetry configuration.

    Raises:
        Exception: If structlog configuration fails.

    Note:
        This function has global side effects and should only be called
        during system initialization with proper locking.
    """
    processors = _build_complete_processor_chain(config)
    _apply_structlog_configuration(processors)

def _handle_globally_disabled_setup() -> None:
    """
    Handles the setup process when telemetry is globally disabled.

    When telemetry is disabled, we still need to:
    1. Log a notification about the disabled state
    2. Configure structlog with minimal processors to avoid errors

    This ensures that logging calls don't fail even when disabled,
    they just produce no output.
    """
    # Create temporary logger for disabled message
    temp_logger_name = f"{_CORE_SETUP_LOGGER_NAME}_temp_disabled_msg"
    temp_logger = stdlib_logging.getLogger(temp_logger_name)

    # Check if we need to configure this temporary logger
    needs_configuration = (
        not temp_logger.handlers or
        not any(
            isinstance(h, stdlib_logging.StreamHandler) and h.stream == sys.stderr
            for h in temp_logger.handlers
        )
    )

    if needs_configuration:
        # Clear and reconfigure
        for h in list(temp_logger.handlers):
            temp_logger.removeHandler(h)

        temp_handler = stdlib_logging.StreamHandler(sys.stderr)
        temp_formatter = stdlib_logging.Formatter(
            "[Pyvider Setup] %(levelname)s (%(name)s): %(message)s"
        )
        temp_handler.setFormatter(temp_formatter)
        temp_logger.addHandler(temp_handler)
        temp_logger.setLevel(stdlib_logging.INFO)
        temp_logger.propagate = False

    temp_logger.info("⚙️➡️🚫 Pyvider telemetry globally disabled.")

    # Configure minimal structlog setup to avoid errors
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory()
    )

def reset_pyvider_setup_for_testing() -> None:
    """
    Resets structlog defaults and Pyvider logger state for isolated testing.

    This function ensures that tests do not interfere with each other by:
    1. Resetting structlog to default configuration
    2. Clearing Pyvider logger state
    3. Restoring default log stream
    4. Recreating setup logger

    Note:
        This is crucial for test isolation and should be called before
        each test that configures telemetry.
    """
    global _core_setup_logger, _PYVIDER_LOG_STREAM

    with _PYVIDER_SETUP_LOCK:
        structlog.reset_defaults()
        logger_base_module.logger._is_configured_by_setup = False
        logger_base_module.logger._active_config = None
        _PYVIDER_LOG_STREAM = sys.stderr
        _core_setup_logger = _create_core_setup_logger()

def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Initializes and configures the Pyvider telemetry system (structlog).

    This is the main entry point for setting up logging. It configures structlog
    processors, formatters, and log levels based on the provided configuration
    or environment variables if no configuration is given.

    The setup process includes:
    1. Thread-safe initialization with locking
    2. Configuration loading (programmatic or environment-based)
    3. Processor chain building and configuration
    4. Logger state management

    Args:
        config: An optional TelemetryConfig instance. If None, configuration
                is loaded from environment variables via TelemetryConfig.from_env().

    Thread Safety:
        This function is thread-safe and uses internal locking to prevent
        concurrent setup operations. Multiple calls are safe but only the
        first call will perform actual configuration.

    Example:
        >>> # Simple setup with defaults
        >>> setup_telemetry()

        >>> # Setup with custom configuration
        >>> config = TelemetryConfig(service_name="my-service")
        >>> setup_telemetry(config)
    """
    global _PYVIDER_LOG_STREAM, _core_setup_logger

    with _PYVIDER_SETUP_LOCK:
        # Reset state to ensure clean initialization
        structlog.reset_defaults()
        logger_base_module.logger._is_configured_by_setup = False
        logger_base_module.logger._active_config = None

        # Load configuration from parameter or environment
        current_config = config if config is not None else TelemetryConfig.from_env()
        _core_setup_logger = _create_core_setup_logger(
            globally_disabled=current_config.globally_disabled
        )

        # Log setup start (unless globally disabled)
        if not current_config.globally_disabled:
            _core_setup_logger.info("⚙️➡️🚀 Starting Pyvider (structlog) setup...")

        # Handle the two main setup paths
        match current_config.globally_disabled:
            case True:
                _handle_globally_disabled_setup()
            case False:
                _configure_structlog_output(current_config)

        # Mark as configured and store active configuration
        logger_base_module.logger._is_configured_by_setup = True
        logger_base_module.logger._active_config = current_config

        if not current_config.globally_disabled:
            _core_setup_logger.info("⚙️➡️✅ Pyvider (structlog) setup process completed.")

async def shutdown_pyvider_telemetry(timeout_millis: int = 5000) -> None:  # pragma: no cover
    """
    Performs shutdown procedures for Pyvider telemetry.

    Currently, this primarily logs a shutdown message and performs cleanup.
    In the future, it might be used to flush telemetry buffers or release resources.

    Args:
        timeout_millis: A timeout in milliseconds for shutdown operations.
                        Currently unused but reserved for future buffer flushing.

    Thread Safety:
        This function is async-safe and does not modify global state.
        It can be safely called from async contexts.

    Note:
        This function is async to support future enhancements like
        buffer flushing or network resource cleanup.

    Example:
        >>> # In async context
        >>> await shutdown_pyvider_telemetry()

        >>> # In sync context
        >>> import asyncio
        >>> asyncio.run(shutdown_pyvider_telemetry())
    """
    _core_setup_logger.info("🔌➡️🏁 Pyvider telemetry shutdown called.")

# 🐍🛠️
