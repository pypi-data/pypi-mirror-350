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


import os.path
import numpy as np

from skimage.io import imsave
from skimage.util import img_as_ubyte

from glue.config import subset_mask_exporter



@subset_mask_exporter(label='edxia: Numpy', extension=["npy",])
def numpy_mask_exporter(filename, masks):
    """Export a mask as a npy-format file"""
    if len(masks) == 1:
        for (key, val) in masks.items():
            val = np.flipud(val)
            np.save(filename, val)
    else:
        root, ext = os.path.splitext(filename)
        for (key, val) in masks.items():
            nfile = root+"_"+key+ext
            val = np.flipud(val)
            np.save(nfile, val)

@subset_mask_exporter(label='edxia: Numpy text', extension=["txt",])
def numpytxt_mask_exporter(filename, masks):
    """Export a mask as a text format"""
    if len(masks) == 1:
        for (key, val) in masks.items():
            val = np.flipud(val).astype(np.uint8)
            np.savetxt(filename, val, fmt="%i", delimiter=",")
    else:
        root, ext = os.path.splitext(filename)
        for (key, val) in masks.items():
            nfile = root+"_"+key+ext
            val = np.flipud(val).astype(np.uint8)
            np.savetxt(nfile, val, fmt="%i",  delimiter=",")

@subset_mask_exporter(label='edxia: Image', extension=["tif","png","jpg","bmp"])
def image_mask_exporter(filename, masks):
    """Export a mask as a tif image"""
    if len(masks) == 1:
        for (key, val) in masks.items():
            val = img_as_ubyte(np.flipud(val))
            imsave(filename,val)
    else:
        root, ext = os.path.splitext(filename)
        for (key, val) in masks.items():
            nfile = root+"_"+key+ext
            val = img_as_ubyte(np.flipud(val))
            imsave(nfile, val)