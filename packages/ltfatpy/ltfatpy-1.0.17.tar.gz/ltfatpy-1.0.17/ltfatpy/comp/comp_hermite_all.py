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


""" Module of sampling of all Hermite function computation

Ported from ltfat_2.1.0/comp/comp_hermite_all.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np


def comp_hermite_all(n, x):
    """ Compute all Hermite functions up to an order

    - Usage:

        | ``y = comp_hermite_all(n, x)``

    This function evaluates the Hermite functions
    of degree 0 through n-1 at the vector x.
    The functions are normalized to have the :math:`L^2` norm
    on :math:`]-\\infty,\\infty[` equal to one. No effort is made to
    avoid unerflow during recursion.

    - Input parameters:

    :param int n: the number of Hermite functions
    :param numpy.ndarray x: the vector of arguments

    - Output parameters:

    :return numpy.ndarray y: the values of the first n Hermite functions at
                             the nodes x
    """
    if not isinstance(x, np.ndarray) or len(x.shape) > 1:
        raise TypeError("x should be a numpy array of dimension 1")
    rt = 1 / np.sqrt(np.sqrt(np.pi))

    # conducting the recursion.
    y = np.zeros((len(x), n))

    if n == 0:
        y = rt * np.exp(-0.5 * x**2)
    else:
        y[:, 0] = rt * np.exp(-0.5 * x**2)
        if n > 1:
            y[:, 1] = rt * np.sqrt(2) * x * np.exp(-0.5 * x**2)
            for k in range(2, n):
                y[:, k] = np.sqrt(2)*x*y[:, k-1] - np.sqrt(k-1)*y[:, k-2]
                y[:, k] = y[:, k] / np.sqrt(k)
    return y
