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


"""Test of the firkaiser function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
from numpy.testing import assert_allclose

from ltfatpy.sigproc.firkaiser import firkaiser
from ltfatpy.tests.datasets.read_ref_mat import read_ref_mat
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestFirkaiser(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestFirkaiser')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        L = 7
        # test with beta of wrong type (float is expected)
        self.assertRaises(TypeError, firkaiser, L, 'test')
        self.assertRaises(TypeError, firkaiser, L, [0.1, 0.2])
        self.assertRaises(TypeError, firkaiser, L, 7)

        """
        The following test is removed as long as the stype='derived'
        option is not implemented
        # L must be even when stype = 'derived'
        self.assertRaises(ValueError, firkaiser, L, 0.5, stype='derived')
        """

    def test_known(self):
        """Checking firkaiser on some known results taken from Octave
        """
        filename = get_dataset_path('firkaiser_ref.mat')
        data = read_ref_mat(filename)
        for inputs, outputs in data:
            """
            As long as the stype='derived' option is not implemented, we need
            to filter the tested values on the stype option
            """
            if inputs['stype'] == 'normal':
                inputs.pop('stype')
                out = firkaiser(**inputs)
                msg = ('Wrong value in output of firkaiser with inputs ' +
                       str(inputs))
                assert_allclose(out, outputs[0], rtol=1e-15, err_msg=msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFirkaiser)
    unittest.TextTestRunner(verbosity=2).run(suite)
