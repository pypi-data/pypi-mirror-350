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


"""Module of greasy signal loading

Ported from ltfat_2.1.0/signals/greasy.m

.. moduleauthor:: Denis Arrivault,
                  Florent Jaillet
"""

from __future__ import print_function, division

from scipy.io.wavfile import read as wavread
import pkg_resources
import numpy as np


def greasy():
    """Load the 'greasy' test signal

    - Usage:

        | ``(s, fs) = greasy()``

    - Output parameters:

    :returns: ``(s, fs)``
    :rtype: tuple

    :var numpy.ndarray s: 'greasy' signal
    :var int fs: sampling frequency in Hz

    ``greasy`` loads the 'greasy' signal. It is a recording of a woman
    pronouncing the word "greasy".

    The signal is 5880 samples long and recorded at 16 kHz with around 11
    bits of effective quantization.

    The signal has been scaled to not produce any clipping when
    played. To get integer values use ``numpy.rint(greasy()[0]*2048.)``.

    The signal was obtained from Wavelab
    (`<http://www-stat.stanford.edu/~wavelab/>`_), it is a part of the first
    sentence of the TIMIT speech corpus "She had your dark suit in greasy
    wash water all year":
    `<http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC93S1>`_.

    - Examples:

        Plot of 'greasy' in the time-domain:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy import greasy
        >>> _ = plt.plot(np.arange(5880.)/16000., greasy()[0]);
        >>> _ = plt.xlabel('Time (seconds)')
        >>> _ = plt.ylabel('Amplitude')
        >>> plt.show()

        Plot of 'greasy' in the time-frequency-domain:

        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy import greasy, sgram
        >>> _ = sgram(greasy()[0], 16000., 90.)
        >>> plt.show()

    .. image:: images/greasy_1.png
       :width: 700px
       :alt: time domain image
       :align: center
    .. image:: images/greasy_2.png
       :width: 600px
       :alt: spectrogram image
       :align: center

    - References:
        :cite:`mazh93`
    """

    f = pkg_resources.resource_stream(__name__, "greasy.wav")

    fs, s = wavread(f)
    s = s.astype(np.float64) / 2.**15.
    return (s, fs)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
