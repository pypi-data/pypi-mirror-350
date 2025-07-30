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


"""Module of instantaneous frequency plot

Ported from ltfat_2.1.0/gabor/instfreqplot.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.plotdgt import plotdgt
from ltfatpy.gabor.plotdgtreal import plotdgtreal
from ltfatpy.gabor.gabimagepars import gabimagepars
from ltfatpy.fourier.fftresample import fftresample
from ltfatpy.gabor.dgt import dgt
from ltfatpy.gabor.gabphasegrad import gabphasegrad


def instfreqplot(f, fs=None, tfr=1., wlen=None, nf=None, thr=None, fmax=None,
                 xres=800, yres=600, method='dgt', climsym=None, **kwargs):
    """Plot of instantaneous frequency

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
        **thr** times the largest magnitude. Set the instantaneous frequency of
        the rest of the coefficients to zero.
    :param float fmax: Display **fmax** as the highest frequency.
    :param int xres: Approximate number of pixels in the time direction
    :param int yres: Number of pixels in the frequency direction
    :param str method: Specify the method used for instantaneous frequency
        computation. Possible values are 'dgt', 'phase' and 'abs'. See the help
        of :func:`~ltfatpy.gabor.gabphasegrad` for details.
    :param float climsym: Use a colormap ranging from ``-climsym`` to
        ``+climsym``
    :param `**kwargs`: ``instfreqplot`` supports all the optional parameters of
        :func:`~ltfatpy.gabor.tfplot.tfplot`. Please see the help of
        :func:`~ltfatpy.gabor.tfplot.tfplot` for an exhaustive list.

    - Output parameters:

    :returns: The instantaneous frequency data used in the plotting
    :rtype: numpy.ndarray

    ``instfreqplot(f)`` plots the instantaneous frequency of **f** using a
    Discrete Gabor Transform (:func:`~ltfatpy.gabor.dgt.dgt`).

    The instantaneous frequency contains extreme spikes in regions
    where the spectrogram is close to zero. These points are usually
    uninteresting and destroy the visibility of the plot. Use the thr
    or clim or climsym options to remove these points.

    - An example:

        >>> from ltfatpy import instfreqplot, greasy
        >>> from matplotlib.pyplot import show
        >>> _ = instfreqplot(greasy()[0], 16000., thr=.03, climsym=100.)
        >>> show()

        will produce a nice instantaneous frequency plot of the
        :func:`~ltfatpy.signals.greasy.greasy` signal.

    .. image:: images/instfreqplot.png
       :width: 600px
       :alt: instantaneous frequency of the greasy signal
       :align: center

    .. seealso:: :func:`~ltfatpy.gabor.sgram.sgram`, :func:`resgram`,
        :func:`~ltfatpy.gabor.phaseplot.phaseplot`
    """

    if not isinstance(f, np.ndarray):
        raise TypeError('f must be a 1D numpy.ndarray')

    if f.ndim > 1:
        raise ValueError('Input must be a vector.')

    if nf is None:
        if np.isrealobj(f):
            nf = False
        else:
            nf = True

    # Override the setting from tfplot, because instfreqplot does not support
    # the dB-settings
    kwargs['normalization'] = 'lin'

    # Downsample
    if fmax:
        if fs:
            resamp = fmax*2./fs
        else:
            resamp = fmax*2./f.shape[0]

        f = fftresample(f, int(round(f.shape[0] * resamp)))
        fs = 2. * fmax

    Ls = f.shape[0]

    if not nf:
        yres = 2*yres

    try:
        a, M, L, N, Ndisp = gabimagepars(Ls, xres, yres)

    except ValueError:
        raise ValueError(
            'The signal is too long. instfreqplot cannot visualize all the '
            'details.\nTry a shorter signal or increase the image resolution '
            'by calling:\n\ninstfreqplot(..., xres=xres, yres=yres)\n\n'
            'for larger values of xres and yres.\nThe current values are:\n  '
            'xres = {0}\n  yres = {1}'.format(xres, yres))
    except:
        raise

    # Set an explicit window length, if this was specified.
    if wlen:
        tfr = wlen**2 / L

    g = {'name': 'gauss', 'tfr': tfr}

    if method == 'dgt':
        coef, fgrad, dgtcoef = gabphasegrad('dgt', f, g, a, M)
    elif method == 'phase':
        dgtcoef = dgt(f, g, a, M)[0]
        coef, fgrad = gabphasegrad('phase', np.angle(dgtcoef), a)
    elif method == 'abs':
        dgtcoef = dgt(f, g, a, M)[0]
        coef, fgrad = gabphasegrad('abs', np.abs(dgtcoef), g, a)

    if thr:
        # keep only the largest coefficients.
        maxc = np.max(np.abs(dgtcoef))
        mask = np.abs(dgtcoef) < maxc*thr
        coef[mask] = 0.

    # Cut away zero-extension.
    coef = coef[:, 0:Ndisp]

    # Convert climsym into a normal clim
    if climsym:
        kwargs['clim'] = [-climsym, climsym]
    else:
        # handle default value for clim
        if 'clim' not in kwargs:
            kwargs['clim'] = (0., 1.)

    if nf:
        plotdgt(coef, a, fs=fs, **kwargs)
    else:
        coef = coef[:int(np.floor(M/2))+1, :]
        plotdgtreal(coef, a, M, fs=fs, **kwargs)

    return coef


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
