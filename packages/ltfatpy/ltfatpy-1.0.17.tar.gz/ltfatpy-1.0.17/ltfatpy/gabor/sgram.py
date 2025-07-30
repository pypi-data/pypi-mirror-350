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


"""Module of spectrogram plotting

Ported from ltfat_2.1.0/gabor/sgram.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.plotdgt import plotdgt
from ltfatpy.gabor.plotdgtreal import plotdgtreal
from ltfatpy.gabor.gabimagepars import gabimagepars
from ltfatpy.fourier.fftresample import fftresample
from ltfatpy.sigproc.largestr import largestr
from ltfatpy.gabor.dgt import dgt
from ltfatpy.gabor.dgtreal import dgtreal


def sgram(f, fs=None, tfr=1., wlen=None, nf=None, thr=None, fmax=None,
          xres=800, yres=600, norm='2', **kwargs):
    """Spectrogram

    - Input:

    :param numpy.ndarray f: Analyzed signal
    :param float fs: Sampling rate in Hz of the analyzed signal
    :param float tfr: Set the ratio of frequency resolution to time resolution.
        A value ``tfr = 1.0`` is the default. Setting ``tfr > 1.0`` will give
        better frequency resolution at the expense of a worse time resolution.
        A value of ``0.0 < tfr < 1.0`` will do the opposite.
    :param int wlen: Window length. Specifies the length of the window
        measured in samples. See help of :func:`~ltfatpy.fourier.pgauss` on the
        exact details of the window length (parameter **width**).
    :param bool nf: If ``True``, display negative frequencies, with the
        zero-frequency centered in the middle. For real signals, this will just
        mirror the upper half plane. This is standard for complex signals.
    :param float thr: Keep only the largest fraction **thr** of the
        coefficients, and set the rest to zero.
    :param float fmax: Display **fmax** as the highest frequency. Default value
        of ``None`` means to use the Nyquist frequency.
    :param int xres: Approximate number of pixels along x-axis / time
    :param int yres: Approximate number of pixels along y-axis / frequency
    :param string norm: Window normalization. See parameter **norm** in the
        help of :func:`~ltfatpy.fourier.pgauss`.
    :param `**kwargs`: ``sgram`` supports all the optional parameters of
        :func:`~ltfatpy.gabor.tfplot.tfplot`. Please see the help of
        :func:`~ltfatpy.gabor.tfplot.tfplot` for an exhaustive list.

    - Output parameters:

    :returns: The image to be displayed as a matrix. Use this in conjunction
        with imwrite etc. These coefficients are *only* intended to be used by
        post-processing image tools. Numerical Gabor signal analysis and
        synthesis should *always* be done using the
        :func:`~ltfatpy.gabor.dgt.dgt`, :func:`~ltfatpy.gabor.idgt.idgt`,
        :func:`~ltfatpy.gabor.dgtreal.dgtreal` and
        :func:`~ltfatpy.gabor.idgtreal.idgtreal` functions.
    :rtype: numpy.ndarray

    ``sgram(f)`` plots a spectrogram of **f** using a Discrete Gabor Transform
    (:func:`~ltfatpy.gabor.dgt.dgt`).

    - Examples:

        The :func:`~ltfatpy.signals.greasy.greasy` signal is sampled using a
        sampling rate of 16 kHz. To  display a spectrogram of
        :func:`~ltfatpy.signals.greasy.greasy` with a dynamic range of 90 dB,
        use:

        >>> from ltfatpy import sgram, greasy
        >>> from matplotlib.pyplot import show
        >>> _ = sgram(greasy()[0], 16000., dynrange=90)
        >>> show()

        To create a spectrogram with a window length of 20 ms (which is
        typically used in speech analysis) use :

        >>> from ltfatpy import sgram, greasy
        >>> from matplotlib.pyplot import show
        >>> fs = 16000.
        >>> _ = sgram(greasy()[0], fs, dynrange=90, wlen=round(20./1000.*fs))
        >>> show()

    .. image:: images/sgram_1.png
       :width: 600px
       :alt: spectrogram image a dynamic range of 90 dB
       :align: center

    .. image:: images/sgram_2.png
       :width: 600px
       :alt: spectrogram image with a window length of 20 ms
       :align: center

    .. seealso:: :func:`~ltfatpy.gabor.dgt.dgt`,
        :func:`~ltfatpy.gabor.dgtreal.dgtreal`

    """

    if not isinstance(f, np.ndarray):
        raise TypeError('f must be a 1D numpy.ndarray')

    if f.ndim > 1:
        raise ValueError('Input must be a vector.')

    # NOTE: The Octave code of this function in LTFAT 2.1.0 contains the
    # following comment and code:
    #
    # Override the setting from tfplot, because SGRAM does not support the
    # 'dbsq' setting (it does not make sense).
    # definput.flags.log={'db','lin'};
    #
    # But this seems to have no practical effect as we can still run tfplot
    # with the dbsq option in Octave (and all the other normalization options).
    # So to have  similar results than the Octave function in this Python port
    # we don't limit the possible values for normalization.

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

    Ls = f.shape[0]

    if not nf:
        yres = 2*yres

    try:
        a, M, L, N, Ndisp = gabimagepars(Ls, xres, yres)

    except ValueError:
        raise ValueError(
            'The signal is too long. sgram cannot visualize all the '
            'details.\nTry a shorter signal or increase the image resolution '
            'by calling:\n\nsgram(..., xres=xres, yres=yres)\n\n'
            'for larger values of xres and yres.\nThe current values are:\n  '
            'xres = {0}\n  yres = {1}'.format(xres, yres))

    except:
        raise

    # Set an explicit window length, if this was specified.
    if wlen:
        tfr = wlen**2 / L

    g = {'name': 'gauss', 'tfr': tfr, 'norm': norm}

    if nf:
        coef = np.abs(dgt(f, g, a, M)[0])
    else:
        coef = np.abs(dgtreal(f, g, a, M)[0])

    # Cut away zero-extension.
    coef = coef[:, 0:Ndisp]

    if thr:
        # keep only the largest coefficients.
        coef = largestr(coef, thr)[0]

    if nf:
        coef = plotdgt(coef, a, fs=fs, **kwargs)
    else:
        coef = plotdgtreal(coef, a, M, fs=fs, **kwargs)

    return coef

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
