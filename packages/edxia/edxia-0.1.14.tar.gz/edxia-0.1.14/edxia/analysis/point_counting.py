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

"""This module provides tools for point counting on 2D image
"""

import random
import numpy as np

def make_grid(npimage, nbpoints, fixed_grid=True):
    """A mesh on a 2D image

    - Compute the number of points close to the requested number
    - Also add an offset to "center" the grid

    :param npimage: a 2D numpy array
    :param nbpoints: the requested number of points

    :returns: a 3-tuple: selected rows, selected columns and number of intersection points"""

    if nbpoints <= 0:
        raise ValueError("The number of point should be bigger than 0 !")

    shape = npimage.shape
    if len(shape)  != 2:
        raise ValueError("A 2D image is required ! (ndim={0})".format(len(shape)))

    nrow = shape[0]
    ncol = shape[1]

    ratio = nrow/ncol
    nvtilde = np.sqrt(nbpoints/ratio)
    nutilde = ratio*nvtilde

    if nvtilde>ncol/2 or nutilde>nrow/2:
        raise ValueError("The number of point requested is too high: '{0}'".format(nbpoints))

    # nb points in each direction
    nv = int(np.floor(nvtilde))
    nu = int(np.floor(nutilde))

    # offset
    if fixed_grid:
        v_offset = np.floor((ncol-(np.floor(ncol/nv)*nv))/2)
        u_offset = np.floor((nrow-(np.floor(nrow/nu)*nu))/2)
    else:
        max_v_offset = (ncol-(np.floor(ncol/nv)*nv))-1
        max_u_offset = (nrow-(np.floor(nrow/nu)*nu))-1
        v_offset = random.uniform(1,max_v_offset)
        u_offset = random.uniform(1, max_u_offset)

    vs = np.linspace(v_offset, ncol, nv, endpoint=False, dtype=int)
    us = np.linspace(u_offset, nrow, nu, endpoint=False, dtype=int)

    return (us,vs,nv*nu)

class CountingGrid:
    """A grid to do counting operations on images"""
    def __init__(self, npimage, nbpoints, fixed=True):
        """
        :param npimage: a 2D numpy array
        :param nbpoints: the requested number of points
        """
        self.shape = npimage.shape
        self.us, self.vs, self.n = make_grid(npimage, nbpoints, fixed)
        self.nu = len(self.us)
        self.nv = len(self.vs)

    def count_on_mask(self, mask):
        """Return the point fraction of a mask"""
        if self.shape != mask.shape:
            raise ValueError("Image shape does not correspond to the grid shape")
        asum = 0
        for j in self.vs:
            for i in self.us:
                if mask[i,j]:
                    asum+=1
        return asum/self.n

def multiple_size_counts(npmask):
    """Run multiple point counts on a mask."""
    pts = []
    frac = []
    tot_size = npmask.shape[0]*npmask.shape[1]

    reqpts = np.array([0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25])*tot_size
    for reqpt in reqpts:
        grid = CountingGrid(npmask, reqpt)
        pts.append(grid.n)
        frac.append(grid.count_on_mask(npmask))

    return (pts, frac)

def multiple_counts(npmask, npoints=0.05, n=25):
    """Run multiple point counts on a mask."""
    pts = []
    frac = np.zeros((n,))
    tot_size = npmask.shape[0]*npmask.shape[1]

    reqpt = npoints*tot_size
    for ind in range(n):
        grid = CountingGrid(npmask, reqpt, fixed=False)
        pts.append(grid.n)
        frac[ind] = grid.count_on_mask(npmask)

    return pts[0], frac

if __name__== "__main__":
    img = np.load("../../data/test_data/amask.npy")
    pts, frac = multiple_counts(img, 0.005)

    import matplotlib.pyplot as plt
    plt.semilogx(pts, frac, ".")
    plt.axhline(np.count_nonzero(img)/img.size, color="black")
    print(np.mean(frac))
    print(np.std(frac))
    plt.axhline(np.mean(frac), color="blue")
    plt.axhline(np.mean(frac)+np.std(frac), ls="--", color="blue")
    plt.axhline(np.mean(frac)-np.std(frac), ls="--", color="blue")