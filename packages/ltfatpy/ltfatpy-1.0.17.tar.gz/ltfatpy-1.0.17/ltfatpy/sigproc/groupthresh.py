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


""" Module of group thresholding

Ported from ltfat_2.1.0/sigproc/groupthresh.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post
from ltfatpy.sigproc.thresh import thresh


def groupthresh(xi, lamb, dim=1, group_type='group', thresh_type='soft'):
    """Group thresholding

    - Usage:

        | ``xo = groupthresh(xi, lamb)``
        | ``xo = groupthresh(xi, lamb, dim)``
        | ``xo = groupthresh(xi, lamb, ...)``

    - Input parameters:

    :param numpy.ndarray xi: Input array. ``xi`` must be a two-dimensional
        array, with dimension ``0`` labelling groups, and dimension ``1``
        labelling members. This means that the groups are the row vectors of
        the input (the vectors along the dimension ``1``).
    :param float lamb: Threshold
    :param int dim: Dimension along which to choose the groups
        (default ``dim=1``)
    :param str group_type: Optional flag specifying the grouping behaviour
        (see possible values below)
    :param str thresh_type: Optional flag specifying the type of thresholding
        within each group (see the parameter ``thresh_type`` in the help
        of :func:`~ltfatpy.sigproc.thresh.thresh` for possible values,
        default ``thresh_type=soft``)

    - Output parameters:

    :returns: Array of the same shape as **xi** containing data from **xi**
        after group thresholding
    :rtype: numpy.ndarray

    ``groupthresh(xi, lamb)`` performs group thresholding on ``xi``, with
    threshold ``lamb``.

    ``groupthresh(xi, lamb, dim)`` chooses groups along dimension ``dim``.

    The parameter **group_type** can take the following values:
        =========== =======================================================
        ``'group'`` Shrinks all coefficients within a given group according
                    to the value of the :math:`l^2` norm of the group in
                    comparison to the threshold ``lamb``.
                    This is the default

        ``'elite'`` Shrinks all coefficients within a given group according
                    to the value of the :math:`l^1` norm of the group in
                    comparison to the threshold value ``lamb``
        =========== =======================================================

    .. seealso::
        :func:`~ltfatpy.sigproc.thresh.thresh`

    - References:
        :cite:`Kowalski08sparsity,kowalski2009mixed,yu2008audio`
    """

    # Note: This function doesn't support the handling of sparse matrices
    # available in the Octave version. Only full numpy arrays are supported in
    # input and output.

    if not isinstance(lamb, float):
        raise TypeError('lamb must be a float')

    # dim (the time or frequency selector) is handled by assert_sigreshape_pre
    xi, L, NbMembers, NbGroups, dim, permutedshape, order = \
        assert_sigreshape_pre(xi, None, dim)

    # Dense case (this Python port doesn't handle the sparse matrix case)
    xo = np.zeros(xi.shape, dtype=xi.dtype)

    if group_type == 'group':
        groupnorm = np.sqrt(np.sum(np.abs(xi)**2., axis=0))
        w = thresh(groupnorm, lamb, thresh_type=thresh_type)[0] / groupnorm

        # Clean w for NaN. NaN appears if the input has a group with norm
        # exactly 0.
        w[np.isnan(w)] = 0

        xo = xi * w

    elif group_type == 'elite':
        for ii in range(NbGroups):
            y = np.sort(np.abs(xi[:, ii]))[::-1]
            rhs = np.cumsum(y)
            rhs = rhs * lamb / (1. + lamb*np.arange(1., NbMembers+1))
            M_ii = np.nonzero(np.diff(np.sign(y-rhs)))[0]
            # Note: the test on M_ii in the Octave version of this function
            # is surprisingly written as find can only return non-zero values
            # or an empty array. Here an equivalent test is written using a
            # more explicit formulation.
            if M_ii.size != 0:
                tau_ii = float(lamb * np.linalg.norm(y[:M_ii[0]+1], 1) /
                               (1. + lamb*(M_ii[0]+1)))
            else:
                tau_ii = 0.

            xo[:, ii] = thresh(xi[:, ii], tau_ii, thresh_type=thresh_type)[0]

    xo = assert_sigreshape_post(xo, dim, permutedshape, order)

    return xo
