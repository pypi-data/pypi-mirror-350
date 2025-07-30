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

"""
The :mod:`edxia.io.loader` module offers loader classes to be able to easily
load component maps, composite or map stacks.

Three main loaders are defined:

- :class:`edxia.io.loader.DefaultLoader`: A simple loader, applies the filters every time
- :class:`edxia.io.loader.PickleLoader`: A loader with a cache, apply the filters only once
- :class:`edxia.io.loader.StackLoader`: A loader not working from the filesystem, but using a :class:`edxia.core.map.MapsStack` as an input data.


The main functions are:

- :py:meth:`edxia.io.loader.base_loader.AbstractLoader.load_edsmap`: load a BSE/EDS map, :class:`edxia.core.map.Map`.
- :py:meth:`edxia.io.loader.base_loader.AbstractLoader.load_stack`: load a set of maps, :class:`edxia.core.map.MapsStack`
- :py:meth:`edxia.io.loader.base_loader.AbstractLoader.load_composite`: load a composite map, :class:`edxia.composite.CompositeMap`

"""

from .default_loader import DefaultLoader
from .pickle_loader import PickleLoader
from .stack_loader import StackLoader

__all__ = ["DefaultLoader", "PickleLoader", "StackLoader"]
