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


"""Test of the gabphasegrad function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
from six import text_type
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

from ltfatpy.gabor.gabphasegrad import gabphasegrad
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestGabphasegrad(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestGabphasegrad')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        # method should be a string containing either 'dgt' or 'phase' or 'abs'
        self.assertRaises(TypeError, gabphasegrad, 1)
        self.assertRaises(TypeError, gabphasegrad, 1.0)
        self.assertRaises(TypeError, gabphasegrad, (1, 2))
        self.assertRaises(ValueError, gabphasegrad, 'test')

        # check that passing a wrong L with method 'dgt' raises an exception
        f = np.random.random((8,))
        g = 'gauss'
        a = 2
        M = 4
        self.assertRaises(ValueError, gabphasegrad, 'dgt', f, g, a, M, L=3)

        # check that passing a too long window g with method 'dgt' raises an
        # exception
        g = np.ones(9)
        self.assertRaises(ValueError, gabphasegrad, 'dgt', f, g, a, M)
        g = np.ones(5)
        self.assertRaises(ValueError, gabphasegrad, 'dgt', f, g, a, M, L=4)

        # check that passing complex values instead of real phase values with
        # method 'phase' raises an exception
        shape = (3, 2)
        cphase = np.random.random(shape) + 1.0j*np.random.random(shape)
        self.assertRaises(TypeError, gabphasegrad, 'phase', cphase, a)

        # check that passing negative values when an absolute value is
        # expected with method 'abs' raises an exception
        s = - np.random.random(shape)
        g = 'gauss'
        self.assertRaises(ValueError, gabphasegrad, 'abs', s, g, a)

        # check that passing a non-gaussian window g with method 'abs' raises
        # an exception
        s = np.random.random(shape)
        g = np.ones(4)
        self.assertRaises(ValueError, gabphasegrad, 'abs', s, g, a)

    def test_known(self):
        """Check gabphasegrad on some known results taken from Octave
        """
        filename = get_dataset_path('gabphasegrad_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data:
            method = str(inputs['method'])
            if method == 'dgt':
                f, g, a, M = (inputs[var] for var in ('f', 'g', 'a', 'M'))
                kwargs = dict()
                if 'L' in inputs:
                    kwargs['L'] = inputs['L']
                if 'minlvl' in inputs:
                    kwargs['minlvl'] = inputs['minlvl']
                if isinstance(g, text_type):
                    # force g to be str instead of unicode under Python 2
                    g = str(g)
                tgrad, fgrad, c = gabphasegrad(method, f, g, a, M, **kwargs)
                msg = 'wrong output in gabphasegrad with inputs ' + str(inputs)
                assert_allclose(tgrad, outputs[0], rtol=4e-15, err_msg=msg)
                assert_allclose(fgrad, outputs[1], rtol=1e-15, err_msg=msg)
                assert_allclose(c, outputs[2], rtol=1e-15, err_msg=msg)
            elif method == 'phase':
                cphase, a = (inputs[var] for var in ('cphase', 'a'))
                tgrad, fgrad = gabphasegrad(method, cphase, a)
                msg = 'wrong output in gabphasegrad with inputs ' + str(inputs)
                assert_array_equal(tgrad, outputs[0], msg)
                assert_array_equal(fgrad, outputs[1], msg)
            elif method == 'abs':
                s, g, a = (inputs[var] for var in ('s', 'g', 'a'))
                kwargs = dict()
                if 'difforder' in inputs:
                    kwargs['difforder'] = inputs['difforder']
                if isinstance(g, text_type):
                    # force g to be str instead of unicode under Python 2
                    g = str(g)
                tgrad, fgrad = gabphasegrad(method, s, g, a, **kwargs)
                msg = 'wrong output in gabphasegrad with inputs ' + str(inputs)
                assert_array_equal(tgrad, outputs[0], msg)
                assert_array_equal(fgrad, outputs[1], msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGabphasegrad)
    unittest.TextTestRunner(verbosity=2).run(suite)
