#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
# Credits
# #######
#
# Copyright(c) 2015-2025
# ----------------------
#
# * `LabEx Archimède <http://labex-archimede.univ-amu.fr/>`_
# * `Laboratoire d'Informatique Fondamentale <http://www.lif.univ-mrs.fr/>`_
#   (now `Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>`_)
# * `Institut de Mathématiques de Marseille <http://www.i2m.univ-amu.fr/>`_
# * `Université d'Aix-Marseille <http://www.univ-amu.fr/>`_
#
# This software is a port from LTFAT 2.1.0 :
# Copyright (C) 2005-2025 Peter L. Soendergaard <peter@sonderport.dk>.
#
# Contributors
# ------------
#
# * Denis Arrivault <contact.dev_AT_lis-lab.fr>
# * Florent Jaillet <contact.dev_AT_lis-lab.fr>
#
# Description
# -----------
#
# ltfatpy is a partial Python port of the
# `Large Time/Frequency Analysis Toolbox <http://ltfat.sourceforge.net/>`_,
# a MATLAB®/Octave toolbox for working with time-frequency analysis and
# synthesis.
#
# Version
# -------
#
# * ltfatpy version = 1.0.17
# * LTFAT version = 2.1.0
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########

from __future__ import print_function, division
import sys
import os
import shutil
import distutils.spawn as ds
import distutils.dir_util as dd

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
from distutils.command.clean import clean
from distutils.command.sdist import sdist

# Test if Cython is installed
USE_CYTHON = True
try:
    from Cython.Distutils import build_ext
except ImportError:
    USE_CYTHON = False
    from distutils.command.build_ext import build_ext

USE_COPYRIGHT = True
try:
    from copyright import writeStamp, eraseStamp
except ImportError:
    USE_COPYRIGHT = False


###################
# Get ltfat version
####################
def get_version():
    v_text = open('VERSION').read().strip()
    v_text_formted = '{"' + v_text.replace('\n', '","').replace(':', '":"')
    v_text_formted += '"}'
    v_dict = eval(v_text_formted)
    return v_dict["ltfatpy"]


########################
# Set ltfat __version__
########################
def set_version(ltfat_dir, VERSION):
    filename = os.path.join(ltfat_dir, '__init__.py')
    buf = ""
    for line in open(filename, "rb"):
        if not line.decode("utf8").startswith("__version__ ="):
            buf += line.decode("utf8")
    f = open(filename, "wb")
    f.write(buf.encode("utf8"))
    f.write(('__version__ = "%s"\n' % VERSION).encode("utf8"))

def remove_generated_c_file():
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.c'):
                full_path = os.path.join(dirpath, filename)
                # Optionnel : ne supprime que ceux qui ont un .pyx à côté
                pyx_path = full_path[:-2] + '.pyx'
                if os.path.exists(pyx_path):
                    os.remove(full_path)
#################
# CMake function
#################
def run_cmake(root_dir):
    """ Runs CMake to determine configuration for this build """
    if ds.find_executable('cmake') is None:
        print("CMake is required to build ltfatpy")
        print("Please install cmake version >= 2.6 and re-run setup")
        sys.exit(-1)
    print("Configuring ltfatpy build with CMake.... ")
    print("Root dir : " + root_dir)
    new_dir = os.path.join(root_dir, 'build')
    dd.mkpath(new_dir)
    os.chdir(new_dir)
    try:
        ds.spawn(['cmake', '..'])
    except ds.DistutilsExecError:
        print("Error while running cmake")
        print("run 'setup.py build --help' for build options")
        print("You may also try editing the settings in CMakeLists.txt file " + 
              "and re-running setup")
        sys.exit(-1)


#################
# make function
#################
def run_make(root_dir):
    """ Runs make to build ltfatpy libraries """
    print("Building ltfatpy libraries.... ")
    build_dir = os.path.join(root_dir, 'build')
    os.chdir(build_dir)
    try:
        ds.spawn(['make'])
    except ds.DistutilsExecError:
        print("Error while running make")
        print("run 'setup.py build --help' for build options")
        print("You may also try editing the settings in CMakeLists.txt file " + 
              "and re-running setup")
        sys.exit(-1)


#######################
# make install function
#######################
def run_make_install(root_dir):
    """ Runs make install to install ltfatpy libraries """
    print("Installing ltfatpy libraries.... ")
    build_dir = os.path.join(root_dir, 'build')
    os.chdir(build_dir)
    try:
        ds.spawn(['make', 'install'])
        # +cmake_args.split())
    except ds.DistutilsExecError:
        print("Error while running make install")
        print("run 'setup.py build --help' for build options")
        print("You may also try editing the settings in CMakeLists.txt file " + 
              "and re-running setup")
        sys.exit(-1)


#################
# uninstall libs
#################
def run_uninstall(root_dir):
    """ Un-installs ltfatpy libraries """
    print("Uninstall ltfatpy libraries.... ")
    build_dir = os.path.join(root_dir, 'build')
    os.chdir(build_dir)
    try:
        ds.spawn(['make', 'uninstall'])
    except ds.DistutilsExecError:
        print("Error while running make uninstall")
        print("run 'setup.py build --help' for build options")
        print("You may also try editing the settings in CMakeLists.txt file " + 
              "and re-running setup")
        sys.exit(-1)


#########################
# Custom 'build_ext' command
#########################
# class m_build_ext(build_ext):
#    """  Custom build_ext command """
#    def run(self):
#        root_dir = os.path.dirname(os.path.abspath(__file__))
#        cur_dir = os.getcwd()
#        run_cmake(root_dir)
#        run_make(root_dir)
#        run_make_install(root_dir)
#        os.chdir(cur_dir)
#        build_ext.run(self)

class m_build_ext(build_ext):
    def run(self):
        if USE_CYTHON:
            remove_generated_c_file()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cur_dir = os.getcwd()
        run_cmake(root_dir)
        run_make(root_dir)
        run_make_install(root_dir)
        os.chdir(cur_dir)
        build_ext.run(self)
##########################
# File path read command
##########################
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    from io import open
    with open(os.path.join(*paths), 'r', encoding='utf-8') as f:
        return f.read()


#####################################
# Directory pyx files scan command
#####################################
def findpyxfiles(directory, files=[]):
    """scan a directory for pyx extension files."""
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            findpyxfiles(path, files)
    return files


#################
# Extension maker
#################
def makeExtension(extName, fileExt, lib_dir):
    """Generate an Extension object from its dotted name."""
    extPath = extName.replace(".", os.path.sep) + fileExt
    print("Found " + extName + " extension...")
    return Extension(
        extName,
        [extPath],
        language="c",
        extra_compile_args=['-O3'],
        libraries=["fftw3", "m", "blas", "lapack"],
        extra_objects=[os.path.join(lib_dir, "libltfat.a"),
                       os.path.join(lib_dir, "libltfatf.a")],
        )


######################
# Custom clean command
######################
class m_clean(clean):
    """ Remove build directories, and compiled file in the source tree"""

    def run(self):
        clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('doc' + os.path.sep + '_build'):
            shutil.rmtree('doc' + os.path.sep + '_build')
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if (filename.endswith('.so') or
                        filename.endswith('.pyd') or
                        filename.endswith('.dll') or
                        filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


##############################
# Custom sdist command
##############################
class m_sdist(sdist):
    """ Build source package

    WARNING : The stamping must be done on an default utf8 machine !
    """

    def run(self):
        if USE_COPYRIGHT:
            writeStamp()
            sdist.run(self)
            # eraseStamp()
        else:
            sdist.run(self)


####################
# Setup method
####################
def setup_package():
    """ Setup function"""
    # set version
    VERSION = get_version()

    lib_dir = os.path.join('ltfat_C_kernel', 'lib')
    ltfat_dir = 'ltfatpy'
    set_version(ltfat_dir, get_version())
    # get the list of extensions
    extNames = findpyxfiles(ltfat_dir)
    # authors=[{"name" : "Denis Arrivault" },
    #              {"name" : "Florent Jaillet" },
    #              {"name" : "Valentin Emiya" , "email" : "valentin.emiya@lis-lab.fr"}],
    # and build up the set of Extension objects
    if USE_CYTHON:
        fileExt = ".pyx"
        print("Cython Used")
    else:
        fileExt = ".c"
        print("witout Cython")

    extensions = [makeExtension(name, fileExt, lib_dir) for name in extNames]
    # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    setup(name="ltfatpy",
          version=VERSION,
          description='The Large Time-Frequency Toolbox (LTFAT) in Python',
          long_description=(read('README.rst') + '\n\n' + 
                            read('HISTORY.rst') + '\n\n' + 
                            read('AUTHORS.rst')),
          packages=find_packages(),
          package_data={'ltfatpy.signals': ['*.wav'],
                        'ltfatpy.comp': ['*.pxd'],
                        'ltfatpy.tests.datasets': ['*.mat']},
          url="https://gitlab.lis-lab.fr/dev/ltfatpy",
          license='GNU GPL V3',
          license_files='LICENSE.rst',
          author='Denis Arrivault and Florent Jaillet',
          author_email='valentin.emiya@lis-lab.fr',
          ext_modules=extensions,
          test_suite='nose.collector',
          tests_require=['nose', 'coverage'],
          cmdclass={'build_ext': m_build_ext,
                    'clean': m_clean, 'sdist': m_sdist},
          classifiers=['Development Status :: 5 - Production/Stable',
                       'Intended Audience :: Science/Research',
                       'Intended Audience :: End Users/Desktop',
                       'Intended Audience :: Developers',
                       'Natural Language :: English',
                       'Operating System :: MacOS :: MacOS X',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: C',
                       'Programming Language :: Python :: 3.4',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Programming Language :: Python :: 3.9',
                       'Programming Language :: Python :: 3.10',
                       'Topic :: Scientific/Engineering :: Mathematics',
                       'Topic :: Scientific/Engineering'
                       ],
          install_requires=['scipy>=0.18', 'numpy>=1.8', 'matplotlib>=1.4', 'six>=1.10'],
          )


if __name__ == "__main__":
    setup_package()
