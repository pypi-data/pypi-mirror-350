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


"""Module of Gabor window calculation

Ported from ltfat_2.1.0/gabor/gabwin.m


.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

from ltfatpy.comp.comp_window import comp_window


def gabwin(g, a, M, L=None):
    """Computes a Gabor window

    - Usage:

        | ``(g, info) = gabwin(g, a, M, L)``

    - Input parameters:

    :param g: the gabor window
    :param int a: the length of time shift
    :param int M: the number of channels
    :param int L: the length of window (optional)
    :type g: numpy.ndarray or str or dict

    - Output parameters:

    :returns: ``(g, info)``
    :rtype: tuple
    :var numpy.ndarray g: the computed gabor window
    :var dict info: the information dictionary (see before)

    With the transform length parameter **L** specified, it computes a window
    that fits well with the specified number of channels **M**, time shift
    **a** and transform length **L**. The window itself is specified by a
    text description or a dictionary containing additional parameters.

    The window can be specified directly as a vector of numerical
    values. In this case, ``gabwin`` only checks assumptions about transform
    sizes etc.

    Without the transform length parameter **L**, it does the same, but the
    window must be a FIR window.

    The window can be specified as one of the following text strings:

        ===========  =======================================
        'gauss'      Gaussian window fitted to the lattice,
                     i.e. :math:`tfr = a * M / L`.

        'dualgauss'  Canonical dual of Gaussian window.

        'tight'      Tight window generated from a Gaussian.
        ===========  =======================================

    In these cases, a long window is generated with a length of **L**.

    It is also possible to specify one of the window names from
    :func:`~ltfatpy.sigproc.firwin.firwin`. In such a case,
    :func:`~ltfatpy.gabor.gabwin.gabwin` will generate the specified FIR
    window with a length of **M**.

    The window can also be specified as a dictionary. The possibilities are:

        - {'name': 'gauss', 'tfr': 1.0, 'fs': 0.0, 'width': 0.0,
           'bw': 0.0, 'c_f': 0.0, 'centering': 'hp', 'delay': 0.0, 'norm': 2}:
           Additional parameters are passed to
           :func:`~ltfatpy.fourier.pgauss.pgauss`.
        - {'name': ('dual',...), ...}:
            Canonical dual window of whatever follows. See the examples below.
        - {'name': ('tight',...), ...}:
            Canonical tight window of whatever follows.

    It is also possible to specify one of the window names from
    :func:`~ltfatpy.sigproc.firwin.firwin` as a string. In this case, the
    remaining entries of the cell array are passed directly to
    :func:`~ltfatpy.sigproc.firwin.firwin`.

    - Some examples:

        To compute a Gaussian window of length **L** fitted for a system with
        time-shift **a** and **M** channels use::

            g = gabwin('gauss', a, M, L)[0]

        To compute Gaussian window with equal time and frequency support
        irrespective of **a** and **M**::

            g = gabwin({'name': 'gauss', 'tfr': 1}, a, M, L)[0]

        To compute the canonical dual of a Gaussian window fitted for a
        system with time-shift **a** and **M** channels::

            gd = gabwin('gaussdual', a, M, L)[0]

        To compute the canonical tight window of the Gaussian window fitted
        for the system::

            gd = gabwin({'name': ('tight','gauss')}, a, M, L)[0]

        To compute the dual of a Hann window of length 20::

            g = gabwin({'name': ('dual', 'hann'), 'M': 20}, a, M, L)[0]

    The returned **info** dictionary provides some information about the
    computed window:

    =========   ===========================================================
    keys        Values
    =========   ===========================================================
    'gauss'     True if the window is a Gaussian.
    'tfr'       Time/frequency support ratio of the window.
                Set whenever it makes sense.
    'wasrow'    True if input was a row window
    'isfir'     True if input is an FIR window
    'isdual'    True if output is the dual window of the auxiliary window.
    'istight'   True if output is known to be a tight window.
    'auxinfo'   Info about auxiliary window.
    'gl'        Length of window.
    =========   ===========================================================

    .. seealso:: :func:`~ltfatpy.fourier.pgauss.pgauss`,
        :func:`~ltfatpy.sigproc.firwin.firwin`, :func:`wilwin`
    """
    # Assert correct input.
    (g, info) = comp_window(g, a, M, L)
#     if info['isfir']:
#         if info['istight']:
#             # g = g / math.sqrt(2)
    return (g, info)
