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

from .base_loader import AbstractLoader
from ...core.map import Map
import os
import os.path
from ..raw_io import load_pickle_map, save_pickle_map
from copy import copy

class PickleLoader(AbstractLoader):
    """This loader cache filtered map so long filtering can be done only once.
    """
    _pickle_extension = ".npy"

    def __init__(self, exp_manager, filters=None, no_BSE_filter=True, remove_previous=True):
        """
        :params exp_manager: The experiment manager
        :params filters: The filters to apply on loading of the math
        :params no_BSE_filter: if True (default), do not filter the BSE map
        :params remove_previous: If True (default), remove existing saved filtered maps
        """
        super().__init__(exp_manager, filters)
        self.no_BSE_filter=True
        if remove_previous:
            self.remove_npy_files()
            self._remove_on_deletion = True
        else:
            self._remove_on_deletion = False

    def __del__(self):
        if self._remove_on_deletion:
            self.remove_npy_files()

    def denoise_and_renormalise(self):
        """Denoise and renormalize all maps.

        This can be used to correctly normalize the maps after filtering.
        Might be useful, or not, depending on the quality of the map.
        """
        components = copy(self.exp_manager.list_components)
        components.remove("BSE")

        # first pass, denoise and compute normalization map
        maps = []
        normalization = None
        for component in components:
            pickle_path = self.get_path_picklemap(component)
            tmap = self.exp_manager.load_raw_map(component)
            eds_map = Map(component, tmap, self.exp_manager)
            for afilter in self.filters:
                afilter.apply(eds_map)
            maps.append(eds_map.map)
            if normalization is None:
                normalization = eds_map.map.copy()
            else:
                normalization += eds_map.map

        # secodn pass, normalize and save
        for ind, component in enumerate(components):
            nmap = maps[ind]/normalization
            pickle_path = self.get_path_picklemap(component)
            save_pickle_map(pickle_path, nmap)


    def get_path_picklemap(self, component):
        """Return the path to the pickle map of 'component'."""
        path = self.exp_manager.get_path_map(component)
        return (os.path.splitext(path)[0] +
                               PickleLoader._pickle_extension)

    def remove_npy_files(self):
        """Remove existing pickle files."""
        for component in self.exp_manager.list_components:
            path = self.get_path_picklemap(component)
            if os.path.exists(path):
                #pass
                os.remove(path)

    def reset_filters(self, filters):
        """Reset the filters"""
        self.remove_npy_files()
        self._filters = filters

    def load_edsmap_single(self, component):
        """Load a map.

        Search the cache first if such a map exist.
        """
        pickle_path = self.get_path_picklemap(component)
        if os.path.exists(pickle_path):
            npy_exists = True
            tmap = load_pickle_map(pickle_path)
        else:
            npy_exists = False
            tmap = self.exp_manager.load_raw_map(component)

        eds_map = Map(component, tmap, self.exp_manager)

        if not npy_exists:
            if component != "BSE" or not self.no_BSE_filter:
                for afilter in self.filters:
                    afilter.apply(eds_map)
            save_pickle_map(pickle_path, eds_map.map)
        return eds_map