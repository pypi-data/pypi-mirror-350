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


"""This module contains sampled, periodized Gaussian window function

Ported from ltfat_2.1.0/fourier/pgauss.m

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

from ltfatpy.comp import comp_pgauss as pg
from ltfatpy.sigproc.normalize import normalize


def pgauss(L, tfr=1.0, fs=0.0, width=0.0, bw=0.0, c_f=0.0, centering='wp',
           delay=0.0, norm='2', **kwargs):
    """Sampled, periodized Gaussian

    - Usage:
        | ``(g, tfr) =  pgauss(L)``
        | ``(g, tfr) =  pgauss(L, tfr, fs, width, bw, c_f, centering, delay,
            norm)``

    - Input parameters:

    :param int L: Length of the output vector.
    :param float tfr: determines the ratio between the effective support
        of **g** and the effective support of the DFT of **g**. If
        :math:`tfr>1` then **g** has a wider support than the DFT of **g**.
        Default is 1.
    :param float fs: Use a sampling rate of **fs** Hz as unit for specifying
        the width, bandwidth, centre frequency and delay of the Gaussian.
        Default is :math:`fs=0` which indicates to measure everything in
        samples.
    :param float width: Set the width of the Gaussian such that it has an
        effective support of **width** samples. This means that
        approx. 96% of the energy or 79% of the area under the graph is
        contained within **width** samples. This corresponds to a -6 db
        cutoff. This is equivalent to calling ``pgauss(L,tfr = s^2/L)``.
        Default is zero, unset.
    :param float bw: As for the **width** argument, but specifies the width
        in the frequency domain. The bandwidth is measured in normalized
        frequencies, unless the **fs** value is given. Default is zero, unset.
    :param float c_f: Set the centre frequency of the Gaussian to **cf**.
        Default is zero.
    :param str centering: "wp" means output is whole point even. This is the
        default. Setting it to **hp** means output is half point even which
        is the case for the most Matlab filters routines.
    :param float delay: Delay the output by **delay**. Default is zero.
    :param str norm: normalization to apply (default is L2)


    - Normalization types :

                 +-------+---------+
                 | Name  | Norms   |
                 +=======+=========+
                 | '1'   | L1-norm |
                 +-------+---------+
                 | '2'   | L2-norm |
                 +-------+---------+

    - Output parameters:

    :returns: ``(g, tfr)``
    :rtype: tuple
    :var numpy array g: window array of length **L**
    :var int tfr: ratio between the effective support of **g** and the
        effective support of the DFT of **g**.

    ``pgauss(L,tfr)`` samples of a periodized Gaussian. The function returns
    a numpy array **g** containing a regular sampling of the periodization of
    the function :math:`\\exp(-\\pi*(x^2/tfr))`.

    The :math:`l^2` norm of the returned Gaussian is equal to 1.

    The function is whole-point even. This implies that
    ``fft(pgauss(L, tfr))`` is real for any **L** and **tfr**. The DFT of
    **g** is equal to ``pgauss(L, 1/tfr)``.

    If this function is used to generate a window for a Gabor frame, then
    the window giving the smallest frame bound ratio is generated by
    ``pgauss(L, a*M/L)``.

    - Examples:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from ltfatpy import sgram
    >>> # This example creates a Gaussian function, and demonstrates that it is
    >>> # its own Discrete Fourier Transform:
    >>> g = pgauss(128)[0]
    >>> # Test of DFT invariance: Should be close to zero.
    >>> np.linalg.norm(g - np.fft.fft(g)/np.sqrt(128)) <= 1e-10
    True
    >>> # The next plot shows the Gaussian in the time domain:
    >>> _ = plt.plot(np.fft.fftshift(g))
    >>> plt.show()
    >>> # The next plot shows the Gaussian in the time-frequency plane:
    >>> _ = sgram(g, nf=True, tc=True, normalization='lin')
    >>> plt.show()

    .. image:: images/pgauss_1.png
       :width: 700px
       :alt: Gaussian in the time domain
       :align: center
    .. image:: images/pgauss_2.png
       :width: 700px
       :alt: Gaussian in the time-frequency plane
       :align: center

    .. note:: **g** is real if **c_f** = 0 and complex if not.

    .. seealso:: :func:`~ltfatpy.gabor.dgtlength.dgtlength`,
        :func:`~ltfatpy.fourier.psech.psech`,
        :func:`~ltfatpy.sigproc.firwin.firwin`, :func:`pbspline`,
        :func:`~ltfatpy.sigproc.normalize.normalize`
    """
    cent = 0
    if centering == 'hp':
        cent = 0.5
    elif centering != 'wp':
        raise ValueError("centering should be 'wp' or 'hp'")
    if (type(L) is not int or L <= 0):
        raise TypeError("L should be non null integer")
    if(type(tfr) is int):
        tfr = float(tfr)
    if (type(tfr) is not float):
        raise TypeError("tfr should be float")

    if fs == 0:
        if width != 0:
            tfr = width**2 / L
        if bw != 0:
            tfr = L / (bw * L/2)**2
    else:
        if width != 0:
            tfr = (width * fs)**2 / L
        if bw != 0:
            tfr = L / (bw / fs * L)**2
        delay = delay*fs
        c_f = c_f/fs*L

    g = pg.comp_pgauss(L, tfr, cent-delay, c_f)
    g = normalize(g, norm)[0]
    return(g, tfr)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
