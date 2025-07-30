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


""" Module of original permuted shape restoration

Ported from ltfat_2.1.0/comp/assert_sigreshape_post.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np


def assert_sigreshape_post(f, dim, permutedshape, order):
    """Restore the original permuted shape

    - Input parameters:

    :param numpy.ndarray f: Reshaped signal as returned in **f** by
        :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre`
    :param int dim: Verified dim as returned in **dim** by
        :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre`
    :param tuple permutedshape: **permutedshape** value as returned by
        :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre`
    :param tuple order: **order** value as returned by
        :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre`

    - Output parameters:

    :returns: The signal reshaped to its original shape
    :rtype: numpy.ndarray

    .. warning::
        This function returns a view of **f** if possible. Any value changed
        in this view will also be changed in **f**.
    """

    f = f.reshape(permutedshape)

    if dim > 0:
        # Undo the permutation.
        f = f.transpose(np.argsort(order))

    return f
