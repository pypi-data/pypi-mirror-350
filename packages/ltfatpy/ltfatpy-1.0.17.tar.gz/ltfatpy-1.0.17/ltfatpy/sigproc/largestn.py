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


""" Module of N largest coefficients extraction

Ported from ltfat_2.1.0/sigproc/largestn.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import six
import numpy as np

from ltfatpy.sigproc.thresh import thresh


def largestn(xi, N, thresh_type='hard'):
    """Keep N largest coefficients

    - Usage:

        | ``(xo, Nout) = largestn(xi, N)``
        | ``(xo, Nout) = largestn(xi, N, thresh_type)``

    - Input parameters:

    :param numpy.ndarray xi: Input array
    :param int N: Number of kept coefficients
    :param str thresh_type: Optional flag specifying the type of thresholding
        (see possible values below)

    - Output parameters:

    :returns: ``(xo, Nout)``
    :rtype: tuple

    :var numpy.ndarray xo: Array of the same shape as **xi** keeping
        the **N** largest coefficients
    :var int Nout: Number of coefficients kept

    The parameter **thresh_type** can take the following values:
        ============ ======================================================
        ``'hard'``   Perform hard thresholding. This is the default.

        ``'wiener'`` Perform empirical Wiener shrinkage. This is in between
                     soft and hard thresholding.

        ``'soft'``   Perform soft thresholding.
        ============ ======================================================

    If the coefficients represents a signal expanded in an orthonormal
    basis then this will be the best N-term approximation.

    .. note::
        If soft- or Wiener thresholding is selected, only ``N-1``
        coefficients will actually be returned. This is caused by the Nth
        coefficient being set to zero.

    .. seealso::
        :func:`~ltfatpy.sigproc.largestr.largestr`

    - References:
        :cite:`ma98`
    """

    if not isinstance(N, six.integer_types):
        raise TypeError('N must be an int.')

    # Sort the absolute values of the coefficients.
    sxi = np.sort(abs(xi.flatten()))

    # Find the coefficient sitting at position N through the array,
    # and use this as a threshing value.
    if N <= 0:
        # Choose a thresh value higher than max
        lamb = sxi[-1] + 1.
    else:
        lamb = sxi[-N]

    xo, Nout = thresh(xi, lamb, thresh_type)

    return (xo, Nout)
