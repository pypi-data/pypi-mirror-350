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


"""Test of the s0norm function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np
# from math import *
# import matplotlib.pyplot as plt
# from fractions import gcd

from ltfatpy.gabor.s0norm import s0norm
from ltfatpy.tests.datasets.read_s0norm_ex_mat import S0Examples
from ltfatpy.tests.datasets.get_dataset_path import get_dataset_path


class TestS0Norm(unittest.TestCase):
    # Called before the tests.
    def setUp(self):
        self.filename = get_dataset_path('s0_norm_test.mat')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_default(self):
        """ Comparing results with Matlab generated ones
        """
        pass
        dgs = S0Examples(self.filename)
        (gl, R, dim, rel, G, S0, S0Shape) = dgs.read_next_frame()
        while gl != '':
            dim = dim - 1
            mess = "\ngl = " + str(gl) + "\nR = " + str(R)
            mess += "\ndim = " + str(dim) + "\nrel = " + str(rel)
            mess += "\nG = " + str(G) + "\nS0 = " + str(S0)
            mess += "\nS0Shape = " + str(S0Shape)
            if rel == 'rel':
                s0r = s0norm(G, True, dim)
            else:
                s0r = s0norm(G, False, dim)
            mess += "\ns0r = " + str(s0r)
            self.assertTrue(np.linalg.norm(np.squeeze(s0r)-S0) <= 1e-10, mess)
            if(len(s0r.shape) > 1):
                self.assertEqual(s0r.shape, tuple(S0Shape), mess)
            (gl, R, dim, rel, G, S0, S0Shape) = dgs.read_next_frame()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestS0Norm)
    unittest.TextTestRunner(verbosity=2).run(suite)
