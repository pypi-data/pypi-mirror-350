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


"""Module that extends fir windows with zeros

Ported from ltfat_2.1.0/sigproc/fir2long.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.fourier.middlepad import middlepad


def fir2long(gin, Llong):
    """Extend FIR window to LONG

    - Usage:

        | ``g= fir2long(g, Llong)``

    - Input parameters:

    :param numpy.ndarray g: input window
    :param int Llong: new length

    - Ouput parameters:

    :return: extended window
    :rtype: numpy.ndarray

    ``fir2long(g,Llong)`` will extend the FIR window **g** to a length
    **Llong** window by inserting zeros. Note that this is a slightly
    different behaviour than :py:meth:`~ltfatpy.fourier.middlepad`.

    ``fir2long`` can also be used to extend a FIR window to a longer FIR
    window, for instance in order to satisfy the usual requirement that the
    window length should be divisible by the number of channels.

    .. seealso::  :func:`~ltfatpy.sigproc.long2fir.long2fir`,
        :func:`~ltfatpy.fourier.middlepad.middlepad`
    """
    if not isinstance(gin, np.ndarray):
        raise TypeError("gin must be a numpy array")
#     if gin.ndim > 1:
#         raise ValueError("gin must be a vector (dim = 1)")
    Lfir = gin.shape[0]
    if Lfir > Llong:
        raise ValueError('Llong must be larger than length of window.')
    if Lfir % 2 == 0:
        # HPE middlepad works the same way as the FIR extension (e.g. just
        # inserting zeros) for even-length signals.
        gout = middlepad(gin, Llong, centering='hp')
    else:
        # WPE middlepad works the same way as the FIR extension (e.g. just
        # inserting zeros) for odd-length signals.
        gout = middlepad(gin, Llong)
    return gout
