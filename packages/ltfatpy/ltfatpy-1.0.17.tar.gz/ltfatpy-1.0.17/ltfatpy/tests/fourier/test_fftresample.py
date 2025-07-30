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


"""Test of the fftresample function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_allclose

from ltfatpy.fourier.fftresample import fftresample
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestFftresample(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestFftresample')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_shape(self):
        """Check that the output has the expected shape
        """
        shapes = ((4,), (4, 3), (4, 3, 2))
        L_val = (2, 3, 6, 7)
        data_types = ('real', 'complex')
        inputs = {}
        for shape in shapes:
            for data_type in data_types:
                if data_type == 'real':
                    inputs['f'] = np.random.random(shape)
                elif data_type == 'complex':
                    inputs['f'] = (np.random.random(shape) +
                                   1.0j * np.random.random(shape))
                for dim in range(len(shape)):
                    inputs['dim'] = dim
                    for L in L_val:
                        inputs['L'] = L
                        h = fftresample(**inputs)
                        expected_shape = list(shape)
                        expected_shape[dim] = L
                        expected_shape = tuple(expected_shape)
                        msg = ('Wrong shape in the ouput of fftresample with '
                               'inputs ' + str(inputs))
                        self.assertEqual(h.shape, expected_shape, msg)

    def test_same_length(self):
        """Check that the data are unchanged when using the original length
        """
        shape = (16, 17)
        inputs = {}
        data_types = ('real', 'complex')
        for data_type in data_types:
            if data_type == 'real':
                inputs['f'] = np.random.random(shape)
            elif data_type == 'complex':
                inputs['f'] = (np.random.random(shape) +
                               1.0j * np.random.random(shape))
            for dim in range(len(shape)):
                inputs['dim'] = dim
                inputs['L'] = shape[dim]
                h = fftresample(**inputs)
                msg = ('Input and output should be almost equal when '
                       'resampling to the same length in fftresample with '
                       'inputs ' + str(inputs))
                assert_allclose(inputs['f'], h, rtol=1e-12, atol=1e-14,
                                err_msg=msg)

    def test_known(self):
        """Checking fftresample on some known results taken from Octave
        """
        filename = get_dataset_path('fftresample_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data:
            h = fftresample(**inputs)
            msg = ('Wrong value in output of fftresample with inputs ' +
                   str(inputs))
            assert_allclose(h, outputs[0], rtol=1e-14, err_msg=msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFftresample)
    unittest.TextTestRunner(verbosity=2).run(suite)
