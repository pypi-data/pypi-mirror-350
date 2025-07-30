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


"""Module of phaselocking

Ported from ltfat_2.1.0/gabor/phaselock.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import six
import numpy as np


def phaselock(c, a):
    """Phaselock Gabor coefficients

    - Usage:

        | ``c_out = phaselock(c, a)``

    - Input parameters:

    :param numpy.ndarray c: non-phaselocked Gabor coefficients
    :param int a: Length of time shift

    - Output parameters:

    :returns: phaselocked Gabor coefficients
    :rtype: numpy.ndarray

    ``phaselock(c, a)`` phaselocks the Gabor coefficients **c**. The
    coefficients must have been obtained from a :func:`~ltfatpy.gabor.dgt.dgt`
    with parameter **a**.

    Phaselocking the coefficients modifies them so as if they were obtained
    from a time-invariant Gabor system. A filter bank produces phase locked
    coefficients.

    Phaselocking of Gabor coefficients corresponds to the following transform:

    Consider a signal ``f`` of length ``L`` and define ``N = L/a``.

    The output from ``c = phaselock(dgt(f, g, a, M), a)`` is given by


    ..               L-1
        c(m+1,n+1) = sum f(l+1)*exp(-2*pi*i*m*(l-n*a)/M)*conj(g(l-a*n+1)),
                     l=0

    .. math:: c\left(m+1,n+1\\right)=\sum_{l=0}^{L-1}f(l+1)
              e^{-2\pi im(l-na)/M}\overline{g(l-an+1)},

    where ``m = 0,..., M-1`` and ``n = 0,..., N-1`` and ``l-a*n`` are computed
    modulo ``L``.

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`,
                 :func:`~ltfatpy.gabor.phaseunlock.phaseunlock`,
                 :func:`symphase`

    - References:
        :cite:`puc95`
    """

    # NOTE: This function doesn't support the parameter lt (lattice type)
    # supported by the corresponding octave function and the lattice used is
    # seperable (square lattice lt = (0, 1)).

    if not isinstance(a, six.integer_types):
        raise(TypeError('a must be an integer'))

    M = c.shape[0]
    N = c.shape[1]
    L = N * a
    b = L / M

    if b % 1 != 0.:
        raise(ValueError('Lattice error. The a parameter is probably '
                         'incorrect.'))

    TimeInd = np.arange(N) * a
    FreqInd = np.arange(M)

    phase = FreqInd[:, np.newaxis].dot(TimeInd[np.newaxis, :])
    phase = np.mod(phase, M)
    phase = np.exp(2.*1.j*np.pi*phase/M)

    # Handle multisignals
    shape = np.array(c.shape)
    if shape.shape[0] > 2:
        shape[2:] = 1
    c_out = c * phase.reshape(shape)

    return c_out
