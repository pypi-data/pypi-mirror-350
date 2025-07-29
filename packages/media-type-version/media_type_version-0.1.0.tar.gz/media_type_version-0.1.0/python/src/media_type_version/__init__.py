# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Extract the format version from a media type string."""

from __future__ import annotations

from .defs import VERSION
from .defs import Config
from .defs import MTVError
from .impl import extract


__all__ = [
    "VERSION",
    "Config",
    "MTVError",
    "extract",
]
