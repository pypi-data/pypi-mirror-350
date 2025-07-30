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


"""Test of the rms function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np

from ltfatpy.sigproc.rms import rms


class TestSigprocRms(unittest.TestCase):
    """ Unittest class for Sigproc rms"""
    digit = 9

    def setUp(self):
        pass

    def tearDown(self):
        print('Test done')

    def test_default(self):
        f1 = np.arange(10)
        f2 = 10*np.arange(10)
        f = np.vstack((f1, f2)).T
        y1 = rms(f1)
        y2 = rms(f2)
        y = rms(f)
        np.testing.assert_equal(y[0, 0], y1)
        np.testing.assert_equal(y[0, 1], y2)
        y1 = rms(f1, ac=True)
        y2 = rms(f2, ac=True)
        y = rms(f, ac=True)
        np.testing.assert_equal(y[0, 0], y1)
        np.testing.assert_equal(y[0, 1], y2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSigprocRms)
    unittest.TextTestRunner(verbosity=2).run(suite)
