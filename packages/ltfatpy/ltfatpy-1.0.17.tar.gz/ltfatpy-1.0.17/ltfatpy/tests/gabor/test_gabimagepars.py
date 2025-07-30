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


"""Test of the gabimagepars function

NOTE: Only the non-graphical features of gabimagepars are tested here

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest

from ltfatpy.gabor.gabimagepars import gabimagepars

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestGabimagepars(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestGabimagepars')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_working(self):
        """Check that gabimagepars is working as expected
        """
        in_val = ((10, 11, 12), (10, 5, 5), (100, 60, 18), (512, 64, 32))
        out_oct = ((1, 10, 10, 10, 10), (2, 5, 10, 5, 5), (3, 18, 108, 36, 34),
                   (8, 32, 512, 64, 64))
        inputs = {}
        for val, out_ref in zip(in_val, out_oct):
            inputs['Ls'] = val[0]
            inputs['x'] = val[1]
            inputs['y'] = val[2]
            out = gabimagepars(**inputs)
            msg = ('wrong output in gabimagepars with inputs ' + str(inputs))
            self.assertEqual(out_ref, out, msg)

        self.assertRaises(ValueError, gabimagepars, 100, 6, 13)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGabimagepars)
    unittest.TextTestRunner(verbosity=2).run(suite)
