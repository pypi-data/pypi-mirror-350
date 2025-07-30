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


"""Test of the comp_gabdual_long function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.comp.comp_gabdual_long import comp_gabdual_long


class TestCompGabDual(unittest.TestCase):
    # Called before the tests.
    def setUp(self):
        pass

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        # g should be float64 or complex128
        g = np.arange(9)
        mess = "g data should be numpy.float64 or numpy.complex128"
        try:
            assertRaisesRegex = self.assertRaisesRegex
        except AttributeError:
            assertRaisesRegex = self.assertRaisesRegexp

        # I checked that the command comp_gabdual_long(g, 0, 0) raises a
        # TypeError with the correct message -- Still complaining with NULL
        # being returned
        assertRaisesRegex(TypeError, mess, comp_gabdual_long, g, 0, 0)
        g = g.astype(np.float64)
        # g dim should be < 3
        mess = "g dimensions should be 1 or 2."
        # Same as above -- Is that a change of behaviour of assertRaisesRegex?
        assertRaisesRegex(
            TypeError, mess, comp_gabdual_long, g.reshape((3, 1, 3)), 0, 0)
        # basic test:
        g.resize((3, 3))
        gd = comp_gabdual_long(g, 1, 1)
        self.assertEqual(gd.shape, (3, 3), "Bad output dimensions")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCompGabDual)
    unittest.TextTestRunner(verbosity=2).run(suite)
