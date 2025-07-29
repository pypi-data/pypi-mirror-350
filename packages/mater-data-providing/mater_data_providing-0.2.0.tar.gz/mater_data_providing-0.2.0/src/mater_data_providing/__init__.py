"""
This module defines the functions of the package, the logging configuration and the __version__ of the package.

Copyright (C) 2025 @verzierf <francois.verzier@univ-grenoble-alpes.fr>

SPDX-License-Identifier: LGPL-3.0-or-later
"""

import logging
from importlib.metadata import PackageNotFoundError, version

from .core import (
    dump_json,
    metadata_definition,
    provider_definition,
    replace_equivalence,
    to_json,
)

# Version
try:
    __version__ = version("mater-data-providing")
except PackageNotFoundError:
    __version__ = "unknown"

# Wildcard imports
__all__ = [
    "metadata_definition",
    "provider_definition",
    "to_json",
    "replace_equivalence",
    "dump_json",
]

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
