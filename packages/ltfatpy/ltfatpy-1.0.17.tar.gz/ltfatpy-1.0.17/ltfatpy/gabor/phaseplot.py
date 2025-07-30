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


"""Module of phase plot

Ported from ltfat_2.1.0/gabor/phaseplot.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.plotdgt import plotdgt
from ltfatpy.gabor.plotdgtreal import plotdgtreal
from ltfatpy.fourier.fftresample import fftresample
from ltfatpy.gabor.dgt import dgt
from ltfatpy.gabor.dgtreal import dgtreal


def phaseplot(f, fs=None, tfr=1., wlen=None, nf=None, thr=None, fmax=None,
              phase='timeinv', norm='2', **kwargs):
    """Phase plot

    - Input parameters:

    :param numpy.ndarray f: Analyzed signal
    :param float fs: Sampling rate in Hz of the analyzed signal
    :param float tfr: Set the ratio of frequency resolution to time resolution.
        A value ``tfr = 1.0`` is the default. Setting ``tfr > 1.0`` will give
        better frequency resolution at the expense of a worse time resolution.
        A value of ``0.0 < tfr < 1.0`` will do the opposite.
    :param int wlen: Window length. Specifies the length of the window
        measured in samples. See help of :func:`~ltfatpy.fourier.pgauss` on the
        exact details of the window length (parameter width).
    :param bool nf: If ``True``, display negative frequencies, with the
        zero-frequency centered in the middle. For real signals, this will just
        mirror the upper half plane. This is standard for complex signals.
    :param float thr: Keep the coefficients with a magnitude larger than
        **thr** times the largest magnitude. Set the phase of the rest of the
        coefficients to zero. This is useful, because for small amplitude the
        phase values can be meaningless.
    :param float fmax: Display **fmax** as the highest frequency.
    :param str phase: Phase convention for the dgt computation. Use
        phase='timeinv' to display the phase as computed by a time-invariant
        dgt (this is the default) or phase='freqinv' to display the phase as
        computed by a frequency-invariant dgt.
    :param string norm: Window normalization. See parameter **norm** in the
        help of :func:`~ltfatpy.fourier.pgauss`.
    :param `**kwargs`: ``phaseplot`` supports all the optional parameters of
        :func:`~ltfatpy.gabor.tfplot.tfplot`. Please see the help of
        :func:`~ltfatpy.gabor.tfplot.tfplot` for an exhaustive list.

    - Output parameters:

    :returns: The phase data used in the plotting
    :rtype: numpy.ndarray

    ``phaseplot(f)`` plots the phase of **f** using a dgt.

    ``phaseplot`` should only be used for short signals (shorter than the
    resolution of the screen), as there will otherwise be some visual
    aliasing, such that very fast changing areas will look very smooth.
    ``phaseplot`` always calculates the phase of the full time/frequency plane
    (as opposed to :func:`~ltfatpy.gabor.sgram.sgram`), and you therefore risk
    running out of memory for long signals.

    For the best result when using phaseplot, use a circulant color
    map, for instance hsv.

    - Examples:

        The following code shows the phaseplot of a periodic, hyperbolic
        secant visualized using the hsv colormap:

        >>> from matplotlib.pyplot import hsv, show
        >>> from ltfatpy import phaseplot, psech
        >>> hsv()
        >>> _ = phaseplot(psech(200)[0], tc=True, nf=True)
        >>> show()

        The following phaseplot shows the phase of white, Gaussian noise:

        >>> from numpy.random import randn
        >>> from matplotlib.pyplot import hsv, show
        >>> from ltfatpy import phaseplot
        >>> hsv()
        >>> _ = phaseplot(randn(200))
        >>> show()

    .. image:: images/phaseplot_1.png
       :width: 600px
       :alt: phase image of a periodic, hyperbolic secant
       :align: center

    .. image:: images/phaseplot_2.png
       :width: 600px
       :alt: phase image of white, Gaussian noise
       :align: center

    .. seealso:: :func:`~ltfatpy.gabor.phaselock.phaselock`

    - References:
        :cite:`Carmona98practical`
    """

    if not isinstance(f, np.ndarray):
        raise TypeError('f must be a 1D numpy.ndarray')

    if f.ndim > 1:
        raise ValueError('Input must be a vector.')

    # Override the setting from tfplot, because phaseplot only uses the 'lin'
    # plotting.
    kwargs['normalization'] = 'lin'

    if nf is None:
        if np.isrealobj(f):
            nf = False
        else:
            nf = True

    # Downsample
    if fmax:
        if fs:
            resamp = fmax*2./fs
        else:
            resamp = fmax*2./f.shape[0]

        f = fftresample(f, int(round(f.shape[0] * resamp)))
        fs = 2. * fmax

    # Always do the full STFT
    L = f.shape[0]
    a = 1
    M = L

    # Set an explicit window length, if this was specified.
    if wlen:
        tfr = wlen**2 / L

    g = {'name': 'gauss', 'tfr': tfr, 'norm': norm}

    if nf:
        coef = dgt(f, g, a, M, pt=phase)[0]
    else:
        coef = dgtreal(f, g, a, M, pt=phase)[0]

    if thr:
        # keep only the largest coefficients.
        maxc = np.max(np.abs(coef))
        mask = np.abs(coef) < maxc*thr
        coef[mask] = 0.

    coef = np.angle(coef)

    if nf:
        plotdgt(coef, a, fs=fs, **kwargs)
    else:
        plotdgtreal(coef, a, M, fs=fs, **kwargs)

    return coef


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
