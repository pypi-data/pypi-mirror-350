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



import numpy as np
from skimage.restoration import denoise_tv_chambolle
from scipy.ndimage import gaussian_filter, uniform_filter, median_filter
from skimage.segmentation import slic
from skimage.measure import regionprops
#default skimage.filters.rank are on int images

try:
    from cv2.ximgproc import jointBilateralFilter
except ImportError:
    jointBilateralFilter = None

from .base_filter import AbstractFilter


class DenoiseFilter(AbstractFilter):
    """Denoising filter"""
    def __init__(self, weight=0.1, **kwargs):
        self.weight = 0.1
        self.params = kwargs

    def apply_impl(self, np_map):
        return denoise_tv_chambolle(np_map, weight=self.weight, **(self.params))

class UniformFilter(AbstractFilter):
    """Uniform filter"""
    def __init__(self, size, **kwargs):
        self.radius = size
        self.params = kwargs

    def apply_impl(self, np_map):
        return uniform_filter(np_map, size=self.radius, **(self.params))

class MedianFilter(AbstractFilter):
    """Median filter"""
    def __init__(self, size):
        self.radius = size

    def apply_impl(self, np_map):
        return median_filter(np_map, self.radius)

class GaussianFilter(AbstractFilter):
    """GaussianFilter"""
    def __init__(self, sigma, **kwargs):
        self.sigma = sigma
        self.params = kwargs

    def apply_impl(self, np_map):
        return gaussian_filter(np_map, sigma=self.sigma, **(self.params))

class SegmentationFilter(AbstractFilter):
    """Filter based on BSE segmentation"""
    def __init__(self, nb_regions, compactness, exp, **kwargs):
        bse_map = np.float32(exp.load_raw_map("BSE"))
        self.labels = slic(bse_map, n_segments=nb_regions, compactness=compactness, start_label=1, channel_axis=None)

    def apply_impl(self, np_map):
        map_copy = np.copy(np_map)
        for prop in regionprops(self.labels):
            map_copy[prop.slice] = np.mean(np_map[prop.slice])
        return map_copy

if jointBilateralFilter is not None:
    class CVJointBilateralFilter(AbstractFilter):
        def __init__(self, sigma_s, sigma_r, exp):
            self.sigma_s = sigma_s
            self.sigma_r = sigma_r
            self.bse_map = np.float32(exp.load_raw_map("BSE"))

        def apply_impl(self, np_map):
            dst = jointBilateralFilter(self.bse_map, np.float32(np_map), 0, self.sigma_s, self.sigma_r)
            return np.float64(dst)