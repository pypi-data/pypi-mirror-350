========
geoarray
========


Fast Python interface for geodata - either on disk or in memory.

The geoarray package facilitates reading and writing of all GDAL compatible image file formats
and provides functions for geospatial processing.


* Free software: Apache 2.0
* Documentation: https://danschef.git-pages.gfz-potsdam.de/geoarray/doc/


Status
------

.. image:: https://git.gfz-potsdam.de/danschef/geoarray/badges/main/pipeline.svg
        :target: https://git.gfz-potsdam.de/danschef/geoarray/commits/main
.. image:: https://git.gfz-potsdam.de/danschef/geoarray/badges/main/coverage.svg
        :target: https://danschef.git-pages.gfz-potsdam.de/geoarray/coverage/
.. image:: https://img.shields.io/pypi/v/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray
.. image:: https://img.shields.io/conda/vn/conda-forge/geoarray.svg
        :target: https://anaconda.org/conda-forge/geoarray
.. image:: https://img.shields.io/pypi/l/geoarray.svg
        :target: https://git.gfz-potsdam.de/danschef/geoarray/blob/main/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/geoarray.svg
        :target: https://img.shields.io/pypi/pyversions/geoarray.svg
.. image:: https://img.shields.io/pypi/dm/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray


See also the latest coverage_ report and the pytest_ HTML report.


Features and usage
------------------

* There is an example notebook that shows how to use geoarray: here_.


Installation
------------

Using Anaconda or Miniconda (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using conda_ (latest version recommended), geoarray is installed as follows:


1. Create virtual environment for geoarray (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name geoarray python=3
    $ conda activate geoarray


2. Then install geoarray itself:

   .. code-block:: bash

    $ conda install -c conda-forge geoarray


This is the preferred method to install geoarray, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is also a `pip`_ installer for geoarray. However, please note that geoarray depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:

    * cartopy >=0.20
    * gdal >=3.8.0
    * geopandas
    * holoviews  # optional, in case you want to use interactive plotting
    * matplotlib
    * numpy
    * pandas
    * pyproj >2.2.0
    * scikit-image
    * shapely

Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install geoarray

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.


History / Changelog
-------------------

You can find the protocol of recent changes in the geoarray package
`here <https://git.gfz-potsdam.de/danschef/geoarray/-/blob/main/HISTORY.rst>`__.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: https://danschef.git-pages.gfz-potsdam.de/geoarray/coverage/
.. _pytest: https://danschef.git-pages.gfz-potsdam.de/geoarray/test_reports/report.html
.. _conda: https://docs.conda.io/
.. _here: https://git.gfz-potsdam.de/danschef/geoarray/-/blob/main/examples/notebooks/features_and_usage.ipynb
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
