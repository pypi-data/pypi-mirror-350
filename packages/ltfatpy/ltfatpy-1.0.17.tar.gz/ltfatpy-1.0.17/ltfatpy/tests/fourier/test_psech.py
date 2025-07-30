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


"""Test of the psech function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np
from numpy import linalg as LA
from math import sqrt
from ltfatpy.fourier.psech import psech


class TestPsech(unittest.TestCase):
    """ Unittest class for Fourier pgauss"""
    def setUp(self):
        self.L = random.randint(10, 100)

    def tearDown(self):
        print('Test done')

    def test_default(self):
        (g_r1, _) = psech(self.L)
        (g_r2, _) = psech(self.L, tfr=1, width=0.0, bw=0.0, c_f=0.0,
                          centering='wp', delay=0.0, norm='2')
        mess = "\nTest default values with L = " + str(self.L) + "\n"
        self.assertTrue(np.array_equal(g_r1, g_r2), mess)

    def test_exceptions(self):
        mess = "\nException TypeError should be raised with declaration "
        mess += "psech(10.2)\n"
        self.assertRaises(TypeError, psech, 10.2, mess)
        mess = "\nException TypeError should be raised with declaration "
        mess += "psech(10, s=(1,1))\n"
        self.assertRaises(TypeError, psech, 10, s=(1, 1))

    def test_invariance_property(self):
        g = psech(self.L)[0]
        gf = np.fft.fft(g)/sqrt(self.L)
        mess = "Test DFT invariance."
        self.assertAlmostEqual(LA.norm(g-gf), 0, 10, mess)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPsech)
    unittest.TextTestRunner(verbosity=2).run(suite)
