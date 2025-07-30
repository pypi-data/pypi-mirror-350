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


""" Module of comp_sigreshape_pre calculation

Ported from ltfat_2.1.0/comp/comp_sigreshape_pre.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np


def comp_sigreshape_pre(f, do_ndim):
    """Set good dimensionality

    .. warning::
        This function returns **f** or a view of **f**. Any value changed in
        the returned variable will also be changed in **f**.
    """
    if not isinstance(f, np.ndarray):
        raise ValueError("f should be a numpy array.")
    elif f.size == 0 or (not np.issubdtype(f.dtype, np.floating) and
                         not np.issubdtype(f.dtype, np.complexfloating) and
                         not np.issubdtype(f.dtype, np.integer)):
        raise ValueError('The input must be non-empty numeric.')

    wasrow = False

    # Rember the shape if f is multidimensional.
    remembershape = f.shape
    fd = len(remembershape)

    # Multi-dimensional mode, apply to first dimension.
    if fd > 2:
        if do_ndim > 0 and fd > do_ndim:
            raise ValueError('Cannot process multidimensional arrays.')

        fl = f.shape[0]
        W = np.prod(remembershape)//fl

        # Reshape to matrix if multidimensional.
        f = f.reshape((fl, W))
    else:
        if f.shape[0] == 1:
            wasrow = True
            # Make f a column vector.
            f = f.squeeze()
        fl = f.shape[0]
        if f.ndim > 1:
            W = f.shape[1]
        else:
            W = 1

    return (f, fl, W, wasrow, remembershape)
