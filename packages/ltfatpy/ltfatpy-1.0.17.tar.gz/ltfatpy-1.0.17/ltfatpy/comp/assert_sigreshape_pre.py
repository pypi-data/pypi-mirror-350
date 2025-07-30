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


""" Module of dimension input proprocessing and handling

Ported from ltfat_2.1.0/comp/assert_sigreshape_pre.m

.. moduleauthor:: Denis Arrivault
                  Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np
import sys
import six


def assert_sigreshape_pre(f, L=None, dim=None):
    """Preprocess and handle dimension input

    - Input parameters:

    :param numpy.ndarray f: Signal
    :param int L: L parameter
    :param int dim: dim parameter

    - Output parameters:

    :returns: ``(f, L, Ls, W, dim, permutedshape, order)``
    :rtype: tuple

    :var numpy.ndarray f: Input signal as matrix.
    :var int L: Verified L.
    :var int Ls: Length of signal along dimension to be processed.
    :var W: Number of transforms to do.
    :vartype W: int
    :var int dim: Verified dim.
    :var tuple permutedshape: Pass to
        :func:`~ltfatpy.comp.assert_sigreshape_post.assert_sigreshape_post`
    :var tuple order: Pass to
        :func:`~ltfatpy.comp.assert_sigreshape_post.assert_sigreshape_post`

    .. warning::
        This function returns a view of **f**. Any value changed in this
        view will also be changed in **f**.
    """

# ---- Format f as a numpy array
    if type(f).__module__ != np.__name__:
        f = np.asarray(f)

# ----Check that f type is numeric
    if (not np.issubdtype(f.dtype, np.floating) and
       not np.issubdtype(f.dtype, np.complexfloating) and
       not np.issubdtype(f.dtype, np.integer)):
        raise TypeError("f data type should be numeric.")
    D = f.ndim
    order = (1,)
    if dim is None:
        dim = 0
        if (sum(item > 1 for item in f.shape) == 1):
            # ---- We have a vector, find the dimension where it lives.
            dim = [i for i, v in enumerate(f.shape) if v > 1][0]
    else:
        if (not isinstance(dim, six.integer_types) and
           not isinstance(dim, np.int_)):
            raise TypeError("dim should be an integer.")
        if dim < 0 or dim > D:
            raise TypeError("dim must be in the range from 0 to "
                            "{0:d}.".format(D-1))

    if L is not None:
        if not isinstance(L, six.integer_types):
            raise TypeError("L should be an integer.")

    if dim > 0:
        # NOTE: the use of list below is needed for Python3 compatibility
        order = tuple([dim]+list(range(0, dim))+list(range(dim+1, D)))
        # ---- Put the desired dimension first.
        f = np.transpose(f, order)

    Ls = f.shape[0]
    # ---- If L is None it is set to be the length of the transform.
    if L is None:
        L = Ls

    # ---- Remember the exact shape for later and modify it for the new length
    permutedshape = f.shape
    permutedshape = (L,) + permutedshape[1:]

    # ---- Reshape f to a matrix.
    if f.size != 0:
        f = np.reshape(f, (f.shape[0], f.size // f.shape[0]))

    W = f.shape[1]

    return (f, L, Ls, W, dim, permutedshape, order)
