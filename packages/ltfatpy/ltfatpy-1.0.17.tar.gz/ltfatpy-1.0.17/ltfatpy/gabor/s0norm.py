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


"""Module of S0 norm calculation

Ported from ltfat_2.1.0/gabor/s0norm.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
from numpy import linalg as LA

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def s0norm(f, rel=False, dim=None):
    """S0-norm of signal

    - Usage:

        | ``y = s0norm(f)``

    - Input parameters:

    :param numpy.ndarray f: is the signal
    :param bool rel: True if returning result should be relative to the
                        :math:`l^2` norm (the energy) of the signal.
                        False by default
    :param int dim: dimension along which norm is applied (first
                    non-singleton dimension as default)

    - Output parameters:

    :return: s0-norm
    :rtype: float

    ``s0norm(f)`` computes the :math:`S_0`-norm of a vector.

    If the input is a matrix or ND-array, the :math:`S_0`-norm is computed
    along the first (non-singleton) dimension, and a vector of values is
    returned.

    .. warning:: The :math:`S_0`-norm is computed by computing a full
        short-time Fourier transform of a signal, which can be quite
        time-consuming. Use this function with care for long signals.
    """
    #  ------ Computation --------------------------
    (f, L, _unused, W, dim, permutedsize, order) = assert_sigreshape_pre(
                                                    f, dim=dim)
    permutedsize_list = [1] + list(permutedsize[1:])
    permutedsize = tuple(permutedsize_list)
    if len(permutedsize_list) == 1:
        permutedsize_list.append(1)
    y = np.zeros(tuple(permutedsize_list), dtype=f.dtype)
    g = __call_pgauss(L)

    for ii in range(W):
        # Compute the STFT by the simple algorithm and sum each column of the
        # STFT as they are computed, to avoid L^2 memory usage.
        for jj in range(L):
            y[0, ii] = y[0, ii] + np.sum(np.abs(np.fft.fft(f[:, ii] *
                                         np.roll(g, jj, axis=0))))

        if rel:
            y[0, ii] = y[0, ii] / LA.norm(f[:, ii])

    y /= L
    y = assert_sigreshape_post(y, dim, permutedsize, order)
    return y


def __call_pgauss(L):
    from ltfatpy.fourier.pgauss import pgauss
    return pgauss(L)[0]
