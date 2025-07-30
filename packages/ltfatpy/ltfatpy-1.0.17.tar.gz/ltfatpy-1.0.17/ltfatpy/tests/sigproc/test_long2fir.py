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


"""Test of the long2fir function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.sigproc.long2fir import long2fir


class TestSigprocLong2fir(unittest.TestCase):
    """ Unittest class for Sigproc long2fir"""
    digit = 9

    def setUp(self):
        pass

    def tearDown(self):
        print('Test done')

    def test_default(self):
        self.assertRaises(TypeError, long2fir, "foo", 10)
        self.assertRaises(ValueError, long2fir, np.ones(10), None)
        self.assertRaises(ValueError, long2fir, np.ones(10), 15)
        self.assertRaises(ValueError, long2fir, np.ones(10), 5,
                          centering='foo')

        gin = np.arange(20, dtype='f4')

        g = long2fir(gin, 10)
        np.testing.assert_array_equal(g, np.hstack((np.arange(5),
                                                    np.arange(15, 20))))
        g = long2fir(gin, 11)
        np.testing.assert_array_equal(g, np.hstack((np.arange(6),
                                                    np.arange(15, 20))))
        g = long2fir(gin, 10, centering='wp')
        np.testing.assert_array_equal(g, np.hstack((np.arange(5),
                                                    np.array([0]),
                                                    np.arange(16, 20))))
        g = long2fir(gin, 11, centering='hp')
        np.testing.assert_array_equal(g, np.hstack((np.arange(5),
                                                    np.array([0]),
                                                    np.arange(15, 20))))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSigprocLong2fir)
    unittest.TextTestRunner(verbosity=2).run(suite)
