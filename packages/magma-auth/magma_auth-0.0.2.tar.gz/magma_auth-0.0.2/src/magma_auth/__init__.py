#!/usr/bin/env python
# -*- coding: utf-8 -*-

from magma_auth.magma_auth import MagmaAuth, auth
from pkg_resources import get_distribution

__version__ = get_distribution("magma-auth").version
__author__ = "Martanto"
__author_email__ = "martanto@live.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-auth"

__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "MagmaAuth",
    "auth",
]
