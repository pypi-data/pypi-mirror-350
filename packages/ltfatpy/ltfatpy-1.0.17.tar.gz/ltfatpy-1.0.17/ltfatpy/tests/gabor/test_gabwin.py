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


"""Test of the gabwin function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np

# from math import *
# import matplotlib.pyplot as plt
# from fractions import gcd

from ltfatpy.gabor.gabwin import gabwin
from ltfatpy.fourier.pgauss import pgauss
from ltfatpy.fourier.psech import psech
from ltfatpy.gabor.gabdual import gabdual
from ltfatpy.gabor.gabtight import gabtight
from ltfatpy.sigproc.firwin import firwin
from ltfatpy.gabor.dgtlength import dgtlength
from ltfatpy.comp.arg_firwin import arg_firwin
from ltfatpy.fourier import isevenfunction as ie
from ltfatpy.sigproc.fir2long import fir2long
from ltfatpy.tools.lcm import lcm


class TestGabWin(unittest.TestCase):
    # Called before the tests.
    def setUp(self):
        pass

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        a = 10
        M = 40
        self.assertRaises(ValueError, gabwin, "gauss", a, M)
        L = 160
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin("gauss", a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertTrue(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = pgauss(L, a*M/L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

    def test_str_entries(self):
        a = random.randint(10, 40)
        M = random.randint(10, 40)
        L = M * random.randint(2, 5)

        # psech
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin("psech", a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = psech(L, a*M/L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, "sech", a, M)

        # dualgauss
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin("dualgauss", a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertTrue(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = gabdual(pgauss(L, a*M/L)[0], a, M)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, "gaussdual", a, M)

        # tight
        L = dgtlength(L, a, M)
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin("tight", a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertTrue(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = gabtight(None, a, M, L)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, "tight", a, M)

        # firwin
        name = random.sample(arg_firwin(), 1)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        (g, info) = gabwin(name, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        if name in {'sine', 'cosine', 'sqrthann', 'sqrttria', 'itersine',
                    'ogg'}:
            self.assertTrue(info['istight'], mess)
        else:
            self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertTrue(info['isfir'], mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = firwin(name, M, norm='2')[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

        # Unknown
        self.assertRaises(ValueError, gabwin, "foo", a, M, L)

    def test_simple_dictionnaries_entries(self):
        a = random.randint(10, 40)
        M = random.randint(10, 40)
        L = M * random.randint(2, 5)

        # default
        self.assertRaises(ValueError, gabwin, {'a': 1}, a, M, L)

        # pgauss without tfr
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin({'name': 'pgauss'}, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertTrue(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = pgauss(L, a*M/L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, {'name': 'pgauss'}, a, M)
        # pgauss with tfr specified
        (g, info) = gabwin({'name': 'pgauss', 'tfr': 1}, a, M, L)
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertEqual(info["tfr"], 1, mess)
        gt = pgauss(L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

        # psech without tfr
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin({'name': 'psech'}, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["tfr"], a*M/L, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = psech(L, a*M/L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, {'name': 'sech'}, a, M)
        # psech with tfr specified
        (g, info) = gabwin({'name': 'sech', 'tfr': 1}, a, M, L)
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertEqual(info["tfr"], 1, mess)
        gt = psech(L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

        # Test adding args in dict
        name = 'gauss'
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        (g, info) = gabwin({'name': name, 'centering': 'hp'}, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(ie.isevenfunction(g, centering='wp'), mess)

        # firwin without M
        name = random.sample(arg_firwin(), 1)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        self.assertRaises(ValueError, gabwin, {'name': name}, a, M, L)

        # firwin with M
        name = random.sample(arg_firwin(), 1)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        Ml = 2*M+1
        (gl, info) = gabwin({'name': name, 'M': Ml}, a, M)
        mess += "\nMl = " + str(Ml)
        mess += "\ng = " + str(gl)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        if name in {'sine', 'cosine', 'sqrthann', 'sqrttria', 'itersine',
                    'ogg'}:
            self.assertTrue(info['istight'], mess)
        else:
            self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertTrue(info['isfir'], mess)
        self.assertEqual(info["gl"], len(gl), mess)
        gt = firwin(name, Ml, norm='2')[0]
        gt = fir2long(gt, int(np.ceil(gt.shape[0] / M) * M))
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(gl, gt, 10, mess)

        # Unknown
        self.assertRaises(ValueError, gabwin, {'name': 'foo'}, a, M, L)

    def test_composed_dictionnaries_entries(self):
        a = random.randint(10, 40)
        M = random.randint(10, 40)
        L = lcm(a, M)

        # default
        self.assertRaises(TypeError, gabwin, {'name': 1}, a, M, L)

        # dual psech
        tfr = 10
        gd = {'name': ('dual', 'sech'), 'tfr': tfr}
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        mess += str(gd)
        (g, info) = gabwin(gd, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertTrue(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info['auxinfo']["tfr"], tfr, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = gabdual(psech(L, tfr)[0], a, M, L)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, gd, a, M)

        # dual pgauss
        tfr = 10
        gd = {'name': ('dual',), 'tfr': tfr}
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        mess += str(gd)
        (g, info) = gabwin(gd, a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertTrue(info['auxinfo']['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertTrue(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info['auxinfo']["tfr"], tfr, mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = gabdual(pgauss(L, tfr)[0], a, M, L)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)
        self.assertRaises(ValueError, gabwin, gd, a, M)

        # dual fir
        name = random.sample(arg_firwin(), 1)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        (g, info) = gabwin({'name': ('dual', name)}, a, M)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertTrue(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertTrue(info['isfir'], mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = firwin(name, M, norm='2')[0]
        gt = gabdual(gt, a, M, L)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

        # tight fir
        name = random.sample(arg_firwin(), 1)[0]
        mess = "a = {0:d}, M = {1:d}, L = {2:d}, name = {3:s}".format(a, M, L,
                                                                      name)
        (g, info) = gabwin({'name': ('tight', name)}, a, M)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertFalse(info['gauss'], mess)
        self.assertTrue(info['wasreal'], mess)
        self.assertTrue(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertFalse(info['wasrow'], mess)
        self.assertTrue(info['isfir'], mess)
        self.assertEqual(info["gl"], len(g), mess)
        gt = firwin(name, M, norm='2')[0]
        gt = gabtight(gt, a, M, L)
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

    def test_array_entries(self):
        a = random.randint(10, 40)
        M = random.randint(10, 40)
        L = lcm(a, M)
        mess = "a = {0:d}, M = {1:d}, L = {2:d}".format(a, M, L)
        (g, info) = gabwin(np.reshape(pgauss(L)[0], (1, L)), a, M, L)
        mess += "\ng = " + str(g)
        mess += "\ninfo = " + str(info)
        self.assertTrue(info['wasreal'], mess)
        self.assertFalse(info['istight'], mess)
        self.assertFalse(info['isdual'], mess)
        self.assertTrue(info['wasrow'], mess)
        self.assertFalse(info['isfir'], mess)
        self.assertEqual(info["gl"], L, mess)
        gt = pgauss(L)[0]
        mess += "\ngt = " + str(gt)
        np.testing.assert_array_almost_equal(g, gt, 10, mess)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGabWin)
    unittest.TextTestRunner(verbosity=2).run(suite)
