# -*- coding: utf-8 -*-

# geoarray, A fast Python interface for image geodata - either on disk or in memory.
#
# Copyright (C) 2017-2023
# - Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences Potsdam,
#   Germany (https://www.gfz-potsdam.de/)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from osgeo import gdal as _gdal
if 'MPLBACKEND' not in os.environ:
    os.environ['MPLBACKEND'] = 'Agg'

from .baseclasses import GeoArray  # noqa: E402
from .masks import BadDataMask  # noqa: E402
from .masks import NoDataMask  # noqa: E402
from .masks import CloudMask  # noqa: E402

from .version import __version__, __versionalias__   # noqa (E402 + F401)


__author__ = """Daniel Scheffler"""
__email__ = 'danschef@gfz-potsdam.de'
__all__ = ['__version__',
           '__versionalias__',
           '__author__',
           '__email__',
           'GeoArray',
           'BadDataMask',
           'NoDataMask',
           'CloudMask'
           ]

# enable GDAL exceptions
_gdal.UseExceptions()

# $PROJ_LIB was renamed to $PROJ_DATA in proj=9.1.1, which leads to issues with fiona>=1.8.20,<1.9
# https://github.com/conda-forge/pyproj-feedstock/issues/130
# -> fix it by setting PROJ_DATA
if 'GDAL_DATA' in os.environ and 'PROJ_DATA' not in os.environ and 'PROJ_LIB' not in os.environ:
    os.environ['PROJ_DATA'] = os.path.join(os.path.dirname(os.environ['GDAL_DATA']), 'proj')
