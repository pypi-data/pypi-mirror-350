Installation
############

.. toctree::


Prerequisites
=============

Before installing **ltfatpy** you must check that the following software are installed on your system.

For `Debian <https://www.debian.org/>`_ based Linux systems (including `Ubuntu <https://www.ubuntu.com/>`_) and `Conda <https://conda.io>`_ users on Linux and macOS, simple solutions are provided in the section `Installing ltfatpy`_ to easily install the recquired dependencies.

Windows users should be able to use `Ubuntu on Windows <https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6>`_ via the `Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl>`_ to be able to run **ltfatpy** on Windows.

CMake
-----
A version of `cmake <https://cmake.org/>`_ >= 2.6 is required to install **ltfatpy**.
To install **CMake** follow the instructions given `here <https://cmake.org/install/>`__.

Python
------

* Make sure you have **python** >= 2.7 installed. If not follow the instructions from `here <https://wiki.python.org/moin/BeginnersGuide/Download>`__.
* According to your python version, make sure you have **pip** installed. If not follow the instructions from `here <https://pip.pypa.io/en/stable/installing/>`__.

For developpers only:

* If you need to recompile the whole ltfatpy C kernel interface you have to install **cython** >= 0.21.
* It can be installed by following the instructions given `here <http://docs.cython.org/src/quickstart/install.html>`__.

Scientific Python libraries
---------------------------

* You need to have **libfftw3**, development version, installed. 
    * For Debian based Linux systems use::

        apt install libfftw3-dev

    * For macOS based systems, you may use::

        sudo port install fftw-3 fftw-3-single

    * For other systems, please read the documentation of `fftw <http://www.fftw.org/>`_.

* You need to have the `LAPACK <http://www.netlib.org/lapack/>`_ library.

    * For Debian based Linux systems use::

        apt install liblapack-dev

* **ltfatpy** is using **numpy** >= 1.9, **scipy** >= 0.15 and **matplotlib** >= 1.4. For installing those packages read the instructions `here <http://www.scipy.org/install.html>`__.

Downloading **ltfatpy**
=======================

* The last stable release of **ltfatpy** is available on `PyPI <https://pypi.org/project/ltfatpy/>`_.
* You can clone the Git repository of **ltfatpy** from `here <https://gitlab.lis-lab.fr/dev/ltfatpy>`__.
* Conda packages of **ltfatpy** are available `here <https://anaconda.org/ltfatpy/>`__.

Installing **ltfatpy**
======================

From sources
------------

From ltfatpy-x.x.x/ directory use::

    pip install .

From PyPI
---------

Just use::

    pip install ltfatpy

For Debian based Linux systems
------------------------------

A precompiled **python3-ltfatpy** package is available for Debian Sid and Ubuntu 17.10 and later.
It can be installed with::

    apt install python3-ltfatpy

Alternatively, to compile the package, the following dependencies are required::

    apt install --no-install-recommends libdpkg-perl cmake gcc g++ make libfftw3-dev liblapack-dev cython3 python3 python3-dev python3-setuptools python3-pip python3-wheel python3-tk python3-matplotlib python3-scipy

The package can then be installed using pip::

    pip3 install --no-deps ltfatpy

For Conda users
---------------

A prebuilt Conda package of **ltfatpy** might already be available for your plateform. You can check `here <https://anaconda.org/ltfatpy/>`__.
If it is the case, simply install this Conda package with::

    conda install -c anaconda -c conda-forge -c ltfatpy ltfatpy

If no prebuilt Conda package is available, the following instructions can be used to install **ltfatpy** in Anaconda using pip.

When installing **ltfatpy** in Anaconda, it is important to note that **ltfatpy** is not compatible with the `MKL-powered binary versions <https://docs.anaconda.com/mkl-optimizations/>`_  of NumPy and SciPy.

Therefore, before installing **ltfatpy**, it is necessary to force the installation of the non-MKL version of the NumPy and SciPy Conda packages with::

    conda install nomkl numpy scipy

To be able to compile **ltfatpy** you need the gcc compiler (or an equivalent on macOS) installed on your computer.

For Debian based Linux systems that mean that the following packages must be installed::

    apt install --no-install-recommends gcc g++

For macOS that means that you need to install the **Xcode Command Line Tools**.

In Anaconda, the **ltfatpy** dependencies can directly be installed as Conda packages.
Some needed dependencies are not provided in the main anaconda channel, but they are provided in the conda-forge channel.

These dependencies can be installed with the following commands::

    conda install cmake make fftw cython six nomkl numpy scipy matplotlib
    conda install -c conda-forge lapack openblas

The **ltfatpy** package can then be installed using pip::

    pip install ltfatpy


Building documentation with Sphinx
==================================

Make sure you have Sphinx installed as described `here <http://sphinx-doc.org/tutorial.html#install-sphinx>`__.

Before building documentation you have to install **sphinxcontrib-bibtex**::

    pip install sphinxcontrib-bibtex

Then you have to use the setup.py build_sphinx command::

    python setup.py build_sphinx

If errors occur, make sure you installed ltfatpy before building the sphinx documentation.
