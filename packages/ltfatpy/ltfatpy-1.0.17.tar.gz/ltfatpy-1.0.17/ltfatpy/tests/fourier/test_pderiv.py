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


"""Test of the pderiv function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from copy import deepcopy

from ltfatpy.fourier.pderiv import pderiv
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestPderiv(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestPderiv')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        f = np.random.random((3,))
        # Possible values for difforder are: 2, 4, float('inf')
        self.assertRaises(ValueError,  pderiv, f, difforder=3)

    def test_shape(self):
        """Check that the output has the expected shape
        """
        shapes = ((7,), (7, 6), (7, 6, 5))
        difforders = (2, 4, float('inf'))
        inputs = {}
        for shape in shapes:
            inputs['f'] = np.random.random(shape)
            for dim in range(len(shape)):
                inputs['dim'] = dim
                for difforder in difforders:
                    inputs['difforder'] = difforder
                    fd = pderiv(**inputs)
                    msg = ('Wrong shape in the ouput of pderiv with '
                           'inputs ' + str(inputs))
                    self.assertEqual(fd.shape, shape, msg)

    def test_known(self):
        """Checking pderiv on some known results taken from Octave
        """
        filename = get_dataset_path('pderiv_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data[:-1]:
            fd = pderiv(**inputs)
            msg = ('Wrong value in output of pderiv with inputs ' +
                   str(inputs))
            assert_array_equal(fd, outputs[0], msg)

        inputs, outputs = data[-1]
        fd = pderiv(**inputs)
        msg = ('Wrong value in output of pderiv with inputs ' + str(inputs))
        assert_allclose(fd, outputs[0], rtol=1e-14, err_msg=msg)

    def test_param_dim(self):
        """Check that the parameter dim is taken into account
        """
        inputs_0 = {}
        tmp = np.random.random((5,))
        inputs_0['f'] = np.dot(tmp[:, np.newaxis], tmp[np.newaxis, :])
        inputs_1 = deepcopy(inputs_0)
        inputs_0['dim'] = 0
        inputs_1['dim'] = 1
        fd_0 = pderiv(**inputs_0)
        fd_1 = pderiv(**inputs_1)
        msg = ('Wrong use of dim in pderiv when comparing inputs ' +
               str(inputs_0) + ' and ' + str(inputs_1))
        assert_array_equal(fd_0, fd_1.T, msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPderiv)
    unittest.TextTestRunner(verbosity=2).run(suite)
