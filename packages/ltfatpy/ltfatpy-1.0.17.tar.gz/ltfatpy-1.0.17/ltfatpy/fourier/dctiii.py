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


"""This module contains dctIII function

Ported from ltfat_2.1.0/fourier/dctiii.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

from ltfatpy.comp.comp_dct import comp_dct
from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post
from ltfatpy.tools.postpad import postpad


def dctiii(f, L=None, dim=None):
    """Discrete Cosine Transform type III

    - Usage:

        | ``c = dctiii(f)``
        | ``c = dctiii(f,L,dim)``

    - Input parameters:

    :param numpy.ndarray f: Input data. **f** dtype has to be float64 or
        complex128.
    :param int L: Length of the output vector. Default is the length of
        **f**.
    :param int dim: dimension along which the transformation is applied.
        Default is the first non-singleton dimension.

    - Output parameter:

    :return: ``c``
    :rtype: numpy.ndarray

    ``dctiii(f)`` computes the discrete cosine transform of type III of the
    input signal **f**. If **f** is a matrix then the transformation is applied
    to each column. For N-D arrays, the transformation is applied to the first
    non-singleton dimension.

    ``dctiii(f,L)`` zero-pads or truncates **f** to length **L** before doing
    the transformation.

    ``dctiii(f,dim=dim)`` or ``dctiii(f,L,dim)`` applies the transformation
    along dimension **dim**.

    The transform is real (output is real if input is real) and
    it is orthonormal.

    This is the inverse of \|dctii\|.

    Let f be a signal of length **L**, let :math:`c=dctiii(f)` and define the
    vector **w** of length **L** by

    .. w = [1/sqrt(2) 1 1 1 1 ...1/sqrt(2)]

    .. math::

        w\\left(n\\right)=\\begin{cases}\\frac{1}{\\sqrt{2}} & \\text{if }n=0
        \\text{ or }n=L-1 \\\ 1 & \\text{otherwise}\\end{cases}

    Then

    .. math::

        c\\left(n+1\\right)=\\sqrt{\\frac{2}{L}}\\sum_{m=0}^{L-1}w\\left(
        m\\right)f\\left(m+1\\right)\\cos\\left(\\frac{\\pi}{L}\\left(
        n+\\frac{1}{2}\\right)m\\right)

    - Examples:

    The following figures show the first 4 basis functions of the dctiii of
    length 20:

    >>> import numpy as np
    >>> # The dctiii is its own adjoint.
    >>> F = dctiii(np.eye(20, dtype=np.float64))
    >>> import matplotlib.pyplot as plt
    >>> plt.close('all')
    >>> fig = plt.figure()
    >>> for ii in range(1,5):
    ...    ax = fig.add_subplot(4,1,ii)
    ...    ax.stem(F[:,ii-1])
    ...
    <Container object of 3 artists>
    <Container object of 3 artists>
    <Container object of 3 artists>
    <Container object of 3 artists>
    >>> plt.show()

    .. image:: images/dctiii.png
       :width: 700px
       :alt: dctiii image
       :align: center
    .. seealso::  :func:`~ltfatpy.fourier.dctiv`,
        :func:`~ltfatpy.fourier.dstiii`

    - References:
        :cite:`rayi90,wi94`
    """
    (f, L, _, _, dim, permutedsize, order) = assert_sigreshape_pre(f, L, dim)
    if L is not None:
        f = postpad(f, L)
    if L == 1:
        c = f
    else:
        c = comp_dct(f, 3)
    return assert_sigreshape_post(c, dim, permutedsize, order)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
