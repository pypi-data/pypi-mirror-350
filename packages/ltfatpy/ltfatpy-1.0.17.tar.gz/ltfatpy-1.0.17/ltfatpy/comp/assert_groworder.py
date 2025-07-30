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


""" Module of order parameter growing

Ported from ltfat_2.1.0/comp/assert_groworder.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np


def assert_groworder(order):
    """Grow the order parameter

    - Input parameter:

    :param tuple order: Order indices obtained with
        :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre`

    - Ouput parameter:

    :return: Order indices
    :rtype: tuple

    ``assert_groworder`` is meant to be used in conjunction with
    :func:`~ltfatpy.comp.assert_sigreshape_pre.assert_sigreshape_pre` and
    :func:`~ltfatpy.comp.assert_sigreshape_post.assert_sigreshape_post`. It is
    used to modify the **order** parameter in between calls in order to expand
    the processed dimension by ``1``, i.e. for use in a routine that creates 2D
    output from 1D input, for instance in :func:`~ltfatpy.gabor.dgt.dgt` or
    :func:`filterbank`.
    """

    if len(order) > 1:
        # We only need to handle the non-trivial order, where dim>1
        p = order[0]
        # Shift orders higher that the working dimension by 1, to make room for
        # the new dimension, but leave lower dimensions untouched.
        ordernp = np.asarray(order)
        ordernp[ordernp > p] = ordernp[ordernp > p]+1
        return (p, p+1) + tuple(ordernp[1:])
    return order
