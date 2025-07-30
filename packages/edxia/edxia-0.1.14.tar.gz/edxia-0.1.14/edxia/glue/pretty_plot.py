"""
Tools to replotting and customization of glue figures.


Create the colored image using hue and saturation coloring of grey image.
"""

import numpy as np

from glue.core.state import load
from glue.viewers.image.state import get_sliced_data_maker
import matplotlib.patches as mpatches
from glue.utils import color2rgb
from skimage.color import gray2rgb, rgb2hsv, hsv2rgb
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb


class Layer:
    """Interface to a glue layer"""
    def __init__(self, name, mpl_color, alpha=1):

        self.label = name
        self.set_from_rgb(color2rgb(mpl_color))
        self.a = alpha
        self.enabled = True

    def set_from_rgb(self, color):
        """Set the color from an rgb color"""
        hsv = rgb_to_hsv(color)
        self.h, self.s, self.v = hsv
        self.s = self.s -0.4

    @property
    def hsv(self):
        """Return the color of the layer in hsv space"""
        return (self.h, self.s, self.v)

    @property
    def rgb(self):
        """Return the color of the layer in rgb space"""
        return hsv_to_rgb(self.hsv)

    @property
    def alpha(self):
        """Return the transparency of the layer"""
        return self.a

    @property
    def visible(self):
        """If true, the layer will be displayed"""
        return self.enabled

    @visible.setter
    def set_visible(self, enabled):
        self.enabled = enabled


class LayerInfos:
    """A container for the layers of the image (i.e. the subsets to display)"""
    def __init__(self, map_data):
        self._len = len(map_data.subsets)

        self.layers = []
        self.subset_index = []

        for i in range(self._len):
            subset = map_data.subsets[i]
            self.subset_index.append(i)
            style = subset.style
            self.layers.append(Layer(subset.label, style.color, style.alpha))

    def __len__(self):
        return self._len

    def __getitem__(self, ind):
        return self.layers[ind]

    def reorder(self, new_list):
        """Reorder the layers"""
        self.layers = [self.layers[i] for i in new_list]
        self.subset_index = [self.subset_index[i] for i in new_list]


none_slice = (slice(None, None, None), slice(None, None, None))

class MapDataContainer:
    """A container for the data"""
    def __init__(self, filename):
        self._dc = load(filename)
        self._imap = 0 # map index in dc
        self._pmap = 1
        if self._dc[0].size < self._dc[1].size:
            self._imap = 1
            self._pmap = 0

        self.BSE_shape = self.map_data['BSE', none_slice].shape
        #TODO don't assume calcium
        self.EDS_shape = self.map_data['Ca', none_slice].shape

        self.layers = LayerInfos(self._dc[self._imap])

        #correct value
        hsv_image = rgb2hsv(self.bse_map)
        for il, layer in self.itlayers():
            mask = self.mask_from_layer(il)
            value = np.mean(hsv_image[mask, 2])
            layer.v = value

    @property
    def nb_layers(self):
        """Return the number of layers (subsets) in the map"""
        return len(self.layers)

    def add_layer(self, hsv):
        """Add a layer"""
        self.layers.append(Layer(hsv))

    @property
    def map_data(self):
        """Return the Glue map data"""
        return self._dc[self._imap]

    @property
    def point_data(self):
        """Return the glue point data"""
        return self._dc[self._pmap]

    @property
    def bse_map(self):
        """Return the BSE map"""
        return gray2rgb(self.map_data['BSE', none_slice])

    def hsv(self, il):
        """Return the color of a layer in hsv space"""
        return self.layers[il].hsv

    def rgb(self, il):
        """Return the color of a layer in rgb space"""
        return self.layers[il].rgb

    def label(self, il):
        """Return the label of a layer"""
        return self.layers[il].label

    def set_label(self, il, label):
        """Set the label of the layer"""
        self.layers[il].label = label

    def get_subset(self, il):
        """Return the glue map subset corresponding to a layer"""
        return self.map_data.subsets[self.layers.subset_index[il]]

    def get_point_subset(self, il):
        """Return the glue subset corresponding to a layer"""
        return self.point_data.subsets[self.layers.subset_index[il]]

    def mask_from_layer(self, il):
        """Return the mask of a given layer"""
        subset = self.get_subset(il)
        mask = get_sliced_data_maker(data=subset, x_axis=1, y_axis=0, slices=none_slice)(
            [(0, self.BSE_shape[0], self.EDS_shape[0]),
             (0, self.BSE_shape[1], self.EDS_shape[1])])
        return mask

    def reorder(self, new_order):
        """Reorder the layers"""
        self.layers.reorder(new_order)

    def itlayers(self):
        """Iterator over the layers"""
        for il in range(self.nb_layers):
            layer = self.layers[il]
            if layer.visible:
                yield il, layer

    def set_visible(self, il, b=True):
        """Set a layer to be visible"""
        self.layers[il].visible = b

    def hide_all(self):
        """Hide all layers"""
        for layer in self.layers.layers:
            layer.visible = False

    def unhide_all(self):
        """Set all layers to be visible"""
        for layer in self.layers.layers:
            layer.visible = True

    def tint_bse(self, legend=True):
        """Tint the BSE using the layers"""
        hsv_image = rgb2hsv(self.bse_map)
        if legend:
            legend_handles = []
            legend_labels = []

        for il, layer in self.itlayers():
            mask = self.mask_from_layer(il)
            hsv = layer.hsv
            hsv_image[mask, 0] = hsv[0]
            hsv_image[mask, 1] = hsv[1] #saturation

            if legend:
                handle = mpatches.Patch(color=hsv_to_rgb(hsv))
                legend_handles.append(handle)
                legend_labels.append(layer.label)

        rgb_image = hsv2rgb(hsv_image)

        if legend:
            return rgb_image, (legend_handles, legend_labels)
        else:
            return rgb_image

    def mask_image(self, rgb_image, il, rgb_t_mask):
        """Mask an RGB image given a subset"""
        mask = self.mask_from_layer(il)
        for i in range(3):
            rgb_image[mask, i] = rgb_t_mask[i]
        return rgb_image


    def points_values(self, component, il=None):
        """Return the values from the point, possibly from a subset"""
        if il is None:
            return self.point_data[component]
        else:
            return self.get_point_subset(il)[component]



