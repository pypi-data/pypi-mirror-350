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


"""Module of dgt calculation

Ported from ltfat_2.1.0/gabor/dgt.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.comp_sepdgt import comp_sepdgt
from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.gabor.gabwin import gabwin
from ltfatpy.comp.assert_groworder import assert_groworder
from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def dgt(f, g, a, M, L=None, pt='freqinv'):
    """Discrete Gabor Transform

    - Usage:

        | ``(c, Ls, g) = dgt(f, g, a, M)``
        | ``(c, Ls, g) = dgt(f, g, a, M, L)``
        | ``(c, Ls, g) = dgt(f, g, a, M, L, pt)``

    - Input parameters:

    :param numpy.ndarray f: Input data. **f** dtype has to be float64 or
        complex128.
    :param g: Window function.
    :param int a: Length of time shift.
    :param int M: Number of channels.
    :param int L: Length of transform to do. Default is None.
    :param str pt: 'freqinv' or 'timeinv'. Default is 'freqinv'
    :type g: str, dict or numpy.ndarray

    - Output parameters:

    :returns: ``(c, Ls, g)``
    :rtype: tuple
    :var numpy.ndarray c: :math:`M*N` array of gabor transform coefficients.
        Its dtype is complex128.
    :var int Ls: length of input signal
    :var numpy.ndarray g: updated window function. Its dtype is float64 or
        complex128 depending on **f** dtype.

    ``dgt(f, g, a, M)`` computes the Gabor coefficients (also known as a
    windowed Fourier transform) of the input signal **f** with respect to the
    window **g** and parameters **a** and **M**. The output is a one or two
    dimensional :class:`numpy.ndarray` in a rectangular layout.

    The length of the transform will be the smallest multiple of **a** and
    **M** that is larger than the signal. **f** will be zero-extended to the
    length of the transform. If **f** is a 2d array, the transformation is
    applied to each column. The length of the transform done can be obtained
    by ``L = c.shape[1] * a``

    The window **g** may be an array of numerical values, a text string or a
    dictionary. See the help of :func:`~ltfatpy.gabor.gabwin` for more
    details.

    ``dgt(f, g, a, M, L)`` computes the Gabor coefficients as above, but does
    a transform of length **L**. **f** will be cut or zero-extended to length
    **L** before the transform is done.

    ``(c, Ls) = dgt(f, g, a, M)`` or ``(c, Ls) = dgt(f, g, a, M, L)`` returns
    the length of the input signal **f**. This is handy for reconstruction:

    - Examples:

    In the following example we create a Hermite function, which is a
    complex-valued function with a circular spectrogram, and visualize
    the coefficients using both :func:`~matplotlib.pyplot.imshow` and
    :func:`~ltfatpy.gabor.plotdgt.plotdgt`:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from ltfatpy import plotdgt
    >>> from ltfatpy import pherm
    >>> a = 10
    >>> M = 40
    >>> L = a * M
    >>> h, _ = pherm(L, 4)  # 4th order hermite function.
    >>> c = dgt(h, 'gauss', a, M)[0]
    >>> # Simple plot: The squared modulus of the coefficients on
    >>> # a linear scale
    >>> _ = plt.imshow(np.abs(c)**2, interpolation='nearest', origin='upper')
    >>> plt.show()
    >>> # Better plot: zero-frequency is displayed in the middle,
    >>> # and the coefficients are show on a logarithmic scale.
    >>> _ = plotdgt(c, a, dynrange=50)
    >>> plt.show()

    .. image:: images/dgt_1.png
       :width: 700px
       :alt: imshow image
       :align: center
    .. image:: images/dgt_2.png
       :width: 600px
       :alt: plotdgt image
       :align: center

    ``(c, Ls, g)=dgt(...)`` outputs the window used in the transform. This is
    useful if the window was generated from a description in a string or
    dictionary.

    The Discrete Gabor Transform is defined as follows: Consider a window
    **g** and a one-dimensional signal **f** of length **L** and define
    :math:`N = L / a`. The output from ``c = dgt(f, g, a, M)`` is then given
    by:

    .. math::

        c\\left(m+1,n+1\\right)=\\sum_{l=0}^{L-1}f(l+1)\\overline{g(l-an+1)}
        e^{-2\\pi ilm/M}

    where :math:`m=0,\ldots,M-1`, :math:`n=0,\ldots,N-1` and :math:`l-an`
    are computed modulo **L**.

    - Additional parameters:

        ``dgt`` takes the following keyword at the end of the line of input
        arguments:

        pt = 'freqinv'
            Compute a DGT using a frequency-invariant phase. This
            is the default convention described above.

        pt = 'timeinv'
            Compute a DGT using a time-invariant phase. This
            convention is typically used in FIR-filter algorithms.

    .. seealso::  :func:`~ltfatpy.gabor.idgt.idgt`,
        :func:`~ltfatpy.gabor.gabwin.gabwin`, :func:`dwilt`,
        :func:`~ltfatpy.gabor.gabdual.gabdual`,
        :func:`~ltfatpy.gabor.phaselock.phaselock`

    - References:
        :cite:`fest98,gr01`
    """

    # Verify f and determine its length
    # Change f to correct shape.
    (f, _unused, Ls, W, dim, permutedshape, order) = assert_sigreshape_pre(f,
                                                                           L)

    # Verify a, M and L
    if L is None:
        # Verify a, M and get L from the signal length f
        L = dgtlength(Ls, a, M)
    else:
        # Verify a, M and get L
        Luser = dgtlength(L, a, M)
        if Luser != L:
            raise ValueError(("Incorrect transform length L={0:d} specified." +
                              " Next valid length  is L={1:d}. See the help" +
                              " of DGTLENGTH for the requirements.").
                             format(L, Luser))
    # verify pt
    if pt == 'timeinv':
        pt = 1
    elif pt == 'freqinv':
        pt = 0
    else:
        raise ValueError("pt argument should be 'timeinv' or 'freqinv'.")
    # Determine the window
    (gnum, info) = gabwin(g, a, M, L)
    if L < info['gl']:
        raise ValueError('Window is too long.')

    # final cleanup
    # Postpad
    C = 0
    if Ls < L:
        f = np.concatenate((f, C*np.ones((L-Ls, W))), axis=0)
    else:
        f = f[:L]

    # call the computation subroutines
    c = comp_sepdgt(f, gnum, a, M, pt)
    # flags_do_timeinv = 1
    order = assert_groworder(order)
    permutedshape = (M, L//a) + permutedshape[1:]
    c = assert_sigreshape_post(c, dim, permutedshape, order)

    if [i for i in c.shape if i > 2] and c.shape[0] == 1:
        c = c.squeeze()

    return (c, Ls, gnum)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
