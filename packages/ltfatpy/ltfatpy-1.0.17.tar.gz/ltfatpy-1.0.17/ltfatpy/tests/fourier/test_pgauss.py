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


"""Test of the pgauss function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np
from numpy import linalg as LA
from math import sqrt
from ltfatpy.fourier import pgauss as pg


class TestFourierPgauss(unittest.TestCase):
    """ Unittest class for Fourier pgauss"""
    def setUp(self):
        self.L = random.randint(10, 100)

    def tearDown(self):
        print('Test done')

    def test_default(self):
        (g_r1, _) = pg.pgauss(self.L)
        (g_r2, _) = pg.pgauss(self.L, tfr=1, width=0.0, bw=0.0, c_f=0.0,
                              centering='wp', delay=0.0, norm='2')
        mess = "\nTest default values with L = " + str(self.L) + "\n"
        self.assertTrue(np.array_equal(g_r1, g_r2), mess)

    def test_centering(self):
        (g, _) = pg.pgauss(10, centering='hp')
        np.testing.assert_array_almost_equal(g[:5], g[:4:-1], 6)

    def test_options(self):
        np.testing.assert_array_almost_equal(pg.pgauss(10, bw=2.0)[0],
                                             pg.pgauss(10, tfr=0.1)[0], 6)
        np.testing.assert_array_almost_equal(pg.pgauss(10, width=2.0)[0],
                                             pg.pgauss(10, tfr=2/5.0)[0], 6)
        np.testing.assert_array_almost_equal(pg.pgauss(10, fs=2.0)[0],
                                             pg.pgauss(10)[0], 6)
        np.testing.assert_array_almost_equal(pg.pgauss(10, delay=1, fs=2.0)[0],
                                             pg.pgauss(10, delay=2)[0], 6)
        np.testing.assert_array_almost_equal(pg.pgauss(10, bw=1, fs=2.0)[0],
                                             pg.pgauss(10, tfr=0.4)[0], 6)
        np.testing.assert_array_almost_equal(pg.pgauss(10, fs=2.0,
                                                       width=2.0)[0],
                                             pg.pgauss(10, tfr=1.6)[0], 6)

    def test_exceptions(self):
        mess = "\nException TypeError should be raised with declaration "
        mess += "pgauss(10.2)\n"
        self.assertRaises(TypeError, pg.pgauss, 10.2, mess)
        mess = "\nException TypeError should be raised with declaration "
        mess += "pgauss(10,(1,1))\n"
        self.assertRaises(TypeError, pg.pgauss, 10, (1, 1))
        self.assertRaises(ValueError, pg.pgauss, 10, centering='foo')

    def test_gauss_property(self):
        g = pg.pgauss(self.L)[0]
        gf = np.fft.fft(g)/sqrt(self.L)
        mess = "Test that tfr=1 works."
        self.assertAlmostEqual(LA.norm(g-gf), 0, 10, mess)

    def test_dilatation_property(self):
        mess = "Test pgauss dilatation propertie."
        g = pg.pgauss(self.L, 7)[0]
        gf = np.fft.fft(pg.pgauss(self.L, 1/7)[0])/sqrt(self.L)
        self.assertAlmostEqual(LA.norm(g-gf), 0, 6, mess)

    def test_norm(self):
        mess = "Test pgauss norm."
        g = pg.pgauss(self.L)[0]
        self.assertAlmostEqual(LA.norm(g)-1, 0, 10, mess)

    def test_shift_property(self):
        mess = "Test that dft(freq shift) == time shift"
        g = pg.pgauss(self.L, delay=5)[0]
        gf = np.fft.fft(pg.pgauss(self.L, c_f=5)[0])/sqrt(self.L)
        self.assertAlmostEqual(LA.norm(g-gf), 0, 10, mess)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFourierPgauss)
    unittest.TextTestRunner(verbosity=2).run(suite)
