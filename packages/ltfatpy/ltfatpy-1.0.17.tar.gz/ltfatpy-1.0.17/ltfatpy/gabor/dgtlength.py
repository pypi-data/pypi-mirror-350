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


"""Module of dgtlength calculation

Ported from ltfat_2.1.0/gabor/dgtlength.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import six
import numpy as np

from ltfatpy.tools.lcm import lcm


def dgtlength(Ls, a, M):
    """DGT length from signal

    - Usage:

         | ``L = dgtlength(Ls, a, M)``

    - Input parameters:

    :param int Ls: Signal length
    :param int a: Length of time shift.
    :param int M: Number of channels.

    - Output parameters:

    :return: Corrected signal length
    :rtype: int

    ``dgtlength(Ls, a, M)`` returns the length of a Gabor system that is long
    enough to expand a signal of length **Ls**. Please see the help on
    :func:`~ltfatpy.gabor.dgt.dgt` for an explanation of the parameters **a**
    and **M**.

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`
    """
    if not(isinstance(M, six.integer_types)):
        raise TypeError('M must be an integer')
    if not(isinstance(a, six.integer_types)):
        raise TypeError('a must be an integer')
    if M <= 0:
        raise ValueError('M must be positive')
    if a <= 0:
        raise ValueError('a must be positive')
    if not(isinstance(Ls, (six.integer_types, float, complex))):
        raise TypeError('Ls must be a scalar')

    Lsmallest = lcm(a, M)
    L = np.ceil(Ls/Lsmallest)*Lsmallest
    return int(L)
