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


""" Module of signal normalization

Ported from ltfat_2.1.0/sigproc/normalize.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
from numpy import linalg as LA

from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre
from ltfatpy.comp.assert_sigreshape_post import assert_sigreshape_post
from ltfatpy.sigproc.rms import rms
from ltfatpy.gabor.s0norm import s0norm


def normalize(f, norm='2', dim=None):
    """Normalize input signal by specified norm

    - Usage:

        | ``(f, fnorm) = normalize(f)``
        | ``(f, fnorm) = normalize(f, 'area')``
        | ``(f, fnorm) = normalize(f, dim=2)``
        | ...

    :param numpy.ndarray f: Input signal
    :param str norm: Name of the norm to apply
    :param int dim: Dimension along which norm is applied (first non-singleton
                    dimension as default)

    - Output parameters:

    :return: ``(f, fnorm)``
    :rtype: tuple
    :var numpy.ndarray f: normalized signal
    :var numpy.ndarray fnorm: norm of the signal

    ``normalize(f,...)`` will normalize the signal **f** by the specified norm.

    The norm is specified as a string and may be one of:
        ============ ==========================================================
        ``'1'``      Normalize the :math:`l^1` norm to be *1*.
        ``'area'``   Normalize the area of the signal to be *1*. This is
                     exactly the same as ``'1'``.
        ``'2'``      Normalize the :math:`l^2` norm to be *1*. This is the
                     default
        ``'energy'`` Normalize the energy of the signal to be *1*. This is
                     exactly the same as ``'2'``.
        ``'inf'``    Normalize the :math:`l^{\inf}` norm to be *1*.
        ``'peak'``   Normalize the peak value of the signal to be *1*.
                     This is exactly the same as ``'inf'``.
        ``'rms'``    Normalize the Root Mean Square (RMS) norm of the signal to
                     be *1*.
        ``'s0'``     Normalize the S0-norm to be *1*.
        ``'wav'``    Normalize to the :math:`l^{\inf}` norm to be *0.99* to
                     avoid possible clipping introduced by the quantization
                     procedure when saving as a wav file. This only works with
                     floating point data types.
        ``'null'``   Do NOT normalize, output is identical to input.
        ============ ==========================================================

    .. seealso::
        :func:`~ltfatpy.sigproc.rms.rms`,
        :func:`~ltfatpy.gabor.s0norm.s0norm`
    """
    if not isinstance(norm, str):
        raise TypeError('norm should be string.')
    norm = norm.lower()
    f = f.copy()

    (f, _unused, _unused, W, dim, permutedshape, order) = \
        assert_sigreshape_pre(f, dim=dim)

    if np.issubdtype(f.dtype, np.integer) and norm == 'wav':
        raise TypeError('Integer data types are unsupported for wav norm.')

    fnorm = np.zeros((W, ))
    for ii in range(W):
        if norm == '1' or norm == 'area':
            fnorm[ii] = LA.norm(f[:, ii], 1)
            f[:, ii] = f[:, ii] / fnorm[ii]
        elif norm == '2' or norm == 'energy':
            fnorm[ii] = LA.norm(f[:, ii], 2)
            f[:, ii] = f[:, ii] / fnorm[ii]
        elif norm == 'inf' or norm == 'peak':
            fnorm[ii] = LA.norm(f[:, ii], np.inf)
            f[:, ii] = f[:, ii] / fnorm[ii]
        elif norm == 'rms':
            fnorm[ii] = rms(f[:, ii])
            f[:, ii] = f[:, ii] / fnorm[ii]
        elif norm == 's0':
            fnorm[ii] = s0norm(f[:, ii])
            f[:, ii] = f[:, ii] / fnorm[ii]
        elif norm == 'wav':
            if np.issubdtype(f.dtype, np.floating):
                fnorm[ii] = LA.norm(f[:, ii], np.inf)
                f[:, ii] = 0.99 * f[:, ii] / fnorm[ii]
            else:
                raise TypeError("TO DO: Normalizing integer data types not"
                                "supported yet.")

    f = assert_sigreshape_post(f, dim, permutedshape, order)
    return (f, fnorm)
