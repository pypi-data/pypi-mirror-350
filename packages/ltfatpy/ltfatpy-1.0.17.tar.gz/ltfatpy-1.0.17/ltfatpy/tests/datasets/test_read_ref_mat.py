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


"""Test of the read_ref_mat function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
import numpy as np
from numpy.testing import assert_array_equal
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestReadRefMat(unittest.TestCase):
    """ Test read_ref_mat.py """

    # Called before the tests.
    def setUp(self):
        print('\nTestReadRefMat')
        self.filename = get_dataset_path('read_ref_mat_test.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        """Test read_ref_mat on some known data
        """

        expected = [({u'fun': u'abs', u'dim': 1, u'var': 1.3},
                     [np.array([3., 2.2]), 1.5]),
                    ({u'fun': u'dgt', u'do_it': True}, [np.array([1.4, 1.2])])]

        res = read_ref_mat(self.filename)

        # NOTE: We would like to compare res and expected, but as they contain
        # some numpy.ndarray, they cannot be direclty compared using == or
        # assertEqual (this leads to the ValueError:
        # The truth value of an array with more than one element is ambiguous.
        # Use a.any() or a.all())
        # So we need to manually loop to compare the results:
        msg = 'Wrong output of read_ref_mat on reference test data'
        self.assertEqual(len(expected), len(res), msg)
        for (in_exp, out_exp), (in_res, out_res) in zip(expected, res):
            self.assertEqual(in_exp, in_res, msg)
            self.assertEqual(len(out_exp), len(out_res), msg)
            for val_exp, val_res in zip(out_exp, out_res):
                if isinstance(val_exp, np.ndarray):
                    assert_array_equal(val_exp, val_res, msg)
                else:
                    self.assertEqual(val_exp, val_res, msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReadRefMat)
    unittest.TextTestRunner(verbosity=2).run(suite)
