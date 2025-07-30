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


"""Test of the largestr function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal
from copy import deepcopy

from ltfatpy.sigproc.largestr import largestr
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestLargestr(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestLargestr')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_known(self):
        """Checking largestr on some known results taken from Octave
        """
        filename = get_dataset_path('largestr_ref.mat')
        data = read_ref_mat(filename)
        for inputs, outputs in data:
            xo, Nout = largestr(**inputs)
            msg = ('Wrong value in output xo of largestr with inputs ' +
                   str(inputs))
            assert_array_equal(xo, outputs[0], msg)
            msg = ('Wrong value in output Nout of largestr with inputs ' +
                   str(inputs))
            self.assertEqual(Nout, outputs[1], msg)

    def test_shape(self):
        """Check that input and output shapes match
        """
        shapes = ((4,), (4, 3), (4, 3, 2))
        thresh_types = ('hard', 'wiener', 'soft')
        inputs = {}
        inputs['p'] = 0.5
        for shape in shapes:
            inputs['xi'] = np.random.random(shape)
            for thresh_type in thresh_types:
                inputs['thresh_type'] = thresh_type
                xo = largestr(**inputs)[0]
                msg = ('Wrong shape in output xo of largestr with inputs ' +
                       str(inputs))
                self.assertEqual(xo.shape, shape, msg)

    def test_default_param(self):
        """Check that the default value for thresh_type is right
        """
        inputs_def = {}
        inputs_def['xi'] = np.random.random((4, 3))
        inputs_def['p'] = 0.5
        inputs_hard = deepcopy(inputs_def)
        inputs_hard['thresh_type'] = 'hard'
        xo_def = largestr(**inputs_def)[0]
        xo_hard = largestr(**inputs_hard)[0]
        msg = ('Wrong default value for thresh_type in largestr when '
               'comparing results with inputs ' + str(inputs_def) + ' and ' +
               str(inputs_hard))
        assert_array_equal(xo_def, xo_hard, msg)

    def test_type(self):
        """Check that the type for p is correctly checked
        """
        xi = np.ones((4, 3))
        # test with p of wrong type (str, when float is expected)
        p = 'test'
        self.assertRaises(TypeError, largestr, xi, p)
        # test with p of wrong type (int, when float is expected)
        p = 1
        self.assertRaises(TypeError, largestr, xi, p)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLargestr)
    unittest.TextTestRunner(verbosity=2).run(suite)
