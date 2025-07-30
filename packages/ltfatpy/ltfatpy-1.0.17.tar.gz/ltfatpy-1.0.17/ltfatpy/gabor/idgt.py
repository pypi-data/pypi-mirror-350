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


"""Module of idgt calculation

Ported from ltfat_2.1.0/gabor/idgt.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
import six
from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.gabor.gabwin import gabwin
from ltfatpy.comp.comp_isepdgt import comp_isepdgt
from ltfatpy.tools.postpad import postpad
from ltfatpy.comp.comp_sigreshape_post import comp_sigreshape_post


def idgt(coef, g, a, Ls=None, pt='freqinv'):
    """Inverse discrete Gabor transform

    - Usage:

        | ``(f, g) = idgt(c, g, a)``
        | ``(f, g) = idgt(c, g, a, Ls)``
        | ``(f, g) = idgt(c, g, a, Ls, pt)``

    - Input parameters:

    :param numpy.ndarray c: Array of coefficients
    :param g: Window function
    :param int a: Length of time shift
    :param int Ls: Length of signal
    :param str pt: 'freqinv' or 'timeinv'. Default is 'freqinv'.
    :type g: str, dict or numpy.ndarray

    - Output parameters:

    :return: Signal (dtype = complex128)
    :rtype: numpy.ndarray

    ``idgt(c, g, a)`` computes the Gabor expansion of the input coefficients
    **c** with respect to the window **g** and time shift **a**. The number of
    channels is deduced from the size of the coefficients **c**.

    ``idgt(c, g, a, Ls)`` does as above but cuts or extends **f** to length
    **Ls**.

    ``(f, g)=idgt(...)`` additionally outputs the window used in the
    transform. This is useful if the window was generated from a description
    in a string or cell array.

    For perfect reconstruction, the window used must be a dual window of the
    one used to generate the coefficients.

    The window **g** may be a vector of numerical values, a text string or a
    cell array. See the help of :func:`~ltfatpy.gabor.gabwin` for more details.

    If **g** is a row vector, then the output will also be a row vector. If
    **c** is 3-dimensional, then ``idgt`` will return a matrix consisting of
    one column vector for each of the TF-planes in **c**.

    Assume that ``f=idgt(c, g, a, L)`` for an array **c** of size
    :math:`M \times N`. Then the following holds for :math:`k=0,\ldots,L-1`:

    .. math::

        f(l+1) = \\sum_{n=0}^{N-1}\\sum_{m=0}^{M-1}c(m+1,n+1)e^{2\\pi iml/M}
            g(l-an+1)

    - Additional parameters:

        ``idgt`` takes the following keyword at the end of the line of input
        arguments:

        pt='freqinv'
            Compute a DGT using a frequency-invariant phase. This
            is the default convention described above.
        pt='timeinv'
            Compute a DGT using a time-invariant phase. This
            convention is typically used in FIR-filter algorithms.

    - Examples:

        The following example demonstrates the basic principles for getting
        perfect reconstruction (short version)::

            >>> from ltfatpy import greasy
            >>> from ltfatpy import dgt
            >>> f = greasy()[0]   # Input test signal
            >>> a = 32  # time shift
            >>> M = 64  # frequency shift
            >>> gs = {'name': 'blackman', 'M': 128}  # synthesis window
            >>> # analysis window
            >>> ga = {'name' : ('dual', gs['name']), 'M' : 128}
            >>> (c, Ls) = dgt(f, ga, a, M)[0:2]  # analysis
            >>> # ... do interesting stuff to c at this point ...
            >>> r = idgt(c, gs, a, Ls)[0]  # synthesis
            >>> np.linalg.norm(f-r) < 1e-10 # test
            True

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`,
        :func:`~ltfatpy.gabor.gabwin.gabwin`, :func:`dwilt`,
        :func:`~ltfatpy.gabor.gabtight.gabtight`
  """
    if (not isinstance(g, np.ndarray) and not isinstance(g, str) and
       not isinstance(g, dict)):
        raise TypeError('g must be a numpy.array or str or dict.')

    if (isinstance(g, np.ndarray) and g.size < 2):
        raise ValueError('g must be a vector (you probably forgot to supply' +
                         ' the window function as input parameter.)')

    # Define initial value for flags and key/value pairs.
    if coef.ndim < 2:
        raise ValueError('coef must have at least 2 dimensions')
    M = coef.shape[0]
    N = coef.shape[1]
    if coef.ndim > 2:
        W = coef.shape[2]
    else:
        W = 1

    if not isinstance(a, six.integer_types):
        raise TypeError('a must be an integer')

    L = N * a
    Ltest = dgtlength(L, a, M)
    if Ltest != L:
        ValueError('Incorrect size of coefficient array or "a" parameter. ' +
                   ' See the help of DGTLENGTH for the requirements.')
    # verify pt
    if pt == 'timeinv':
        pt = 1
    elif pt == 'freqinv':
        pt = 0
    else:
        mes = "pt (" + str(pt) + ") argument should be 'timeinv' or 'freqinv'."
        raise ValueError(mes)

    # Determine the window
    gnum = gabwin(g, a, M, L)[0]
    f = comp_isepdgt(coef, gnum, a, pt)

    # Cut or extend f to the correct length, if desired.
    if Ls is not None:
        f = postpad(f, Ls)
    else:
        Ls = L

    f = comp_sigreshape_post(f, Ls, 0, (0, W))
    return (f, gnum)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
