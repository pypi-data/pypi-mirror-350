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


""" Module of fir windows calculation

Ported from ltfat_2.1.0/sigproc/firwin.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import six

import numpy as np
from numpy.lib.scimath import sqrt as npsqrt

from ltfatpy.sigproc.normalize import normalize


def firwin(name, M=0, x=None, **kwargs):
    """ Returns a FIR window of length *M* of type *name*.

    - Usage:

        | ``(g, info) = firwin(name, M)``
        | ``(g, info) = firwin(name, M,...)``
        | ``(g, info) = firwin(name, x)``

    - Input parameters:

    :param str name: is the window.
    :param int M: is the length of the window
    :param numpy.ndarray x: is a points vector (default = None)

    - Output parameters:

    :returns: ``(g, info)``
    :rtype: tuple

    :var numpy.ndarray g: window values array
    :var dict info: the information dictionary

    All windows are symmetric and generate zero delay and zero phase
    filters. They can be used for the Wilson and WMDCT transform, except
    when noted otherwise.

    ``firwin(name, x=numpy.array(...))`` where **x** is a vector will sample
    the window definition as the specified points. The normal sampling
    interval for the windows is :math:`-.5< x <.5`.

    In the following PSL means "Peak Sidelobe level", and the main lobe
    width is measured in normalized frequencies.

    If a window **g** forms a "partition of unity" (PU) it means specifically
    that

    .. math::

        g + \mbox{fftshift}(g) = \mathbf{1}_L

    A PU can only be formed if the window length is even, but some windows
    may work for odd lengths anyway.

    If a window is the square root of a window that forms a PU, the window
    will generate a tight Gabor frame / orthonormal Wilson/WMDCT basis if
    the number of channels is less than **M**.

    - The windows available are:

        ===========  =========================================================
        'hann'       von Hann window. Forms a PU. The Hann window has a
                     mainlobe with of 8/M, a PSL of -31.5 dB and decay rate
                     of 18 dB/Octave.

        'sine'       Sine window. This is the square root of the Hanning
                     window. The sine window has a mainlobe width of 8/M,
                     a  PSL of -22.3 dB and decay rate of 12 dB/Octave.

                        - Aliases: `'cosine'`, `'sqrthann'`

        'rect'       (Almost) rectangular window. The rectangular window has a
                     mainlobe width of 4/M, a  PSL of -13.3 dB and decay
                     rate of 6 dB/Octave. Forms a PU if the order is odd.

                        - Alias: `'square'`

        'tria'       (Almost) triangular window. Forms a PU.

                        - Alias: `'bartlett'`

        'sqrttria'   Square root of the triangular window.

        'hamming'    Hamming window. Forms a PU that sums to 1.08 instead
                     of 1.0 as usual. The Hamming window has a
                     mainlobe width of 8/M, a  PSL of -42.7 dB and decay
                     rate of 6 dB/Octave. This window should not be used for
                     a Wilson basis, as a reconstruction window cannot be
                     found by `wildual`.

        'blackman'   Blackman window. The Blackman window has a
                     mainlobe width of 12/M, a PSL of -58.1 dB and decay
                     rate of 18 dB/Octave.

        'blackman2'  Alternate Blackman window. This window has a
                     mainlobe width of 12/M, a PSL of -68.24 dB and decay
                     rate of 6 dB/Octave.

        'itersine'   Iterated sine window. Generates an orthonormal
                     Wilson/WMDCT basis. This window is described in
                     Wesfreid and Wickerhauser (1993) and is used in the
                     ogg sound codec.

                        - Alias: `'ogg'`

        'nuttall'    Nuttall window. The Nuttall window has a
                     mainlobe width of 16/M, a PSL of -93.32 dB and decay
                     rate of 18 dB/Octave.
        'nuttall10'  2-term Nuttall window with 1 continuous derivative.

                        - Alias: `'hann'`, `'hanning'`.

        'nuttall01'  2-term Nuttall window with 0 continuous derivatives.
                     This is a slightly improved Hamming window. It has a
                     mainlobe width of 8/M, a  PSL of -43.19 dB and decay
                     rate of 6 dB/Octave.

        'nuttall20'  3-term Nuttall window with 3 continuous derivatives.
                     The window has a mainlobe width of 12/M, a PSL of
                     -46.74 dB and decay rate of 30 dB/Octave.

        'nuttall11'  3-term Nuttall window with 1 continuous derivative.
                     The window has a mainlobe width of 12/M, a PSL of
                     -64.19 dB and decay rate of 18 dB/Octave.
        'nuttall02'  3-term Nuttall window with 0 continuous derivatives.
                     The window has a mainlobe width of 12/M, a PSL of
                     -71.48 dB and decay rate of 6 dB/Octave.

        'nuttall30'  4-term Nuttall window with 5 continuous derivatives.
                     The window has a mainlobe width of 16/M, a PSL of
                     -60.95 dB and decay rate of 42 dB/Octave.

        'nuttall21'  4-term Nuttall window with 3 continuous derivatives.
                     The window has a mainlobe width of 16/M, a PSL of
                     -82.60 dB and decay rate of 30 dB/Octave.

        'nuttall12'  4-term Nuttall window with 1 continuous derivatives.

                        - Alias: `'nuttall'`.

        'nuttall03'  4-term Nuttall window with 0 continuous derivatives.
                     The window has a mainlobe width of 16/M, a PSL of
                     -98.17 dB and decay rate of 6 dB/Octave.
        ===========  =========================================================

    - Additional keywords arguments:

        ``firwin`` understands the following keyword arguments at the end
        of the list of input:

        **shift** = s
             Shift the window by :math:`s` samples. The value can be a
             fractional number.
        **centering** = 'wp' or 'hp'
             Point even output type : whole or half point even.
             Whole point even is the default. It corresponds to a shift
             of :math:`s=0`.
             Half point even is the convention of most Matlab filter
             routines. It corresponds to a shift of :math:`s=-.5`
        **taper** = t
             Extend the window by a flat section in the middle. The
             argument t is the ratio of the rising and falling
             parts as compared to the total length of the
             window. The default value of 1 means no
             tapering. Accepted values lie in the range from 0 to 1.

    Additionally, ``firwin`` accepts flags to normalize the output.
    Please see the help of :py:meth:`~ltfatpy.sigproc.normalize`.
    Default is to use no normalization.
    For filtering in the time-domain, a normalization of `'1'` or `'area'`
    is preferable.

    .. seealso:: :func:`~ltfatpy.fourier.pgauss.pgauss`, :func:`pbspline`,
        :func:`firkaiser`, :func:`~ltfatpy.sigproc.normalize.normalize`

    - References:
        :cite:`opsc89,harris1978,nuttall1981,wesfreid1993`
    """
    info = {}
    g = None
    if not isinstance(name, str):
        raise TypeError("First argument must be a string containing the name" +
                        " of a window")
    if isinstance(M, float):
        M = int(M)
    if not isinstance(M, six.integer_types):
        raise TypeError("Second argument must be an integer containing the" +
                        " length of the window")
    # Always set to this
    info['isfir'] = True
    # Default values, may be overwritten later in the code
    info['ispu'] = False
    info['issqpu'] = False
    name = name.lower()

    # Define initial value for flags and key/value pairs.
    shift = 0
    if 'shift' in kwargs:
        shift = kwargs['shift']
    if 'centering' in kwargs:
        if kwargs['centering'] == 'hp':
            shift = .5
    taper = 1
    if 'taper' in kwargs:
        if kwargs['taper'] < 1 and kwargs['taper'] >= 0:
            taper = kwargs['taper']

    if M == 0 and x is None:
        return (g, info)

    Xdefined = True

    if x is None:
        # Deal with tapering
        Xdefined = False
        if taper == 0:
            # Window is only tapering, do this and bail out, because subsequent
            # code may fail.
            return (np.ones(M), info)
        # Modify M to fit with tapering
        Morig = M
        M = int(np.round(M * taper))
        Mtaper = Morig - M

        p1 = int(np.round(Mtaper / 2))
        p2 = Mtaper - p1

        # Switch centering if necessary
        if p1 != p2:
            if shift == 0:
                shift = .5
            elif shift == .5:
                shift = 1

        # This is the normally used sampling vector.
        if (M % 2) == 0:  # For even M the sampling interval is [-.5,.5-1/M]
            # Matlab : [0:1/M:.5-1/M,-.5:1/M:-1/M]'
            x = np.r_[0:.5:1/M, -.5:0:1/M]
        else:  # For odd M the sampling interval is [-.5+1/(2M),.5-1/(2M)]
            # Matlab : x = [0:1/M:.5-.5/M,-.5+.5/M:1/M:-1/M]'
            x = np.r_[0:.5:1/M, -.5+.5/M:-.5/M:1/M]

        x = x + shift / M
    else:
        if M != 0 and M != len(x):
            raise ValueError("M should be equel to len(x).")
        M = len(x)

    do_sqrt = False

    if name in {'hanning', 'hann', 'nuttall10'}:
        g = (.5 + .5 * np.cos(2 * np.pi * x))
        info['ispu'] = True
    elif name in {'sine', 'cosine', 'sqrthann'}:
        g = firwin('hanning', M, **kwargs)[0]
        info['issqpu'] = True
        do_sqrt = True
    elif name == 'hamming':
        g = 0.54 + 0.46 * np.cos(2 * np.pi * x)
        # This is the definition taken from the Harris paper
        # elif name is 'hammingacc'
        # g = 25/46 + 21/46 * np.cos(2 * np.pi *x)
    elif name == 'nuttall01':
        g = 0.53836 + 0.46164 * np.cos(2 * np.pi * x)
    elif name in {'square', 'rect'}:
        g = np.asarray(np.abs(x) < .5, dtype='f8')
    elif name in {'tria', 'triangular', 'bartlett'}:
        g = 1.0 - 2.0 * np.abs(x)
        info['ispu'] = True
    elif name == 'sqrttria':
        arg_centering = {}
#         if 'shift' in kwargs:
#             arg_centering['shift'] = kwargs['shift']
        if 'centering' in kwargs:
            arg_centering['centering'] = kwargs['centering']
        g = firwin('tria', M, **arg_centering)[0]
        info['issqpu'] = True
        do_sqrt = True
    # Rounded version of blackman2
    elif name == 'blackman':
        g = 0.42 + 0.5 * np.cos(2 * np.pi * x) + 0.08 * np.cos(4 * np.pi * x)
    elif name == 'blackman2':
        g = 7938/18608 + 9240/18608 * np.cos(2 * np.pi * x) + 1430/18608 * \
            np.cos(4 * np.pi * x)
    elif name in {'nuttall', 'nuttall12'}:
        g = 0.355768 + 0.487396 * np.cos(2 * np.pi * x) + 0.144232 * \
            np.cos(4 * np.pi * x) + 0.012604 * np.cos(6 * np.pi * x)
    elif name in {'itersine', 'ogg'}:
        g = np.sin(np.pi / 2 * np.cos(np.pi * x)**2)
        info['issqpu'] = True
    elif name == 'nuttall20':
        g = 3/8 + 4/8 * np.cos(2 * np.pi * x) + 1/8 * np.cos(4 * np.pi * x)
    elif name == 'nuttall11':
        g = 0.40897 + 0.5 * np.cos(2 * np.pi * x) + 0.09103 * \
            np.cos(4 * np.pi * x)
    elif name == 'nuttall02':
        g = 0.4243801 + 0.4973406 * np.cos(2 * np.pi * x) + 0.0782793 * \
            np.cos(4 * np.pi * x)
    elif name == 'nuttall30':
        g = 10/32 + 15/32 * np.cos(2 * np.pi * x) + 6/32 * \
            np.cos(4 * np.pi * x) + 1/32 * np.cos(6 * np.pi * x)
    elif name == 'nuttall21':
        g = 0.338946 + 0.481973 * np.cos(2 * np.pi * x) + 0.161054 * \
            np.cos(4 * np.pi * x) + 0.018027 * np.cos(6 * np.pi * x)
    elif name == 'nuttall03':
        g = 0.3635819 + 0.4891775 * np.cos(2 * np.pi * x) + 0.1365995 * \
            np.cos(4 * np.pi * x) + 0.0106411 * np.cos(6 * np.pi * x)
    else:
        raise ValueError('Unknown window: ' + name + '.')

    # Force the window to 0 outside (-.5,.5)
    g = g * np.array(np.abs(x) < .5, dtype=int)

    if not Xdefined and taper < 1:
        # Perform the actual tapering.
        g = np.hstack((np.ones(p1), g, np.ones(p2)))
    # Do sqrt if needed.
    if do_sqrt:
        g = npsqrt(g)

    if 'norm' in kwargs:
        g = normalize(g, norm=kwargs['norm'])[0]
#     else:
#         g = normalize(g, norm = 'null')[0]

    return (g, info)

if __name__ == '__main__':  # pragma: no cover
    (g, info) = firwin(name='sine', M=18, centering='wp')
    print(g)
    print(info)
