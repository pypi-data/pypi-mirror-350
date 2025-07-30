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
This module contains the utilities to describe an experiment.
The main class is :class:`edxia.core.experiment.MappingExperiment`.

"""

from ..utils import path
from ..io import raw_io

class MappingExperiment:
    """This class contains the main information describing an experiment, such
    as the filepaths, the map formats, the list of components... This class is
    shared between many other classes.

    Example:

        exp = MappingExperiment("mymap_{components}.csv", label="OPC 28d")



    :param str pattern: the pattern of the file paths
    :param label: short, unique label for this set of map
    :type label: str or None
    :param str description: optional, longer description
    :type description: str or None
    :param map_format: the file format of the raw EDS maps.
    :type map_format: edxia.io.raw_io.TextMapFormat
    :param bse_format: the file format of the raw EDS maps.
    :type bse_format: edxia.io.raw_io.TextMapFormat
    :param list[str] components: list of available components for this experiment
    """

    _exp_number=0 # variable for automatic labelling of experiments

    def __init__(self, pattern,
                 label=None,
                 description=None,
                 map_format=None, bse_format=None,
                 map_scale_factor=1,
                 components=None):
        self._pattern = pattern
        if description is None:
            description = ""
        if label is None:
            label = str(MappingExperiment._exp_number)
            MappingExperiment._exp_number += 1
        if map_format is None:
            map_format=raw_io.esprit_ascii_map_format
        if bse_format is None:
            bse_format=raw_io.esprit_ascii_bse_format
        self._label = label
        self._description = description
        self._map_format = map_format
        self._bse_format = bse_format
        self._map_scale_factor = map_scale_factor
        if components is None:
            components = path.find_components(pattern)
        self._list_components = components
        if len(self._list_components) == 0:
            raise RuntimeError("No components found for pattern '{0}'".format(pattern))

    @property
    def pattern(self):
        """
        :return: the pattern of filepaths to the maps
        :rtype: str
        """
        return self._pattern

    @property
    def label(self):
        """
        :return: an identifying label for this experiment
        :rtype: str
        """
        return self._label

    @property
    def list_components(self):
        """
        :return: a list of available components
        :rtype: list[str]
        """
        return self._list_components

    @property
    def map_format(self):
        """
        :return: the format of the EDS maps
        :rtype: edxia.io.raw_io.TextMapFormat
        """
        return self._map_format

    @property
    def bse_format(self):
        """
        :return: the format of the raw BSE map
        :rtype: edxia.io.raw_io.TextMapFormat
        """
        return self._bse_format

    def get_path_map(self, component):
        """
        :return: the filepath to the raw map of 'component'
        :rtype: str
        :raises RuntimeError: if the component is not valid
        """
        if component not in self._list_components:
            raise RuntimeError("'{0}' is not a valid component.".format(component))
        return path.find_component_path(self._pattern, component)


    def load_raw_map(self, component):
        """Load the map for a component.

        This is a low-level function, a loader (:mod:`edxia.io.loader`) should be used in normal operations

        :return: a map
        :rtype: a numpy array
        """
        if component == "BSE":
            return raw_io.load_txt_map(self.get_path_map(component), self.bse_format)
        else:
            return raw_io.load_txt_map(self.get_path_map(component),
                                       self.map_format,
                                       resize=self._map_scale_factor
                                       )
    def is_valid(self):
        """Check if the experiment describes a valid set of maps.

        :return: True if the experiment is valid, and the exception otherwise
        :rtype: tuple(bool, Exception or None)
        """
        if len(self._list_components) == 0:
            return (False, RuntimeError("No components found"))
        try:
            amap = self.load_raw_map("BSE")
        except Exception as e:
            return (False, e)
        return (True, None)

class PointsExperiment:
    """
    An experiment describing a EDS point experiment
    """
    def __init__(self,
                 components,
                 label=None,
                 description=None):
        pass

    def is_valid(self):
        """Check if the experiment describes a valid set of maps.

        :return: True if the experiment is valid, and the exception otherwise
        :rtype: tuple(bool, Exception or None)
        """
        return (True, None)


    @property
    def label(self):
        """
        :return: an identifying label for this experiment
        :rtype: str
        """
        return self._label

    @property
    def list_components(self):
        """
        :return: a list of available components
        :rtype: list[str]
        """
        return self._list_components


class PartOfExperiment:
    """
    Base class for a subset of an experiment.


    Classes that should have access to the information provided by
    :class:`edxia.core.experiment.Experiment` should inherit from this class.
    """
    def __init__(self, parent=None):
        self._parent = parent

    @property
    def parent(self):
        """
        :returns: the experiment from which this effect was created
        :rtype: edxia.core.experiment.Experiment
        """
        return self._parent