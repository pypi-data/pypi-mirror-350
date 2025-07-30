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


"""This module computes the least common multiple

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

from math import copysign
try:
    from math import gcd
except ImportError:
    # fractions.gcd() is deprecated since Python 3.5 and math.gcd() should be
    # used instead, but for backward compatibilty we use fractions.gcd() if
    # math.gcd() is not available
    from fractions import gcd


def lcm(X, Y):
    """Compute the least common multiple

    - Inputs:

    :param int X: The first of the two integers for which to compute the
                  least common multiple
    :param int Y: The second of the two integers for which to compute the
                  least common multiple

    - Outputs:

    :returns: Least common multiple of **X** and **Y**
    :rtype: int

    """

    if (not isinstance(X, int) or not isinstance(Y, int)):
        raise TypeError('X and Y must be int.')

    if Y == 0 or X == 0:
        return 0

    res = X * Y // gcd(X, Y)

    # Note: Some sign modification is needed to match the results in Octave
    # when we have negative values
    res = int(abs(res) * copysign(1, X) * copysign(1, Y))

    return res
