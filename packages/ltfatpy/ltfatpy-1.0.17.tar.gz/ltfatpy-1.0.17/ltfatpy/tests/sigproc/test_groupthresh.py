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


"""Test of the groupthresh function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal
from copy import deepcopy

from ltfatpy.sigproc.groupthresh import groupthresh
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestGroupthresh(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestGroupthresh')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_known(self):
        """Checking groupthresh on some known results taken from Octave
        """
        filename = get_dataset_path('groupthresh_ref.mat')
        data = read_ref_mat(filename)
        for inputs, outputs in data:
            # lamb is incorreclty converted to an int for certain values by
            # read_ref_mat, so we convert it back to float as needed by
            # groupthresh
            inputs['lamb'] = float(inputs['lamb'])
            out = groupthresh(**inputs)
            msg = ('Wrong value in output of groupthresh with inputs ' +
                   str(inputs))
            assert_array_equal(out, outputs[0], msg)

    def test_shape(self):
        """Check that input and output shapes match
        """
        shape = (4, 3)
        thresh_types = ('hard', 'wiener', 'soft')
        group_types = ('group', 'elite')
        dims = (0, 1)
        inputs = {}
        inputs['xi'] = np.random.random(shape)
        inputs['lamb'] = 0.5
        for dim in dims:
            inputs['dim'] = dim
            for group_type in group_types:
                inputs['group_type'] = group_type
                for thresh_type in thresh_types:
                    inputs['thresh_type'] = thresh_type
                    xo = groupthresh(**inputs)
                    msg = ('Wrong shape in output xo of groupthresh with '
                           'inputs ' + str(inputs))
                    self.assertEqual(xo.shape, shape, msg)

    def test_default_param(self):
        """Check that the default value for thresh_type is right
        """
        inputs_def = {}
        inputs_def['xi'] = np.random.random((4, 3))
        inputs_def['lamb'] = 0.5
        xo_def = groupthresh(**inputs_def)

        inputs_group = deepcopy(inputs_def)
        inputs_group['dim'] = 1
        xo_group = groupthresh(**inputs_group)
        msg = ('Wrong default value for dim in groupthresh when '
               'comparing results with inputs ' + str(inputs_def) + ' and ' +
               str(inputs_group))
        assert_array_equal(xo_def, xo_group, msg)

        inputs_group = deepcopy(inputs_def)
        inputs_group['group_type'] = 'group'
        xo_group = groupthresh(**inputs_group)
        msg = ('Wrong default value for group_type in groupthresh when '
               'comparing results with inputs ' + str(inputs_def) + ' and ' +
               str(inputs_group))
        assert_array_equal(xo_def, xo_group, msg)

        inputs_hard = deepcopy(inputs_def)
        inputs_hard['thresh_type'] = 'soft'
        xo_hard = groupthresh(**inputs_hard)
        msg = ('Wrong default value for thresh_type in groupthresh when '
               'comparing results with inputs ' + str(inputs_def) + ' and ' +
               str(inputs_hard))
        assert_array_equal(xo_def, xo_hard, msg)

    def test_type(self):
        """Check that the type for lamb is correctly checked
        """
        xi = np.ones((4, 3))
        # test with lamb of wrong type (str, when float is expected)
        lamb = 'test'
        self.assertRaises(TypeError, groupthresh, xi, lamb)
        # test with lamb of wrong type (int, when float is expected)
        lamb = 1
        self.assertRaises(TypeError, groupthresh, xi, lamb)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroupthresh)
    unittest.TextTestRunner(verbosity=2).run(suite)
