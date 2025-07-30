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


"""Module of normalized discrete Fourier transform

Ported from ltfat_2.1.0/fourier/dft.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def dft(f, N=None, dim=0):
    """Normalized Discrete Fourier Transform

    - Usage:

        | ``c = dft(f)``
        | ``c = dft(f, N, dim)``

    - Input parameters:

    :param numpy.ndarray f: Input array
    :param int N: DFT length
    :param int dim: Axis over which to compute the DFT. By default the first
        axis is used.

    - Output parameters:

    :returns: Normalized discrete Fourier coefficients of **f**
    :rtype: numpy.ndarray

    :func:`~ltfatpy.fourier.dft.dft` computes a normalized or unitary discrete
    Fourier transform. The unitary discrete Fourier transform is computed by

    ..                       L-1
        c(k+1) = 1/sqrt(L) * sum f(l+1)*exp(-2*pi*i*k*l/L)
                             l=0

    .. math::

        c\\left(k+1\\right)=\\frac{1}{\\sqrt{L}}
        \\sum_{l=0}^{L-1}f\\left(l+1\\right)e^{-2\\pi ikl/L}


    for :math:`k=0,\ldots,L-1`.

    The output of :func:`~ltfatpy.fourier.dft.dft` is a scaled version of the
    output from :func:`numpy.fft.fft`. The function takes the same first three
    arguments as :func:`numpy.fft.fft`. See the help on :func:`numpy.fft.fft`
    for a thorough description.

    .. seealso:: :func:`~ltfatpy.fourier.idft.idft`

    """

    f, N, Ls, W, dim, permutedsize, order = assert_sigreshape_pre(f, N, dim)

    # Force fft along dimension 0, since we have permuted the dimensions
    # manually
    c = np.fft.fft(f, N, 0) / np.sqrt(N)

    c = assert_sigreshape_post(c, dim, permutedsize, order)

    return c
