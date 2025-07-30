# Copyright (c) 2019 Fabien Georget <fabien.georget@epfl.ch>, EPFL
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""This module computes correlation functions from numpy 2D arrays
"""


import numpy as np
from numba import jit


@jit(nopython=True)
def two_point_correlation_function(binary, size):
    """S2(r) the two point correlation function"""

    rowL = binary.shape[0]
    colL = binary.shape[1]

    s2 = np.zeros((size,))
    num_trials = np.zeros_like(s2)

    for dx in range(size):
        for r in range(rowL):
            for c in range(colL):
                num_trials[dx] += 2
                if binary[r,c] == 0:
                    continue
                r1,c1 = ((r+dx)%rowL, c)
                if binary[r1,c1] == 1:
                    s2[dx] += 1
                r1,c1 = (r, (c+dx)%colL)
                if binary[r1,c1] == 1:
                    s2[dx] += 1
    return s2/num_trials



@jit(nopython=True)
def chord_lengths(binary):
    """Compute the chords length distribution"""

    rowL = binary.shape[0]
    colL = binary.shape[1]

    cs = []

    for r in range(rowL):
        init_chord_length=-1
        for c in range(colL):
            if init_chord_length==-1:
                if binary[r,c] == 0:
                    continue
                else:
                    init_chord_length=c
            else:
                if binary[r,c] == 1:
                    continue
                else:
                    cs.append(c-init_chord_length)
                    init_chord_length=-1
    for c in range(colL):
        init_chord_length=-1
        for r in range(rowL):
            if init_chord_length==-1:
                if binary[r,c] == 0:
                    continue
                else:
                    init_chord_length=r
            else:
                if binary[r,c] == 1:
                    continue
                else:
                    cs.append(r-init_chord_length)
                    init_chord_length=-1
    return cs

def chord_lengths_density(cs, size):
    """Compute the chord-length density function from a distribution of chord-lengths"""
    N = len(cs)
    n, _ = np.histogram(cs, bins=size, range=(0,size), density=False)
    return n/N


def lineal_path(binary, size):
    """Compute the lineal_path function.

    Return the lineal path function and the chord-length density function"""

    rowL = binary.shape[0]
    colL = binary.shape[1]

    cs = chord_lengths(binary)

    lineal_paths = np.zeros((size,))
    for chord in cs:
        for i in range(min(size,chord)):
            lineal_paths[i] += (chord-i)/rowL/colL/2

    p_cs = chord_lengths_density(cs, size)

    return lineal_paths, p_cs