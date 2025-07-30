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


""" Module of Kaiser-Bessel window calculation

Ported from ltfat_2.1.0/sigproc/firkaiser.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.sigproc.normalize import normalize


def firkaiser(L, beta, centering='wp', norm='null'):
    """Kaiser-Bessel window

    - Usage:

        | ``g = firkaiser(L, beta)``
        | ``g = firkaiser(L, beta,...)``

    - Input parameters:

    :param int L: length of the window
    :param int beta: beta parameter of the Kaiser-Bessel window
    :param str centering: Flag specifying if the generated window **g** is
        whole point even when ``centering='wp'`` or half point even when
        ``centering='hp'``
    :param str norm: Normalization flag for the output. Please see the
        parameter **norm** in the help of
        :func:`~ltfatpy.sigproc.normalize.normalize` for possible values.

    - Output parameters:

    :returns: Kaiser-Bessel window of length ``L`` with parameter ``beta``
    :rtype: numpy.ndarray

    ``firkaiser(L, beta)`` computes the Kaiser-Bessel window of length **L**
    with parameter **beta**. The smallest element of the window is set to zero
    when the window has an even length. This gives the window perfect
    whole-point even symmetry, and makes it possible to use the window for a
    Wilson basis.

    .. note::

        This Python port only implements the ``'normal'`` option of the
        original ``firkaiser`` function available in LTFAT for Octave.

        The ``'derived'`` option is not currently implemented in this port
        because the original ``firkaiser`` function contains a reported
        `bug <http://sourceforge.net/p/ltfat/bugs/124/>`_.

        We are thus waiting for the correction of the original code to add the
        ``'derived'`` option to this port.

    .. seealso:: :func:`~ltfatpy.sigproc.firwin.firwin`
                 :func:`~ltfatpy.sigproc.normalize.normalize`

    - References:
        :cite:`opsc89`
    """

    """ NOTE:
    All the elements for the implementation of the stype='derived' option
    have been left as comments in the following code, so that it can be easily
    implemented once the corrected code will be provided by the LTFAT for
    Octave project.

    The function definition should be:
    def firkaiser(L, beta, centering='wp', stype='normal', norm='null'):

    The following should be added in the docstring:
        :param str stype: Flag specifying the type of generated window **g**,
        returning a normal Kaiser-Bessel window when ``stype='normal'`` and a
        derived Kaiser-Bessel window when ``stype='derived'``

    The test on stype should uncommented below, and the code for the 'derived'
    case should be uncommented and corrected.

    test_firkaiser, the test function of firkaiser should also be updated.
    """

    if not isinstance(beta, float):
        raise TypeError('beta must be a float.')
    cent = 0.
    if centering == 'hp':
        cent = 0.5

    # if stype == 'normal':
    if L == 1:
        g = np.array([1.])
    else:
        k = np.arange(L) + (L % 2)/2. - 0.5 + cent
        # NOTE: to take the sqrt of negative values we need to convert
        # the data to complex, otherwise np.sqrt returns nan
        tmp = k*(L-1.-k)
        tmp = tmp.astype('complex128')
        k = np.real(2. * beta / (L-1) * np.sqrt(tmp))
        g = np.i0(k) / np.i0(beta)

    g = np.fft.ifftshift(g)

    if ((centering == 'wp' and L % 2 == 0) or
            (centering == 'hp' and L % 2 == 1)):
        # Explicitly zero last element. This is done to get the right
        # symmetry, and because that element sometimes turn negative.
        g[int(np.floor(L/2.))] = 0.

    """
    elif stype == 'derived':
        if L % 2 == 1:
            raise ValueError('The length of the choosen window must be even.')

        if centering == 'wp':
            if L % 4 == 0:
                L2 = L/2 + 2
            else:
                L2 = L/2 + 1
        else:
            L2 = int(np.floor((L+1.)/2.))

        # Compute a normal Kaiser window
        g_normal = np.fft.fftshift(firkaiser(L2, beta, centering=centering))

        g1 = np.sqrt(np.cumsum(g_normal[:L2])/np.sum(g_normal[:L2]))

        if centering == 'wp':
            # NOTE: Here the Octave code differentiate two cases if L is even
            # or odd. This is useless, since this part of the code can only be
            # reached when L is even due to the error thrown above when L is
            # odd. So this Python port only includes the L even case.
            g = np.concatenate((g1[::-1], g1[1:L/2]))
        else:
            g = np.concatenate((g1[::-1], g1))

        if ((centering == 'wp' and L % 2 == 0) or
                (centering == 'hp' and L % 2 == 1)):
            # Explicitly zero last element. This is done to get the right
            # symmetry, and because that element sometimes turn negative.
            g[np.floor(L/2.)] = 0.
    """

    # In Octave/MATLAB, the besseli computation sometimes generates a zero
    # imaginary component. It is not sure if numpy.i0 does the same, but for
    # safety we keep this line.
    g = np.real(g)

    g = normalize(g, norm=norm)[0]
    return g
