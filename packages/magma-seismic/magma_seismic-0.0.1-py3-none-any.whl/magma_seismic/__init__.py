#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution
from .dowload import Download

__version__ = get_distribution("magma-seismic").version
__author__ = "Martanto"
__author_email__ = "martanto@live.COM"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-seismic"
