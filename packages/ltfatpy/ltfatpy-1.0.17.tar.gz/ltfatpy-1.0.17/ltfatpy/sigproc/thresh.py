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


""" Module of coefficient thresholding

Ported from ltfat_2.1.0/sigproc/thresh.m

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np


def thresh(xi, lamb, thresh_type='hard'):
    """Coefficient thresholding

    - Usage:

        | ``(xo, N) = thresh(xi, lamb)``
        | ``(xo, N) = thresh(xi, lamb, thresh_type)``

    - Input parameters:

    :param numpy.ndarray xi: Input array
    :param lamb: Threshold
    :type lamb: float or numpy.ndarray
    :param str thresh_type: Optional flag specifying the type of thresholding
        (see possible values below)

    - Output parameters:

    :returns: ``(xo, N)``
    :rtype: tuple

    :var numpy.ndarray xo: Array of the same shape as **xi**
        containing data from **xi** after thresholding
    :var int N: Number of coefficients kept

    ``thresh(xi, lamb)`` will perform hard thresholding on **xi**, i.e. all
    elements with absolute value less than scalar **lamb** will be set to zero.

    ``thresh(xi, lamb, 'soft')`` will perform soft thresholding on **xi**, i.e.
    **lamb** will be substracted from the absolute value of every element of
    **xi**.

    The lamb parameter can also be a vector with number of elements
    equal to ``xi.size`` or it can be a numpy array of the same shape
    as **xi**. **lamb** is then applied element-wise and in a column major
    order if **lamb** is a vector.

    The parameter **thresh_type** can take the following values:
        ============ ======================================================
        ``'hard'``   Perform hard thresholding. This is the default.

        ``'wiener'`` Perform empirical Wiener shrinkage. This is in between
                     soft and hard thresholding.

        ``'soft'``   Perform soft thresholding.
        ============ ======================================================

    The function ``wthresh`` in the Matlab Wavelet toolbox implements some of
    the same functionality.

    - Example:

        The following code produces a plot to demonstrate the difference
        between hard and soft thresholding for a simple linear input:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from ltfatpy.sigproc.thresh import thresh
        >>> t = np.linspace(-4, 4, 100)
        >>> _ = plt.plot(t, thresh(t, 1., 'soft')[0], 'r',
        ... t, thresh(t, 1., 'hard')[0], '.b',
        ... t, thresh(t, 1., 'wiener')[0], '--g')
        >>> _ = plt.legend(('Soft thresh.', 'Hard thresh.',  'Wiener thresh.'),
        ... loc='upper left')
        >>> plt.show()

    .. image:: images/thresh.png
       :width: 700px
       :alt: thresh image
       :align: center

    .. seealso::
        :func:`~ltfatpy.sigproc.largestr.largestr`,
        :func:`~ltfatpy.sigproc.largestn.largestn`

    - References:
        :cite:`lim1979enhancement,ghael1997improved`
    """

    # Note: This function doesn't support the handling of sparse matrices
    # available in the Octave version. Only full numpy arrays are supported in
    # input and output.

    error_msg = ('lamb must be a float or a numpy vector with '
                 'lamb.size == xi.size or whatever shape xi has such that '
                 'lamb.shape == xi.shape')

    if not (isinstance(lamb, float) or isinstance(lamb, np.ndarray)):
        raise TypeError(error_msg)

    if isinstance(lamb, np.ndarray):  # lamb is not scalar
        if lamb.size != xi.size:
            # lamb does not have the same number of elements
            raise ValueError(error_msg)

        # Reshape lamb if it is a vector
        if lamb.shape != xi.shape:
            lamb = lamb.reshape(xi.shape, order='F')

    # Dense case (this Python port doesn't handle the sparse matrix case)
    xo = np.zeros(xi.shape, dtype=xi.dtype)

    # Create a mask with a value of 1 for non-zero elements. For full
    # matrices, this is faster than the significance map.

    if thresh_type == 'hard':
        mask = abs(xi) >= lamb
        N = np.count_nonzero(mask)
        xo = xi * mask

    elif thresh_type == 'soft':
        # In the following lines, the +0 is significant: It turns
        # -0 into +0, oh! the joy of numerics.
        # Note: It is not sure that the "+0." needed in Octave is also needed
        # in Python, but it is kept here for safety.
        xa = abs(xi)-lamb
        mask = xa >= 0.
        xo = (mask*xa + 0.) * np.sign(xi)
        N = np.count_nonzero(mask) - np.count_nonzero(xa == 0.)

    elif thresh_type == 'wiener':
        with np.errstate(divide='ignore'):
            # NOTE: divide by 0 warnings are ignored because they are handled
            # below
            xa = lamb / abs(xi)
        xa[np.isinf(xa)] = 0
        xa = 1. - xa**2
        mask = xa > 0
        xo = xi * xa * mask
        N = np.count_nonzero(mask)

    return (xo, N)

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
