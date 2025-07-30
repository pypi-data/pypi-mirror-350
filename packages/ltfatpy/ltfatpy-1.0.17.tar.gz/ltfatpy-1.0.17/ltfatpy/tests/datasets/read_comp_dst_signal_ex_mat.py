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


"""Read .mat data files generated with the Matlab version of Ltfat and
containing signals, dst from comp_dst for validations.

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import scipy.io


class DstSignals:
    """This class opens the file and provides :func:`read_next_signal`
    method for reading each (type, signal, L, W, dst, dst_type) tuples
    contained in the file.
    """

    def __init__(self, filename):
        """Constructor

        - Input parameter:

        :param str filename: Name of the matlab data file
        """
        self.Data = scipy.io.loadmat(filename, struct_as_record=False,
                                     squeeze_me=True)['Data']
        self.ind = 0
        self.size = self.Data.shape[0]

    def read_next_signal(self):
        """Read the next signal of the file.

        - Usage:

            | :literal:`(type, signal, L, W, dst, dst_type) =
            |                        dstSignals("file.mat").read_next_signal()`

        - Output parameters:

        :returns:
            :literal:`(type, signal, L, W, dst, dst_type)`

            Empty strings if all signals have been read.
        """
        if(self.ind >= self.size):
            return ('', '', '', '', '', '')

        TYPE = str(self.Data[self.ind].rname)
        L = self.Data[self.ind].L
        W = self.Data[self.ind].W
        dst_type = self.Data[self.ind].dst_type
        SIGNAL = self.Data[self.ind].f
        DST = self.Data[self.ind].cc
        self.ind += 1
        return (TYPE, SIGNAL, L, W, DST, dst_type)
