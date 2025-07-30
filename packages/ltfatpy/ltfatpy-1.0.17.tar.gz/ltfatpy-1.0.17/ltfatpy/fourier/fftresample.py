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


""" Module of signal resampling using Fourier interpolation

Ported from ltfat_2.1.0/fourier/fftresample.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post
from ltfatpy.tools.postpad import postpad
from ltfatpy.fourier.middlepad import middlepad
from ltfatpy.fourier.fftreal import fftreal
from ltfatpy.fourier.ifftreal import ifftreal


def fftresample(f, L, dim=None):
    """Resample signal using Fourier interpolation

    - Usage:
        | ``h = fftresample(f, L)``
        | ``h = fftresample(f, L, dim)``

    - Input parameters:

    :param numpy.ndarray f: Input array
    :param int L: Length of the output resampled array
    :param int dim: Axis over which to do the resampling

    - Output parameters:

    :returns: Resampled array
    :rtype: numpy.ndarray

    ``fftresample(f, L)`` returns a Fourier interpolation of the signal **f**
    to length **L**. If the function is applied to a matrix, it will apply
    to each column.

    ``fftresample(f, L, dim)`` does the same along dimension **dim**.

    If the input signal is *not* a periodic signal (or close to), the
    :func:`dctresample` method gives much better results at the endpoints.

    .. seealso:: :func:`dctresample`,
        :func:`~ltfatpy.fourier.middlepad.middlepad`
    """

    f, L, Ls, W, dim, permutedsize, order = assert_sigreshape_pre(f, L, dim)

    # The 'axis=0' and 'dim=0' below have been added to avoid fft and middlepad
    # being smart about choosing the dimension.
    if np.isrealobj(f):
        L2 = int(np.floor(L/2))+1
        # Note: There is a bug in the call of postpad below in ltfat 2.1.0. for
        # Octave. This bug has been reported and confirmed here:
        # http://sourceforge.net/p/ltfat/bugs/117/
        # This Python port corrects the bug by correclty padding with zeros
        # instead of ones in the Octave version.
        h = ifftreal(postpad(fftreal(f, dim=0), L2, dim=0), L, dim=0)/Ls*L
    else:
        h = np.fft.ifft(middlepad(np.fft.fft(f, axis=0), L, dim=0),
                        axis=0)/Ls*L

    h = assert_sigreshape_post(h, dim, permutedsize, order)

    return h
