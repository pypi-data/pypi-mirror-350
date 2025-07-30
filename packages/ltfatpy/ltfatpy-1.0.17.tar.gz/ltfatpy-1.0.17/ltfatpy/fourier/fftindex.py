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


""" Module of frequency index of FFT modulations computation

Ported from ltfat_2.1.0/fourier/fftindex.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np


def fftindex(N, nyquistzero=False):
    """Frequency index of FFT modulations

    - Usage:

        | ``n = fftindex(N)``

    - Input parameters:

    :param int N: FFT length
    :param bool nyquistzero: If ``True``, sets the Nyquist frequency to zero

    - Output parameters:

    :returns: Indexes of the frequencies of the standard FFT
    :rtype: numpy.ndarray

    ``fftindex(N)`` returns the index of the frequencies of the standard FFT
    of length **N** as they are ordered in the output from the
    :func:`numpy.fft.fft` routine. The numbers returned are in the range
    ``-ceil(N/2)+1:floor(N/2)``.

    ``fftindex(N, True)`` does as above, but sets the Nyquist frequency to
    zero.

    .. seealso:: :func:`dft`
    """

    if not nyquistzero:
        if N % 2 == 0:
            n = np.r_[0:N//2+1, -N//2+1:0]
        else:
            n = np.r_[0:(N+1)//2, -(N-1)//2:0]
    else:
        if N % 2 == 0:
            n = np.r_[0:N//2, 0, -N//2+1:0]
        else:
            n = np.r_[0:(N+1)//2, -(N-1)//2:0]

    return n
