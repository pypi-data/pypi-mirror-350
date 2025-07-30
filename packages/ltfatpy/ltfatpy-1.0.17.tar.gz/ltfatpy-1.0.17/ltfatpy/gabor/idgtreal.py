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


"""Module of idgtreal calculation

Ported from ltfat_2.1.0/gabor/idgtreal.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.gabor.gabwin import gabwin
from ltfatpy.comp.comp_isepdgtreal import comp_isepdgtreal
from ltfatpy.tools.postpad import postpad
from ltfatpy.comp.comp_sigreshape_post import comp_sigreshape_post


def idgtreal(coef, g, a, M, Ls=None, pt='freqinv'):
    """Inverse discrete Gabor transform for real-valued signals

    - Usage:
        | ``(f, g) = idgtreal(c, g, a, M)``
        | ``(f, g) = idgtreal(c, g, a, M, Ls)``
        | ``(f, g) = idgtreal(c, g, a, M, Ls, pt)``

    - Input parameters:

    :param numpy.ndarray c: Array of coefficients
    :param g: Window function
    :param int a: Length of time shift
    :param int M: Number of channels
    :param int Ls: Length of signal
    :param str pt: 'freqinv' or 'timeinv'. Default is 'freqinv'.
    :type g: str, dict or numpy.ndarray

    - Output parameters:

    :returns: ``(f, g)``
    :rtype: tuple
    :var numpy.ndarray f: signal
    :var numpy.ndarray g: window


    ``idgtreal(c, g, a, M)`` computes the Gabor expansion of the input
    coefficients **c** with respect to the real-valued window **g**, time
    shift **a** and number of channels **M**. **c** is assumed to be the
    positive frequencies of the Gabor expansion of a real-valued signal.

    It must hold that ``c.shape[0] == np.floor(M/2)+1``. Note that since the
    correct number of channels cannot be deduced from the input, ``idgtreal``
    takes an additional parameter as opposed to
    :func:`~ltfatpy.gabor.idgt.idgt`.

    The window **g** may be a vector of numerical values, a text string or a
    dictionary. See the help of :func:`~ltfatpy.gabor.gabwin.gabwin` for more
    details.

    ``idgtreal(c, g, a, M, Ls)`` does as above but cuts or extends **f** to
    length **Ls**.

    ``(f, g) = idgtreal(...)`` outputs the window used in the transform. This
    is useful if the window was generated from a description in a string or
    dictionary.

    For perfect reconstruction, the window used must be a dual window of the
    one used to generate the coefficients.

    If **g** is a row vector, then the output will also be a row vector. If
    **c** is 3-dimensional, then ``idgtreal`` will return a matrix consisting
    of one column vector for each of the TF-planes in **c**.

    See the help on :func:`~ltfatpy.gabor.idgt.idgt` for the precise definition
    of the inverse Gabor transform.

    - Additional parameters

    ``idgtreal``  optionnaly takes a **pt** arguments that can take the
    following values:

        ==========  ===========================================================
        'freqinv'   Compute a ``idgtreal`` using a frequency-invariant phase.
                    This is the default convention described in the help for
                    :func:`~ltfatpy.gabor.dgt.dgt`.

        'timeinv'   Compute a ``idgtreal`` using a time-invariant phase. This
                    convention is typically used in filter bank algorithms.
        ==========  ===========================================================

    - Examples

        The following example demonstrates the basic principles for getting
        perfect reconstruction (short version)::

            >>> from ltfatpy import greasy
            >>> from ltfatpy import dgtreal
            >>> f = greasy()[0]   # Input test signal
            >>> a = 32  # time shift
            >>> M = 64  # frequency shift
            >>> gs = {'name': 'blackman', 'M': 128}  # synthesis window
            >>> # analysis window
            >>> ga = {'name' : ('dual', gs['name']), 'M' : gs['M']}
            >>> (c, Ls) = dgtreal(f, ga, a, M)[0:2]  # analysis
            >>> r = idgtreal(c, gs, a, M, Ls)[0]  # synthesis
            >>> np.linalg.norm(f-r) < 1e-10 # test
            True

    .. seealso::  :func:`~ltfatpy.gabor.idgt.idgt`,
        :func:`~ltfatpy.gabor.gabwin.gabwin`,
        :func:`~ltfatpy.gabor.gabdual.gabdual`, :func:`dwilt`
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
    N = coef.shape[1]
    if coef.ndim > 2:
        W = coef.shape[2]
    else:
        W = 1

    # Make a dummy call to test the input parameters
    Lsmallest = dgtlength(1, a, M)
    M2 = np.floor(M/2)+1

    if M2 != coef.shape[0]:
        mess = ('Mismatch between the specified number of channels ' +
                'and the size of the input coefficients: ' +
                'M2 = {0:f}, coef.shape = {1:s}')
        raise ValueError(mess.format(M2, '%s' % (coef.shape, )))

    L = N * a

    if L % Lsmallest > 0:
        raise ValueError('Invalid size of coefficient array.')

    # Determine the window

    (g, info) = gabwin(g, a, M, L)

    if L < info['gl']:
        raise ValueError('Window is too long.')

    if not np.issubdtype(g.dtype, np.floating):
        raise ValueError('The window must be real-valued.')

    # verify pt
    if pt == 'timeinv':
        pt = 1
    elif pt == 'freqinv':
        pt = 0
    else:
        mes = "pt (" + str(pt) + ") argument should be 'timeinv' or 'freqinv'."
        raise ValueError(mes)

    # Do the actual computation.
    f = comp_isepdgtreal(coef, g, a, M, pt)

    # Cut or extend f to the correct length, if desired.
    if Ls is not None:
        f = postpad(f, Ls)
    else:
        Ls = L
    f = comp_sigreshape_post(f, Ls, 0, (0, W))
    return (f, g)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
