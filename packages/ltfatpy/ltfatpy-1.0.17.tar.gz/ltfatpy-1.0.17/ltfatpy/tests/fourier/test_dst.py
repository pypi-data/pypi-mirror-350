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


"""Test of the dsti, dstii, dstiii, dstiv functions

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np


from ltfatpy.fourier.dsti import dsti
from ltfatpy.fourier.dstii import dstii
from ltfatpy.fourier.dstiii import dstiii
from ltfatpy.fourier.dstiv import dstiv
from ltfatpy.tests.datasets.read_comp_dst_signal_ex_mat import DstSignals
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestDST(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        self.filename = get_dataset_path('comp_dst_signal_ex.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        """ Comparing results with Matlab generated ones
        """
        dgs = DstSignals(self.filename)
        (TYPE, SIGNAL, L, W, DST, dst_type) = dgs.read_next_signal()
        while TYPE != '':
            mess = "\n\nTYPE = " + TYPE + "\nL = " + str(L)
            mess += "\nW = " + str(W) + "\ndst_type = " + str(dst_type)
            mess += "\nSIGNAL =\n" + str(SIGNAL)
            mess += "\nDST\n" + str(DST)
            if dst_type == 1:
                pydst = dsti(SIGNAL)
            elif dst_type == 2:
                pydst = dstii(SIGNAL)
            elif dst_type == 3:
                pydst = dstiii(SIGNAL)
            elif dst_type == 4:
                pydst = dstiv(SIGNAL)
            else:
                self.assertTrue(False, "Error in test datas")
            mess += "\npydst = \n" + str(pydst)
            self.assertTrue(np.linalg.norm(pydst-DST) <= 1e-10, mess)
            (TYPE, SIGNAL, L, W, DST, dst_type) = dgs.read_next_signal()

    def test_limit(self):
        """ Some limit tests
        """
        f = np.random.random_sample((128))
        pydst = dsti(f, 1)
        np.testing.assert_equal(f[0], pydst, "L = 1")
        pydst = dstii(f, 1)
        np.testing.assert_array_equal(f[0], pydst, "L = 1")
        pydst = dstiii(f, 1)
        np.testing.assert_array_equal(f[0], pydst, "L = 1")
        pydst = dstiv(f, 1)
        np.testing.assert_array_equal(f[0], pydst, "L = 1")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDST)
    unittest.TextTestRunner(verbosity=2).run(suite)
