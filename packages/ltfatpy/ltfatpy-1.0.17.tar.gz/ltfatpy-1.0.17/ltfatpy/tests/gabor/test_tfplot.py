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


"""Test of the tfplot function

NOTE: The validity of the plotting features of tfplot are not tested here, only
the fact that they can run without error is tested.

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal
import matplotlib.pyplot as plt

from ltfatpy.gabor.tfplot import tfplot

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestTfplot(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestTfplot')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_exceptions(self):
        """Check that the right exceptions are raised when expected
        """
        # coef must be a 2D numpy.ndarray, check that we get the right
        # exceptions if not
        self.assertRaises(TypeError, tfplot, 'test', 1, np.array([0., 1.]))
        self.assertRaises(TypeError, tfplot, 1, 1, np.array([0., 1.]))
        self.assertRaises(TypeError, tfplot, 1., 1, np.array([0., 1.]))
        self.assertRaises(TypeError, tfplot, [0, 2], 1, np.array([0., 1.]))
        self.assertRaises(ValueError, tfplot, np.ones((4,)), 1,
                          np.array([0., 1.]))
        self.assertRaises(ValueError, tfplot, np.ones((4, 3, 2)), 1,
                          np.array([0., 1.]))

    def test_normalization(self):
        """Check that the parameter normalization is used as expected
        """
        normalizations = ('db', 'dbsq', 'linsq', 'linabs')
        zeros_array = np.zeros((2, 2), dtype=np.float64)
        outs = (40. + zeros_array, 20. + zeros_array, 10000. + zeros_array,
                100. + zeros_array)

        inputs = {}
        inputs['coef'] = 0.0+100.0j + zeros_array
        inputs['step'] = 1
        inputs['yr'] = np.array([0., 1.])
        inputs['display'] = False

        for normalization, out_ref in zip(normalizations, outs):
            inputs['normalization'] = normalization
            out = tfplot(**inputs)
            msg = ('tfplot is misusing normalization with inputs ' +
                   str(inputs))
            assert_array_equal(out_ref, out, msg)

        inputs['normalization'] = 'lin'
        self.assertRaises(ValueError, tfplot, **inputs)

        inputs['coef'] = 100. + zeros_array
        out = tfplot(**inputs)
        msg = ('tfplot is misusing normalization with inputs ' + str(inputs))
        assert_array_equal(inputs['coef'], out, msg)

    def test_tc(self):
        """Check that the parameter tc is used as expected
        """
        coefs = (np.array([[1., 2., 3.], [4., 5., 6.]]),
                 np.array([[1., 2., 3., 4.], [5., 6., 7., 8.]]))
        outs = (np.array([[3., 1., 2.], [6., 4., 5.]]),
                np.array([[3., 4., 1., 2.], [7., 8., 5., 6.]]))

        inputs = {}
        inputs['step'] = 1
        inputs['yr'] = np.array([0., 1.])
        inputs['display'] = False
        inputs['normalization'] = 'lin'
        inputs['tc'] = True

        for coef, out_ref in zip(coefs, outs):
            inputs['coef'] = coef
            out = tfplot(**inputs)
            msg = ('tfplot is misusing tc with inputs ' + str(inputs))
            assert_array_equal(out_ref, out, msg)

    def test_clim_dynrange(self):
        """Check that the parameters clim and dynrange are used as expected
        """
        inputs = {}
        inputs['coef'] = np.array([[1., 10., 100.], [1000., 10000., 100000.]])
        inputs['step'] = 1
        inputs['yr'] = np.array([0., 1.])
        inputs['display'] = False

        inputs['clim'] = [20., 80.]
        out_clim = np.array([[20., 20., 40.], [60., 80., 80.]])
        out = tfplot(**inputs)
        msg = ('tfplot is misusing clim with inputs ' + str(inputs))
        assert_array_equal(out_clim, out, msg)

        inputs.pop('clim')
        inputs['dynrange'] = 60.
        out_dynrange = np.array([[40., 40., 40.], [60., 80., 100.]])
        out = tfplot(**inputs)
        msg = ('tfplot is misusing dynrange with inputs ' + str(inputs))
        assert_array_equal(out_dynrange, out, msg)

        inputs['clim'] = [20., 80.]
        out = tfplot(**inputs)
        msg = ('tfplot is misusing clim and dynrange, clim should takes '
               'precedence over dynrange  with inputs ' + str(inputs))
        assert_array_equal(out_clim, out, msg)

    def test_plot(self):
        """Check that the all the plotting sections of tfplot can be run
        """
        # NOTE: To avoid an error when running the tests in a environnement
        # with no $DISPLAY variable defined, we switch matplotlib to a
        # non-interactive backend
        plt.switch_backend("ps")

        coef = np.random.random((5, 4))
        step = 1
        yr = np.array([0., 1.])
        plottypes = ('image', 'contour', 'surf', 'pcolor')
        for plottype in plottypes:
            tfplot(coef, step, yr, plottype=plottype)

        fs = 10.
        tfplot(coef, step, yr, plottype='image', fs=fs)

        clim = (0., 1.)
        tfplot(coef, step, yr, plottype='image', clim=clim)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTfplot)
    unittest.TextTestRunner(verbosity=2).run(suite)
