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


""" Module of window calculation from descriptions

Ported from ltfat_2.1.0/comp/comp_window.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import numpy as np
import copy

from ltfatpy.comp.arg_firwin import arg_firwin
from ltfatpy.comp.comp_pgauss import comp_pgauss
from ltfatpy.gabor.gabdual import gabdual
from ltfatpy.gabor.gabtight import gabtight
from ltfatpy.sigproc.firwin import firwin
from ltfatpy.fourier.psech import psech
from ltfatpy.sigproc.fir2long import fir2long
from ltfatpy.fourier.pgauss import pgauss


def comp_window(g, a, M, L=None):
    """Compute the window from numpy.ndarray, str or dictionary.

    - Usage:

        | ``(g, info) = comp_window(g, a, M, L)``

    - Input parameters:

    :param g: window parameters
    :type g: str or dict (with parameters of the window as keywords)
    :param int a: the length of time shift.
    :param int M: the number of channels.
    :param int L: the length of window.

    - Output parameters:

    :returns: ``(g, info)``
    :rtype: tuple
    :var numpy.ndarray g: the computed window
    :var dict info: the information dictionary

    It will compute the window from a text description or a dictionary
    containing additional parameters.

    .. note:: One field of the g dictionary must be the name of the window
        and should be define with the **name** key.

    .. note:: This function is the driving routine behind
        :func:`~ltfatpy.gabor.gabwin.gabwin`. Consider using this function
        instead.

    .. seealso:: :func:`~ltfatpy.gabor.gabwin.gabwin`, :func:`wilwin`

    .. note:: Basic discovery: some windows depend on *L*, and some windows
        help define *L*, so the calculation of *L* is window dependant.
    """
    # As this function can modify the content of g, we work on a copy to
    # avoid modifying the passed data
    g = copy.deepcopy(g)

    # Default values
    info = {}
    info['gauss'] = False
    info['wasrow'] = False
    info['isfir'] = False
    info['istight'] = False
    info['isdual'] = False
    errorMessage = "You must specify a length L if a window is represented"
    errorMessage += " as a text string or dictionary."

    # Manually get the list of FIR window names
    firwinnames = arg_firwin()

    # Create window if string was given as input.
    if isinstance(g, str):
        winname = g.lower()
        if winname in {'pgauss', 'gauss'}:
            if L is None:
                raise ValueError(errorMessage)
            g = comp_pgauss(L, a*M/L, 0, 0)
            info['gauss'] = True
            info['tfr'] = a*M/L
        elif winname in {'psech', 'sech'}:
            if L is None:
                raise ValueError(errorMessage)
            g = psech(L, a*M/L)[0]
            info['tfr'] = a*M/L
        elif winname in {'dualgauss', 'gaussdual'}:
            if L is None:
                raise ValueError(errorMessage)
            g = comp_pgauss(L, a*M/L, 0, 0)
            g = gabdual(g, a, M)
            info['isdual'] = True
            info['tfr'] = a*M/L
        elif winname in {"tight"}:
            if L is None:
                raise ValueError(errorMessage)
            g = gabtight(None, a, M, L)
            info['tfr'] = a*M/L
            info['istight'] = True
        elif winname in firwinnames:
            (g, firinfo) = firwin(winname, M, norm='2')
            info['isfir'] = True
            if firinfo['issqpu']:
                info['istight'] = True
        else:
            raise ValueError('Unknown window : ' + winname)
    # Create window if dictionary was given as input.
    elif isinstance(g, dict):
        if 'name' not in g:
            raise ValueError("the g dict must contain a key 'name'.")
#         if not isinstance(g['name'], str):
#             raise ValueError("the g['name'] value must be a string.")
        winname = g.pop('name')
        wintype = None
        if isinstance(winname, tuple):
            wintype = winname[0]
            if len(winname) > 1:
                winname = winname[1].lower()
            else:
                winname = 'gauss'
        elif isinstance(winname, str):
            winname = winname.lower()
        else:
            raise TypeError("the g['name'] value must be a string " +
                            "or a tuple.")
        if wintype is None:
            if winname in {'pgauss', 'gauss'}:
                if L is None:
                    raise ValueError(errorMessage)
                if 'tfr' not in g:
                    g, tfr = pgauss(L, a*M/L, **g)
                else:
                    g, tfr = pgauss(L, **g)
                info['tfr'] = tfr
                info['gauss'] = True
            elif winname in {'psech', 'sech'}:
                if L is None:
                    raise ValueError(errorMessage)
                if 'tfr' not in g:
                    g, tfr = psech(L,  a*M/L, **g)
                else:
                    g, tfr = psech(L, **g)
                info['tfr'] = tfr
            elif winname in firwinnames:
                if 'M' not in g:
                    raise ValueError("M has to be specified in the g " +
                                     "dictionary for fir windows.")
                else:
                    g, firinfo = firwin(winname, norm='energy', **g)
                info['isfir'] = True
                if firinfo['issqpu']:
                    info['istight'] = True
            else:
                raise ValueError('Unsupported window : ' + winname)
        elif wintype == 'dual':
            gorig = g.copy()
            gorig['name'] = winname
            if winname in firwinnames and 'M' not in gorig:
                gorig['M'] = M
            g, info['auxinfo'] = comp_window(gorig, a, M, L)
            g = gabdual(g, a, M, L)
            # gorig can be string or dict
            if info['auxinfo']['isfir'] and __test_isfir(gorig, M):
                info['isfir'] = True
            info['isdual'] = True
        elif wintype == 'tight':
            gorig = g.copy()
            gorig['name'] = winname
            if winname in firwinnames and 'M' not in gorig:
                gorig['M'] = M
            g, info['auxinfo'] = comp_window(gorig, a, M, L)
            g = gabtight(g, a, M, L)
            # The same as in dual?
            if info['auxinfo']['isfir'] and __test_isfir(gorig, M):
                info['isfir'] = True
            info['istight'] = True

    if isinstance(g, np.ndarray):
        if g.ndim > 1 and g.shape[1] > 1:
            if g.shape[0] == 1:
                # g was a row vector.
                g = g.squeeze()
                info['wasrow'] = True

        if g.shape[0] % M > 0:
            # Zero-extend the window to a multiple of M
            g = fir2long(g, int(np.ceil(g.shape[0] / M) * M))

        # Information to be determined post creation.
        info['wasreal'] = np.issubdtype(g.dtype, np.floating)
        info['gl'] = g.shape[0]
        if L is not None and info['gl'] < L:
            info['isfir'] = True
    return (g, info)


def __test_isfir(gorig, M):
    """ Internal function that tests if original window is FIR.

    Dual window is FIR if length of the original window is <= M. This is true
    if the length was not explicitly defined and gorig is a string.

    - Input parameters:

    :param gorig: window parameters
    :type gorig: dict (with parameters of the window as keywords)
    :param int M: the number of channels.

    - Output parameters:

    :rtype: boolean
    """
    if (isinstance(gorig, dict) and gorig):
        if ('M' in gorig) and (gorig['M'] <= M):
            return True
    if isinstance(gorig, str):
        return True
    return False
