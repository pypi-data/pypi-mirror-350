# Copyright (c) 2019,2020 Fabien Georget <fabien.georget@epfl.ch>, EPFL
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

"""This module loads the quantified EDS maps into Glue
"""


import os.path

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

import qtpy.QtWidgets as qtw
import qtpy.QtGui as qtg
import qtpy.QtCore as qtc
import qtpy.compat as qcompat

from glue.config import importer
from glue_qt.utils.helpers import load_ui
from glue.core.coordinates import AffineCoordinates


## edxia import

from ...core.experiment import MappingExperiment

from edxia.filters import denoise

from edxia.filters.denoise import DenoiseFilter, UniformFilter, GaussianFilter, MedianFilter
from edxia.io.loader import DefaultLoader, StackLoader
from edxia.composite import CompositeChannels
from edxia.composite.segmentation import SlicSegmenter
from edxia.composite.color_analysis import ColorPCA
from edxia.point_analysis.points import points_from_segmentation
from edxia.core import Map

from edxia.io.raw_io import TextMapFormat
from edxia.io import raw_io
from edxia.io.hdf5 import save_dataset, read_dataset

from edxia.utils.qt import SetBusyApp

from .. import gluedata_from_points, gluedata_from_stack_and_composite, gluedata_from_stack


from skimage.filters.rank import median, maximum, minimum
from skimage.morphology import disk



class PreviewBSE(FigureCanvas):
    """Preview the BSE map."""
    def __init__(self, parent=None):
        fig = Figure()
        grid = GridSpec(3,1)
        self.ax = fig.add_subplot(grid[:2,0])
        self.ax_hist = fig.add_subplot(grid[2,0])
        self.ax.axis("off")
        self.ax_hist.set_xlim([0,1])
        self.ax_hist.axis("off")

        super().__init__(fig)
        self.setParent(parent)

    def draw_bse(self, img):
        self.ax.cla()
        self.ax.imshow(img, cmap=plt.cm.gray)

        self.ax_hist.cla()
        self.ax_hist.hist(img.ravel(), bins=100, range=(0,1))
        self.ax_hist.set_xlim([0,1])

        self.figure.tight_layout()

        self.draw()
        self.flush_events()

    def reset_bse(self):
        self.ax.cla()
        self.ax.axis("off")
        self.ax_hist.cla()
        self.ax_hist.axis("off")
        self.draw()
        self.flush_events()


class LoadEDSdata(qtw.QDialog):
    """A dialog to load a glue dataset"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info = {}
        self._ui = load_ui('loader.ui', self,
            directory=os.path.dirname(__file__))

        self.fill_esprit_format()

        self.disable_all_params()

        ui = self._ui

        ui.browse_button.clicked.connect(self.browse_for_pattern)
        ui.pattern_box.editingFinished.connect(self.load_preview)

        ui.browse_dset_button.clicked.connect(self.browse_for_dataset)

        ui.load_esprit_button.clicked.connect(self.fill_esprit_format)
        ui.load_aztec_button.clicked.connect(self.fill_aztec_format)
        ui.load_imagej_button.clicked.connect(self.fill_imagej_format)

        ui.reload_preview_button.clicked.connect(self.format_has_changed)

        ui.test_filter_button.clicked.connect(self.test_filter)
        ui.test_segmentation_button.clicked.connect(self.test_segmentation)

        self.set_preview_canvas()
        self.results = []


    def fill_bse_format(self, bse_format):
        """Fill the bse format tab"""
        ui = self._ui

        ui.format_bse_delim.setText(bse_format.escaped_delimiter)
        ui.format_bse_max.setText(str(bse_format.max_value))
        ui.format_bse_min.setText(str(bse_format.min_value))


    def fill_format(self, eds_format, bse_format):
        """Fill the format tab"""
        ui = self._ui

        ui.format_eds_delim.setText(eds_format.escaped_delimiter)
        ui.format_eds_max.setText(str(eds_format.max_value))
        ui.format_eds_min.setText(str(eds_format.min_value))

        self.fill_bse_format(bse_format)

    def fill_imagej_format(self):
        """Fill the BSE format tab with the imageJ text image format"""
        self.fill_bse_format(raw_io.imagej_ascii_bse_format)
        self.format_has_changed()

    def fill_esprit_format(self):
        """Fill the format tab with the format of Esprit"""
        self.fill_format(raw_io.esprit_ascii_map_format, raw_io.esprit_ascii_bse_format)
        self.format_has_changed()

    def fill_aztec_format(self):
        """Fill the format tab with the format of Aztec"""
        self.fill_format(raw_io.aztec_ascii_map_format, raw_io.aztec_ascii_bse_format)
        self.format_has_changed()

    def get_bse_format(self):
        """Return the EDS format for reading the EDS maps"""
        ui = self._ui

        min_value = float(ui.format_bse_min.text())
        max_value = float(ui.format_bse_max.text())
        txtformat = TextMapFormat(",", min_value, max_value)
        txtformat.escaped_delimiter = ui.format_bse_delim.text()

        return txtformat

    def get_eds_format(self):
        """Return the format for reading the EDS maps"""
        ui = self._ui

        min_value = float(ui.format_eds_min.text())
        max_value = float(ui.format_eds_max.text())
        txtformat = TextMapFormat(",", min_value, max_value)
        txtformat.escaped_delimiter = ui.format_eds_delim.text()

        return txtformat

    def format_has_changed(self):
        """Reset the preview if needed"""
        pattern = self._ui.pattern_box.text()
        if pattern != "":
            self.load_preview()


    def browse_for_pattern(self):
        """Browse the filesystem to find a BSE map and transform as pattern."""
        full_bse_path, _ = qcompat.getopenfilename(self,
                                                   caption="Open BSE map",
                                                   filters="txt files (*.txt *.csv);;All Files (*)")
        try:
            head, tail = full_bse_path.rsplit("BSE", maxsplit=1)
        except ValueError as e:
            print(e)
            return

        pattern = head+"{component}"+tail

        short_text = os.path.basename(head)

        self._ui.short_label_edit.setText(short_text)
        self._ui.pattern_box.setText(pattern)

        # Set dataset pattern
        dset = head+"dset"+tail
        root, ext = os.path.splitext(dset)
        dset = root+".hdf5"
        self._ui.dataset_box.setText(dset)


        self._ui.pattern_box.editingFinished.emit()

    def browse_for_dataset(self):
        ds_path, _ = qcompat.getsavefilename(self, caption="Save dataset",
                                             filters="hdf5 files (*.hdf5);;All Files (*)")

        if ds_path != "":
            self._ui.dataset_box.setText(ds_path)


    def set_preview_canvas(self):
        """Initialize the preview displays"""
        preview_tab = self._ui.preview_tab

        layout = qtw.QVBoxLayout()

        self.bse_preview = PreviewBSE()
        layout.addWidget(self.bse_preview)

        preview_tab.setLayout(layout)

    def load_preview(self):
        """Load a preview."""
        pattern = self._ui.pattern_box.text()
        #label = self._ui.short_label_edit.text()
        print("Selected pattern : {0}".format(pattern))
        try:
            self.preview_exp = MappingExperiment(pattern, map_format=self.get_eds_format(), bse_format=self.get_bse_format())
        except RuntimeError as e:
            self.reset_preview()
            raise RuntimeError(e)

        if self.preview_exp is None:
            self.reset_preview()
            raise RuntimeError("Fail to load the preview experiment: Wrong format ?")

        is_valid, exception = self.preview_exp.is_valid()
        if not is_valid:
            self.reset_preview()
            raise RuntimeError("Fail to load the preview experiment, reason: \n"+str(exception))
        else:
            self.enable_all_params()
            self.set_combo_box()
            self.draw_preview()

    def reset_preview(self):
        self.preview_exp = None
        self.disable_all_params()
        self.bse_preview.reset_bse()


    def draw_preview(self):
        """Draw the preview BSE."""
        loader = DefaultLoader(self.preview_exp, filters=None)
        bse = loader.load_edsmap("BSE")
        self.bse_preview.draw_bse(bse.map)



    def set_combo_box(self):
        """Set the combo boxes in parameters."""
        ui = self._ui
        for combo in [ui.green_combo, ui.red_combo, ui.blue_combo, ui.test_filter_combo]:
            combo.clear()
            combo.addItem("None")
            combo.addItems(self.preview_exp.list_components)

        if "Al" in self.preview_exp.list_components:
            ui.green_combo.setCurrentText("Al")
        if "Si" in self.preview_exp.list_components:
            ui.red_combo.setCurrentText("Si")
        if "Ca" in self.preview_exp.list_components:
            ui.blue_combo.setCurrentText("Ca")

    def enable_all_params(self):
        """Enable the params once the preview is loaded."""
        self._change_all_params(True)

    def disable_all_params(self):
        """Disable all the params if the pattern is not correct"""
        self._change_all_params(False)

    def _change_all_params(self, enabled):
        ui = self._ui

        widgets = [
                ui.no_filter_check,
                ui.tv_filter_check,
                ui.mean_filter_check,
                ui.median_filter_check,
                ui.gaussian_filter_check,
                ui.segmentation_filter_check,

                ui.weight_filter_box,
                ui.radius_filter_box,
                ui.radius_filter_box_2,
                ui.sigma_filter_box,
                ui.nbregions_filter_box,
                ui.compactness_filter_box,


                ui.test_filter_button,
                ui.test_filter_combo,

                ui.segmentation_check,
                ui.test_segmentation_button,

                ui.green_combo,
                ui.red_combo,
                ui.blue_combo,

                ui.green_factor_box,
                ui.red_factor_box,
                ui.blue_factor_box,

                ui.bsemix_check,
                ui.alpha_box,

                ui.numberpts_box,

                ui.filterbse_check,
                ui.minbse_box,
                ]

        for widget in widgets:
            widget.setEnabled(enabled)

        if denoise.jointBilateralFilter is not None:
            ui.joint_filter_check.setEnabled(enabled)
            ui.sigmaS_filter_box.setEnabled(enabled)
            ui.sigmaR_filter_box.setEnabled(enabled)

    def get_experiment(self):
        """Return an experiment."""
        pattern = self._ui.pattern_box.text()
        label = self._ui.short_label_edit.text()
        #description = self._ui.description_box.text()
        description = None

        exp = MappingExperiment(pattern, label, description, map_format=self.get_eds_format(), bse_format=self.get_bse_format())
        return exp

    def get_filters(self, exp):
        """Return the filter to load the maps."""
        if self._ui.tv_filter_check.isChecked():
            weight = float(self._ui.weight_filter_box.text())
            name = "TotalVariation({0})".format(weight)
            filters = [DenoiseFilter(weight),]
        elif self._ui.mean_filter_check.isChecked():
            radius = self._ui.radius_filter_box.value()
            name = "UniformFilter({0})".format(radius)
            filters = [UniformFilter(radius),]
        elif self._ui.median_filter_check.isChecked():
            radius = self._ui.radius_filter_box_2.value()
            name = "MedianFilter({0})".format(radius)
            filters = [MedianFilter(radius),]
        elif self._ui.gaussian_filter_check.isChecked():
            sigma = self._ui.sigma_filter_box.value()
            name = "GaussianFilter({0})".format(sigma)
            filters = [GaussianFilter(sigma),]
        elif self._ui.joint_filter_check.isChecked():
            sigmaR = self._ui.sigmaR_filter_box.value()
            sigmaS = self._ui.sigmaS_filter_box.value()
            name = "JointBilateralFilter({0},{1})".format(sigmaR, sigmaS)
            filters = [denoise.CVJointBilateralFilter(sigmaS, sigmaR, exp),]
        elif self._ui.segmentation_filter_check.isChecked():
            nb_regions = self._ui.nbregions_filter_box.value()
            compactness = self._ui.compactness_filter_box.value()
            name = "SegmentationFilter({0},{1})".format(nb_regions, compactness)
            filters = [denoise.SegmentationFilter(nb_regions, compactness, exp),]
        else:
            name = "NoFilter()"
            filters = None
        return filters, name


    def test_filter(self):
        """Test the filter on a chosen map"""
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            self._test_filter()
        finally:
            qtw.QApplication.restoreOverrideCursor()

    def _test_filter(self):
        """Test the filter on a chosen map"""
        exp =self.preview_exp

        filters, name_filter = self.get_filters(exp)
        input_loader = DefaultLoader(exp, filters=filters)

        comp = self._ui.test_filter_combo.currentText()
        if comp == "None":
            return
        filtered_map = input_loader.load_edsmap(comp)

        dialog = qtw.QDialog(self)
        dialog.setModal(False)

        canvas = TestFilterCanvas(filtered_map.map)
        toolbar = NavigationToolbar(canvas, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        dialog.setLayout(layout)
        dialog.setWindowTitle(name_filter)
        dialog.show()



    def get_scale(self):
        """Return the coordinate system"""
        pixel_size = self._ui.dx_scale_box.value() # in nanometer
        if pixel_size > 0:
            scale = 1e-3*pixel_size # in um/pixel
        else:
            scale = 1.0
        # previously: returned a Map coordinates
        # now used the built-in coordinates in Glue
        # requires glue 1.15 to work
        matrix = np.array([[scale, 0, 0],[0, scale, 0], [0, 0, 1]])
        return AffineCoordinates(matrix=matrix)

    def get_channels(self):
        """Return the channels for the composite."""
        ui = self._ui

        components = []

        for combo in [ui.green_combo, ui.red_combo, ui.blue_combo]:
            comp = combo.currentText()
            if comp == "None":
                comp = None
            components.append(comp)

        factors = []
        for fbox in [ui.red_factor_box, ui.green_factor_box, ui.blue_factor_box]:
            factors.append(fbox.value())

        return CompositeChannels(components, factors)

    def is_mass_input(self):
        return (self._ui.unit_pwt_button.isChecked()
                or self._ui.unit_wt_button.isChecked())

    def test_segmentation(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            self._test_segmentation()
        finally:
            qtw.QApplication.restoreOverrideCursor()

    def _test_segmentation(self):
        ui = self._ui

        exp =self.preview_exp

        filters, _ = self.get_filters(exp)
        loader = DefaultLoader(exp, filters=filters)
        channels = self.get_channels()
        composite = loader.load_composite(channels)
        bse_map =  loader.load_edsmap("BSE")

        if ui.bsemix_check.isChecked():
            composite.mix_with_bse(bse_map, ui.alpha_box.value())
        compactness = float(ui.compactness_box.text())
        numberpts = float(ui.numberpts_box.text())
        labels = SlicSegmenter(compactness, numberpts).apply(composite)

        dialog = qtw.QDialog(self)
        dialog.setModal(False)

        canvas = TestSegmentationCanvas(composite, labels)
        toolbar = NavigationToolbar(canvas, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        dialog.setLayout(layout)
        dialog.setWindowTitle("Segmentation test")
        dialog.show()


    def set_data(self):
        ui = self._ui

        exp = self.get_experiment()
        filters, _ = self.get_filters(exp)
        input_loader = DefaultLoader(exp, filters=filters)
        stack = input_loader.load_stack()
        loader = StackLoader(stack)

        coords = self.get_scale()

        extras = {}



        stack_has_changed = False
        if self.is_mass_input():
            if ui.unit_wt_button.isChecked() and ui.sox_box.isChecked():
                print("Computed sox")
                extras["SOX"] = stack.sum_of_oxides_from_mass()
            if ui.atomic_output_box.isChecked():
                stack = stack.to_atomic()
                stack_has_changed = True

        if ui.normalize_box.isChecked():
            stack.normalize()
            stack_has_changed = True

        if stack_has_changed:
            loader = StackLoader(stack)


        if ui.segmentation_check.isChecked():

            bse_map =  loader.load_edsmap("BSE")
            compactness = float(ui.compactness_box.text())
            numberpts = float(ui.numberpts_box.text())
            segmenter = SlicSegmenter(compactness, numberpts)

            channels = self.get_channels()
            composite = loader.load_composite(channels)

            if ui.bsemix_check.isChecked():
                composite.mix_with_bse(bse_map, ui.alpha_box.value())
            if ui.filterbse_check.isChecked():
                composite.map[bse_map.map<0.2,:] = 0


            if ui.compositesegm_button.isChecked():

                # segmentation
                labels = segmenter.apply(composite)

                pca = ColorPCA(labels)
                pca_transformed = pca.transform_rgb(composite.map)
                extras["PCA1"] = pca_transformed[:,:,0]
                extras["PCA2"] = pca_transformed[:,:,1]
                extras["PCA3"] = pca_transformed[:,:,2]

            elif ui.bsesegm_button.isChecked():
                radius = ui.bsesegm_radius_box.value()
                image = median(bse_map.map, disk(radius))
                image = minimum(maximum(image, disk(radius)), disk(radius))
                bse_filter = Map("BSE", image, exp)
                labels = segmenter.apply(bse_filter)

            # stack and pts data
            stack_data = gluedata_from_stack_and_composite(exp.label+"maps", stack, composite, coords=coords, extras=extras)
            pts = points_from_segmentation(stack, labels, mask_img=composite.map, include_yx=True, extras=extras)
            pts_data = gluedata_from_points(exp.label+"points", pts)

        else:
            composite = None
            pts = None
            stack_data = gluedata_from_stack(exp.label+"maps", stack, coords=coords, extras=extras)

        dset_path = ui.dataset_box.text()
        if dset_path != "":
            save_dataset(dset_path, exp, stack=stack, composite=composite, points=pts, extras=extras)

        self.results.append(stack_data)
        if pts is not None:
            self.results.append(pts_data)

    def accept(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            self.set_data()
        except Exception as e:
            print(e)
            qtw.QApplication.restoreOverrideCursor()
            return self.reject()
        qtw.QApplication.restoreOverrideCursor()
        return super().accept()

@importer("edxia: Import EDS/BSE maps")
def load_maps():
    """Load maps in glue"""
    dialog = LoadEDSdata()

    dialog_result = dialog.exec_()
    if dialog_result != qtw.QDialog.Accepted:
        return []

    return dialog.results

@importer("edxia: Import EDS/BSE maps (dataset)")
def load_dataset():
    """Load maps in glue"""
    full_dset_path, _ = qcompat.getopenfilename(None, caption="Open dataset",
                                                filters="hdf5 files (*.hdf5 *.h5);;All Files (*)")
    results = []

    if full_dset_path == "":
        return results

    with SetBusyApp():
        stack, composite, points, extras = read_dataset(full_dset_path)
        exp = stack.parent
        if composite is None:
            results.append(gluedata_from_stack(exp.label+"maps", stack, extras=extras))
        else:
            results.append(gluedata_from_stack_and_composite(exp.label+"maps", stack, composite, extras=extras)) #, coords)

        if points is not None:
            results.append(gluedata_from_points(exp.label+"points", points))

    return results

class TestFilterCanvas(FigureCanvas):
    """The matplotlib canvas for the test-filter dialog"""
    def __init__(self, npmap, parent=None):

        fig = Figure(constrained_layout=True)

        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)

        self.ax = fig.subplots()
        mappable = self.ax.imshow(npmap, cmap=plt.cm.gray)
        fig.colorbar(mappable)

class TestSegmentationCanvas(FigureCanvas):
    """The matplotlib canvas for the test-segmentation dialog"""
    def __init__(self, composite, labels, parent=None):

        fig = Figure(constrained_layout=True)

        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)

        self.ax1, self.ax2 = fig.subplots(1,2)

        self.ax1.imshow(composite.map)
        self.ax2.imshow(labels.label2rgb())
        self.ax1.set_title("Composite image")
        self.ax2.set_title("Segmented composite")