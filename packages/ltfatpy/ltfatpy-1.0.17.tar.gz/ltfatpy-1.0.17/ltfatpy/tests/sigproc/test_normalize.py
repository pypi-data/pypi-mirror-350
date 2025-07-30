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


"""Test of the normalize function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.sigproc.normalize import normalize


class TestSigprocNormalize(unittest.TestCase):
    """ Unittest class for Sigproc normalize"""
    digit = 9

    def setUp(self):
        pass

    def tearDown(self):
        print('Test done')

    def test_default(self):
        self.assertRaises(TypeError, normalize, np.arange(10), 10)
        self.assertRaises(TypeError, normalize, np.arange(10, dtype='i8'),
                          'wav')
        norm_names = {'1', 'area', '2', 'energy', 'inf', 'peak', 'rms', 's0'}
        fin = np.arange(10, dtype=float)
        for n in norm_names:
            f, fnorm = normalize(fin, n)
            np.testing.assert_array_almost_equal(f*fnorm, fin, 6, "f = " +
                                                 str(f) + "\nfnorm = " +
                                                 str(fnorm) + '\n' + n
                                                 )
        f, fnorm = normalize(fin, 'wav')
        np.testing.assert_array_almost_equal(f*fnorm / 0.99, fin, 6, "f = " +
                                             str(f) + "\nfnorm = " +
                                             str(fnorm) + '\nwav')
        f1, fn1 = normalize(fin)
        f2, fn2 = normalize(fin, '2')
        np.testing.assert_array_equal(f1, f2)
        self.assertEqual(fn1, fn2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSigprocNormalize)
    unittest.TextTestRunner(verbosity=2).run(suite)
