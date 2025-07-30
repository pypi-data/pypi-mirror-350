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


"""Module to find Gabor parameters to generate image

Ported from ltfat_2.1.0/gabor/gabimagepars.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.tools.lcm import lcm


def gabimagepars(Ls, x, y):
    """Find Gabor parameters to generate image

    - Usage:

        | ``(a, M, L, N, Ngood) = gabimagepars(Ls, x, y)``

    - Input parameters:

    :param int Ls: Signal length
    :param int x: Approximate number of pixels in the time direction
    :param int y: Number of pixels in the frequency direction

    - Output parameters:

    :returns: ``(a, M, L, N, Ngood)``
    :rtype: tuple

    :var int a: Length of time shift
    :var int M: Number of frequency channels
    :var int L: Length of transform to do
    :var int N: Total number of time steps
    :var int Ngood: Number of time steps (columns in the coefficients
        matrix) that contain relevant information. The columns from
        ``Ngood-1`` until ``N-1`` only contain information from a
        zero-extension of the signal.

    ``(a, M, L, N, Ngood) = gabimagepars(Ls, x, y)`` will compute a reasonable
    set of parameters **a**, **M** and **L** to produce a nice Gabor 'image' of
    a signal of length **Ls**.

    If you use this function to calculate a grid size for analysis of a
    real-valued signal (using :func:`~ltfatpy.gabor.dgtreal.dgtreal`), please
    input twice of the desired size **y**. This is because
    :func:`~ltfatpy.gabor.dgtreal.dgtreal` only returns half as many
    coefficients in the frequency direction as :func:`~ltfatpy.gabor.dgt.dgt`.

    For this function to work properly, the specified numbers for **x** and
    **y** must not be large prime numbers.

    - Example:

        We wish to compute a Gabor image of a real valued signal ``f``
        of length 7500. The image should have an approximate resolution of
        600 x 800 pixels:

        >>> from matplotlib.pyplot import show
        >>> from ltfatpy import linus, gabimagepars, dgtreal, plotdgtreal
        >>> f, fs = linus()
        >>> f = f[4000:4000+7500]
        >>> a, M, L, N, Ngood = gabimagepars(7500, 800, 2*600)
        >>> c = dgtreal(f, 'gauss', a, M)[0]
        >>> _ = plotdgtreal(c, a, M, fs=fs, dynrange=90)
        >>> show()

        The size of ``c`` is ``(M/2)+1 x N`` equal to 601 x 700 pixels.

    .. image:: images/gabimagepars.png
       :width: 600px
       :alt: Gabor image of f
       :align: center

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`,
                 :func:`~ltfatpy.gabor.dgtreal.dgtreal`,
                 :func:`~ltfatpy.gabor.sgram.sgram`
    """

    # Note: There is an inaccuracy in the help of the function gabimagepars in
    # ltfat 2.1.0 for Octave.
    # This inaccuracy concerns the size of the resulting coefficients in the
    # example. See the description and confirmation here:
    # http://sourceforge.net/p/ltfat/bugs/120/
    # This inaccuracy is corrected in the docstring of this Python port.

    if min(x, y) > Ls:
        # Small values case, just do an STFT
        M = Ls
        N = Ls
        a = 1
        Ngood = N
        L = Ls
    else:
        # Set M and N to be what the user specified
        M = y
        N = x

        # Determine the minimum transform size.
        K = lcm(M, N)

        # This L is good, but is it not the same as DGT will choose.
        Llong = np.ceil(Ls/K)*K

        # Fix a from the long L
        a = int(Llong/N)

        # Now we have fixed a and M, so we can use the standard method of
        # choosing L
        Lsmallest = lcm(a, M)
        L = int(np.ceil(Ls/Lsmallest)*Lsmallest)

        # We did not get N as desired.
        N = int(L/a)

        # Number of columns to display
        Ngood = int(np.ceil(Ls/a))

        if M <= a:
            raise ValueError(
                'Cannot generate a frame, the signal is too long '
                'as compared to the size of the image. Increase x and y.')

    return (a, M, L, N, Ngood)


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
