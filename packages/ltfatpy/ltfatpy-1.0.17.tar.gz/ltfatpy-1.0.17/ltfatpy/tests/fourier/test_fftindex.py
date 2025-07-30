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


"""Test of the fftindex function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal

from ltfatpy.fourier.fftindex import fftindex


class TestFftindex(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestFftindex')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_shape(self):
        """Check that the output has the expected shape
        """
        N_val = (13, 14, 31, 32)
        nyquistzero_val = (False, True)
        inputs = {}
        for N in N_val:
            inputs['N'] = N
            for nyquistzero in nyquistzero_val:
                inputs['nyquistzero'] = nyquistzero
                n = fftindex(**inputs)
                msg = ('Wrong shape in the ouput of fftindex with inputs ' +
                       str(inputs))
                self.assertEqual(n.shape, (inputs['N'],), msg)

    def test_known(self):
        """Checking fftindex on some known results taken from Octave
        """
        N_val = (5, 6)
        nyquistzero_val = (False, True)
        # Values of n as returned in Octave with ltfat 2.1.0
        n_oct = ((np.array([0, 1, 2, -2, -1]), np.array([0, 1, 2, -2, -1])),
                 (np.array([0, 1, 2, 3, -2, -1]),
                  np.array([0, 1, 2, 0, -2, -1])))
        inputs = {}
        for N, n_refs in zip(N_val, n_oct):
            inputs['N'] = N
            for nyquistzero, n_ref in zip(nyquistzero_val, n_refs):
                inputs['nyquistzero'] = nyquistzero
                msg = 'Wrong output of fftindex with inputs ' + str(inputs)
                assert_array_equal(fftindex(**inputs), n_ref, msg)

    def test_default_param(self):
        """Check that the default value for nyquistzero is right
        """
        inputs_def = {}
        inputs_def['N'] = 6
        inputs_false = {}
        inputs_false['N'] = inputs_def['N']
        inputs_false['nyquistzero'] = False
        n_def = fftindex(**inputs_def)
        n_false = fftindex(**inputs_false)
        msg = ('Wrong default value for nyquistzero in fftindex when '
               'comparing results with inputs ' + str(inputs_def) + ' and ' +
               str(inputs_false))
        assert_array_equal(n_def, n_false, msg)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFftindex)
    unittest.TextTestRunner(verbosity=2).run(suite)
