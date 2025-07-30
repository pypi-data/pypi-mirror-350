#
# test_property_based.py
#
"""
Property-based tests for Pyvider Telemetry using Hypothesis.

These tests aim to cover a wider range of inputs and edge cases
by generating test data automatically.
"""
from collections.abc import Callable
import io
from typing import Any, TextIO # TextIO is correct

from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import (
    text,
    dictionaries,
    sampled_from,
    booleans,
    # fixed_dictionaries, # Not used, can remove
    one_of,
    none,
    lists,
    integers,
    composite,
    SearchStrategy,
    # DataObject, # Not used, can remove
    # data, # Not used, can remove
)
# import pytest # Not strictly needed for this file if no pytest specific markers are used beyond @given

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger as pyvider_global_logger,
    setup_telemetry,
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
)
from pyvider.telemetry.config import LogLevelStr, ConsoleFormatterStr
from pyvider.telemetry.core import reset_pyvider_setup_for_testing, _set_log_stream_for_testing # Import necessary functions

# --- Strategies ---

# Strategy for valid logger names (simplified for robustness)
logger_names_st = text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._- ",
    min_size=0,
    max_size=50
)

# Strategy for log messages
log_messages_st = text(max_size=200)

# Strategy for DAS (Domain-Action-Status) keys
das_keys_base_st = list(PRIMARY_EMOJI.keys()) + list(SECONDARY_EMOJI.keys()) + list(TERTIARY_EMOJI.keys())
das_values_st = one_of(
    none(),
    sampled_from(das_keys_base_st),
    text(alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=3, max_size=15)
)

# Strategy for arbitrary kwargs
simple_kwargs_st = dictionaries(
    keys=text(alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=1, max_size=20),
    values=one_of(
        none(),
        booleans(),
        integers(),
        text(max_size=50),
    ),
    max_size=5
)

# Strategy for log levels (strings)
log_levels_st = sampled_from(list(LogLevelStr.__args__)) # type: ignore

# Strategy for console formatters
console_formatters_st = sampled_from(list(ConsoleFormatterStr.__args__)) # type: ignore

# Composite strategy for TelemetryConfig
@composite
def telemetry_config_st(draw: Callable[[SearchStrategy[Any]], Any]) -> TelemetryConfig:
    service_name = draw(one_of(none(), text(max_size=30)))
    default_level = draw(log_levels_st)
    
    module_levels_keys = draw(lists(logger_names_st, max_size=5))
    module_levels_values = draw(lists(log_levels_st, min_size=len(module_levels_keys), max_size=len(module_levels_keys)))
    module_levels = dict(zip(module_levels_keys, module_levels_values))

    console_formatter = draw(console_formatters_st)
    logger_name_emoji_enabled = draw(booleans())
    das_emoji_enabled = draw(booleans())
    omit_timestamp = draw(booleans())
    globally_disabled = draw(booleans())

    logging_conf = LoggingConfig(
        default_level=default_level, # type: ignore
        module_levels=module_levels, # type: ignore
        console_formatter=console_formatter, # type: ignore
        logger_name_emoji_prefix_enabled=logger_name_emoji_enabled,
        das_emoji_prefix_enabled=das_emoji_enabled,
        omit_timestamp=omit_timestamp,
    )
    return TelemetryConfig(
        service_name=service_name,
        logging=logging_conf,
        globally_disabled=globally_disabled,
    )

# --- Tests ---

@given(
    config=telemetry_config_st(),
    logger_name=logger_names_st,
    message=log_messages_st,
    domain=das_values_st,
    action=das_values_st,
    status=das_values_st,
    extra_kwargs=simple_kwargs_st,
    log_method_name=sampled_from(["debug", "info", "warning", "error", "critical", "trace", "exception"])
)
@settings(
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.data_too_large,
        HealthCheck.filter_too_much,
        HealthCheck.function_scoped_fixture # Add this to suppress the warning if manual reset is correct
    ],
    deadline=None,
    max_examples=50
)
def test_pyvider_logger_robustness( # Removed pytest fixtures from arguments
    config: TelemetryConfig,
    logger_name: str,
    message: str,
    domain: str | None,
    action: str | None,
    status: str | None,
    extra_kwargs: dict[str, Any],
    log_method_name: str
) -> None:
    """
    Tests that PyviderLogger methods do not crash with varied inputs.
    """
    # Manual setup for each Hypothesis example
    reset_pyvider_setup_for_testing() # Ensure clean state
    current_example_log_capture_buffer = io.StringIO()
    _set_log_stream_for_testing(current_example_log_capture_buffer)

    try:
        setup_telemetry(config) # Use the generated config for this example

        log_call_kwargs = extra_kwargs.copy()
        if domain is not None:
            log_call_kwargs["domain"] = domain
        if action is not None:
            log_call_kwargs["action"] = action
        if status is not None:
            log_call_kwargs["status"] = status
        
        current_logger = pyvider_global_logger
        log_method_to_call = getattr(current_logger, log_method_name)

        if log_method_name == "exception":
            try:
                raise ValueError("Hypothesis test exception")
            except ValueError:
                log_method_to_call(message, **log_call_kwargs)
        elif log_method_name == "trace":
            trace_kwargs = log_call_kwargs.copy()
            if "logger_name" in trace_kwargs:
                del trace_kwargs["logger_name"]
            current_logger.trace(message, _pyvider_logger_name=logger_name, **trace_kwargs)
        else:
            log_method_to_call(message, **log_call_kwargs)

        # Optional: Basic check on output if not globally disabled
        # if not config.globally_disabled:
        #     output = current_example_log_capture_buffer.getvalue()
            # Basic check, e.g., assert len(output) > 0 if a message was expected to be logged
            # This depends on log levels, so it's tricky for a general robustness test.

    except Exception as e: # pragma: no cover
        import pytest # Import pytest here for pytest.fail
        pytest.fail(
            f"Logging call failed unexpectedly with error: {e}\n"
            f"Config: {config}\n"
            f"Logger Name: {logger_name}\n"
            f"Method: {log_method_name}\n"
            f"Message: {message[:100]}...\n"
            f"Domain: {domain}, Action: {action}, Status: {status}\n"
            f"Extra Kwargs: {extra_kwargs}"
        )
    finally:
        # Manual teardown for each Hypothesis example
        _set_log_stream_for_testing(None) # Restore default stream
        current_example_log_capture_buffer.close()

# 🧪🔬
