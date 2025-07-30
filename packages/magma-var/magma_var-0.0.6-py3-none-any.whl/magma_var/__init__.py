#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution
from magma_var import resources
from magma_var.magma_var import MagmaVar
from magma_var.download import Download
from magma_var.plot import Plot
from magma_var import utils

__version__ = get_distribution("magma-var").version
__author__ = "Martanto"
__author_email__ = "martanto@live.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-var"

__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "resources",
    "Plot",
    "MagmaVar",
    "Download",
    "utils",
]
