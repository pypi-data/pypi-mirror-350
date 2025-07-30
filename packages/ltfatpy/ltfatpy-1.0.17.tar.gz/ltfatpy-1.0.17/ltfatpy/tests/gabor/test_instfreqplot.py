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


"""Test of the instfreqplot function

NOTE: Only the non-graphical features of instfreqplot are tested here

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_allclose

from ltfatpy.gabor.instfreqplot import instfreqplot
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestInstfreqplot(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestInstfreqplot')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        # coef must be a 1D numpy.ndarray, check that we get the right
        # exceptions if not
        self.assertRaises(TypeError, instfreqplot, 'test')
        self.assertRaises(TypeError, instfreqplot, 1)
        self.assertRaises(TypeError, instfreqplot, 1.)
        self.assertRaises(TypeError, instfreqplot, [0, 2])
        self.assertRaises(ValueError, instfreqplot, np.ones((4, 2)))

        # wrong values of xres and yres should lead to exceptions
        self.assertRaises(ValueError, instfreqplot, np.random.random((20, )),
                          xres=3, yres=3)
        self.assertRaises(TypeError, instfreqplot, np.random.random((20, )),
                          xres='a', yres=3)

    def test_working(self):
        """Check that instfreqplot is working as expected
        """
        filename = get_dataset_path('instfreqplot_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data:
            out = instfreqplot(**inputs)
            msg = ('Wrong value in output of instfreqplot with inputs ' +
                   str(inputs) +
                   '\nMaximal error: ' + str(np.max(np.abs(outputs[0] - out))))
            assert_allclose(out, outputs[0], atol=1e-13, err_msg=msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInstfreqplot)
    unittest.TextTestRunner(verbosity=2).run(suite)
