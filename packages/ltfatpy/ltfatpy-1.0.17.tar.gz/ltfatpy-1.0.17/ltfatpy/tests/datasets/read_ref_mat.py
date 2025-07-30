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


"""Read .mat files generated with the Octave version of ltfat for validation

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import numpy as np
import scipy.io


def _squeeze_array(val):
    """Remove single-dimensional entries from the shape of Numpy arrays

    - Input parameter:

    :param val: A Python object of any type

    - Output parameter:

    :returns: If **val** is an instance of numpy.ndarray, the squeezed version
        of **val** is returned, otherwise, **val** is returned
    :rtype: Same type as **val**

    If **val** is an instance of numpy.ndarray, this function returns the
    input array **val**, but with all of the dimensions of length 1 removed.
    The output is always **val** itself or a view into **val**.
    """
    res = val
    if isinstance(val, np.ndarray):
        res = np.squeeze(res)
    return res


def _adapt_type(val):
    """Adapt the type of the input

    - Input parameter:

    :param val: A Python object of any type

    - Output parameter:

    :returns: If the type and content of **val** can be adapted to better match
        the expected types and values used in the ltfatpy functions, the
        adapted version of **val** is returned, otherwise, **val** is returned

    The following conversions are done when **val** is an instance of
    numpy.ndarray:

    - Arrays with dtype numpy.unicode are converted to standard Python
      strings, and if their content is ``u'_bool_True_'`` or
      ``u'_bool_False_'`` they are converted to the corresponding boolean value
      (output of type bool)
    - If the array contains a single value, it is extracted from the array and
      converted to the appropriate Python object. If this value is a float
      having an integer value, it is converted to int.

    """
    res = val
    if isinstance(val, np.ndarray):
        if np.issubdtype(val.dtype, np.str_):
            # convert the unicode numpy arrays to standard unicode strings
            res = val.tolist()
            # convert boolean values
            if val == "_bool_True_":
                res = True
            elif val == "_bool_False_":
                res = False
        elif val.size == 1:
            # convert the single value in the array to the corresponding
            # standard Python object
            res = np.squeeze(val).tolist()
            # force type int for integer values
            if isinstance(res, float):
                if res.is_integer():
                    res = int(res)
    return res


def read_ref_mat(filename, squeeze_arrays=True, adapt_types=True):
    """Read reference data saved in a .mat file

    - Input parameter:

    :param str filename: File name of the .mat file containing reference data
        saved in the expected format using Octave or MATLAB
    :param bool squeeze_arrays: Flag specifying if the arrays must be squeezed
        when reading the data (if ``True``, the dimensions of length 1 are
        removed in the shapes of the arrays)
    :param bool adapt_types: Flag specifying if the data types must be adapted
        when reading the data (if ``True`` the types are adapted, see below for
        details)

    - Output parameters:

    :returns: A list of tuples of the form ``(inputs, outputs)``, each tuple
        giving the outputs expected for a given set of inputs
    :rtype: list
    :var dict inputs: The inputs as expected by the tested Python function
        (note that it implies that there can be some differences with the
        inputs used to generate the data in Octave or MATLAB)
    :var list outputs: The expected outputs when running the tested Python
        function with inputs given in **inputs**

    In Octave or MATLAB, the data must be stored in the .mat file as a cell
    array named ``data``.

    Each item of this cell array must be a cell array containing three cell
    arrays, the first containing the keys of **inputs**, the second the values
    of **inputs**, and the third the values of **outputs**.

    Here is an example to illustrate the expected use:

    In Octave or MATLAB, define the following variable::

        data = {{{'fun', 'dim', 'var'}, {'abs', 1, 1.3}, {[3., 2.2], 1.5}}, ...
                {{'fun', 'do_it'}, {'dgt', '_bool_True_'}, {[1.4, 1.2]}}};

    and save it using the save command::

        save('test_filename.mat', 'data', '-V6');

    In Python, using :func:`read_ref_mat` with::

        read_ref_mat('test_filename.mat')

    you get the following output::

        [({u'dim': 1, u'fun': u'abs', u'var': 1.3}, [array([3. ,  2.2]), 1.5]),
         ({u'do_it': True, u'fun': u'dgt'}, [array([1.4,  1.2])])]


    If ``adapt_types=True``, the following conversions are done for data that
    are an instance of numpy.ndarray:

    - Arrays with dtype numpy.unicode are converted to standard Python
      strings, and if their content is ``u'_bool_True_'`` or
      ``u'_bool_False_'`` they are converted to the corresponding boolean value
      (output of type bool)
    - If the array contains a single value, it is extracted from the array and
      converted to the appropriate Python object. If this value is a float
      having an integer value, it is converted to int.

    """
    data = scipy.io.loadmat(filename, chars_as_strings=True)["data"]
    res = list()
    for item in data[0, :]:
        if item[0, 0].size > 0:
            # the tolist in the following is used to convert the unicode array
            # to standard unicode string
            inputs = dict(
                (
                    (key[0].tolist(), val)
                    for key, val in zip(item[0, 0][0, :], item[0, 1][0, :])
                )
            )
        else:
            inputs = dict()

        outputs = item[0, 2][0, :].tolist()

        if squeeze_arrays:
            inputs = {key: _squeeze_array(val) for key, val in inputs.items()}
            outputs = [_squeeze_array(val) for val in outputs]
        if adapt_types:
            inputs = {key: _adapt_type(val) for key, val in inputs.items()}
            outputs = [_adapt_type(val) for val in outputs]
        res.append((inputs, outputs))
    return res
