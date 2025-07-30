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


""" Module of fixed ratio of largest coefficients extraction

Ported from ltfat_2.1.0/sigproc/largestr.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

from ltfatpy.sigproc.largestn import largestn


def largestr(xi, p, thresh_type='hard'):
    """Keep fixed ratio of largest coefficients

    - Usage:

        | ``(xo, Nout) = largestr(xi, p)``
        | ``(xo, Nout) = largestr(xi, p, thresh_type)``

    - Input parameters:

    :param numpy.ndarray xi: Input array
    :param float p: Ratio of kept coefficients
    :param str thresh_type: Optional flag specifying the type of thresholding
        (see possible values below)

    - Output parameters:

    :returns: ``(xo, Nout)``
    :rtype: tuple

    :var numpy.ndarray xo: Array of the same shape as **xi** keeping
        the fraction **p** of the coefficients with the largest magnitude
    :var int Nout: Number of coefficients kept

    .. note::
        If the function is used on coefficients coming from a redundant
        transform or from a transform where the input signal was padded, the
        coefficient array will be larger than the original input signal.
        Therefore, the number of coefficients kept might be higher than
        expected.

    The parameter **thresh_type** can take the following values:
        ============ ======================================================
        ``'hard'``   Perform hard thresholding. This is the default.

        ``'wiener'`` Perform empirical Wiener shrinkage. This is in between
                     soft and hard thresholding.

        ``'soft'``   Perform soft thresholding.
        ============ ======================================================

    .. note::
        If soft- or Wiener thresholding is selected, one less
        coefficient will actually be returned. This is caused by that
        coefficient being set to zero.

    .. seealso::
        :func:`~ltfatpy.sigproc.largestn.largestn`

    - References:
        :cite:`ma98`
    """

    if not isinstance(p, float):
        raise TypeError('p must be a float.')

    N = int(round(xi.size * p))

    xo, Nout = largestn(xi, N, thresh_type)

    return (xo, Nout)
