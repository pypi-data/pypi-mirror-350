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


cdef enum dgt_phasetype:
    FREQINV = 0
    TIMEINV = 1

ctypedef size_t ltfatInt

# Values extracted from fftw3.h
cdef enum dct_kind:
    DCTI = 3
    DCTIII = 4
    DCTII = 5
    DCTIV = 6

# Values extracted from fftw3.h
cdef enum dst_kind:
    DSTI = 7
    DSTIII = 8
    DSTII = 9
    DSTIV = 10


# pgauss functions declarations
cdef extern void pgauss_d(const ltfatInt L, const double w, const double c_t,
                          double * g)

cdef extern void pgauss_cmplx_d(const ltfatInt L, const double w,
                                const double c_t, const double c_f,
                                const double complex * g)

# DGT functions declarations
cdef extern void dgt_long_cd(const double complex * f,
                             const double complex * g,
                             const ltfatInt L, const ltfatInt W,
                             const ltfatInt a, const ltfatInt M,
                             const dgt_phasetype ptype, double complex * cout)

cdef extern void dgt_long_d(const double * f, const double * g,
                            const ltfatInt L, const ltfatInt W,
                            const ltfatInt a, const ltfatInt M,
                            const dgt_phasetype ptype, double complex * cout)

cdef extern void dgtreal_long_d(const double * f, const double * g,
                                const ltfatInt L, const ltfatInt W,
                                const ltfatInt a, const ltfatInt M,
                                const dgt_phasetype ptype,
                                double complex * cout)

cdef extern void dgt_fb_cd(const double complex * f, const double complex * g,
                           const ltfatInt L, const ltfatInt gl,
                           const ltfatInt W, const ltfatInt a,
                           const ltfatInt M, const dgt_phasetype ptype,
                           double complex * cout)

cdef extern void dgt_fb_d(const double * f, const double * g,
                          const ltfatInt L, const ltfatInt gl,
                          const ltfatInt W, const ltfatInt a,
                          const ltfatInt M, const dgt_phasetype ptype,
                          double complex * cout)

cdef extern void dgtreal_fb_d(const double * f, const double * g,
                              const ltfatInt L, const ltfatInt gl,
                              const ltfatInt W, const ltfatInt a,
                              const ltfatInt M, const dgt_phasetype ptype,
                              double complex * cout)

cdef extern void idgt_fb_d(const double complex * F, const double complex * g,
                           const ltfatInt L, const ltfatInt gl,
                           const ltfatInt W, const ltfatInt a,
                           const ltfatInt M, const dgt_phasetype ptype,
                           double complex * f)

cdef extern void idgtreal_fb_d(const double complex * F, const double * g,
                               const ltfatInt L, const ltfatInt gl,
                               const ltfatInt W,
                               const ltfatInt a, const ltfatInt M,
                               const dgt_phasetype ptype, double * f)

cdef extern void idgt_long_d(const double complex * F,
                             const double complex * g,
                             const ltfatInt L, const ltfatInt W,
                             const ltfatInt a, const ltfatInt M,
                             const dgt_phasetype ptype,
                             double complex * f)

cdef extern void idgtreal_long_d(const double complex * F, const double * g,
                                 const ltfatInt L, const ltfatInt W,
                                 const ltfatInt a, const ltfatInt M,
                                 const dgt_phasetype ptype, double * f)

cdef extern void gabdual_long_d(const double * g,
                                const ltfatInt L, const ltfatInt R,
                                const ltfatInt a,
                                const ltfatInt M, double * gd)

cdef extern void gabdual_long_cd(const double complex * g,
                                 const ltfatInt L, const ltfatInt R,
                                 const ltfatInt a,
                                 const ltfatInt M, double complex * gd)

cdef extern void gabtight_long_d(const double * g,
                                 const ltfatInt L, const ltfatInt R,
                                 const ltfatInt a, const ltfatInt M,
                                 double * gd)

cdef extern void gabtight_long_cd(const double complex * g,
                                  const ltfatInt L, const ltfatInt R,
                                  const ltfatInt a, const ltfatInt M,
                                  double complex * gd)

cdef extern void dct_d(const double * f, const ltfatInt L, const ltfatInt W,
                       double * cout, const dct_kind kind)

cdef extern void dct_cd(const double complex * f, const ltfatInt L,
                        const ltfatInt W, double complex * cout,
                        const dct_kind kind)

cdef extern void dst_d(const double * f, const ltfatInt L, const ltfatInt W,
                       double * cout, const dst_kind kind)

cdef extern void dst_cd(const double complex * f, const ltfatInt L,
                        const ltfatInt W, double complex * cout,
                        const dst_kind kind)

