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


""" Module of sampling of continuous Hermite function computation

Ported from ltfat_2.1.0/comp/comp_hermite.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
import math


def comp_hermite(n, x):
    """ Compute sampling of continuous Hermite function.

    - Usage:

        | ``y = comp_hermite(n, x)``

    `comp_hermite(n, x)` evaluates the n-th Hermite function at the vector
    **x**. The function is normalized to have the :math:`L^2` norm
    on :math:`]-\\infty,\\infty[` equal to one.

    A minimal effort is made to avoid underflow in recursion.
    If used to evaluate the Hermite quadratures, it works for n <= 2400
    """
    rt = 1 / math.sqrt(math.sqrt(math.pi))

    if n == 0:
        y = rt * np.exp(-0.5 * x**2)
    if n == 1:
        y = rt * math.sqrt(2) * x * np.exp(-0.5 * x**2)

    # if n > 2, conducting the recursion.
    if n >= 2:
        ef = np.exp(-0.5 * (x**2) / (n+1))
        tmp1 = rt * ef
        tmp2 = rt * math.sqrt(2) * x * (ef**2)
        for k in range(2, n+1):
            y = math.sqrt(2)*x*tmp2 - math.sqrt(k-1)*tmp1*ef
            y = ef * y / math.sqrt(k)
            tmp1 = tmp2
            tmp2 = y
    return y
