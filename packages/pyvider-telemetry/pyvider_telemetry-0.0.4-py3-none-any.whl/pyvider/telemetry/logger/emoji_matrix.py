#
# emoji_matrix.py
#
"""
Emoji Matrix Definitions for Pyvider Telemetry.

This module defines the dictionaries mapping keywords for Domain, Action, and Status
(DAS) to their respective emojis. It also provides a utility function to display
this "emoji contract" for developers.
"""
import os

from pyvider.telemetry.logger import base as pyvider_logger_base

PRIMARY_EMOJI: dict[str, str] = {
    "system": "⚙️", "server": "🛎️", "client": "🙋", "network": "🌐",
    "security": "🔐", "config": "🔩", "database": "🗄️", "cache": "💾",
    "task": "🔄", "plugin": "🔌", "telemetry": "🛰️", "di": "💉",
    "protocol": "📡", "file": "📄", "user": "👤", "test": "🧪",
    "utils": "🧰", "core": "🌟", "auth": "🔑", "entity": "🦎",
    "report": "📈",
    "default": "❓",
}
"""Emojis for the 'domain' key in DAS logging."""

SECONDARY_EMOJI: dict[str, str] = {
    "init": "🌱", "start": "🚀", "stop": "🛑", "connect": "🔗",
    "disconnect": "💔", "listen": "👂", "send": "📤", "receive": "📥",
    "read": "📖", "write": "📝", "process": "⚙️", "validate": "🛡️",
    "execute": "▶️", "query": "🔍", "update": "🔄", "delete": "🗑️",
    "login": "➡️", "logout": "⬅️", "auth": "🔑", "error": "🔥",
    "encrypt": "🛡️", "decrypt": "🔓", "parse": "🧩", "transmit": "📡",
    "build": "🏗️", "schedule": "📅", "emit": "📢", "load": "💡",
    "observe": "🧐", "request": "🗣️", "interrupt": "🚦",
    "default": "⚙️",
}
"""Emojis for the 'action' key in DAS logging."""

TERTIARY_EMOJI: dict[str, str] = {
    "success": "✅", "failure": "❌", "error": "🔥", "warning": "⚠️",
    "info": "ℹ️", "debug": "🐞", "trace": "👣", "attempt": "⏳",
    "retry": "🔁", "skip": "⏭️", "complete": "🏁", "timeout": "⏱️",
    "notfound": "❓", "unauthorized": "🚫", "invalid": "💢", "cached": "🎯",
    "ongoing": "🏃", "idle": "💤", "ready": "👍",
    "default": "➡️",
}
"""Emojis for the 'status' key in DAS logging."""

def show_emoji_matrix() -> None: # pragma: no cover
    """
    Prints the Pyvider emoji logging contract to the console if enabled.

    This function checks the `PYVIDER_SHOW_EMOJI_MATRIX` environment variable.
    If set to a truthy value (e.g., "true", "1", "yes"), it logs the mapping
    of keywords to emojis for primary, secondary, and tertiary categories.
    """
    if os.getenv("PYVIDER_SHOW_EMOJI_MATRIX", "false").strip().lower() not in ("true", "1", "yes"):
        return

    matrix_logger = pyvider_logger_base.logger.get_logger("pyvider.telemetry.emoji_matrix_display")
    lines = ["Pyvider Emoji Logging Contract:",
             "  1. Single Prefix (logger name): `EMOJI Your log...`",
             "  2. DAS Prefix (keys): `[D][A][S] Your log...`",
             "="*70, "\nPrimary Emojis (DAS 'domain' key):"]
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in PRIMARY_EMOJI.items())
    lines.append("\nSecondary Emojis (DAS 'action' key):")
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in SECONDARY_EMOJI.items())
    lines.append("\nTertiary Emojis (DAS 'status' key):")
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in TERTIARY_EMOJI.items())
    matrix_logger.info("\n".join(lines))

# 💡🧱


