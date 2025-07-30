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


"""Test of the assert_sigreshape_pre function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np
from ltfatpy.comp.assert_sigreshape_pre import assert_sigreshape_pre as asp
import functools


class TestAssertSigReshapePre(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print("Start TestAssertSigReshapePre")

    # Called after the tests.
    def tearDown(self):
        print("Test done")

    def test_default(self):
        """Basic usual cases"""
        L = random.randint(5, 200)
        f = np.arange(0, L, dtype=np.float64)
        (g, L, Ls, W, dim, _permutedshape, _order) = asp(f)
        mess = "\nL = {0:d}, Ls = {1:d}, W = {2:d}, dim = {3:d}, g.shape = "
        mess += str(g.shape) + ", f.shape = " + str(f.shape)
        mess = mess.format(L, Ls, W, dim)
        np.testing.assert_array_equal(f, g.reshape(L), mess)
        self.assertEqual(L, L, mess)
        self.assertEqual(W, 1, mess)
        self.assertEqual(dim, 0, mess)

        f = f.reshape(L, 1)
        (g, L, Ls, W, dim, _permutedshape, _order) = asp(f)
        mess = "\nL = {0:d}, Ls = {1:d}, W = {2:d}, dim = {3:d}, g.shape = "
        mess += str(g.shape) + ", f.shape = " + str(f.shape)
        mess = mess.format(L, Ls, W, dim)
        np.testing.assert_array_equal(f, g, mess)
        self.assertEqual(L, L, mess)
        self.assertEqual(W, 1, mess)
        self.assertEqual(dim, 0, mess)

    def test_list(self):
        """Basic signal in a list"""
        L = random.randint(5, 200)
        f = [x for x in range(0, L)]
        (g, L, Ls, W, dim, _permutedshape, _order) = asp(f)
        mess = "\nL = {0:d}, Ls = {1:d}, W = {2:d}, dim = {3:d}, g.shape = "
        mess += str(g.shape) + ", len(f) = " + str(len(f))
        mess = mess.format(L, Ls, W, dim)
        np.testing.assert_array_equal(f, g.reshape(L), mess)
        self.assertEqual(L, L, mess)
        self.assertEqual(W, 1, mess)
        self.assertEqual(dim, 0, mess)
        self.assertRaises(TypeError, asp, {"a": 1})
        self.assertRaises(TypeError, asp, f, L, (1, 0))
        self.assertRaises(TypeError, asp, f, L, -4)
        self.assertRaises(TypeError, asp, f, 5.5)

    def test_twodim(self):
        """Many channels signals"""
        shapef = tuple([random.randint(5, 20) for _ in range(2)])
        L = functools.reduce(lambda x, y: x * y, shapef)
        f = np.arange(0, L, dtype=np.complex128)
        f = f.reshape(shapef)
        (g, L, Ls, W, dim, _permutedshape, _order) = asp(f)
        mess = "\nL = {0:d}, Ls = {1:d}, W = {2:d}, dim = {3:d}, g.shape = "
        mess += str(g.shape) + ", f.shape = " + str(f.shape)
        mess = mess.format(L, Ls, W, dim)
        np.testing.assert_array_equal(f, g, mess)
        self.assertEqual(L, L, mess)
        self.assertEqual(W, shapef[1], mess)
        self.assertEqual(dim, 0, mess)
        L = random.randint(5, 200)
        f = np.arange(0, L, dtype=np.float64)
        fcol = f.reshape((1, L))
        (g, L, Ls, W, dim, _permutedshape, _order) = asp(fcol)
        mess = "\nL = {0:d}, Ls = {1:d}, W = {2:d}, dim = {3:d}, g.shape = "
        mess += str(g.shape) + ", f.shape = " + str(fcol.shape)
        mess = mess.format(L, Ls, W, dim)
        np.testing.assert_array_equal(f, g.squeeze(), mess)
        self.assertEqual(L, L, mess)
        self.assertEqual(W, 1, mess)
        self.assertEqual(dim, 1, mess)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAssertSigReshapePre)
    unittest.TextTestRunner(verbosity=2).run(suite)
