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


"""Module that computes Diagonal of Gabor frame operator

Ported from ltfat_2.1.0/gabor/gabframediag.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.sigproc.fir2long import fir2long
from ltfatpy.gabor.dgtlength import dgtlength


def gabframediag(g, a, M, L):
    """Diagonal of Gabor frame operator

    - Usage:

        | ``d = gabframediag(g, a, M, L)``

    - Input parameters:

    :param numpy.ndarray g: Window function
    :param int a: Length of time shift
    :param int M: Number of channels
    :param int L: Length of transform to do

    - Output parameters:

    :returns: Diagonal stored as a column vector
    :rtype: numpy.ndarray

    ``gabframediag(g, a, M, L)`` computes the diagonal of the Gabor frame
    operator with respect to the window **g** and parameters **a** and **M**.
    The diagonal is stored a as column vector of length **L**.

    The diagonal of the frame operator can for instance be used as a
    preconditioner.

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`
    """
    # Verify a, M and get L
    Luser = dgtlength(L, a, M)
    if L != Luser:
        raise ValueError(("Incorrect transform length L={0:d} specified." +
                          " Next valid length  is L={0:d}. See the help" +
                          " of DGTLENGTH for the requirements.").format(L,
                         Luser))

    # Determine the window
    (g, info) = _call_gabwin(g, a, M, L)
    if L < info['gl']:
        raise ValueError('Window is too long.')

    # compute the diagonal
    glong2 = np.abs(fir2long(g, L))**2
    N = L//a

    # The diagonal is a-periodic, so compute a single period by summing up
    # glong2 in slices.
    d = np.tile(np.sum(glong2.reshape(N, a), axis=0), (N,)) * M
    return d


def _call_gabwin(g, a, M, L):
    """ Internal use only """

    from ltfatpy.gabor.gabwin import gabwin
    return gabwin(g, a, M, L)
