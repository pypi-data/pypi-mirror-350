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


""" Module of even function tests

Ported from ltfat_2.1.0/fourier/isevenfunction.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
import numpy.linalg as LA


def isevenfunction(f, tol=1e-10, centering='wp'):
    """ True if function is even

    - Usage:

        | ``t = isevenfunction(f)``
        | ``t = isevenfunction(f, tol)``

    - Input parameters:

    :param numpy.ndarray f: vector of data to test (one dimension)
    :param float tol: tolerance (1e-10 by default)
    :param str centering: Point even function type : whole or half point even.
        **centering** can be 'wp' or 'hp', 'wp' is the default.

    -Output parameter:

    :return: True if **f** is whole point even
    :rtype: bool

    `isevenfunction(f)` returns True if *f* is whole point even. Otherwise it
    returns False.

    ``isevenfunction(f, tol)`` the same, using the tolerance *tol* to measure
    how large the error between the two parts of the vector can be. Default
    is 1e-10.

    Setting **centering** to 'hp', does the same for half point even functions.

    .. seealso:: :func:`~ltfatpy.fourier.middlepad.middlepad`, :func:`peven`
    """
    if f.ndim > 1:
        raise ValueError("f should be a one dimensional vector")

    # Define initial values for flags
    # definput.flags.centering = {'wp','hp'};
    # definput.keyvals.tol     = 1e-10;

    L = f.shape[0]

    if centering == 'wp':
        # Determine middle point of sequence.
        if L % 2 == 0:
            middle = L // 2
        else:
            middle = (L+1) // 2

        # Relative norm of difference between the parts of the signal.
        d = (LA.norm(f[1:middle] - np.conj(np.flipud(f[L-middle+1:L]))) /
             LA.norm(f))
    elif centering == 'hp':
        middle = int(np.floor(L/2))
        d = (LA.norm(f[0:middle] - np.conj(np.flipud(f[L-middle:L]))) /
             LA.norm(f))
    else:
        raise ValueError("centering parameter should be set to 'wp'" +
                         "(default) or 'hp'")

    # Return true if d less than tolerance.
    return (d <= tol)
