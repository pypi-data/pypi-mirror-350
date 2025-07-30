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


"""Test of the comp_hermite function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np
from ltfatpy.comp.comp_hermite import comp_hermite
# import matplotlib.pyplot as plt


class TestCompHermite(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        self.x = np.arange(10)

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        y = comp_hermite(0, self.x)
        yres = np.array([7.51125544e-01, 4.55580672e-01, 1.01653788e-01,
                         8.34425107e-03, 2.51974549e-04, 2.79918439e-06,
                         1.14396268e-08, 1.71987833e-11, 9.51237824e-15,
                         1.93546809e-18])
        np.testing.assert_array_almost_equal(y, yres, 6)

        y = comp_hermite(1, self.x)
        yres = np.array([0.00000000e+00, 6.44288365e-01, 2.87520332e-01,
                         3.54016591e-02, 1.42538330e-03, 1.97932227e-05,
                         9.70684525e-08, 1.70259268e-10, 1.07620275e-13,
                         2.46344870e-17])
        np.testing.assert_array_almost_equal(y, yres, 6)

        y = comp_hermite(2, self.x)
        yres = np.array([-5.31125966e-01, 3.22144183e-01, 5.03160581e-01,
                         1.00304701e-01, 5.52336028e-03, 9.69867910e-05,
                         5.74321677e-07, 1.17965350e-09, 8.54235929e-13,
                         2.20341800e-16])
        np.testing.assert_array_almost_equal(y, yres, 6)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCompHermite)
    unittest.TextTestRunner(verbosity=2).run(suite)
