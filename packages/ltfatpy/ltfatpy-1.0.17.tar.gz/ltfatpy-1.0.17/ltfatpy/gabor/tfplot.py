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


"""Module of time-frequency plotting

Ported from ltfat_2.1.0/gabor/tfplot.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def tfplot(coef, step, yr, fs=None, dynrange=None, normalization='db',
           tc=False, clim=None, plottype='image', colorbar=True, display=True,
           time='Time', frequency='Frequency', samples='samples',
           normalized='normalized'):
    """Plot coefficient matrix on the TF plane

    - Input parameters:

    :param numpy.ndarray coef: 2D coefficient array
    :param float step: Shift in samples between each column of coefficients
    :param numpy.ndarray yr: 2 elements vector containing the lowest and
        highest normalized frequency
    :param float fs: Sampling rate in Hz of the original signal
    :param float dynrange: Limit the dynamical range to dynrange by using a
        colormap in the interval [chigh-dynrange, chigh], where chigh is the
        highest value in the plot. The default value of None means to not limit
        the dynamical range. If both **clim** and **dynrange** are specified,
        then **clim** takes precedence.
    :param str normalization: String specifying the normalization of the plot,
        possible values are listed below
    :param bool tc: Time centering: if ``True``, move the beginning of the
        signal to the middle of the plot. This is usefull for visualizing the
        window functions of the toolbox.
    :param tuple clim: Use a colormap ranging from clim[0] to clim[1]. If both
        **clim** and **dynrange** are specified, then **clim** takes
        precedence.
    :param str plottype: String specifying the type of plot, possible values
        are listed below
    :param bool colorbar: If ``True``, display the colorbar (this is the
        default)
    :param bool display: If ``True``, display the figure (this is the default).
        Using ``display=False`` to avoid displaying the figure is usefull if
        you only want to obtain the output for further processing.
    :param str time: Text customization: the word denoting time
    :param str frequency: Text customization: the word denoting frequency
    :param str samples: Text customization: the word denoting samples
    :param str normalized: Text customization: the word denoting normalized

    - Output parameter:

    :returns: The processed image data used in the plotting. Inputting this
              data directly to :func:`~matplotlib.pyplot.matshow` or similar
              functions will create the plot. This is usefull for custom
              post-processing of the image data.
    :rtype: numpy.ndarray

    ``tfplot(coef, step, yr)`` will plot a rectangular coefficient array on the
    TF-plane.

    ``tfplot`` is not meant to be called directly. Instead, it is called by
    other plotting routines to give a uniform display format.


    Possible values for **normalization**:
        ============ ==========================================================
        ``'db'``     Apply :math:`20*\log_{10}` to the coefficients. This makes
                     it possible to see very weak phenomena, but it might show
                     too much noise. A logarithmic scale is more adapted to
                     perception of sound. This is the default.

        ``'dbsq'``   Apply :math:`10*\log_{10}` to the coefficients. Same as
                     the ``'db'`` option, but assume that the input is already
                     squared.

        ``'lin'``    Show the coefficients on a linear scale. This will display
                     the raw input without any modifications. Only works for
                     real-valued input.

        ``'linsq'``  Show the square of the coefficients on a linear scale.

        ``'linabs'`` Show the absolute value of the coefficients on a linear
                     scale.
        ============ ==========================================================

    Possible values for **plottype**:
        ============= ====================================================
        ``'image'``   Use imshow to display the plot. This is the default.

        ``'contour'`` Do a contour plot.

        ``'surf'``    Do a surface plot.

        ``'pcolor'``  Do a pcolor plot.
        ============= ====================================================

    .. seealso:: :func:`~ltfatpy.gabor.sgram.sgram`,
        :func:`~ltfatpy.gabor.plotdgt.plotdgt`,
        :func:`~ltfatpy.gabor.plotdgtreal.plotdgtreal`,
        :func:`plotwmdct`, :func:`plotdwilt`

    """

    if not isinstance(coef, np.ndarray):
        raise TypeError('coef must be a 2D numpy.ndarray')

    if coef.ndim > 2:
        raise ValueError('Input is multidimensional. coef must be a 2D '
                         'numpy.ndarray')

    if coef.ndim < 2:
        raise ValueError('coef must be a 2D numpy.ndarray')

    M = coef.shape[0]
    N = coef.shape[1]

    # Apply transformation to coefficients.
    if normalization == 'db':
        coef = 20. * np.log10(np.abs(coef) + np.finfo(np.float64).tiny)
    elif normalization == 'dbsq':
        coef = 10. * np.log10(np.abs(coef) + np.finfo(np.float64).tiny)
    elif normalization == 'linsq':
        coef = np.square(np.abs(coef))
    elif normalization == 'linabs':
        coef = np.abs(coef)
    elif normalization == 'lin':
        if not np.isrealobj(coef):
            raise ValueError("Complex valued input cannot be plotted using the"
                             " 'lin' flag. Please use the 'linsq' or 'linabs' "
                             "flag.")
        else:
            # coef is returned in the output so we make a copy to avoid
            # returning a reference to the data passed in input
            coef = coef.copy()

    # 'dynrange' parameter is handled by converting it into clim
    #  clim overrides dynrange, so do nothing if clim is already specified
    if dynrange and not clim:
        maxclim = np.nanmax(coef)
        clim = (maxclim - dynrange, maxclim)

    # Handle clim by thresholding and cutting
    if clim:
        np.clip(coef, clim[0], clim[1], out=coef)

    if tc:
        xr = np.arange(-np.floor(N/2.), np.floor((N-1)/2)+1) * step
        coef = np.fft.fftshift(coef, axes=1)
    else:
        xr = np.arange(0, N) * step

    if display:
        if fs:
            xr = xr / fs
            yr = yr * fs/2

        # Convert yr to range of values
        yr = np.linspace(yr[0], yr[1], M)

        if plottype == 'image':
            xstep = xr[1] - xr[0]
            ystep = yr[1] - yr[0]
            extent = [xr[0] - xstep/2, xr[-1] + xstep/2,
                      yr[0] - ystep/2,  yr[-1] + ystep/2]

            if clim:
                # Call imshow explicitly with clim. This is necessary for the
                # situations where the data is by itself limited (from above
                # or below) to within the specified range. Setting clim
                # explicitly avoids the colormap moves in the top or bottom.
                plt.imshow(coef, extent=extent, aspect='auto',
                           interpolation='nearest', origin='lower', clim=clim)
            else:
                plt.imshow(coef, extent=extent, aspect='auto',
                           interpolation='nearest', origin='lower')

        elif plottype == 'contour':
            # Note: The matlplotlib contour function doesn't give the exact
            # same visual results as in Octave for the same data.
            # So we can expect some slight differences when comparing contour
            # plots produced by tfplot.
            plt.contour(xr, yr, coef, 10)

        elif plottype == 'surf':
            # Note: The following import is needed to be able to use
            # plot_surface
            from mpl_toolkits.mplot3d import Axes3D

            plt.delaxes()
            ax = plt.gcf().add_subplot(111, projection='3d')
            ax.azim = -130.
            ax.elev = 30.
            xgrid, ygrid = np.meshgrid(xr, yr)
            ax.plot_surface(xgrid, ygrid, coef, rstride=1, cstride=1,
                            antialiased=True, linewidth=0, cmap=cm.jet)
            # Note: matplotlib doesn't support orthogonal projection,
            # so the result doesn't look exactly as in Octave. See:
            # http://stackoverflow.com/questions/23840756/ \
            #                          how-to-disable-perspective-in-mplot3d

        elif plottype == 'pcolor':
            plt.pcolor(xr, yr, coef, edgecolors='k', antialiased=False,
                       linewidth=1)
            plt.axis('tight')

        if colorbar:
            if plottype == 'surf':
                # Note: we can use "plottype in ('contour', 'surf')" in the
                # previous test if we want the colorbar in contour plots to
                # look more like the one in Octave
                mappable = cm.ScalarMappable(cmap=cm.jet)
                mappable.set_array(coef)
                plt.colorbar(mappable, ax=plt.gca())
            else:
                plt.colorbar(ax=plt.gca())

        if fs:
            plt.xlabel(time + ' (s)')
            plt.ylabel(frequency + ' (Hz)')
        else:
            plt.xlabel(time + ' (' + samples + ')')
            plt.ylabel(frequency + ' (' + normalized + ')')

    return coef
