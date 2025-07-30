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


""" Module of Root Mean Square calculation

Ported from ltfat_2.1.0/sigproc/rms.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
from numpy import linalg as LA

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def rms(f, ac=False, dim=None):
    """RMS value of signal

    - Usage:

        | ``y = rms(f)``

    - Input parameters:

    :param numpy.ndarray f: Input signal
    :param bool ac: ``True`` if calculation should only consider the AC
        component of the signal (i.e. the mean is removed). ``False`` by
        default.
    :param int dim: Dimension along which norm is applied (first non-singleton
        dimension as default)

    - Output parameters:

    :returns: RMS value
    :rtype: float

    ``rms(f)`` computes the RMS (Root Mean Square) value of a finite sampled
    signal sampled at a uniform sampling rate. This is a vector norm
    equal to the :math:`l^2` averaged by the length of the signal.

    If the input is a matrix or ND-array, the RMS is computed along the
    first (non-singleton) dimension, and a vector of values is returned.

    The RMS value of a signal ``f`` of length ``N`` is computed by

    ..                       N
       rms(f) = 1/sqrt(N) ( sum |f(n)|^2 )^(1/2)
                            n=1

    .. math::
        rms(f) = \\frac{1}{\sqrt N} \left( \sum_{n=1}^N |f(n)|^2
        \\right)^{\\frac{1}{2}}

    """
    # It is better to use 'norm' instead of explicitly summing the squares, as
    # norm (hopefully) attempts to avoid numerical overflow.

    (f, L, _unused, W, dim, permutedsize, order) = \
        assert_sigreshape_pre(f, dim=dim)

    permutedshape = (1,) + permutedsize[1:]
    y = np.zeros(permutedshape)
    if W == 1:
        if ac:
            y[0] = LA.norm(f[:, 0] - np.mean(f[:, 0])) / np.sqrt(L)
        else:
            y[0] = LA.norm(f[:, 0]) / np.sqrt(L)
    else:
        if ac:
            for ii in range(W):
                y[0, ii] = LA.norm(f[:, ii] - np.mean(f[:, ii])) / np.sqrt(L)
        else:
            for ii in range(W):
                y[0, ii] = LA.norm(f[:, ii]) / np.sqrt(L)

    y = assert_sigreshape_post(y, dim, permutedshape, order)
    return y
