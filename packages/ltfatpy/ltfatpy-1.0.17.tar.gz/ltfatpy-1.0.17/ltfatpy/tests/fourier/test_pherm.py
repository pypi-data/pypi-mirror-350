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


"""Test of the pherm function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np
from ltfatpy.fourier.pherm import pherm
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestPherm(unittest.TestCase):
    """ Unittest class for Fourier pherm"""
    def setUp(self):
        self.L = random.randint(10, 100)
        self.filename = get_dataset_path('pherm_ref.mat')

    def tearDown(self):
        print('Test done')

    def test_default(self):
        (g_r1, _) = pherm(self.L, 1)
        (g_r2, _) = pherm(self.L, 1, phase='accurate', orthtype='noorth')
        mess = "\nTest default values with L = " + str(self.L) + "\n"
        self.assertTrue(np.array_equal(g_r1, g_r2), mess)

    def test_exceptions(self):
        mess = "\nException TypeError should be raised with declaration "
        mess += "pherm((10, 2), 1)\n"
        self.assertRaises(TypeError, pherm, (10, 2), 1, mess)
        mess = "\nException TypeError should be raised with declaration "
        mess += "pherm(10.2, 1)\n"
        self.assertRaises(TypeError, pherm, 10.2, 1, mess)
        mess = "\nException TypeError should be raised with declaration "
        mess += "pherm(10, 1, (1,1))\n"
        self.assertRaises(TypeError, pherm, 10, 1, (1, 1))
        mess = "\nException TypeError should be raised with declaration "
        mess += "pherm(10, 'foo')\n"
        self.assertRaises(TypeError, pherm, 10, 'foo')

    def test_calc(self):
        data = read_ref_mat(self.filename)
        for inputs, outputs in data:
            out = pherm(**inputs)
            msg = ('Wrong output in pherm with inputs ' +
                   str(inputs))
            if inputs['orthtype'] == 'qr':
                np.testing.assert_array_almost_equal(np.abs(out[0]),
                                                     np.abs(outputs[0]), 6,
                                                     msg)
                np.testing.assert_array_almost_equal(out[1], outputs[1], 6,
                                                     msg)
            else:
                np.testing.assert_array_almost_equal(out[0], outputs[0], 6,
                                                     msg)
                np.testing.assert_array_almost_equal(out[1], outputs[1], 6,
                                                     msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPherm)
    unittest.TextTestRunner(verbosity=2).run(suite)
