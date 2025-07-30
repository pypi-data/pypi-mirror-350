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


"""This module contains interface functions for the LTFAT computed
versions of dct calculations.

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division
import cython
import numpy as np

from ltfat cimport ltfatInt, dct_kind, dct_cd, dct_d
from ltfatpy.comp.ltfat cimport DCTI, DCTII, DCTIII, DCTIV


# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cdef comp_dct_cd(const double complex[:] f, const ltfatInt L,
                 const ltfatInt W, const dct_kind kind, double complex[:] out):
    """ Internal function, do not use it """
    dct_cd(& f[0], L, W, & out[0], kind)

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cdef comp_dct_d(const double[:] f, const ltfatInt L,
                const ltfatInt W, const dct_kind kind, double[:] out):
    """ Internal function, do not use it """
    dct_d(&f[0], L, W, & out[0], kind)

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef comp_dct(f, type):
    """Function that computes dct

    This is a computational subroutine, do not call it directly, use
    :func:`~ltfatpy.fourier.dct.dcti`, :func:`~ltfatpy.fourier.dct.dctii`,
    :func:`~ltfatpy.fourier.dct.dctiii` or func:`~ltfatpy.fourier.dct.dctiv`
    instead.
    """
    cdef ltfatInt L, W
    if (f.dtype.type != np.float64) and (f.dtype.type != np.complex128):
        raise TypeError("f data should be numpy.float64 or complex128")
    if type not in {1, 2, 3, 4}:
        raise TypeError("type should be 1, 2, 3 or 4")

    dct_type = {1: DCTI, 2: DCTII, 3: DCTIII, 4: DCTIV}

    if f.ndim > 1:
        if f.ndim > 2:
            f = np.squeeze(f, axis=range(2, f.ndim-1))
        L = f.shape[0]
        W = f.shape[1]
        f_combined = f.reshape(L * W, order='F')
    else:
        L = f.shape[0]
        W = 1
        f_combined = f

    if f.dtype.type == np.float64:
        res = np.ndarray((L * W), dtype=np.float64)
        comp_dct_d(f_combined, L, W, dct_type[type], res)
    else:
        res = np.ndarray((L * W), dtype=np.complex128)
        comp_dct_cd(f_combined, L, W, dct_type[type], res)
    if W > 1:
        res = np.reshape(res, (L, W), order='F')
    return res
