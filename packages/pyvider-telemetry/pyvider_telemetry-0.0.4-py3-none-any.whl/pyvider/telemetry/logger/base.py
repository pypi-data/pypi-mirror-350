#
# base.py
#
"""
Base PyviderLogger implementation (structlog-based).

This module defines the `PyviderLogger` class, which provides the main
logging interface for applications using `pyvider.telemetry`. It wraps
`structlog` to offer standard logging methods like info, debug, error, etc.,
along with a custom 'trace' level and Pyvider-specific behaviors.
"""
from typing import TYPE_CHECKING, Any

import structlog

from pyvider.telemetry.logger.custom_processors import TRACE_LEVEL_NAME

if TYPE_CHECKING: # pragma: no cover
    from pyvider.telemetry.config import TelemetryConfig

class PyviderLogger:
    """
    A structlog-based logger for Pyvider applications.

    Provides standard logging methods and integrates with Pyvider's
    telemetry configuration and custom structlog processors.
    A global instance of this class is available as `pyvider.telemetry.logger`.

    This class serves as the primary interface between application code and
    the underlying structlog infrastructure, providing:
    - Standard logging methods (debug, info, warning, error, critical)
    - Custom TRACE level logging for ultra-verbose output
    - Exception logging with automatic traceback capture
    - Named logger creation for component-specific logging
    - Integration with Pyvider's emoji and filtering systems

    Thread Safety:
        This class is thread-safe. Multiple threads can safely call logging
        methods on the same instance or create separate logger instances.

    Performance:
        The logger is optimized for high-throughput scenarios with minimal
        overhead. Processor chains are configured once during setup and
        reused for all subsequent logging operations.
    """

    def __init__(self) -> None:
        """
        Initializes the PyviderLogger.

        Creates the internal structlog logger instance and initializes
        configuration tracking state. The logger is not fully functional
        until setup_telemetry() has been called.

        Note:
            This constructor should generally not be called directly.
            Use the global `logger` instance or create named loggers
            via `logger.get_logger(name)`.
        """
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None

    def get_logger(self, name: str | None = None) -> Any:
        """
        Retrieves a `structlog` bound logger instance with the specified name.

        This method creates a new logger instance that inherits the current
        configuration but is bound to a specific name. The name is used for:
        - Module-specific log level filtering
        - Emoji prefix selection
        - Log routing and identification

        Named loggers enable fine-grained control over logging behavior for
        different components of an application.

        Args:
            name: The desired name for the logger. If None, defaults to
                  "pyvider.default". Names should follow module-like conventions
                  (e.g., "app.auth.oauth", "database.connection") for best
                  integration with filtering and emoji systems.

        Returns:
            A `structlog.BoundLogger` instance configured with the specified
            name and ready for logging operations.

        Example:
            >>> auth_logger = logger.get_logger("app.auth")
            >>> auth_logger.info("User authentication successful")

            >>> db_logger = logger.get_logger("database.queries")
            >>> db_logger.debug("Executing SELECT query", table="users")

        Note:
            The returned logger inherits all configuration from the parent
            but can have different behavior based on its name (e.g., different
            log levels, emoji prefixes).
        """
        effective_name: str = name if name is not None else "pyvider.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def _log_with_level(self, level_method_name: str, event: str, **kwargs: Any) -> None:
        """
        Internal helper to dispatch log events to structlog with specified level.

        This method provides a unified interface for logging at different levels
        by dynamically calling the appropriate structlog method. It handles the
        common pattern of creating a named logger and calling a specific method.

        Args:
            level_method_name: The name of the structlog method to call
                              (e.g., 'info', 'debug', 'error', 'warning', 'critical').
                              Must correspond to a valid method on the structlog logger.
            event: The primary log message text. Should be a formatted string
                   (printf-style formatting should be done by the caller).
            **kwargs: Additional structured data to include in the log entry.
                     These key-value pairs will be available for filtering,
                     formatting, and processing by the configured processor chain.

        Raises:
            AttributeError: If level_method_name does not correspond to a valid
                           method on the structlog logger instance.

        Example:
            >>> # These are equivalent:
            >>> self._log_with_level("info", "User logged in", user_id=123)
            >>> self.info("User logged in", user_id=123)

        Note:
            This method is for internal use only. Application code should use
            the public logging methods (info, debug, error, etc.) instead.
        """
        log = self.get_logger("pyvider.dynamic_call")
        method_to_call = getattr(log, level_method_name)
        method_to_call(event, **kwargs)

    def _format_message_with_args(self, event: str, args: tuple[Any, ...]) -> str:
        """
        Safely format a log message with printf-style arguments.

        This helper method handles printf-style formatting with proper error
        handling to ensure logging never fails due to format string issues.

        Args:
            event: The format string (e.g., "User %s logged in")
            args: Tuple of arguments for formatting

        Returns:
            Formatted string, or safely constructed fallback if formatting fails

        Example:
            >>> self._format_message_with_args("User %s logged in", ("alice",))
            "User alice logged in"

            >>> self._format_message_with_args("Invalid %q format", ("test",))
            "Invalid %q format test"  # Fallback formatting
        """
        if not args:
            return event

        try:
            return event % args
        except (TypeError, ValueError, KeyError):
            # Fallback: append args as space-separated values
            args_str = ' '.join(str(arg) for arg in args)
            return f"{event} {args_str}"

    def trace(self, event: str, *args: Any, _pyvider_logger_name: str | None = None, **kwargs: Any) -> None:
        """
        Logs a message with TRACE level (ultra-verbose debugging).

        The TRACE level is below DEBUG and intended for extremely detailed
        logging that would be too verbose for normal debugging but useful
        for deep troubleshooting or performance analysis.

        This method supports printf-style formatting and provides an option
        to override the logger name for this specific call, enabling precise
        control over trace output routing.

        Args:
            event: The log message, can be a printf-style format string.
                   If args are provided, this string will be formatted using
                   the % operator with appropriate error handling.
            *args: Arguments for printf-style formatting in `event`.
                   If formatting fails, arguments will be appended as a
                   space-separated string to maintain log integrity.
            _pyvider_logger_name: Optional logger name override for this specific call.
                                  If None, defaults to "pyvider.dynamic_call_trace".
                                  This allows routing trace messages to specific
                                  logger hierarchies for filtering purposes.
            **kwargs: Additional structured key-value pairs to include in the log entry.
                     Standard DAS fields (domain, action, status) are supported
                     for semantic logging integration.

        Example:
            >>> # Basic trace logging
            >>> logger.trace("Entering function", function="authenticate_user")

            >>> # With printf-style formatting
            >>> logger.trace("Processing item %d of %d", 5, 100, item_type="user")

            >>> # With custom logger name for routing
            >>> logger.trace("OAuth token validation details",
            ...              _pyvider_logger_name="auth.oauth.trace",
            ...              token_type="bearer", expires_in=3600)

        Note:
            TRACE level logging should be used sparingly as it can generate
            large volumes of output. Consider using module-specific filtering
            to enable TRACE only for components under investigation.
        """
        formatted_event = self._format_message_with_args(event, args)

        logger_name_for_call = _pyvider_logger_name if _pyvider_logger_name is not None else "pyvider.dynamic_call_trace"
        log = structlog.get_logger().bind(logger_name=logger_name_for_call)

        event_kwargs = kwargs.copy()
        event_kwargs["_pyvider_level_hint"] = TRACE_LEVEL_NAME.lower()
        log.msg(formatted_event, **event_kwargs)

    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with DEBUG level.

        DEBUG level is intended for detailed information that is typically
        only of interest when diagnosing problems. This includes variable
        values, execution flow, and intermediate calculations.

        Args:
            event: The log message, can be a printf-style format string.
                   For example: "User %s logged in with role %s"
            *args: Arguments for printf-style formatting in `event`.
                   These will be substituted into the format string using
                   the % operator with error handling for format mismatches.
            **kwargs: Additional structured key-value pairs to include in the log entry.
                     Common patterns include component names, request IDs,
                     user IDs, and other contextual information.

        Example:
            >>> logger.debug("Authentication attempt", user="alice", method="password")
            >>> logger.debug("Query executed in %d ms", 45, table="users", rows=150)

        Note:
            DEBUG messages are typically filtered out in production environments
            but can be selectively enabled per module for troubleshooting.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with INFO level.

        INFO level is for general informational messages that confirm that
        things are working as expected. This includes successful operations,
        significant state changes, and normal application milestones.

        Args:
            event: The log message, can be a printf-style format string.
                   Should be concise but descriptive of the event that occurred.
            *args: Arguments for printf-style formatting in `event`.
                   Will be safely substituted with error handling for mismatches.
            **kwargs: Additional structured key-value pairs to include in the log entry.
                     Use domain/action/status for semantic logging integration.

        Example:
            >>> logger.info("Application started", version="1.0.0", port=8080)
            >>> logger.info("User %s completed registration", "alice@example.com",
            ...             domain="user", action="register", status="success")

        Note:
            INFO is typically the default log level for production environments,
            so these messages should be meaningful but not too verbose.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with WARNING level.

        WARNING level indicates that something unexpected happened, or there's
        an indication of some problem in the near future (e.g., 'disk space low').
        The software is still working as expected, but attention is needed.

        Args:
            event: The log message describing the warning condition.
                   Should clearly indicate what went wrong and potential impact.
            *args: Arguments for printf-style formatting in `event`.
                   Used to include specific values related to the warning.
            **kwargs: Additional structured key-value pairs providing context.
                     Consider including thresholds, current values, and remediation hints.

        Example:
            >>> logger.warning("Disk space low", available_gb=2.5, threshold_gb=5.0)
            >>> logger.warning("Slow database query detected", duration_ms=5000,
            ...               query="SELECT * FROM users", threshold_ms=1000)

        Note:
            Warnings should be actionable - they should indicate conditions
            that operators or developers should investigate or monitor.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    warn = warning # Alias for warning

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with ERROR level.

        ERROR level indicates that a serious problem has occurred that prevented
        the software from performing a function. The application may continue
        running, but functionality has been impaired.

        Args:
            event: The log message describing the error condition.
                   Should be specific about what failed and provide context
                   for debugging and remediation.
            *args: Arguments for printf-style formatting in `event`.
                   Often used to include error codes, failed values, or IDs.
            **kwargs: Additional structured key-value pairs providing error context.
                     Consider including error codes, request IDs, user context,
                     and any relevant state information.

        Example:
            >>> logger.error("Database connection failed", host="db.example.com",
            ...              error_code="CONNECTION_TIMEOUT", retry_count=3)
            >>> logger.error("Payment processing failed for order %s", "ORD-12345",
            ...              user_id=789, amount=99.99, payment_method="credit_card")

        Note:
            ERROR level events typically require immediate attention and may
            trigger alerts in production monitoring systems.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with ERROR level and includes exception information.

        This method should be called from an exception handler to capture
        both the error message and the full exception traceback. It provides
        comprehensive debugging information by automatically including stack
        traces and exception details.

        Args:
            event: The log message describing the context in which the exception occurred.
                   Should explain what the code was trying to do when it failed.
            *args: Arguments for printf-style formatting in `event`.
                   Can include operation details, input parameters, or identifiers.
            **kwargs: Additional structured key-value pairs providing context.
                     The 'exc_info' parameter is automatically set to True to
                     capture exception details. Other useful fields include
                     operation names, user context, and input data.

        Example:
            >>> try:
            ...     result = risky_operation(user_id=123)
            ... except ValueError as e:
            ...     logger.exception("Failed to process user data",
            ...                     user_id=123, operation="data_validation",
            ...                     input_size=len(user_data))

            >>> # With printf formatting
            >>> try:
            ...     connect_to_database(host)
            ... except ConnectionError:
            ...     logger.exception("Database connection failed for host %s", host,
            ...                     timeout=30, retry_count=retry_count)

        Note:
            This method must be called from within an exception handler (try/except block)
            to capture the current exception. Calling it outside of an exception
            context will not include traceback information.
        """
        formatted_event = self._format_message_with_args(event, args)
        kwargs.setdefault('exc_info', True)
        self._log_with_level("error", formatted_event, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with CRITICAL level.

        CRITICAL level indicates that a very serious error has occurred that
        may cause the application to abort or become unable to continue.
        These are the most severe errors that typically require immediate
        intervention.

        Args:
            event: The log message describing the critical failure.
                   Should clearly communicate the severity and impact of the situation.
            *args: Arguments for printf-style formatting in `event`.
                   Used to include critical system state or failure details.
            **kwargs: Additional structured key-value pairs providing critical context.
                     Should include everything necessary for rapid response and
                     system recovery procedures.

        Example:
            >>> logger.critical("System out of memory", available_mb=0, required_mb=512)
            >>> logger.critical("Database corruption detected in table %s", "users",
            ...                 corruption_type="index_mismatch", affected_rows=15000)

        Note:
            CRITICAL level events often trigger immediate alerts and may indicate
            that the application should shut down gracefully to prevent data loss
            or corruption.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None: # pragma: no cover
        """
        Custom attribute setter to protect internal state.

        This method ensures that critical internal attributes can only be
        set through proper initialization and configuration procedures.

        Args:
            name: The attribute name being set.
            value: The value to assign to the attribute.

        Note:
            This method is primarily for internal protection and should not
            be relevant to normal usage of the logger.
        """
        if name in ("_internal_logger", "_is_configured_by_setup", "_active_config"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

logger: PyviderLogger = PyviderLogger()
"""
Global PyviderLogger instance for immediate use.

This is the primary logger instance that applications should use for logging.
It provides access to all logging methods and can create named logger instances
for component-specific logging.

Example:
    >>> from pyvider.telemetry import logger
    >>> logger.info("Application started")
    >>>
    >>> # Create component-specific loggers
    >>> auth_logger = logger.get_logger("auth.service")
    >>> auth_logger.debug("Processing authentication request")
"""

# 🐍📖
