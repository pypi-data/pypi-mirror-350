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


"""Module of Canonical dual window calculation

Ported from ltfat_2.1.0/gabor/gabdual.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.gabor.gabframediag import gabframediag
from ltfatpy.sigproc.fir2long import fir2long
from ltfatpy.sigproc.long2fir import long2fir
from ltfatpy.comp.comp_gabdual_long import comp_gabdual_long


def gabdual(g, a, M, L=None):
    """Canonical dual window of Gabor frame

    - Usage:

        | ``gd = gabdual(g, a, M)``
        | ``gd = gabdual(g, a, M, L)``

    - Input parameters:

    :param g: the gabor window.
    :param int a: the length of time shift.
    :param int M: the number of channels.
    :param int L: the length of window. (optional)
    :type g: numpy.ndarray or str or dict

    - Output parameters:

    :returns: the canonical dual window
    :rtype: numpy.ndarray

    ``gabdual(g, a, M)`` computes the canonical dual window of the discrete
    Gabor frame with window **g** and parameters **a**, **M**.

    The window **g** may be a vector of numerical values, a text string or a
    dictionary.

    If the length of **g** is equal to **M**, then the input window is
    assumed to be an FIR window. In this case, the canonical dual window also
    has length of **M**. Otherwise the smallest possible transform length is
    chosen as the window length.

    ``gabdual(g, a, M, L)`` returns a window that is the dual window for a
    system of length **L**. Unless the dual window is a FIR window, the dual
    window will have length **L**.

    If :math:`a > M` then the dual window of the Gabor Riesz sequence with
    window **g** and parameters **a** and **M** will be calculated.

    - Example:

    The following example shows the canonical dual window of the Gaussian
    window.

        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy import pgauss, gabdual
        >>> a = 20
        >>> M = 30
        >>> L = 300
        >>> g = pgauss(L, a*M/L)[0]
        >>> gd = gabdual(g, a, M)
        >>> # Plot in the time-domain
        >>> _ = plt.plot(gd)
        >>> plt.show()

    .. image:: images/gabdual.png
       :width: 700px
       :alt: pgauss gabdual image
       :align: center

    .. seealso:: :func:`~ltfatpy.gabor.gabtight.gabtight`,
        :func:`~ltfatpy.gabor.gabwin.gabwin`,
        :func:`~ltfatpy.sigproc.fir2long.fir2long`,
        :func:`~ltfatpy.gabor.dgt.dgt`
    """
    # Verify a, M and L
    if L is None:
        if isinstance(g, np.ndarray):
            Ls = g.shape[0]
        else:
            Ls = 1
        L = dgtlength(Ls, a, M)
    else:
        Luser = dgtlength(L, a, M)
        if L != Luser:
            raise ValueError(("Incorrect transform length L={0:d} specified" +
                              " for a = {1:d} and M = {2:d}." +
                              " Next valid length  is L={3:d}. See the help" +
                              " of DGTLENGTH for the requirements.").
                             format(L, a, M, Luser))
    # Determine the window
    (g, info) = _call_gabwin(g, a, M, L)

    if L < info['gl']:
        raise ValueError('Window is too long.')

    R = 1
    if (g.ndim > 1):
        R = g.shape[1]

    # Are we in the Riesz sequence of in the frame case
    scale = 1
    if a > M*R:
        # Handle the Riesz basis (dual lattice) case.
        # Swap a and M, and scale differently.
        scale = a / M
        a, M = M, a

    # Compute
    # Rectangular case
    if info['gl'] <= M and R == 1:
        # Diagonal of the frame operator
        d = gabframediag(g, a, M, L)
        gd = g / long2fir(g=d, L=info['gl'])
    else:
        # Long window case
        # Just in case, otherwise the call is harmless.
        g = fir2long(g, L)
        gd = comp_gabdual_long(g, a, M)*scale

    # post process result
    if np.issubdtype(g.dtype, np.floating):
        # If g is real then the output is known to be real.
        gd = gd.real

    return gd


def _call_gabwin(g, a, M, L):
    from ltfatpy.gabor.gabwin import gabwin
    return gabwin(g, a, M, L)


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
