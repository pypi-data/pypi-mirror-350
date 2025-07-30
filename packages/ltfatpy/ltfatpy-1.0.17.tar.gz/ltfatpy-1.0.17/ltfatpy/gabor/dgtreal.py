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


"""Module of dgtreal calculation

Ported from ltfat_2.1.0/gabor/dgtreal.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.comp.gabpars_from_windowsignal import gabpars_from_windowsignal
from ltfatpy.comp.comp_sepdgtreal import comp_sepdgtreal


def dgtreal(f, g, a, M, L=None, pt='freqinv'):
    """Discrete Gabor transform for real signals

    - Usage:
        | ``(c, Ls, g) = dgtreal(f, g, a, M)``
        | ``(c, Ls, g) = dgtreal(f, g, a, M, L)``
        | ``(c, Ls, g) = dgtreal(f, g, a, M, L, pt)``

    - Input parameters:

    :param numpy.ndarray f: Input data. **f** dtype should be float64
    :param g: Window function.
    :param int a: Length of time shift.
    :param int M: Number of modulations.
    :param int L: Length of transform to do. Default is None.
    :param str pt: 'freqinv' or 'timeinv'. Default is 'freqinv'.
    :type g: str, dict or numpy.ndarray of float64

    - Output parameters:

    :returns: ``(c, Ls, g)``
    :rtype: tuple
    :var numpy.ndarray c: :math:`M*N` array of complex128 coefficients.
    :var int Ls: length of input signal
    :var numpy.ndarray g: updated window function. dtype is float64.

    ``dgtreal(f, g, a, M)`` computes the Gabor coefficients (also known as a
    windowed Fourier transform) of the real-valued input signal **f** with
    respect to the real-valued window **g** and parameters **a** and **M**.
    The output is a vector/matrix in a rectangular layout.

    As opposed to :func:`~ltfatpy.gabor.dgt.dgt` only the coefficients of the
    positive frequencies of the output are returned. ``dgtreal`` will refuse
    to work for complex valued input signals.

    The length of the transform will be the smallest multiple of **a** and
    **M** that is larger than the signal. **f** will be zero-extended to the
    length of the transform. If **f** is a matrix, the transformation is
    applied to each column. The length of the transform done can be obtained
    by ``L = c.shape[1] * a``.

    The window **g** may be a vector of numerical values, a text string or a
    dictionary. See the help of :py:meth:`~ltfatpy.gabor.gabwin` for more
    details.

    ``dgtreal(f, g, a, M, L)`` computes the Gabor coefficients as above, but
    does a transform of length **L**. **f** will be cut or zero-extended to
    length **L** before the transform is done.

    The ``dgtreal`` function  returns the length of the input signal **f**.
    This is handy for reconstruction:

    >>> (c, Ls, g) = dgtreal(f, g, a, M) # doctest: +SKIP
    >>> fr = idgtreal(c, gd, a, M, Ls) # doctest: +SKIP

    will reconstruct the signal **f** no matter what the length of **f** is,
    provided that **gd** is a dual window of **g**.

    It also outputs the window used in the transform. This is useful if the
    window was generated from a description in a string or dictionary.

    See the help on :func:`~ltfatpy.gabor.dgt.dgt` for the definition of the
    discrete Gabor transform. This routine will return the coefficients for
    channel frequencies from 0 to ``floor(M/2)``.

    ``dgtreal`` optionnaly takes a **pt** argument:

        'freqinv'
            Compute a ``dgtreal`` using a frequency-invariant phase. This
            is the default convention described in the help for
            :func:`~ltfatpy.gabor.dgt.dgt`.
        'timeinv'
            Compute a ``dgtreal`` using a time-invariant phase. This
            convention is typically used in filter bank algorithms.

    ``dgtreal`` can be used to manually compute a spectrogram, if you
    want full control over the parameters and want to capture the output.

    - Example:

    >>> import matplotlib.pyplot as plt
    >>> from ltfatpy import greasy
    >>> (f,fs) = greasy()   # Input test signal
    >>> a = 10         # Downsampling factor in time
    >>> M = 200        # Total number of channels, only 101 will be computed
    >>> # Compute the coefficients using a 20 ms long Hann window
    >>> c = dgtreal(f, {'name' : 'hann', 'M' : 0.02*fs}, a, M)[0]
    >>> # Visualize the coefficients as a spectrogram
    >>> dynrange = 90  # 90 dB dynamical range for the plotting
    >>> from ltfatpy import plotdgtreal
    >>> coef = plotdgtreal(c, a, M, fs=fs, dynrange=dynrange)
    >>> plt.show()

    .. image:: images/dgtreal.png
       :width: 700px
       :alt: spectrogram image
       :align: center

    .. seealso::  :func:`~ltfatpy.gabor.dgt.dgt`,
        :func:`~ltfatpy.gabor.idgtreal.idgtreal`,
        :func:`~ltfatpy.gabor.gabwin.gabwin`, :func:`dwilt`,
        :func:`~ltfatpy.gabor.gabtight.gabtight`,
        :func:`~ltfatpy.gabor.plotdgtreal.plotdgtreal`

    - References:
        :cite:`fest98,gr01`
    """
    (f, gnum, _, Ls) = gabpars_from_windowsignal(f, g, a, M, L)[0:4]

    if not np.issubdtype(gnum.dtype, np.floating):
        raise ValueError('The window must be real-valued.')

    # verify pt
    if pt == 'timeinv':
        pt = 1
    elif pt == 'freqinv':
        pt = 0
    else:
        raise ValueError("pt argument should be 'timeinv' or 'freqinv'.")

    c = comp_sepdgtreal(f, gnum, a, M, pt)
    return (c, Ls, gnum)


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
