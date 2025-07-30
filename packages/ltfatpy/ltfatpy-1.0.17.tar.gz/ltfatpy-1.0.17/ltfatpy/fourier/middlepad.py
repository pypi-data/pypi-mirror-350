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


"""Module of symmetrical zero-extension or cut of data

Ported from ltfat_2.1.0/fourier/middlepad.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import six
import numpy as np

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post


def middlepad(f, L, dim=None, centering='wp'):
    """Symmetrically zero-extends or cuts a function

    - Usage:

        | ``h = middlepad(f, L)``
        | ``h = middlepad(f, L, dim)``
        | ``h = middlepad(f, L, ...)``

    - Input parameters:

    :param numpy.ndarray f: Input array
    :param int L: Length of the output array
    :param int dim: Axis over which to zero-extend or cut **f**
    :param str centering: Flag specifying if **f** is whole point even when
        ``centering='wp'`` or half point even when ``centering='hp'``

    - Output parameters:

    :returns: Zero-extended or cut array
    :rtype: numpy.ndarray

    ``middlepad(f, L)`` zero-extends or cuts **f** to length **L** by
    inserting zeros in the middle of the vector, or by cutting in the middle
    of the vector.

    If **f** is whole-point even, ``middlepad(f, L)`` will also be
    whole-point even.

    ``middlepad(f, L, dim)`` does the same along dimension **dim**.

    If **f** has even length, then **f** will not be purely zero-extended,
    but the last element will be repeated once and multiplied by ``1/2``.
    That is, the support of **f** will increase by one!

    Adding the flag ``centering='wp'`` will cut or extend whole point even
    functions (the default). Adding ``centering='hp'`` will do the same for
    half point even functions.

    .. seealso:: :func:`~ltfatpy.fourier.isevenfunction.isevenfunction`,
                 :func:`~ltfatpy.sigproc.fir2long.fir2long`,
                 :func:`~ltfatpy.fourier.fftresample.fftresample`
    """

    # Note: For a future improvement, it might be possible to replace the use
    # of numpy.concatenate with numpy.r_ in this function to simplify the code.

    if not isinstance(L, six.integer_types):
        raise TypeError('L must be an integer.')

    if L < 1:
        raise ValueError('L must be larger than 0.')

    f, L, Ls, W, dim, permutedsize, order = assert_sigreshape_pre(f, L, dim)

    Lorig = Ls

    # Skip the main section if there is nothing to do. This is necessary
    # because some of the code below cannot handle the case of 'nothing to do'
    if L != Ls:
        if centering == 'wp':

            # ---------------   WPE case --------------------------------------
            if Lorig == 1:
                # Rather trivial case
                h = np.concatenate((f[np.newaxis, 0, :],
                                    np.zeros((L-1, W), dtype=f.dtype)))

            else:

                if Lorig > L:
                    # Cut

                    if L % 2 == 0:

                        # L even. Use average of endpoints.
                        h = np.concatenate((f[:L//2, :],
                                            (f[np.newaxis, L//2, :] +
                                             f[np.newaxis, Lorig-L//2, :]) / 2,
                                            f[Lorig-L//2+1:Lorig, :]))

                    else:

                        # No problem, just cut.
                        h = np.concatenate((f[:(L+1)//2, :],
                                            f[Lorig-(L-1)//2:Lorig, :]))

                else:
                    d = L - Lorig

                    # Extend
                    if Lorig % 2 == 0:
                        # Lorig even. We must split a value.
                        h = np.concatenate((f[:Lorig//2, :],
                                            f[np.newaxis, Lorig//2, :]/2,
                                            np.zeros((d-1, W), dtype=f.dtype),
                                            f[np.newaxis, Lorig//2, :]/2,
                                            f[Lorig//2+1:Lorig, :]))

                    else:
                        # Lorig is odd, we can just insert zeros.
                        h = np.concatenate((f[:(Lorig+1)//2, :],
                                            np.zeros((d, W), dtype=f.dtype),
                                            f[(Lorig+1)//2:Lorig, :]))

        elif centering == 'hp':

            # ------------------ HPE case ------------------------------------

            # NOTE: There is a bug here in LTFAT 2.1.0 for Octave, see:
            # https://sourceforge.net/p/ltfat/bugs/123
            # This bug arise because the case "if Lorig==1" hasn't been
            # implemented in the Octave code when centering = 'hp'.
            # To solve this bug, we simply remove the test "if Lorig==1", which
            # seems to lead to satisfactory results.

            if Lorig > L:

                d = Lorig-L
                # Cut

                if L % 2 == 0:
                    # L even

                    # No problem, just cut.
                    h = np.concatenate((f[:L//2, :], f[Lorig-L//2:Lorig, :]))

                else:
                    # Average of endpoints.
                    h = np.concatenate((f[:(L-1)//2, :],
                                        (f[np.newaxis, (L-1)//2, :] +
                                         f[np.newaxis, Lorig-(L+1)//2, :]) / 2,
                                        f[Lorig-(L-1)//2:Lorig, :]))

            else:

                d = L-Lorig

                # Extend
                if Lorig % 2 == 0:

                    # Lorig even. We can just insert zeros in the middle.
                    h = np.concatenate((f[:Lorig//2, :],
                                        np.zeros((d, W), dtype=f.dtype),
                                        f[Lorig//2:Lorig, :]))

                else:
                    # Lorig odd. We need to split a value in two
                    h = np.concatenate((f[:(Lorig-1)//2, :],
                                        f[np.newaxis, (Lorig-1)//2, :]/2,
                                        np.zeros((d-1, W), f.dtype),
                                        f[np.newaxis, (Lorig-1)//2, :]/2,
                                        f[(Lorig+1)//2:Lorig, :]))

    else:
        # we don't want this function to return a reference or a view to the
        # input, so we make a copy
        h = f.copy()

    h = assert_sigreshape_post(h, dim, permutedsize, order)

    return h
