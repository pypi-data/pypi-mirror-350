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


"""Module of dgtreal coefficients plotting

Ported from ltfat_2.1.0/gabor/plotdgtreal.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np

from ltfatpy.gabor.tfplot import tfplot


def plotdgtreal(coef, a, M, **kwargs):
    """Plot dgtreal coefficients

    :param numpy.ndarray coef: Gabor coefficients
    :param int a: Length of time shift used when computing **coef**
    :param int M: Number of modulations used when computing **coef**
    :param `**kwargs`: ``plotdgtreal`` supports all the optional parameters of
        :func:`~ltfatpy.gabor.tfplot.tfplot`. Please see the help of
        :func:`~ltfatpy.gabor.tfplot.tfplot` for an exhaustive list.

    - Output parameters:

    :returns: The processed image data used in the plotting. Inputting this
        data directly to :func:`~matplotlib.pyplot.matshow` or similar
        functions will create the plot. This is useful for custom
        post-processing of the image data.
    :rtype: numpy.ndarray

    ``plotdgtreal(coef, a, M)`` plots Gabor coefficients from
    :func:`~ltfatpy.gabor.dgtreal.dgtreal`. The parameters **a** and **M**
    must match those from the call to :func:`~ltfatpy.gabor.dgtreal.dgtreal`.

    .. seealso:: :func:`~ltfatpy.gabor.dgtreal.dgtreal`,
        :func:`~ltfatpy.gabor.tfplot.tfplot`,
        :func:`~ltfatpy.gabor.sgram.sgram`,
        :func:`~ltfatpy.gabor.plotdgt.plotdgt`

    """

    if M % 2 == 0:
        yr = np.array([0., 1.])
    else:
        yr = np.array([0, 1.-2./M])

    coef = tfplot(coef, a, yr, **kwargs)

    return coef
