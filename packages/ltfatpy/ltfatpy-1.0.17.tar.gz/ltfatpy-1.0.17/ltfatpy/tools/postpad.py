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


"""This module pads or truncates arrays

Ported from ltfat_2.1.0/mex/postpad.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def postpad(x, L, C=0., dim=None):
    """Pads or truncates an array to a specified length

    - Usage:

        | ``y = postpad(x, L)``
        | ``y = postpad(x, L, C)``
        | ``y = postpad(x, L, C, dim)``

    - Input parameters:

    :param numpy.ndarray x: Input array
    :param int L: Length of the output array
    :param float C: Value of the padded entries
    :param int dim: Axis over which to pad or truncate **x**

    - Ouput parameters:

    :returns: Padded or truncated array
    :rtype: numpy.ndarray

    ``postpad(x, L)`` will add zeros to the end of the vector **x**, until
    the result has length **L**. If **L** is less than the length of the
    signal, it will be truncated. ``postpad`` works along the first
    non-singleton dimension.

    ``postpad(x, L, C)`` will add entries with a value of **C** instead of
    zeros.

    ``postpad(x, L, C, dim)`` works along dimension **dim** instead of the
    first non-singleton.

    .. seealso::
        :func:`~ltfatpy.fourier.middlepad.middlepad`
    """

    if dim is None:
        # by default, dim is the first non-singleton dimension
        dim = int(np.nonzero(np.array(x.shape) > 1)[0][0])

    x, L, Ls, W, dim, permutedsize, order = assert_sigreshape_pre(x, L, dim)

    if Ls < L:
        tmp = np.empty((L-Ls, W), dtype=x.dtype)
        tmp[:] = C
        y = np.concatenate((x, tmp), axis=0)
    else:
        y = x[:L, :].copy()

    y = assert_sigreshape_post(y, dim, permutedsize, order)

    return y
