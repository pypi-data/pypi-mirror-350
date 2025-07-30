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


"""Module of glockenspiel signal loading

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

from scipy.io.wavfile import read as wavread
import pkg_resources
import numpy as np


def gspi():
    """Load the 'glockenspiel' test signal

    - Usage:

        | ``(s, fs) = gspi()``

    - Output parameters:

    :returns: ``(s, fs)``
    :rtype: tuple

    :var numpy.ndarray s: 'glockenspiel' signal
    :var int fs: sampling frequency in Hz

    ``gspi`` loads the 'glockenspiel' signal. This is a recording of a simple
    tune played on a glockenspiel. It is 262144 samples long, mono, recorded
    at 44100 Hz using 16 bit quantization.

    This signal, and other similar audio tests signals, can be found on
    the EBU SQAM test signal CD http://tech.ebu.ch/publications/sqamcd.
    """

    f = pkg_resources.resource_stream(__name__, "gspi.wav")

    fs, s = wavread(f)
    s = s.astype(np.float64) / 2.**15.
    return (s, fs)
