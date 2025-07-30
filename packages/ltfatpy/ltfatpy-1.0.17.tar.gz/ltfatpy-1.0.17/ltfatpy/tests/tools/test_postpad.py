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


"""Test of the postpad function

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.tools.postpad import postpad


class TestPostpad(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestPostpad')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_working(self):
        """Check that postpad works as expected
        """
        inputs = {}
        N = 5
        inputs['x'] = np.arange(N, dtype=float)

        # testing padding
        inputs['L'] = 10
        y = postpad(**inputs)
        msg = ('Wrong shape in postpad output in the padding case using '
               'inputs ' + str(inputs))
        self.assertEqual(y.shape, (inputs['L'],), msg)
        for val_x, val_y in zip(inputs['x'], y[:N]):
            msg = ('Wrong output value in postpad, y should be equal to x in '
                   'the non-padded part. Inputs are ' + str(inputs))
            self.assertEqual(val_x, val_y, msg)
        for val in y[N:]:
            msg = ('Wrong output value in postpad, y should be equal to 0. in '
                   'the padded part. Inputs are ' + str(inputs))
            self.assertEqual(val, 0., msg)

        # testing truncation
        inputs['L'] = 3
        y = postpad(**inputs)
        msg = ('Wrong shape in postpad output in the truncation case using '
               'inputs ' + str(inputs))
        self.assertEqual(y.shape, (inputs['L'],), msg)
        for val_x, val_y in zip(inputs['x'][:inputs['L']], y):
            msg = ('Wrong output value in postpad, y should be equal to x in '
                   'the non-truncated part. Inputs are ' + str(inputs))
            self.assertEqual(val_x, val_y, msg)

    def test_default_val(self):
        """Check that expected default values are used
        """
        # check that default value for C is 0.
        inputs = {}
        N = 3
        inputs['x'] = np.ones(N)
        inputs['L'] = N+1
        y = postpad(**inputs)
        msg = 'Wrong default value for C using inputs ' + str(inputs)
        self.assertEqual(y[-1], 0., )

        # check that default dim is the first non-singleton dimension
        N = 3
        inputs['L'] = N+1
        x_shape = (1, 1, N, 5)
        inputs['x'] = np.ones(x_shape)
        y = postpad(**inputs)
        y_exp_shape = (1, 1, inputs['L'], 5)
        msg = 'Wrong default value for dim using inputs ' + str(inputs)
        self.assertEqual(y.shape, y_exp_shape, msg)

    def test_param_C(self):
        """Check that the value of C is taken into account
        """
        inputs = {}
        N = 3
        inputs['C'] = 2.
        inputs['x'] = np.ones(N)
        inputs['L'] = N+1
        y = postpad(**inputs)
        msg = 'Postpad is misusing C with inputs ' + str(inputs)
        self.assertEqual(y[-1], inputs['C'], msg)

    def test_param_dim(self):
        """Check that dim is taken into account
        """
        inputs = {}
        N = 3
        M = 4
        inputs['L'] = 5
        inputs['x'] = np.ones((N, M))
        inputs['dim'] = 0
        y = postpad(**inputs)
        msg = 'postpad is misusing dim with inputs ' + str(inputs)
        self.assertEqual(y.shape, (inputs['L'], M), msg)
        inputs['dim'] = 1
        y = postpad(**inputs)
        msg = 'postpad is misusing dim with inputs ' + str(inputs)
        self.assertEqual(y.shape, (N, inputs['L']), msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPostpad)
    unittest.TextTestRunner(verbosity=2).run(suite)
