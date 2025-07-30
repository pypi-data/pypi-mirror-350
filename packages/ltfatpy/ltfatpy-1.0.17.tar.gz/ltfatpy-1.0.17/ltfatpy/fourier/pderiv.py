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


""" Module of derivative of smooth periodic function computation

Ported from ltfat_2.1.0/fourier/pderiv.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.fourier.fftindex import fftindex
from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def pderiv(f, dim=None, difforder=4):
    """ Derivative of smooth periodic function

    - Usage:
        | ``fd = pderiv(f)``
        | ``fd = pderiv(f, dim)``
        | ``fd = pderiv(f, dim, difforder)``

    - Input parameters:

    :param numpy.ndarray f: Input array
    :param int dim: Axis over which to compute the derivative
    :param difforder: Order of the centered finite difference scheme used.
        Possible values are: ``2``, ``4``, ``float('inf')``
    :type difforder: int or float

    - Output parameters:

    :returns: Derivative of **f**
    :rtype: numpy.ndarray

    ``pderiv(f)`` will compute the derivative of **f** using a using a 4th
    order centered finite difference scheme. **f** must have been obtained by
    a regular sampling. If **f** is a matrix, the derivative along the
    columns will be found.

    ``pderiv(f, dim)`` will do the same along dimension **dim**.

    ``pderiv(f, dim, difforder)`` uses a centered finite difference scheme of
    order difforder instead of the default.

    ``pderiv(f, dim, float('inf'))`` will compute the spectral derivative
    using a DFT.

    ``pderiv`` assumes that **f** is a regular sampling of a function on the
    torus ``[0, 1)``. The derivative of a function on a general torus
    ``[0, T)`` can be found by scaling the output by ``1/T``.
    """

    f, L, Ls, W, dim, permutedsize, order = assert_sigreshape_pre(f, dim=dim)

    if difforder == 2:
        fd = L * (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / 2
    elif difforder == 4:
        fd = L * (- np.roll(f, -2, 0) + 8*np.roll(f, -1, 0) -
                  8*np.roll(f, 1, 0) + np.roll(f, 2, 0)) / 12
    elif difforder == float('inf'):
        n = fftindex(L, 0)
        n = np.tile(n, (W, 1)).transpose()

        fd = 2*np.pi*np.fft.ifft(1j*n*np.fft.fft(f, axis=0), axis=0)

        if np.isrealobj(f):
            fd = np.real(fd)

    else:
        raise ValueError('The specified differentation order is not '
                         'implemented.')

    fd = assert_sigreshape_post(fd, dim, permutedsize, order)

    return fd
