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


"""Test of the idgt function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np


from ltfatpy.gabor.idgt import idgt
from ltfatpy.gabor.idgtreal import idgtreal
from ltfatpy.tests.datasets.read_dgt_signal_ex_mat import DgtSignals
from ltfatpy.fourier.pgauss import pgauss
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestIDgt(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        self.filename = get_dataset_path('dgt_signal_ex.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        """ Comparing results with Matlab generated ones
        """
        dgs = DgtSignals(self.filename)
        (TYPE, PHASETYPE, L, W, a, M, gl, SIGNAL, WINDOW, DGT, DUAL_WINDOW,
         IDGT) = dgs.read_next_signal()
        while TYPE != '':
            mess = "\n\nTYPE = " + TYPE + "\nPHASETYPE = " + PHASETYPE
            mess += "\nL = " + str(L) + "\nW = " + str(W) + "\na = " + str(a)
            mess += "\nM = " + str(M) + "\ngl = " + str(gl) + "\nSIGNAL =\n"
            mess += str(SIGNAL) + "\nWINDOW =\n" + str(WINDOW)
            mess += "\nDGT\n" + str(DGT) + "\nDUAL_WINDOW\n"
            mess += str(DUAL_WINDOW) + "\nIDGT\n" + str(IDGT)
            if (TYPE == "REAL"):
                pyidgt = idgtreal(DGT, DUAL_WINDOW, a, M, L, PHASETYPE)[0]
            else:
                pyidgt = idgt(DGT, DUAL_WINDOW, a, L, PHASETYPE)[0]
            mess += "\npyidgt = \n" + str(pyidgt)
            self.assertTrue(np.linalg.norm(pyidgt-IDGT) <= 1e-10, mess)
            (TYPE, PHASETYPE, L, W, a, M, gl, SIGNAL, WINDOW, DGT, DUAL_WINDOW,
             IDGT) = dgs.read_next_signal()

    def test_exceptions_cplx(self):
        c = np.array(np.random.random_sample((40, 16)) + 1j *
                     np.random.random_sample((40, 16)))
        a = 10
        M = 40
        L = 160
        self.assertRaises(TypeError, idgt, c, 1, a)
        self.assertRaises(ValueError, idgt, c, np.array((1,)), a)
        cfalse = np.array(np.random.random_sample((40)) + 1j *
                          np.random.random_sample((40)))
        self.assertRaises(ValueError, idgt, cfalse, "Gauss", a)
        self.assertRaises(TypeError, idgt, c, "Gauss", 2.3)
        self.assertRaises(ValueError, idgt, c, "Gauss", a, L, "timeinverse")
        (f, g) = idgt(c, "Gauss", a, pt='timeinv')
        self.assertEqual(len(f), L)
        gs = pgauss(L, a*M/L)[0]
        np.testing.assert_array_almost_equal(g, gs, 10)

    def test_exceptions_real(self):
        c = np.array(np.random.random_sample((21, 16)) + 1j *
                     np.random.random_sample((21, 16)))
        a = 10
        M = 40
        L = 160
        self.assertRaises(TypeError, idgtreal, c, 1, a, M)
        self.assertRaises(ValueError, idgtreal, c, np.array((1,)), a, M)
        cfalse = np.array(np.random.random_sample((21)) + 1j *
                          np.random.random_sample((21)))
        self.assertRaises(ValueError, idgtreal, cfalse, "Gauss", a, M)
        self.assertRaises(TypeError, idgtreal, c, "Gauss", 2.3, M)
        self.assertRaises(ValueError, idgtreal, c, "Gauss", a, M, L,
                          "timeinverse")
        (f, g) = idgtreal(c, "Gauss", a, M, pt='timeinv')
        self.assertEqual(len(f), L)
        gs = pgauss(L, a*M/L)[0]
        np.testing.assert_array_almost_equal(g, gs, 10)
        self.assertRaises(ValueError, idgtreal, c, "Gauss", a, 21)
        g = np.random.random_sample((200))
        self.assertRaises(ValueError, idgtreal, c, g, a, M)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIDgt)
    unittest.TextTestRunner(verbosity=2).run(suite)
