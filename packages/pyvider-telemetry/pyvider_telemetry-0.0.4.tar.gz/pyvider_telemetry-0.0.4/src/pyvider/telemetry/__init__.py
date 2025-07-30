#
# __init__.py
#
"""
Pyvider Telemetry Library (structlog-based).

This module serves as the main entry point for the pyvider.telemetry package,
re-exporting key components for ease of use.
"""

from importlib.metadata import PackageNotFoundError, version

# Dynamic version loading from package metadata
try:
    __version__ = version("pyvider-telemetry")
except PackageNotFoundError:  # pragma: no cover
    # Fallback for development/editable installs
    __version__ = "0.0.0-dev"

from pyvider.telemetry.config import LoggingConfig, LogLevelStr, TelemetryConfig
from pyvider.telemetry.core import setup_telemetry, shutdown_pyvider_telemetry
from pyvider.telemetry.logger import logger
from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
)

__all__ = [
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "LogLevelStr",
    "LoggingConfig",
    "TelemetryConfig",
    "__version__",
    "logger",
    "setup_telemetry",
    "shutdown_pyvider_telemetry",
]

# 🐍📝
