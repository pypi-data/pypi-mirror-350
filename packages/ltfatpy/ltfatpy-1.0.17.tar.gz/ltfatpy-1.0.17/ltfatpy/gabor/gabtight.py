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


"""Module of canonical tight windows calculation

Ported from ltfat_2.1.0/gabor/gabtight.m

.. moduleauthor:: Denis Arrivault,
                  Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.sigproc.fir2long import fir2long
from ltfatpy.sigproc.long2fir import long2fir
from ltfatpy.gabor.gabframediag import gabframediag
from ltfatpy.comp.comp_gabtight_long import comp_gabtight_long


def gabtight(g, a, M, L=None):
    """Canonical tight window of Gabor frame

    - Usage:

        | ``gt = gabtight(None, a, M, L)``
        | ``gt = gabtight(g, a, M)``
        | ``gt = gabtight(g, a, M, L)``

    - Input parameters:

    :param g: Gabor window
    :type g: numpy.ndarray or str or dict
    :param int a: Length of time shift
    :param int M: Number of modulations
    :param int L: Length of window (optional except if **g** is None)

    - Output parameters:

    :return: Canonical tight window
    :rtype: numpy.ndarray

    ``gabtight(None, a, M, L)`` computes a nice tight window of length **L**
    for a lattice with parameters **a**, **M**. The window is not an FIR
    window, meaning that it will only generate a tight system if the system
    length is equal to **L**.

    ``gabtight(g, a, M)`` computes the canonical tight window of the Gabor
    frame with window **g** and parameters **a**, **M**.

    The window **g** may be a vector of numerical values, a text string or a
    dictionary. See the help of :func:`~ltfatpy.gabor.gabwin` for more details.

    If the length of **g** is equal to **M**, then the input window is assumed
    to be a FIR window. In this case, the canonical dual window also has
    length of **M**. Otherwise the smallest possible transform length is
    chosen as the window length.

    ``gabtight(g, a, M, L)`` returns a window that is tight for a system of
    length **L**. Unless the input window **g** is a FIR window, the returned
    tight window will have length **L**.

    If ``a > M`` then an orthonormal window of the Gabor Riesz sequence
    with window **g** and parameters **a** and **M** will be calculated.

    - Examples:

        The following example shows the canonical tight window of the Gaussian
        window. This is calculated by default by
        :func:`~ltfatpy.gabor.gabtight` if no window is specified:

        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy import gabtight
        >>> a = 20
        >>> M = 30
        >>> L = 300
        >>> gt = gabtight(None, a, M, L)
        >>> # Plot in the time-domain
        >>> _ = plt.plot(gt)
        >>> plt.show()

    .. image:: images/gabtight.png
       :width: 700px
       :alt: pgauss gabtight image
       :align: center

    .. seealso::  :func:`~ltfatpy.gabor.gabdual.gabdual`,
                  :func:`~ltfatpy.gabor.gabwin.gabwin`,
                  :func:`~ltfatpy.sigproc.fir2long.fir2long`,
                  :func:`~ltfatpy.gabor.dgt.dgt`
    """
    # Verify a, M and L
    if g is None:
        g = 'gauss'

    if L is None:
        if not isinstance(g, np.ndarray):
            Ls = 1
        else:
            Ls = g.shape[0]
        L = dgtlength(Ls, a, M)
    else:
        Luser = dgtlength(L, a, M)
        if L != Luser:
            raise ValueError(("Incorrect transform length L={0:d} specified." +
                              " Next valid length  is L={1:d}. See the help" +
                              " of DGTLENGTH for the requirements.").format(L,
                             Luser))

    # Determine the window
    (g, info) = _call_gabwin(g, a, M, L)

    if L < info['gl']:
        raise ValueError('Window is too long.\n')
    R = 1
    if g.ndim > 1:
        R = g.shape[1]

    # Are we in the Riesz sequence of in the frame case
    scale = 1
    if a > M*R:
        # Handle the Riesz basis (dual lattice) case.
        # Swap a and M, and scale differently.
        scale = np.sqrt(a/M)
        a, M = M, a

    # Compute the rectangular case
    if info['gl'] <= M and R == 1:
        # Diagonal of the frame operator
        d = gabframediag(g, a, M, L)
        gt = g / np.sqrt(long2fir(d, info['gl']))
    else:
        # Long window case
        # Just in case, otherwise the call is harmless.
        g = fir2long(g, L)
        gt = comp_gabtight_long(g, a, M) * scale

    # post process result
    if np.issubdtype(g.dtype, np.floating):
        # If g is real then the output is known to be real.
        gt = gt.real

    return gt


def _call_gabwin(g, a, M, L):
    # gabwin is imported in a different function to avoid circular imports
    from ltfatpy.gabor.gabwin import gabwin
    return gabwin(g, a, M, L)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
