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


"""Test of the gabtight function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np
# from math import *
# import matplotlib.pyplot as plt
# from fractions import gcd

from ltfatpy.gabor.gabtight import gabtight
from ltfatpy.tests.datasets.read_gabtight_signal_ex_mat import GabTightExamples
from ltfatpy.fourier.pgauss import pgauss
from ltfatpy.fourier.psech import psech
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestGabTight(unittest.TestCase):
    # Called before the tests.
    def setUp(self):
        self.filename = get_dataset_path('gabtight_signal_ex.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        """ Comparing results with Matlab generated ones
        """
        pass
        dgs = GabTightExamples(self.filename)
        (L, a, M, rname, G, GT) = dgs.read_next_frame()
        while L != '':
            mess = "\nL = " + str(L) + "\na = " + str(a)
            mess += "\nM = " + str(M) + "\nrname = " + str(rname)
            mess += "\nG = " + str(G) + "\nGT = " + str(GT)
            t = gabtight(G, a, M, L)
            mess += "\ngt = " + str(t)
            self.assertTrue(np.linalg.norm(t-GT) <= 1e-10, mess)
            (L, a, M, rname, G, GT) = dgs.read_next_frame()

    def test_properties(self):
        self.assertRaises(ValueError, gabtight, "Gauss", 6, 8, 16)
        a = 10
        M = 40
        L = 160
        g = pgauss(L)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        np.testing.assert_array_equal(gabtight(g, a, M), gabtight(g, a, M, L),
                                      mess)
        a = 20
        M = 49
        gt = gabtight("Gauss", a, M)
        L = gt.shape[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        np.testing.assert_array_almost_equal(gt, gabtight(None, a, M, L), 10,
                                             mess)
        g = pgauss(L)[0]
        gt = gabtight(g.reshape(L//2, 2), a, M)
        self.assertEqual(gt.shape, (L, 2))
        M = 10
        gt = gabtight("Gauss", a, M)
        self.assertEqual(gt.shape, (a,))
        gt1 = gabtight('sech', a, M)
        L = gt.shape[0]
        g = psech(L, a*M/L)[0]
        gt2 = gabtight(g, a, M)
        mess = "a = {0:d}, M = {1:d}".format(a, M)
        np.testing.assert_array_almost_equal(gt1, gt2, 10, mess)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGabTight)
    unittest.TextTestRunner(verbosity=2).run(suite)
