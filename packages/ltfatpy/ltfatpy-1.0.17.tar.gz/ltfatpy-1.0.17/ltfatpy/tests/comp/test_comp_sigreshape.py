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


"""Test of the comp_sigreshape_pre and comp_sigreshape_post functions

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import random
import numpy as np
from ltfatpy.comp.comp_sigreshape_pre import comp_sigreshape_pre as cpre
from ltfatpy.comp.comp_sigreshape_post import comp_sigreshape_post as cpost
import functools


class TestCompSigReshape(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print("Start TestCompSigReshape")

    # Called after the tests.
    def tearDown(self):
        print("Test done")

    def test_default(self):
        self.assertRaises(ValueError, cpre, "toto", 10)
        self.assertRaises(ValueError, cpre, np.empty((0,)), 10)
        self.assertRaises(ValueError, cpre, np.ones((10, 10, 2)), 1)

    def test_onedim(self):
        """One channel"""
        L = random.randint(5, 200)
        f = np.arange(0, L, dtype=np.float64)
        (fin, fl, W, wasrow, remembershape) = cpre(f, 0)
        fres = cpost(fin, fl, wasrow, remembershape)
        mess = "\nfl = {:d}, W = {:d}, wasrow = {:d},remembershape.shape = "
        mess += str(remembershape) + ", f.shape = " + str(f.shape)
        mess += ", fres.shape = " + str(fres.shape)
        mess = mess.format(fl, W, wasrow)
        np.testing.assert_array_equal(f, fres, mess)
        L = random.randint(5, 200)
        f = np.arange(0, L, dtype=np.float64)
        f.resize((1, L))
        (fin, fl, W, wasrow, remembershape) = cpre(f, 0)
        fres = cpost(fin, fl, wasrow, remembershape)
        mess = "\nfl = {:d}, W = {:d}, wasrow = {:d},remembershape.shape = "
        mess += str(remembershape) + ", f.shape = " + str(f.shape)
        mess += ", fres.shape = " + str(fres.shape)
        mess = mess.format(fl, W, wasrow)
        np.testing.assert_array_equal(f, fres, mess)

    def test_twodim(self):
        """Many channels signals"""
        shapef = tuple([random.randint(5, 20) for _ in range(2)])
        L = functools.reduce(lambda x, y: x * y, shapef)
        f = np.arange(0, L, dtype=np.complex128)
        f = f.reshape(shapef)
        (fin, fl, W, wasrow, remembershape) = cpre(f, 1)
        fres = cpost(fin, fl, wasrow, remembershape)
        mess = "\nfl = {:d}, W = {:d}, wasrow = {:d},remembershape.shape = "
        mess += str(remembershape) + ", f.shape = " + str(f.shape)
        mess += ", fres.shape = " + str(fres.shape)
        mess = mess.format(fl, W, wasrow)
        np.testing.assert_array_equal(f, fres, mess)

    def test_multidim(self):
        """Multidimensionnal signals"""
        shapef = tuple([random.randint(5, 20) for _ in range(4)])
        L = np.prod(shapef)
        f = np.arange(0, L, dtype=np.complex128)
        f = f.reshape(shapef)
        (fin, fl, W, wasrow, remembershape) = cpre(f, 5)
        fres = cpost(fin, fl, wasrow, remembershape)
        mess = "\nfl = {:d}, W = {:.2f}, wasrow = {:d},remembershape.shape = "
        mess += str(remembershape) + ", f.shape = " + str(f.shape)
        mess += ", fres.shape = " + str(fres.shape)
        mess = mess.format(fl, W, wasrow)
        np.testing.assert_array_equal(f, fres, mess)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCompSigReshape)
    unittest.TextTestRunner(verbosity=2).run(suite)
