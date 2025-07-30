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


"""Test of the middlepad function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal
from copy import deepcopy

from ltfatpy.fourier.middlepad import middlepad


class TestMiddlepad(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestMiddlepad')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        f = np.random.random((3,))
        # L must be an integer, check that we get an error if not
        self.assertRaises(TypeError,  middlepad, f, 'test')
        self.assertRaises(TypeError,  middlepad, f, 3.4)

        # L must be larger than 0, check that we get an error if not
        self.assertRaises(ValueError,  middlepad, f, -2)

    def test_known(self):
        """Checking middlepad on some known results taken from Octave
        """
        inputs = {}
        N_val = (1, 1, 3, 4, 3, 4, 7, 8, 7, 8)
        L_val = (2, 3, 7, 7, 8, 8, 3, 3, 4, 4)
        centerings = ('wp', 'hp')

        # Values of h as returned in Octave with ltfat 2.1.0
        all_h_oct = ((np.array([1., 0.]),
                      np.array([1., 0., 0.]),
                      np.array([1., 2., 0., 0., 0., 0., 3.]),
                      np.array([1., 2., 1.5, 0., 0., 1.5, 4.]),
                      np.array([1., 2., 0., 0., 0., 0., 0., 3.]),
                      np.array([1., 2., 1.5, 0., 0., 0., 1.5, 4.]),
                      np.array([1., 2., 7.]),
                      np.array([1., 2., 8.]),
                      np.array([1., 2., 4.5, 7.]),
                      np.array([1., 2., 5., 8.])),
                     (np.array([0.5, 0.5]),
                      np.array([0.5, 0., 0.5]),
                      np.array([1., 1., 0., 0., 0., 1., 3.]),
                      np.array([1., 2., 0., 0., 0., 3., 4.]),
                      np.array([1., 1., 0., 0., 0., 0., 1., 3.]),
                      np.array([1., 2., 0., 0., 0., 0., 3., 4.]),
                      np.array([1., 4., 7.]),
                      np.array([1., 4.5, 8.]),
                      np.array([1., 2., 6., 7.]),
                      np.array([1., 2., 7., 8.])))

        for centering, h_oct in zip(centerings, all_h_oct):
            inputs['centering'] = centering
            for N, L, h_ref in zip(N_val, L_val, h_oct):
                inputs['L'] = L
                inputs['f'] = np.arange(1., float(N+1))
                h = middlepad(**inputs)
                msg = ('Wrong value in putput of middlepad with inputs ' +
                       str(inputs))
                assert_array_equal(h_ref, h, msg)

    def test_known_shapes(self):
        """Check that middlepad resturns the same shapes as in Octave
        """
        shapes_in = ((1, 1), (2, 1), (1, 2), (1, 2, 3), (1, 1, 2),
                     (1, 1, 2, 3))
        shapes_out = ((3, 1), (3, 1), (1, 3), (3, 2, 3), (1, 1, 3),
                      (3, 1, 2, 3))
        inputs = {}
        inputs['L'] = 3
        for shape_in, shape_out in zip(shapes_in, shapes_out):
            inputs['f'] = np.ones(shape_in)
            h = middlepad(**inputs)
            msg = ('Wrong shape in the output of middlepad with inputs ' +
                   str(inputs))
            self.assertEqual(shape_out, h.shape, msg)

    def test_default_val(self):
        """Check that expected default value is used
        """
        # check that default value for centering is 'wp'
        inputs_def = {}
        N = 3
        inputs_def['f'] = np.ones((N,))
        inputs_def['L'] = N+1
        h_def = middlepad(**inputs_def)
        inputs = deepcopy(inputs_def)
        inputs['centering'] = 'wp'
        h = middlepad(**inputs)
        msg = ('Wrong default value for centering when coparing inputs ' +
               str(inputs_def) + ' and ' + str(inputs))
        assert_array_equal(h_def, h, msg)

    def test_param_dim(self):
        """Check that dim is taken into account
        """
        inputs = {}
        N = 3
        M = 4
        inputs['L'] = 5
        inputs['f'] = np.ones((N, M))
        inputs['dim'] = 0
        h = middlepad(**inputs)
        msg = 'middlepad is misusing dim with inputs ' + str(inputs)
        self.assertEqual(h.shape, (inputs['L'], M), msg)
        inputs['dim'] = 1
        h = middlepad(**inputs)
        msg = 'middlepad is misusing dim with inputs ' + str(inputs)
        self.assertEqual(h.shape, (N, inputs['L']), msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiddlepad)
    unittest.TextTestRunner(verbosity=2).run(suite)
