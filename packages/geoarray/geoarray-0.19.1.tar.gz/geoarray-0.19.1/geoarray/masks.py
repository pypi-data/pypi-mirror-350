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

from typing import Optional, Union
import numpy as np

# internal imports
from .baseclasses import GeoArray

__author__ = 'Daniel Scheffler'


class _Mask(GeoArray):
    _CLASSNAME = 'Mask baseclass'

    def _validate_array_values(self, array: np.ndarray) -> None:
        if not array.dtype == bool:
            if np.issubdtype(array.dtype, np.integer):
                if np.min(array) < 0 or np.max(array) > 1:
                    pixelvals = sorted(list(np.unique(array)))
                    assert len(pixelvals) <= 2, 'The %s must have only two pixel values (boolean) - 0 and 1 or ' \
                                                'False and True! The given mask for %s contains the values %s.' \
                                                % (self._CLASSNAME, self.basename, pixelvals)
                    assert pixelvals in [[0, 1], [0], [1], [False, True], [False], [True]], \
                        'Found unsupported pixel values in the given %s for %s: %s. ' \
                        'Only the values True, False, 0 and 1 are supported. ' \
                        % (self._CLASSNAME, self.basename, pixelvals)
            else:
                raise TypeError('Boolean or integer array expected.')


class BadDataMask(_Mask):
    _CLASSNAME = 'bad data mask'

    def __init__(self,
                 path_or_array: Union[str, np.ndarray, GeoArray],
                 geotransform: tuple = None,
                 projection: str = None,
                 bandnames: list = None,
                 nodata: Union[float, int] = False,
                 progress: bool = True,
                 q: bool = False
                 ) -> None:
        super(BadDataMask, self).__init__(path_or_array, geotransform=geotransform, projection=projection,
                                          bandnames=bandnames, nodata=nodata, progress=progress, q=q)

        if self.is_inmem:
            # validate input data - before converting to bool
            self._validate_array_values(self.arr)
            self.arr = self.arr.astype(bool)

            # del self._mask_baddata, self.mask_baddata # TODO delete property (requires deleter)

    @property
    def arr(self) -> Optional[np.ndarray]:
        return self._arr

    @arr.setter
    def arr(self, ndarray: np.ndarray) -> None:
        assert isinstance(ndarray, np.ndarray), "'arr' can only be set to a numpy array!"
        self._validate_array_values(ndarray)
        self._arr = ndarray.astype(bool)


class NoDataMask(_Mask):
    _CLASSNAME = 'no data mask'

    def __init__(self,
                 path_or_array: Union[str, np.ndarray, GeoArray],
                 geotransform: tuple = None,
                 projection: str = None,
                 bandnames: list = None,
                 nodata: Union[float, int] = False,
                 progress: bool = True,
                 q: bool = False
                 ) -> None:
        super(NoDataMask, self).__init__(path_or_array, geotransform=geotransform, projection=projection,
                                         bandnames=bandnames, nodata=nodata, progress=progress, q=q)

        if self.is_inmem:
            # validate input data - before converting to bool
            self._validate_array_values(self.arr)
            self.arr = self.arr.astype(bool)

            # del self._mask_nodata, self.mask_nodata # TODO delete property (requires deleter)
            # TODO disk-mode: init must check the numbers of bands, and ideally also the pixel values in mask

    @property
    def arr(self) -> Optional[np.ndarray]:
        return self._arr

    @arr.setter
    def arr(self, ndarray: np.ndarray) -> None:
        assert isinstance(ndarray, np.ndarray), "'arr' can only be set to a numpy array!"
        self._validate_array_values(ndarray)
        self._arr = ndarray.astype(bool)


class CloudMask(_Mask):
    _CLASSNAME = 'cloud mask'

    def __init__(self,
                 path_or_array: Union[str, np.ndarray, GeoArray],
                 geotransform: tuple = None,
                 projection: str = None,
                 bandnames: list = None,
                 nodata: Union[float, int] = False,
                 progress: bool = True,
                 q: bool = False
                 ) -> None:
        # TODO implement class definitions and specific metadata

        super(CloudMask, self).__init__(path_or_array, geotransform=geotransform, projection=projection,
                                        bandnames=bandnames, nodata=nodata, progress=progress, q=q)

        # del self._mask_nodata, self.mask_nodata # TODO delete property (requires deleter)
        # TODO check that: "Automatically detected nodata value for CloudMask 'IN_MEM': 1.0"

    def to_ENVI_classification(self) -> None:  # pragma: no cover
        raise NotImplementedError  # TODO
