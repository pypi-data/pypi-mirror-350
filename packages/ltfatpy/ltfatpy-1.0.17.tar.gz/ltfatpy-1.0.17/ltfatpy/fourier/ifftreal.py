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


"""Module of inverse FFT for real valued data computation

Ported from ltfat_2.1.0/fourier/ifftreal.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np


def ifftreal(c, N, dim=0):
    """Inverse FFT for real valued signals

    - Usage:

        | ``f = ifftreal(c, N)``
        | ``f = ifftreal(c, N, dim)``

    - Input parameters:

    :param numpy.ndarray c: Discrete Fourier coefficients of a real array for
        positive frequencies
    :param int N: IFFT length
    :param int dim: Axis over which to compute the IFFT. By default the first
        axis is used.

    - Output parameters:

    :returns: Reconstructed signal
    :rtype: numpy.ndarray

    ``ifftreal(c, N)`` computes an inverse FFT of the positive frequency
    Fourier coefficients **c**. The length **N** must always be specified,
    because the correct transform length cannot be determined from the
    size of **c**.

    ``ifftreal(c, N, dim)`` does the same along dimension **dim**.

    .. note::

        This Python port doesn't use the C core of LTFAT to implement the
        inverse FFT for real arrays as in the Octave version.

        Instead it direclty uses the implementation available in numpy.

        This can lead to sightly different results when comparing the results
        of the Octave and Python versions of ifftreal.

    .. seealso::  :func:`~ltfatpy.fourier.fftreal.fftreal`

    """

    return np.fft.irfft(c, N, dim)
