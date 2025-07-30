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


"""Test of the firwin function

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import unittest
import numpy as np
import numpy.linalg as LA

from ltfatpy.sigproc.firwin import firwin
from ltfatpy.fourier.isevenfunction import isevenfunction
from ltfatpy.sigproc.fir2long import fir2long


class TestSigprocFirwin(unittest.TestCase):
    """ Unittest class for Sigproc firwin"""
    digit = 9

    def setUp(self):
        pass

    def tearDown(self):
        print('Test done')

    def test_default(self):
        """  This test script verifies the firwin properties """
        allwins = ('hann', 'tria', 'sine', 'sqrttria', 'itersine', 'square',
                   'hamming', 'blackman', 'nuttall', 'nuttall10', 'nuttall01',
                   'nuttall20', 'nuttall11', 'nuttall02', 'nuttall30',
                   'nuttall21', 'nuttall03', 'blackman2')

        for L in (18, 19.0, 20, 21):
            for centype in ('wp', 'hp'):
                for ii in range(len(allwins)):
                    winname = allwins[ii]
                    (g, info) = firwin(winname, L, centering=centype)
                    L = int(L)
                    res = 1 - isevenfunction(fir2long(g, 2*L),
                                             centering=centype)
                    s = "SYMM {0} {1} L: {2:d} {3:0.5g}".format(winname,
                                                                centype, L,
                                                                res)
                    np.testing.assert_almost_equal(res, 0, type(self).digit,
                                                   err_msg=s)
                    if centype == 'wp':
                        res = 1 - g[0]
                        s = "PEAK {0} {1} L: {2:d} {3:0.5g}".format(winname,
                                                                    centype,
                                                                    L, res)
                        np.testing.assert_almost_equal(res, 0,
                                                       type(self).digit,
                                                       err_msg=s)
                    if L % 2 == 0:
                        if info['ispu']:
                            gpu = g + np.fft.fftshift(g)
                            res = LA.norm(gpu-gpu[0] * np.ones(L))
                            s = "SYMM {0} {1} L: {2:d} {3:0.5g}".format(
                                                                winname,
                                                                centype, L,
                                                                res)
                            np.testing.assert_almost_equal(res, 0,
                                                           type(self).digit,
                                                           err_msg=s)
                        if info['issqpu']:
                            gpu = g**2 + np.fft.fftshift(g**2)
                            res = LA.norm(gpu - gpu[0] * np.ones(L))
                            s = "SYMM {0} {1} L: {2:d} {3:0.5g}".format(
                                                                winname,
                                                                centype, L,
                                                                res)
                            np.testing.assert_almost_equal(res, 0,
                                                           type(self).digit,
                                                           err_msg=s)

    def test_exceptions(self):
        """  This test script verifies the firwin exceptions """
        self.assertRaises(TypeError, firwin, 2, 10)
        self.assertRaises(TypeError, firwin, 'hann', '10')
        self.assertRaises(ValueError, firwin, 'toto', 10)
        self.assertRaises(ValueError, firwin, 'hann', 10, np.ones(9))

    def test_param(self):
        np.testing.assert_array_equal(firwin('hann', 10, shift=0.5)[0],
                                      firwin('hann', 10, centering='hp')[0])
        np.testing.assert_array_equal(firwin('hann', 20, taper=0.5)[0],
                                      np.hstack((np.ones(5),
                                                 firwin('hann', 10)[0],
                                                 np.ones(5))))
        self.assertFalse(firwin('hann', 0)[0])
        np.testing.assert_array_equal(firwin('hann', 10, taper=0)[0],
                                      np.ones(10))
        np.testing.assert_array_equal(firwin('hann', 10, taper=0.5)[0],
                                      np.hstack((np.ones(2),
                                                 firwin('hann', 5,
                                                        shift=0.5)[0],
                                                 np.ones(3))))
        np.testing.assert_array_equal(
                        firwin('hann', 11, taper=0.5, shift=0.5)[0],
                        np.hstack((np.ones(2), firwin('hann', 6, shift=1)[0],
                                   np.ones(3)))
                        )
        np.testing.assert_array_equal(firwin('sqrttria', 10)[0],
                                      np.sqrt(firwin('tria', 10)[0]))
        x = np.arange(10)
        g, _ = firwin('hann', x=x, norm='1')
        gres = np.zeros(10, dtype='f4')
        gres[0] = 1.0
        np.testing.assert_array_equal(g, gres)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSigprocFirwin)
    unittest.TextTestRunner(verbosity=2).run(suite)
