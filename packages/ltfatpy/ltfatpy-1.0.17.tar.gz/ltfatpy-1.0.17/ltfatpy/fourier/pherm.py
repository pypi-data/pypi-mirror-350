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


"""This module contains samples of a periodized Hermite function

Ported from ltfat_2.1.0/fourier/pherm.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
import six

from ltfatpy.comp.comp_hermite import comp_hermite
from ltfatpy.comp.comp_hermite_all import comp_hermite_all
from ltfatpy.sigproc.normalize import normalize


def pherm(L, order, tfr=1, phase='accurate', orthtype='noorth'):
    """PHERM  Periodized Hermite function

    - Usage:
        | ``g, = pherm(L,order)``
        | ``g, = pherm(L,order,tfr)``
        | ``g, D = pherm(...)``

    - Input parameters:

    :param int L: Length of vector.
    :param order: Order of Hermite function.
    :type order: scalar or numpy.ndarray
    :param float tfr: ratio between time and frequency support. 1 by default
    :param str phase: 'accurate' or 'fast' (see below)
    :param str orthtype: 'noorth', 'polar' or 'qr' (see below).

    - Output parameters:

    :returns: ``(g, D)``
    :rtype: tuple
    :var numpy.ndarray g: The periodized Hermite function
    :var numpy.ndarray D: The eigenvalues of the Discrete
        Fourier Transform corresponding to the Hermite functions.

    ``pherm(L,order,tfr)`` computes samples of a periodized Hermite function
    of order **order**. **order** is counted from 0, so the zero'th order
    Hermite function is the Gaussian.

    The parameter **tfr** determines the ratio between the effective support
    of **g** and the effective support of the DFT of **g**. If :math:`tfr>1`
    then **g** has a wider support than the DFT of **g**.

    ``pherm(L,order)`` does the same setting :math:`tfr=1`.

    If **order** is a vector, ``pherm`` will return a matrix, where each column
    is a Hermite function with the corresponding **order**.

    ``g, D = pherm(...)`` also returns the eigenvalues **D** of the Discrete
    Fourier Transform corresponding to the Hermite functions.

    The returned functions are eigenvectors of the DFT. The Hermite
    functions are orthogonal to all other Hermite functions with a
    different eigenvalue, but eigenvectors with the same eigenvalue are
    not orthogonal (but see the flags below).

    **phase** can take the following values:

      'accurate'  By default it uses a numerically very accurate that
                  computes each Hermite function individually. This is the
                  default

      'fast'      Use a less accurate algorithm that calculates all the
                  Hermite up to a given order at once.

    **orthtype** can take the following values:

      'noorth'    orthonormalization of the Hermite functions. This is the
                  default.

      'polar'     Orthonormalization of the Hermite functions using the
                  polar decomposition orthonormalization method.

      'qr'        Orthonormalization of the Hermite functions using the
                  Gram-Schmidt orthonormalization method (usign ``qr``).

    If you just need to compute a single Hermite function, there is no
    speed difference between the **accurate** and **fast** algorithm.

    - Examples:

    The following plot shows the spectrograms of 4 Hermite functions of
    length 200 with order 1, 10, 100, and 190:::

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy import sgram
        >>> plt.close('all')
        >>> _ = plt.figure()
        >>> _ = plt.subplot(221)
        >>> _ = sgram(pherm(200, 1)[0], nf=True, tc=True, normalization='lin',
        ... colorbar=False)
        >>> _ = plt.subplot(2,2,2)
        >>> _ = sgram(pherm(200, 10)[0], nf=True, tc=True, normalization='lin',
        ... colorbar=False)
        >>> _ = plt.subplot(2,2,3)
        >>> _ = sgram(pherm(200, 100)[0], nf=True, tc=True,
        ... normalization='lin', colorbar=False)
        >>> _ = plt.subplot(2,2,4)
        >>> _ = sgram(pherm(200, 190)[0], nf=True, tc=True,
        ... normalization='lin', colorbar=False)
        >>> plt.show()

    .. image:: images/pherm.png
       :width: 700px
       :alt: spectrograms
       :align: center
    .. seealso:: :func:`~ltfatpy.fourier.pgauss.pgauss`,
                :func:`~ltfatpy.fourier.psech.psech`
    """
    if not np.isscalar(L) or isinstance(L, str):
        raise TypeError("L must be a scalar")

    if not isinstance(L, six.integer_types):
        raise TypeError('L must be an integer')

    # Parse tfr and order.
    if (not np.isscalar(tfr)):
        raise TypeError('tfr must be a scalar or vector')

    if np.isscalar(order) and not isinstance(order, str):
        W = 1
        order = np.array([order])
    elif isinstance(order, np.ndarray):
        order = order.reshape(-1).copy()
        W = order.shape[0]
    else:
        raise TypeError('order must be a scalar or vector')

    # Calculate W windows.
    if 'accurate' in phase:
        # Calculate W windows.
        g = np.zeros((L, W))
        for w in range(W):
            thisorder = order[w]
            safe = get_safe(thisorder)
            # Outside the interval [-safe,safe]
            # then H(thisorder) is numerically zero.
            nk = int(np.ceil(safe/np.sqrt(L/np.sqrt(tfr))))
            sqrtl = np.sqrt(L)
            lr = np.arange(L)
            for k in range(-nk, nk+1):
                xval = (lr/sqrtl - k*sqrtl) / np.sqrt(tfr)
                g[:, w] = g[:, w] + comp_hermite(thisorder,
                                                 np.sqrt(2*np.pi)*xval)
    else:
        highestorder = np.max(order)
        safe = get_safe(highestorder)
        # Outside the interval [-safe,safe]
        # then H(thisorder) is numerically zero.
        nk = int(np.ceil(safe/np.sqrt(L/np.sqrt(tfr))))
        g = np.zeros((L, highestorder+1))
        sqrtl = np.sqrt(L)
        lr = np.arange(L)
        for k in range(-nk, nk+1):
            xval = (lr/sqrtl - k*sqrtl)/np.sqrt(tfr)
            g = g + comp_hermite_all(highestorder+1, np.sqrt(2*np.pi)*xval)
        g = g[:, order]

    if 'polar' in orthtype:
        # Orthonormalize within each of the 4 eigenspaces
        for ii in range(4):
            subidx = ((order % 4) == ii)
            gsub = g[:, subidx]
            if gsub.size:
                U, _, V = np.linalg.svd(gsub, full_matrices=False)
                gsub = np.dot(U, V)
            else:
                gsub = np.asarray([])
            g[:, subidx] = gsub

    if 'qr' in orthtype:
        # Orthonormalize within each of the 4 eigenspaces
        for ii in range(4):
            subidx = ((order % 4) == ii)
            gsub = g[:, subidx]
            if gsub.size:
                Q, _ = np.linalg.qr(gsub, mode='reduced')
            else:
                Q = np.asarray([])
            g[:, subidx] = Q

    if 'noorth' in orthtype:
        # Just normalize it, no orthonormalization
        g = normalize(g)[0]

    # set up the eigenvalues
    D = np.exp(-1j*order*np.pi/2)
    if W == 1:
        g = g.squeeze()
    return(g, D)


def get_safe(order):
    # These numbers have been computed numerically.
    if order <= 6:
        safe = 4
    else:
        if order <= 18:
            safe = 5
        else:
            if order <= 31:
                safe = 6
            else:
                if order <= 46:
                    safe = 7
                else:
                    # Anything else, use a high number.
                    safe = 12
    return safe

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
