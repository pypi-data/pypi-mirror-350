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


"""Test of the lcm function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.tools.lcm import lcm


class TestLcm(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestLcm')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_types(self):
        """Checking input and output types
        """
        # test with str input, when int is expected
        self.assertRaises(TypeError, lcm, 2, '1')
        # test with float input, when int is expected
        self.assertRaises(TypeError, lcm, 2., 1)
        # check output type (int expected)
        self.assertEqual(type(lcm(3, 5)), int, '\nOutput type should be int')

    def test_known(self):
        """Checking lcm on some known results taken from Octave
        """
        ref = ((30, 12, 60), (-20, 15, -60), (6, -9, -18), (-12, -9, 36),
               (0, 3, 0), (-12, 0, -0), (0, 0, 0))
        inputs = {}
        for X, Y, res in ref:
            inputs['X'] = X
            inputs['Y'] = Y
            msg = 'Wrong output of lcm with inputs ' + str(inputs)
            self.assertEqual(lcm(**inputs), res, msg)

    def test_symmetry(self):
        """Checking that lcm is symmetric
        """
        values = np.random.randint(-1000, 1000, (5,))
        for X in values:
            for Y in values:
                X = int(X)
                Y = int(Y)
                msg = ('lcm is not symetric with X = {0:d} and '
                       'Y = {1:d}'.format(X, Y))
                self.assertEqual(lcm(X, Y), lcm(Y, X), msg)

    def test_primes(self):
        """Checking lcm with prime numbers
        """
        primes = (2, 3, 5, 7, 11, 13, 17)
        inputs = {}
        for X in primes:
            for Y in primes:
                inputs['X'] = X
                inputs['Y'] = Y
                msg = 'Wrong output of lcm with prime inputs ' + str(inputs)
                if inputs['X'] == inputs['Y']:
                    self.assertEqual(lcm(**inputs), inputs['X'], msg)
                else:
                    self.assertEqual(lcm(**inputs),
                                     inputs['X']*inputs['Y'], msg)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLcm)
    unittest.TextTestRunner(verbosity=2).run(suite)
