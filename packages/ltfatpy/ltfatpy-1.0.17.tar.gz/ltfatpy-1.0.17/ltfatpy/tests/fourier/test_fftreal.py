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


"""Test of the fftreal function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_allclose

from ltfatpy.fourier.fftreal import fftreal
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestFftreal(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestFftreal')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_shape(self):
        """Check that the output has the expected shape
        """
        shapes = ((4,), (4, 3), (4, 3, 2))
        N_val = (2, 3, 6, 7)
        inputs = {}
        for shape in shapes:
            inputs['f'] = np.random.random(shape)
            for dim in range(len(shape)):
                inputs['dim'] = dim
                for N in N_val:
                    inputs['N'] = N
                    c = fftreal(**inputs)
                    expected_shape = list(shape)
                    expected_shape[dim] = int(np.ceil((N+1.)/2.))
                    expected_shape = tuple(expected_shape)
                    msg = ('Wrong shape in the ouput of fftreal with inputs ' +
                           str(inputs))
                    self.assertEqual(c.shape, expected_shape, msg)

    def test_known(self):
        """Checking fftreal on some known results taken from Octave
        """
        filename = get_dataset_path('fftreal_ref.mat')
        data = read_ref_mat(filename)

        for inputs, outputs in data:
            h = fftreal(**inputs)
            msg = ('Wrong value in output of fftreal with inputs ' +
                   str(inputs))
            assert_allclose(h, outputs[0], rtol=5e-13, err_msg=msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFftreal)
    unittest.TextTestRunner(verbosity=2).run(suite)
