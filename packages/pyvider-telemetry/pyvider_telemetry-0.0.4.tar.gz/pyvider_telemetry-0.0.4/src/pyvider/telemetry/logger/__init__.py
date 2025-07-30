#
# __init__.py
#
"""
Pyvider Telemetry Logger Interface.

This module exports the primary logger instance and related emoji utilities.
"""
from pyvider.telemetry.logger.base import PyviderLogger, logger
from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    show_emoji_matrix,
)

__all__ = [
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "PyviderLogger",
    "logger",
    "show_emoji_matrix",
]

# 🐍📝


