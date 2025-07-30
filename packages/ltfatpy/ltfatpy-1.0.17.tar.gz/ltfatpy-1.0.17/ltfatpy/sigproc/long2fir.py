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


"""Module that cuts long windows to fir

Ported from ltfat_2.1.0/sigproc/long2fir.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.fourier.middlepad import middlepad


def long2fir(g, L, centering='unsymmetric'):
    """Cut LONG window to FIR

    - Usage:

        | ``g = long2fir(g, L)``
        | ``g = long2fir(g, L, 'hp')``

    - Input parameters:

    :param numpy.ndarray g: long window
    :param int L: length of the output FIR window
    :param str centering: 'wp' or 'hp' for whole point even or half point
        even input window. 'unsymmetric' makes no assumption on the symmetry
        of the input data. Default is 'unsymmetric'

    - Output parameters:

    :returns: the FIR window
    :rtype: numpy.ndarray

    ``long2fir(g, L)`` will cut the LONG window **g** to a length **L** FIR
    window by cutting out the middle part. Note that this is a slightly
    different behaviour than :func:`~ltfatpy.fourier.middlepad.middlepad`.

    ``long2fir(g, L, 'wp')`` or ``long2fir(g, L, 'hp')`` does the same
    assuming the input window is a whole-point even or half-point even
    window, respectively.

    .. seealso::  :func:`~ltfatpy.sigproc.fir2long.fir2long`,
        :func:`~ltfatpy.fourier.middlepad.middlepad`
    """
    if not isinstance(g, np.ndarray):
        raise TypeError("g must be a numpy array")
    if L is None:
        raise ValueError('You must specify a way to shorten the window,' +
                         'either by specifying the length or through a flag.')
    W = len(g)
    if W < L:
        raise ValueError('L must be smaller than length of window.')

    # Not translated from Matlab :
    #     if ~isempty(kv.cutrel)
    #     maxval=max(abs(g));
    #     mask=abs(g)>maxval*kv.cutrel;
    #     L=W-2*min(abs(find(mask)-L/2));
    #     end;

    if centering == 'unsymmetric':
        # No assumption on the symmetry of the window.
        if L % 2 == 0:
            # HPE middlepad works the same way as the FIR cutting (e.g. just
            # removing middle points) for even values of L.
            g = middlepad(g, L, centering='hp')
        else:
            # WPE middlepad works the same way as the FIR cutting (e.g. just
            # removing middle points) for odd values of L.
            g = middlepad(g, L)
    elif centering == 'wp':
        g = middlepad(g, L)
        if L % 2 == 0:
            g[L//2] = 0
    elif centering == 'hp':
        g = middlepad(g, L, centering='hp')
        if L % 2 == 1:
            g[int(np.ceil(L/2)) - 1] = 0
    else:
        raise ValueError("centering should take 'hp','wp' or 'unsymmetric'" +
                         " values.")
    return g
