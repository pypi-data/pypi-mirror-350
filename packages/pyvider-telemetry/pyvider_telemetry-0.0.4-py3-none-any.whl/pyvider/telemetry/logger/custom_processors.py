#
# custom_processors.py
#
"""
Custom structlog processors for Pyvider Telemetry.

This module defines structlog processors that add Pyvider-specific
functionality to the logging pipeline, such as custom log level handling,
log filtering, and emoji prefixing based on logger name or
Domain-Action-Status (DAS) keys.

The processors implemented here are:
- Log level normalization and custom TRACE level support
- Level-based filtering with module-specific overrides
- Logger name-based emoji prefixing with performance optimization
- Domain-Action-Status emoji prefixing for semantic logging
"""
import logging as stdlib_logging
from typing import TYPE_CHECKING, Any, Protocol, cast

import structlog

from pyvider.telemetry.config import LogLevelStr
from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
)

if TYPE_CHECKING:
    # Type checking imports
    pass

# Custom TRACE level configuration
TRACE_LEVEL_NUM: int = 5
"""
Numeric value for the custom TRACE log level (below DEBUG).

This value places TRACE between NOTSET (0) and DEBUG (10), making it
the most verbose logging level available. The choice of 5 provides
room for future intermediate levels if needed.
"""

TRACE_LEVEL_NAME: str = "TRACE"
"""String name for the custom TRACE log level."""

# Register TRACE level with standard library logging if not already present
if not hasattr(stdlib_logging, TRACE_LEVEL_NAME):  # pragma: no cover
    stdlib_logging.addLevelName(TRACE_LEVEL_NUM, TRACE_LEVEL_NAME)

# Mapping of numeric levels to string names for efficient lookup
_NUMERIC_TO_LEVEL_NAME_CUSTOM: dict[int, str] = {
    stdlib_logging.CRITICAL: "critical",
    stdlib_logging.ERROR: "error",
    stdlib_logging.WARNING: "warning",
    stdlib_logging.INFO: "info",
    stdlib_logging.DEBUG: "debug",
    TRACE_LEVEL_NUM: TRACE_LEVEL_NAME.lower(),
}

class StructlogProcessor(Protocol):
    """
    Protocol for structlog processor functions.

    This protocol defines the interface that all structlog processors
    must implement, providing type safety and documentation for the
    processor chain system.
    """
    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """
        Process a log event dictionary.

        Args:
            logger: The logger instance (often unused by processors).
            method_name: The logging method name (e.g., 'info', 'error').
            event_dict: The structured event dictionary to process.

        Returns:
            The processed event dictionary.

        Raises:
            structlog.DropEvent: If the event should be suppressed.
        """
        ...

def add_log_level_custom(
    _logger: Any, method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Structlog processor to add or normalize the 'level' field in the event dictionary.

    This processor ensures that all log events have a consistent 'level' field
    by deriving it from the method name or using a custom hint if provided.
    It also handles special cases like the custom TRACE level and method aliases.

    Args:
        _logger: The logger instance (unused in this processor).
        method_name: The logging method name (e.g., 'info', 'error', 'debug').
        event_dict: The structured event dictionary to process.

    Returns:
        The event dictionary with a normalized 'level' field.

    Note:
        The '_pyvider_level_hint' field is used internally for the custom
        TRACE level and is removed from the final output.

    Example:
        >>> event_dict = {"event": "test message", "_pyvider_level_hint": "trace"}
        >>> result = add_log_level_custom(None, "msg", event_dict)
        >>> assert result["level"] == "trace"
        >>> assert "_pyvider_level_hint" not in result
    """
    # Check for custom level hint (used for TRACE level)
    level_hint: str | None = event_dict.pop("_pyvider_level_hint", None)

    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        # Map method names to standard log levels
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()

    return event_dict

class _LevelFilter:
    """
    Callable class for filtering log events based on configured log levels.

    This filter implements a hierarchical logging system where:
    1. Each logger has an effective log level (default or module-specific)
    2. Events below the effective level are dropped
    3. Module-specific levels override the default level
    4. Longest matching module path takes precedence

    The filter compares the event's log level against the effective level
    for the logger and raises `structlog.DropEvent` if the event should be suppressed.

    Attributes:
        default_numeric_level: The default numeric log level.
        module_numeric_levels: Dict mapping module paths to numeric levels.
        level_to_numeric_map: Dict mapping level strings to numeric values.
        sorted_module_paths: Module paths sorted by length (longest first).
    """

    def __init__(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int]
    ) -> None:
        """
        Initialize the level filter with configuration.

        Args:
            default_level_str: Default log level string.
            module_levels: Dict mapping module names to level strings.
            level_to_numeric_map: Dict mapping level strings to numeric values.
        """
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str]
            for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map

        # Sort module paths by length (longest first) for prefix matching
        self.sorted_module_paths: list[str] = sorted(
            self.module_numeric_levels.keys(), key=len, reverse=True
        )

    def __call__(
        self, _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """
        Filters the log event based on configured levels.

        This method determines the effective log level for the logger and
        compares it against the event's level. If the event level is below
        the threshold, `structlog.DropEvent` is raised to suppress the event.

        Args:
            _logger: The logger instance (unused).
            _method_name: The logging method name (unused).
            event_dict: The event dictionary containing logger_name and level.

        Returns:
            The unmodified event_dict if the event should be logged.

        Raises:
            structlog.DropEvent: If the event should be suppressed.

        Note:
            Module path matching uses prefix matching, so "auth.oauth" will
            match a configured level for "auth" if no more specific match exists.
        """
        # Extract logger name and event level from the event
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info")).upper()
        event_level_text: LogLevelStr = cast(LogLevelStr, event_level_str_from_dict)

        # Convert event level to numeric for comparison
        event_num_level: int = self.level_to_numeric_map.get(
            event_level_text, self.level_to_numeric_map["INFO"]
        )

        # Determine effective threshold level for this logger
        threshold_num_level: int = self.default_numeric_level

        # Find the most specific module-level override
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break

        # Drop event if it's below the threshold
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent

        return event_dict

def filter_by_level_custom(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int]
) -> _LevelFilter:
    """
    Factory function that returns an instance of the `_LevelFilter` processor.

    This function creates a configured level filter that can be added to
    the structlog processor chain to implement hierarchical log filtering.

    Args:
        default_level_str: The default log level for all loggers.
        module_levels: Dict mapping module names to specific log levels.
        level_to_numeric_map: Dict mapping level strings to numeric values.

    Returns:
        A configured _LevelFilter instance ready for use as a processor.

    Example:
        >>> filter_proc = filter_by_level_custom(
        ...     "INFO",
        ...     {"auth": "DEBUG", "database": "ERROR"},
        ...     {"DEBUG": 10, "INFO": 20, "ERROR": 40}
        ... )
    """
    return _LevelFilter(default_level_str, module_levels, level_to_numeric_map)

# Logger name to emoji mapping for visual log parsing
_LOGGER_NAME_EMOJI_PREFIXES: dict[str, str] = {
    'pyvider.telemetry.core.test': '⚙️',
    'pyvider.telemetry.core_setup': '🛠️',
    'pyvider.telemetry.emoji_matrix_display': '💡',
    'pyvider.telemetry': '⚙️',
    'pyvider.telemetry.logger': '📝',
    'pyvider.telemetry.config': '🔩',
    'pyvider.dynamic_call_trace': '👣',
    'pyvider.dynamic_call': '🗣️',
    'pyvider.default': '📦',
    'formatter.test': '🎨',
    'service.alpha': '🇦',
    'service.beta': '🇧',
    'service.beta.child': '👶',
    'service.gamma.trace_enabled': '🇬',
    'service.delta': '🇩',
    'das.test': '🃏',
    'json.exc.test': '💥',
    'service.name.test': '📛',
    'simple': '📄',
    'test.basic': '🧪',
    'unknown': '❓',
    'test': '🧪',
    'default': '🔹',
}

# Sort logger name patterns by length (longest first) for prefix matching
_SORTED_LOGGER_NAME_EMOJI_KEYWORDS: list[str] = sorted(
    _LOGGER_NAME_EMOJI_PREFIXES.keys(), key=len, reverse=True
)

# Performance optimization: Cache emoji lookups for frequently used logger names
_EMOJI_LOOKUP_CACHE: dict[str, str] = {}
_EMOJI_CACHE_SIZE_LIMIT: int = 1000  # Prevent unbounded cache growth

def _compute_emoji_for_logger_name(logger_name: str) -> str:
    """
    Computes the appropriate emoji for a given logger name.

    This function implements the core emoji lookup logic using
    longest-prefix matching against the predefined emoji patterns.

    Args:
        logger_name: The logger name to find an emoji for.

    Returns:
        The appropriate emoji string for the logger name.
    """
    # Find the most specific emoji pattern match
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == 'default':
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]

    # Return default emoji if no match found
    return _LOGGER_NAME_EMOJI_PREFIXES.get('default', '🔹')

def add_logger_name_emoji_prefix(
    _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Structlog processor to prepend an emoji to the log event message based on `logger_name`.

    This processor adds visual context to log messages by prepending emojis
    that correspond to the logger name or module. The emoji selection uses
    prefix matching with performance-optimized caching for frequently used names.

    Args:
        _logger: The logger instance (unused).
        _method_name: The logging method name (unused).
        event_dict: The event dictionary containing logger_name and event message.

    Returns:
        The event dictionary with emoji prepended to the 'event' field.

    Note:
        The emoji selection uses longest-prefix matching, so "pyvider.telemetry.core"
        will match the specific pattern before falling back to "pyvider.telemetry".
        Results are cached for performance optimization.

    Example:
        >>> event_dict = {"logger_name": "auth.service", "event": "User login"}
        >>> result = add_logger_name_emoji_prefix(None, "info", event_dict)
        >>> # result["event"] might be "🔑 User login" if auth maps to key emoji
    """
    logger_name_from_event: str = event_dict.get("logger_name", "default")

    # Check cache first for performance
    if logger_name_from_event in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name_from_event]
    else:
        # Compute emoji and cache the result
        chosen_emoji = _compute_emoji_for_logger_name(logger_name_from_event)

        # Cache management: prevent unbounded growth
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name_from_event] = chosen_emoji
        # If cache is full, we skip caching but still return the computed emoji

    # Prepend emoji to event message
    event_msg: Any = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji

    return event_dict

def add_das_emoji_prefix(
    _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Structlog processor to prepend a Domain-Action-Status (DAS) emoji sequence.

    This processor implements semantic logging by looking for 'domain', 'action',
    and 'status' keys in the event dictionary and converting them to a visual
    emoji prefix in the format [D_emoji][A_emoji][S_emoji].

    The DAS pattern provides structured meaning to log events:
    - Domain: What system/component (auth, database, network, etc.)
    - Action: What operation (login, query, connect, etc.)
    - Status: What outcome (success, error, warning, etc.)

    Args:
        _logger: The logger instance (unused).
        _method_name: The logging method name (unused).
        event_dict: The event dictionary potentially containing DAS fields.

    Returns:
        The event dictionary with DAS emoji prefix and DAS fields removed.

    Note:
        The original 'domain', 'action', 'status' keys are removed from the
        event_dict after processing to avoid duplication in the output.

    Example:
        >>> event_dict = {
        ...     "event": "User authenticated",
        ...     "domain": "auth",
        ...     "action": "login",
        ...     "status": "success"
        ... }
        >>> result = add_das_emoji_prefix(None, "info", event_dict)
        >>> # result["event"] might be "[🔑][➡️][✅] User authenticated"
        >>> assert "domain" not in result
        >>> assert "action" not in result
        >>> assert "status" not in result
    """
    # Extract and remove DAS fields from event dictionary
    domain_val_orig = event_dict.pop("domain", None)
    action_val_orig = event_dict.pop("action", None)
    status_val_orig = event_dict.pop("status", None)

    # Convert to lowercase strings for consistent lookup
    domain_val: str = str(domain_val_orig).lower() if domain_val_orig is not None else ""
    action_val: str = str(action_val_orig).lower() if action_val_orig is not None else ""
    status_val: str = str(status_val_orig).lower() if status_val_orig is not None else ""

    # Only add DAS prefix if at least one field is present
    if domain_val or action_val or status_val:
        # Look up emojis with fallback to defaults
        domain_emoji: str = PRIMARY_EMOJI.get(domain_val, PRIMARY_EMOJI["default"])
        action_emoji: str = SECONDARY_EMOJI.get(action_val, SECONDARY_EMOJI["default"])
        status_emoji: str = TERTIARY_EMOJI.get(status_val, TERTIARY_EMOJI["default"])

        # Build DAS prefix in standard format
        das_prefix = f"[{domain_emoji}][{action_emoji}][{status_emoji}]"

        # Prepend DAS prefix to event message
        event_msg: Any = event_dict.get("event")
        if event_msg is not None:
            event_dict["event"] = f"{das_prefix} {event_msg}"
        else:
            event_dict["event"] = das_prefix

    return event_dict

# Performance monitoring functions for cache effectiveness
def get_emoji_cache_stats() -> dict[str, Any]:  # pragma: no cover
    """
    Returns statistics about the emoji lookup cache for performance monitoring.

    Returns:
        Dictionary containing cache size and hit rate information.

    Note:
        This function is primarily for debugging and performance monitoring.
    """
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100,
    }

def clear_emoji_cache() -> None:  # pragma: no cover
    """
    Clears the emoji lookup cache.

    This can be useful for testing or if cache invalidation is needed
    due to configuration changes.
    """
    global _EMOJI_LOOKUP_CACHE
    _EMOJI_LOOKUP_CACHE.clear()

# 🧱✨
