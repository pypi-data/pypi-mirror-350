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


""" Module of gabpars_from_windowsignal calculation

Ported from ltfat_2.1.0/comp/gabpars_from_windowsignal.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

from ltfatpy.comp.comp_sigreshape_pre import comp_sigreshape_pre
from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.gabor.gabwin import gabwin
from ltfatpy.tools.postpad import postpad


def gabpars_from_windowsignal(f, g, a, M, L=None):
    """Compute g and L from window and signal

    - Usage:

        | ``(g, info, L) = gabpars_from_windowsignal(f, g, a, M, L)``

    Use this function if you know an input signal and a window
    for the DGT. The function will calculate a transform length L and
    evaluate the window g into numerical form. The signal will be padded and
    returned as a column vector.

    If the transform length is unknown (as it usually is unless explicitly
    specified by the user), set L to be None in the input to this function.
    """
    # Verify f and determine its length
    # Change f to correct shape.
    (f, Ls, W, unused_wasrow, unused_remembershape) = comp_sigreshape_pre(f, 0)

    if L is None:
        # Verify a, M and get L from the signal length f
        L = dgtlength(Ls, a, M)
    else:
        # Verify a, M and get L
        Luser = dgtlength(L, a, M)
        if Luser != L:
            raise ValueError('Incorrect transform length L={0:d} specified.' +
                             'Next valid length is L={1:d}.'.format(L, Luser))

    # Determine the window
    (g, info) = gabwin(g, a, M, L)

    if L < info['gl']:
        raise ValueError('Window is too long.')

    # final cleanup
    f = postpad(f, L)

    # If the signal is single precision, make the window single precision as
    # well to avoid mismatches.
    # if isa(f,'single')
    # g=single(g);
    # end;
    return (f, g, L, Ls, W, info)
