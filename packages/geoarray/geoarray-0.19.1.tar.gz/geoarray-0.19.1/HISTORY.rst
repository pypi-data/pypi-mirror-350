=======
History
=======

0.19.1 (2025-05-26)
-------------------

* !57: Pinned holoviews to >1.12.7 to fix an incompatibility within newer environments.
* !58: Fixed #47 (Integer overflow in GeoArray.read_pointData for rasters larger than int16 max (32767)).
* !59: Adapted license declaration in pyproject.toml to new PEP 639.


0.19.0 (26.08.2024)
-------------------

* !55: Updated CI runner to use the latest base image. Adapted build script to upstream changes of GitLab 17.0.
* !56: Migrated setup procedure from using setup.py + setup.cfg to using pyproject.toml only.


0.18.0 (05.07.2024)
-------------------

* !47: Fixed missing handling of int64 input values for GDAL_Metadata.__getitem__
  and improved coverage of GDAL_Metadata.
* !48: Revised tests to use pytest plain assertions.
* !49: Improved documentation of expected order of array dimensions (closes #43).
* !50: Fixed #46 (Numpy 2.0 support: `can_cast` not supported for python dtypes).
* !51: Fixed GDAL-3.9-related RuntimeError within GeoArray.save by using context managers.
  Bumped minimal version of GDAL to 3.8 due to usage of context managers.
* !52: Use GDAL context managers where ever possible.
* Added official support for Python 3.12.
* !53: Removed Test_GeoArray.test_show_map_noepsg because newer versions of pyproj do not
  return None as EPSG code anymore (at least not with the given WKT).
* !54: Fixed DeprecationWarning (replaced deprecated pkgutil.find_loader with importlib.util.find_spec).


0.17.2 (23.11.2023)
-------------------

* !46: Fixed #44 and #45 (unexpected return values from GeoArray.read_pointData).


0.17.1 (03.11.2023)
-------------------

* !44: Updated CI to use Ubuntu-based runner. Revised environment_geoarray.yml.
* !45: Added parameter 'draw_gridlines' to GeoArray.show_map() to allow users to control it by their own.


0.17.0 (15.06.2023)
-------------------

* !38: Removed GeoArray.arg attribute as it is not needed and just consumes memory.
* !39: Revised the project to consistently use new-style type hints.
* !40: Added workaround for missing PROJ_DATA environment variable.
* !41: Revised GeoArray.show to be compatible with new versions of holoviews.
* !42: Dropped support for cartopy<0.20 and removed pyepsg requirement as cartopy>=0.20 uses pyproj instead.
* !43: Dropped support for Python 3.7 and added support for Python 3.11.


0.16.1 (16.02.2023)
-------------------

* Fixed an issue where the output gsd was not considered in GeoArray.get_mapPos()
  if no different projection is set (!37).


0.16.0 (15.02.2023)
-------------------

* Fixed issue #37 (GeoArray.get_mapPos(band2get=0) returns multilayer array) (!36).
* Added new parameter 'out_gsd' to GeoArray.get_mapPos() to set the output spatial resolution (!36).


0.15.11 (09.02.2023)
--------------------

* Fixed issue #36 (clip_to_poly fails for multiband raster) (!34).
* Updated copyright (!35).


0.15.10 (15.11.2022)
--------------------

* Renamed master branch to main.


0.15.9 (21.07.2022)
-------------------

* Added check to avoid computing footprints in case the input dataset contains only nodata values.
* Dropped Python 3.6 support due to end-of-life status.


0.15.8 (16.03.2022)
-------------------

* Added GeoArray.is_rotated attribute to detect pseudo-projections.


0.15.7 (13.01.2022)
-------------------

* Fixed an exception in case of int and float bandnames in the input of GeoArray() (!31).


0.15.6 (16.12.2021)
-------------------

* Migrated test calls from nosetests to pytest (!30).
* Replaced deprecated numpy data type.


0.15.5 (03.12.2021)
-------------------

* GeoArray.footprint_poly now ignores very small polygons in mask when computing footprint polygon
  (much faster in case the mask contains many of them).


0.15.4 (22.11.2021)
-------------------

* Replaced deprecated gdalnumeric import.


0.15.3 (11.11.2021)
-------------------

* Removed deprecated 'maxfeatCount' keyword.
* Updated minimal version of py_tools_ds to 0.19.0 (revises raster2polygon and fill_holes_within_poly).


0.15.2 (29.10.2021)
-------------------

* Added compatibility to the 'HDF:"/path/file.hdf":subdataset' syntax when opening HDF sub-datasets directly.
* Fixed ValueError in case NaN is used as nodata value for float data type.


0.15.1 (22.10.2021)
-------------------

* Slight improvements for GeoArray.show_map().
* Fixed a bug in GeoArray.get_mapPos() which leads to too small output
  in case mapBounds_prj is unequal to GeoArray.prj (!29).
* The mapBounds_prj parameter of GeoArray.get_mapPos is not optional and defaults to GeoArray.prj.


0.15.0 (27.09.2021)
-------------------

* Switch to Apache 2.0 license.


0.14.3 (07.09.2021)
-------------------

* CI now uses Mambaforge.
* Fixed missing nodata value after running GeoArray.save() with ENVI output format.


0.14.2 (09.08.2021)
-------------------

* Added optional 'basename' parameter.


0.14.1 (07.08.2021)
-------------------

* Revised GeoArray.save() which fixes two GDAL warnings when writing cloud optimized GeoTiff (COG) format:

  * *Warning 1*: This file used to have optimizations in its layout, but those have been, at least partly,
    invalidated by later changes
  * *Warning 2*: The IFD has been rewritten at the end of the file, which breaks COG layout.

* Fixed unsupported band-specific nodata values in case of ENVI output format.
* Added two tests that validate the metadata written by GeoArray.save() for ENVI and GTiff format.
* Track tif and bsq files with git-lfs.
* Revised test_geoarray_install CI job (now uses mamba and environment_geoarray.yml).


0.14.0 (2021-07-26)
-------------------

* Added support for GDAL virtual file systems (file paths starting with '/vsi').


0.13.4 (2021-07-13)
-------------------

* Updated minimal version of py_tools_ds which fixes a TypeError in GeoArray.save if nodata value has a numpy data type.
* Force Python data type in GeoArray.nodata setter.
* Fixed bandnames synchronization issue in GeoArray.get_subset().
* Fixed empty plot when plotting a boolean image in GeoArray.show().


0.13.3 (2021-07-12)
-------------------

* Fixed incorrect data type downcast in GeoArray.show() which caused binary images, e.g. for NDVI images.


0.13.2 (2021-07-09)
-------------------

* Fix for not updating the data type and array shape after the complete array was replaced.
* Added type hints for 'metadata' attribute and 'meta' alias.


0.13.1 (2021-07-09)
-------------------

* Added a 'title' keyword to the '.show_profile' methods. Fixed duplicate 'plt.show()'.


0.13.0 (2021-07-08)
-------------------

* Added new methods to show X/Y/Z profiles of the GeoArray instance
  (GeoArray.show_xprofile(), GeoArray.show_yprofile() and GeoArray.show_zprofile()) + tests and documentation.


0.12.5 (2021-07-08)
-------------------

* The nodata value is no more implicitly computed in the GeoArray.save() method.


0.12.4 (2021-07-02)
-------------------

* Fixed inconsistency in 'data ignore value' metadata key that may cause duplicates in ENVI headers.
* Removed requirements files because requirements are properly stored in setup.py.
* Updated package classifiers and added minimal Python version.


0.12.3 (2021-05-29)
-------------------

* Metadata attributes set to numpy arrays are now correctly handled in ENVI format.
* Replaced deprecated URL.
* GeoArray.meta attributes are now correctly written in case of linked (not in-memory) datasets.


0.12.2 (2021-05-28)
-------------------

* Fixed GeoArray.is_map_geo not containing a bool.
* Increased timeout of footprint computation to 15 seconds.


0.12.1 (2021-05-08)
-------------------

* Fixed a bug causing float nodata values to be rejected in case of integer array data types.


0.12.0 (2021-05-08)
-------------------

* The initialization of NoDataMask and BadDataMask is now much faster in case a boolean array is passed.
* Increased timeout for footprint computation to 5 seconds.
* Dropped Python 2.7 support due to end-of-life status.


0.11.1 (2021-05-07)
-------------------

* Added a validation that checks if the given nodata value is within the valid value range of the array data type.


0.11.0 (2021-04-22)
-------------------

* GeoArray.projection is now always set to a WKT1 string (GDAL conform),
  no matter if the input WKT has an EPSG code or not.
* Added compatibility of GeoArray.show_map() and GeoArray.show_footprint() with input WKTs that have no EPSG equivalent.


0.10.12 (2021-04-13)
--------------------

* GeoArray.__getitem__() now first reads a band subset instead of the whole array if only a single band is requested
  (fixes #31).
* Fixed remaining test outputs aufter running Test_Geoarray.test_save().


0.10.11 (2021-04-08)
--------------------

* Fixed another numpy data type DeprecationWarning.
* Added 'make docs' artifacts to .gitignore.
* Fixed undeleted output of Test_GeoArray.test_save().
* Added .gitkeep to tests/output/ folder.
* 'make lint' now directly prints the log outputs.
* Band names and nodata values are now correctly read in case of data formats other than ENVI.
* Improved saved metadata for all formats (mainly applies to band names and nodata values).
* Fixed nodata value not passed through when reading a data format other than ENVI and saving in ENVI format.


0.10.10 (2021-02-19)
--------------------

* Fixed issue that tested GeoArray is altered by test methods and
  thus not passed as a newly created instance to some tests.


0.10.9 (2021-02-19)
-------------------

* Revised tests.
* Added parameterized as test requirement.
* Replaced deprecated numpy data types with builtin types.
* Fixed dead link in the docs.
* Added test for GeoArray.show().
* Fixed holoviews DeprecationWarning within GeoArray.show().


0.10.8 (2021-01-28)
-------------------

* Fixed an issue in GeoArray.show() that caused an invisible plot for some input images.


0.10.7 (2021-01-27)
-------------------

* Fixed a numpy overflow error within GeoArray.show() due to float16 data type.


0.10.6 (2021-01-25)
-------------------

* Added URL checker CI job and fixed all dead URLs.
* Fixed wrong package name in environment_geoarray.yml.
* Moved folium and geojson to optional dependencies. Revised 'extras_require' parameter in setup.py.
* Removed .travis.yml.


0.10.5 (2020-12-08)
-------------------

* Fixed issue #30 (GeoArray.read_pointdata() returns values for coordinates geographically outside of the image.).
* Implemented tests for GeoArray.read_pointdata().


0.10.4 (2020-11-02)
-------------------

* Replaced deprecated osgeo imports.


0.10.3 (2020-10-28)
-------------------

* Fixed issue #29 (Exception: Cannot label gridlines on a _EPSGProjection plot.
  Only PlateCarree and Mercator plots are currently supported.)


0.10.2 (2020-10-27)
-------------------

* Removed cartopy pinning and added a warning about the missing grid labels in GeoArray.show() with cartopy<0.18.0.


0.10.2 (2020-10-27)
-------------------

* Added pyepsg to requirements as it is now an optional requirement of cartopy and it is used in geoarray.


0.10.1 (2020-10-27)
-------------------

* Updated the minimal version of cartopy.


0.10.0 (2020-10-19)
-------------------

* Added 'flag' parameter to GeoArray.calc_nodata_mask() + tests.
* Fixed type hints and some issues in test_geoarray.py.
* The geoarray package is now on conda-forge! Updated the installation instructions accordingly.
* Revised environment_geoarray.yml
* Replaced deprecated 'source activate' by 'conda activate'.


0.9.3 (2020-10-12)
------------------

* Use SPDX license identifier and set all files to GLP3+ to be consistent with license headers in the source files.
* Excluded tests from being installed via 'pip install'.


0.9.2 (2020-10-08)
------------------

* Bugfix for not setting nodata values transparent in GeoArray.show().
* Moved cartopy import from module level to class level.
* Filled HISTORY.rst.


0.9.1 (2020-10-06)
------------------

* Bumped version.


0.9.0 (2020-10-06)
------------------

* Fixed missing comma.
* Added cartopy setup to test_geoarray to make CI work.
* Revised GeoArray.show_map() and replaced basemap by cartopy. Dropped mpld3 requirement. Fixed issue #28.
* Added GeoArray._get_cmap_vmin_vmax() and moved code from .show(), .show_map() and .show_map_utm() there.

0.8.37 (2020-10-02)
-------------------

* Fixed broken pip installation of basemap within setup.py.


0.8.36 (2020-09-30)
-------------------

* Revised previous commit.
* Replaced requirement 'basemap' by ssh link in setup.py to fix exception during 'pip install'.


0.8.35 (2020-09-29)
-------------------

* Basemap is now no longer optional as it is easily installable via conda-forge. Holoviews is now officially optional.


0.8.34 (2020-09-28)
-------------------

* Removed dask frm dependencies as it was only an indirect dependency.


0.8.33 (2020-09-18)
-------------------

* Removed restriction that GeoArray.projection cannot be set if the associated file on disk has another projection.


0.8.32 (2020-08-22)
-------------------

* Updated deprecated HTTP links.
* Avoid to update conda base environment with the defaults channel.
* Added environment update before installing geoarray env.
* Fixed syntax in build_testsuite_image.sh. geoarray_ci.docker now inherits from ci_base_centos:0.1.
* Removed channel 'ioam' for holoviews.
* Updated CI setup files and .gitlab.ci.yml.


0.8.31 (2020-08-21)
-------------------

* Moved matplotlib imports to class method level to avoid static TLS import issues.
* Added Python 3.8 and 3.9 to setup.py classifiers.


0.8.30 (2020-08-21)
-------------------

* Fixed .gitlab-ci.yml
* Updated installation instructions.
* Updated minimal version of geoarray.
* Added tolerance in GeoArray.footprint_poly to avoid wrong return values due to float uncertainties.
* Updated minimal version of py_tools_ds.


0.8.29 (2020-08-17)
-------------------

* Adapted code to latest changes in py_tools_ds.
* Bugfix for not setting nodata values transparent in GeoArray.show().
* Fixed a deprecation warning related to matplotlib colormaps.
* Updated minimal version of py_tools_ds.


0.8.28 (2020-03-19)
-------------------

* The algorithm to compute the nodata mask is now much faster, especially for datasets with many spectral bands.


0.8.27 (2020-01-08)
-------------------

* The geopandas dependency is not needed anymore.
* Updated conda environment.
* Updated minimal version of py_tools_ds.


0.8.26 (2020-01-08)
-------------------

* Disabled Python update in test_geoarray_install.
* Added conda and Python update to test_geoarray_install.
* Removed pyresample from dependencies (not needed anymore).
* Revised dependencies and test_geoarray_install job.
* Fixed broken badge.
* Added downloads badge.


0.8.25 (2019-10-10)
-------------------

* Fixed mixed types of band names.


0.8.24 (2019-10-10)
-------------------

* Fixed band names not properly read (fixed issue #26).


0.8.23 (2019-10-04)
-------------------

* Fixed typing issue.


0.8.22 (2019-08-14)
-------------------

* Replaced deprecated PyPi upload commands by twine.


0.8.21 (2019-07-22)
-------------------

* Added license texts.


0.8.20 (2019-07-09)
-------------------

* Lists are now allowed in zslice parameter for GeoArray.get_subset().


0.8.19 (2019-05-22)
-------------------

* Bugfix.


0.8.18 (2019-05-14)
-------------------

* Bugfix.
* Added ignore_rotation to GeoArray.show().


0.8.17 (2019-05-10)
-------------------

* Fixed issue #24 (TypeError: function takes exactly 1 argument (0 given)).
* Fixed issue #25 (RuntimeError: b'major axis or radius = 0 or not given').


0.8.16 (2019-04-29)
-------------------

* Fixed gray value stretching issue in case of rotated ENVI images without inherent nodata value.


0.8.15 (2019-04-29)
-------------------

* Fix for issue #23 (GeoArray.show_map does not respect ENVI rotation in map info if image has less than
  1.000.000 pixels per band).


0.8.14 (2019-03-29)
-------------------

* Fixed linting.
* Nodata values are now properly written to ENVI header files.


0.8.13 (2019-03-29)
-------------------

* Updated requirements.
* Fixed issue #22 (GeoArray[slice, slice, np.integer] returns the full array instead of a single band).


0.8.12 (2019-03-29)
-------------------

* Merge branch 'bugfix/fix_np_integer_indexing' into 'master'


0.8.11 (2019-03-29)
-------------------

* Fixed issue #22 (GeoArray[slice, slice, np.integer] returns the full array instead of a single band).
* Fixed FutureWarning regarding the use of a non-tuple sequence for multidimensional indexing.


0.8.10 (2018-12-15)
-------------------

* Fixed corrupted makefile.
* Fixed AssertionError in case GeoArray is instanced with a file from disk without map information and projection
  is set afterwards.

0.8.9 (2018-12-13)
------------------

* Added 'is_map_geo' attribute to GeoArray.

0.8.8 (2018-12-05)
------------------

* Replaced 'importlib.util.find_spec' with 'pkgutil.find_loader' to ensure Python 2.7 compatibility.
* Added some type hints.


0.8.7 (2018-09-17)
------------------

* Bugfix for wrong shape of return value when GeoArray instance is indexed with an instance of np.integer.
* Improved colormap handling within GeoArray.show().


0.8.6 (2018-09-13)
------------------

* Refactored function name and updated docstring.
* Fixed behaviour of GeoArray.__getitem__() unequal to numpy behaviour (caused issue #18).
* Added tests.


0.8.5 (2018-09-11)
------------------

* GeoArray.show() now returns the matplotlib object in non-interactive mode.

0.8.4 (2018-09-11)
------------------

* Fixed deploy_pypi CI job.
* Fixed GeoArray.show_histogram() (issue #17).


0.8.3 (2018-09-11)
------------------

* Added parameter 'ax' to GeoArray.show().


0.8.2 (2018-08-31)
------------------

* Changed behaviour of calc_mask_nodata() recognizing pixels as nodata that contain the nodata value in any band.
* Now they need to contain it in ALL bands.


0.8.1 (2018-08-27)
------------------

* Fixed TypeError within metadata module.
* Try to fix ncurses issue.
* Force libgdal to use conda-forge.
* Docker image now inherits from gms_base_centos:0.2.
* CI setup now updates ci_env environment installed via docker_pyenvs instead of creating an independent environment.
* Fix test_geoarray_install.
* Fix test_geoarray_install.
* Fix test_geoarray_install.
* Fix.
* Fix.
* Fix for CI issue.
* CI Python environment is now separate from base env. Added defaults channels below conda-forge in environment.yml
* Updated README.
* Updated README.
* Updated cell output.
* Updated cell output.
* Updated cell output.
* Updated cell output.
* Removed interactive map from notebook.
* Cleaned up.
* Changed link.
* Revised example notebook.
* Added some readme files.
* Added some readme files.
* Added example notebook.

0.8.0 (2018-08-10)
------------------

* Added tests for test_get_subset_2D.
* Bugfixes. Added tests for get_subset.
* Fix for broken GeoArray.get_subset() in case GeoArray.is_inmem == True.
* Fixed linting.
* GeoArray.get_subset() now properly returns GeoArray instance subsets with all metadata and attributes inherited
  from the full GeoArray.
* Added .copy() t make sure metadata.band_meta is really copied.
* Fixed GeoArray.save() for other formats than ENVI.
* Fixed code style issue.
* Fixed metadata setter. Removed deprecated code.
* GDAL_Metadata instances are now subscriptable.
* Bugfix for not updating GeoArray.metadata.bands within GeoArray.get_subset().
* Fixed issue that bandnames are not written to ENVI header by GeoArray.save().
* Bugfixes.
* Enhanced setters, added test data, added tests.
* Band names and description are now correctly saved in ENVI format.
* First implementation of metadata class in GeoArray.
* Added a first prototype of a metadata class.
* Added GDAL cache flushing.
* Added GDAL cache flushing.
* GDAL metadata values are now forced to be strings.
* Updated docker runner build script.


0.7.16 (2018-05-07)
-------------------

* Fixed linting.
* Fixed issue #19 (GeoArray.tiles() fails in case of 2D array).


0.7.15 (2018-04-09)
-------------------

* Fix.


0.7.14 (2018-04-09)
-------------------

* Added version.py.
* Fixed unequal return value of __getitem__ depending on is_inmem.


0.7.13 (2018-03-15)
-------------------

* Fixed wrong copying of bandnames from GeoArray instance within GeoArray.__init__().


0.7.12 (2018-02-22)
-------------------

* Fixed issue #15 (ValueError: 'axis' entry is out of bounds).


0.7.11 (2018-01-17)
-------------------

* Fixed GeoArray.save()


0.7.10 (2018-01-17)
-------------------

* Fixed GeoArray.save()


0.7.9 (2017-12-11)
------------------

* Fixed GeoArray.get_subset().


0.7.8 (2017-11-30)
------------------

* Improved GeoArray.get_subset().


0.7.7 (2017-11-30)
------------------

* Bugfix for GeoArray.get_subset()


0.7.6 (2017-11-27)
------------------

* Bugfix for GeoArray.get_subset()


0.7.5 (2017-11-24)
------------------

* Fix.


0.7.4 (2017-11-22)
------------------

* Added tests for plotting functions.
* Revised GeoArray.get_subset(). Added bandnames deleter. Renamed some test functions.
* Added test___getitem__() and test_get_subset().

0.7.3 (2017-11-20)
------------------

* Removed duplicate.
* Revised docker setup workflow.
* Replaced pandas  by geopandas within CI installer test.

0.7.2 (2017-11-16)
------------------

* Fixed issue #12 (incorrect footprint polygon).
* Updated README.
* Updated README. Moved geopandas to conda dependencies.


0.7.1 (2017-11-07)
------------------

* Bugfix
* GeoArray.tiles now has a length (added __len__).


0.7.0 (2017-11-03)
------------------

* Fixed linting issue.
* Fixed bad handling of local projections in GeoArray.set_gdalDataset_meta().
* Updated docker container version tag.
* Updated minimum version of py_tools_ds.
* Added docstring to GeoArray.tiles() and corresponding tests.
* Added function GeoArray.tiles().
* Added requirements_pip.txt.


0.6.16 (2017-10-19)
-------------------

* Fixed mpld3 exception. Revised availability checks for optional libs.


0.6.15 (2017-10-12)
-------------------

* Updated minimal version of py_tools_ds.


0.6.14 (2017-10-12)
-------------------

* Speedup for GeoArray.footprint_poly and GeoArray.mask_nodata.
* Updated minimal version of py_tools_ds.
* Updated README.rst


0.6.13 (2017-10-11)
-------------------

* Excluded some funcs from coverage.
* Reverted previous commit.
* Excluded installation of numpy, scikit-image and matplotlib from test_geoarray_install CI job.
* Renamed CI job 'deploy_pages' tp 'pages'.
* Fixed missing lib within docker setup.
* Updated deploy_pages CI job to make pages work again.
* Updated deploy_pages CI job to make pages work again.
* test_geoarray_install now runs on latest Python 3.
* test_geoarray_install is now only executed for master branch.
* Removed installation of testing libs from CI job.


0.6.12 (2017-10-10)
-------------------

* Updated Anaconda version within docker builder.
* Changed upgrade of py_tools_ds within CI job.
* Updated docker builder.
* Added auto-update of py_tools_ds within CI job.


0.6.11 (2017-10-10)
-------------------

* Simplified optional dependency check.
* Updated minimal version of py_tools_ds.


0.6.10 (2017-10-10)
-------------------

* GeoArray.geotransform.setter: Improved input validation.


0.6.9 (2017-10-06)
------------------

* Added parameters 'pmax' and 'pmin' to GeoArray.show().


0.6.8 (2017-10-06)
------------------

* GeoArray.geotransform now always returns a list.
* GeoArray.set_gdalDataset_meta(): Bugfix for returning gt with positive ygsd in case of arbitrary coordinates.


0.6.7 (2017-10-06)
------------------

* GeoArray.clip_to_poly(): Fix for not updating self._footprint_poly.
* Added GeoArray.clip_to_footprint() and GeoArray.clip_to_poly(). Simplified GeoArray.get_mapPos().


0.6.6 (2017-09-20)
------------------

* Suppressed flake8 warning.
* Disabled matplotlib figure popups during unittests.
* Fix for computing wrong footprint poly if nodata value is NaN.


0.6.5 (2017-09-20)
------------------

* Fixed wring stretching of GeoArray.show() in case image contains np.nan.
* Fixed wrong nodata value detection in case nodata is np.nan.


0.6.4 (2017-09-17)
------------------

* Updated version info.


0.6.3 (2017-09-17)
------------------

* Suppressed code compatibility check.
* Added type hints.
* Added style libs to docker container setup. Updated .gitlab_ci.yml.
* Removed explicit typing to avoid circular dependency.
* PEP8 editing. Added linting.


0.6.2 (2017-09-17)
------------------

* Added dask to setup_requirements.


0.6.1 (2017-09-17)
------------------

* Updated installation instructions within README.rst.


0.6.0 (2017-09-12)
------------------

* Fix holoviews import error.
* Added test for geoarray installer. Removed fixed version of holoviews within docker container setup.
* Activated artifacts for failed pipelines.
* Revised test requirements.


0.5.14 (2017-09-11)
-------------------

* Fix pandas bug.


0.5.13 (2017-09-11)
-------------------

* Updated minimal py_tools_ds version.
* Cleaned up .gitlab_ci.yml
* Updated docker container setup and cleaned-up gitlab_ci.yml.
* Added LD_LIBARY_PATH to gitlab_ci.yml.
* Fixed gitlab_ci.yml. danschef 9/11/17, 7:30 PM
* Fixed gitlab_ci.yml.
* Updated docker container setup and adjusted gitlab_ci.yml
* Updated docker container version tag.
* Validated Python 2.7 support.


0.5.12 (2017-09-11)
-------------------

* Updated minimal version of py_tools_ds.
* Fixed some Windows-incompatible paths within test_geoarray. PEP8-editing for the tests.


0.5.11 (2017-09-01)
-------------------

* Updated README.rst.
* Updated pip package setups within docker container setup.
* minor changes
* Adding comments to the test script.
* Extending the test-script: testing the save-function and several plot-functions.
* Extending the test-script: testing the save-function and several plot-functions.
* Commiting a BadDataMask for the tested .tif-Image. Extending the test-functions test_NoDataValueOfTiff and
  test_MaskBaddataOffTiff (before: test_MaskBaddataIsNone).


0.5.10 (2017-08-30)
-------------------

* Fixed bug related to matplotlib backend (issue #8).
* Extent the files Makefile and .gitlab-ci.yml for a more detailed coverage report.


0.5.9 (2017-08-23)
------------------

* Bugfix
* Bugfixes and minor improvements.
* Improved error handling within GeoArray.from_path().


0.5.8 (2017-08-20)
------------------

* Adjusted code according to changes within py_tools_ds.


0.5.7 (2017-08-19)
------------------

* Specified minimal version for py_tools_ds.
* Updated docker setup (disabled caching).
* Updated makefile.
* Fixed double installation of coverage during docker container setup; added python-devel to docker setup to
  speed up coverage.
* Fixed wrong references in test_geoarray.py
* Added py_tools_ds to docker container setup to avoid circular dependencies.
* Updated build_testsuite_image.sh.
* Fixed osr import error.
* Fix setup.py; rebuilt docker container.
* Added new test requirements to docker container setup.

0.5.6 (2017-07-26)
------------------

* updated subsetting._clip_array_at_mapPos()


0.5.5 (2017-07-24)
------------------

* Added GeoArray.show_histogram().
* Tracebacks are now printed in case of exception during 'make docs'.


0.5.4 (2017-07-19)
------------------

* Clearer error message in case the optional library Basemap is missing.


0.5.2 (2017-07-19)
------------------

* Added dummy function.
* Updated setup.py and added scikit-image to setup requirements.
* Added basemap setup and to docker builder ant to setup requirements.


0.5.1 (2017-07-05)
------------------

* Revised badges.


0.5.0 (2017-07-05)
------------------

* Added auto-deploy to PyPI; revised badges.


0.4.7 (2017-07-03)
------------------

* Updated setup requirements.


0.4.6 (2017-07-03)
------------------

* Added py_tools_ds to external dependencies within setup.py.


0.4.5 (2017-07-03)
------------------

* First release on PyPI.


0.4.4 (2017-07-03)
------------------

* Updated README.rst.


0.4.3 (2017-07-03)
------------------

* Updated HISTORY.rst.
* Updated docker builder and setup requirements.
* Updated docker builder.
* Updated setup requirements to fix holoviews installation issue.
* Updated installation instructions within README.rst; Updated CONTRIBUTING.rst, installation.rst, HISTORY.rst
* Added holoviews setup to docker builder; updated setup.py.


0.4.0 (2017-06-28)
------------------

* Updated setup.py
* Added requirements.txt
* Revised CI setup.
* Updated README.rst
* Updated setup.py
* Updated README.rst
* Updated README.rst
* Updated README.rst
* Updated CI system builder.
* Updated metadata handling (not yet completely working).
* Updated build_testsuite_image.sh
* Passed metadata through to GeoArray subset that comes out of GeoArray.get_subset()
* Added first version of CI files (not yet working).
* Bugfix Issue #7: GeoArray.get_subset()
* Bugfix
* Updated README.
* Updated README.
* Added submodules to setup.py.


0.3.0 (2017-06-09)
------------------

* Updated deprecated import statements.
* Biggest changes: Corrected the relative path to an absolute path, added the beginning of the second test case and
  extended the test suite to execute the second test case, only when the first test case was successful.
* updated some docstrings
* The new test case for the basic functions of geoarray.
* Commiting the first part of the new test case
* Fixed insufficient input validation in GeoArray.
* Fixed a bug in GeoArray.show()
* Commiting the first part of the new test case


0.2.0 (2017-05-29)
------------------

* fixed FileNotFoundError within Test_GeoarrayAppliedOnTiffPath.setUpClass
* added a function to get a subset GeoArray
* Commiting the first part of the new test case
* Commiting the first part of the new test case
* Trail: Commiting changes through the new branch "Tests"
* Trail: Commiting changes through the new branch "Tests"
* updated README
* changed package name in accordance to PEP8
* updated README
* renamed README
* adjusted some imports, modified README
* added first compilation of GeoArray source codes
* First commit of boilerplate code and cut cookies...


0.1.0 (2017-03-31)
------------------

* Package creation.
