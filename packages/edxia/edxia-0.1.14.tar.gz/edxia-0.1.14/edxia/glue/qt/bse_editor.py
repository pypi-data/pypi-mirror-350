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

"""This module is used to edit the BSE directly in glueviz
"""

import os.path

from glue_qt.utils.helpers import load_ui
from glue.config import menubar_plugin


import qtpy.QtWidgets as qtw

from skimage.exposure import rescale_intensity, equalize_adapthist, equalize_hist
from skimage.filters import gaussian
from skimage import transform

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.cm as mpl_cm

import edxia.io.raw_io as raw_io
from edxia.utils.qt import SetBusyApp

class BSEEditor:
    def __init__(self, BSE_array):

        self.orig_bse = BSE_array
        self.previous = BSE_array.copy()
        self.bse = BSE_array.copy()

        self._undo_valid = False

    def _set_undo(self):
        self._undo_valid = True

    @property
    def undo_valid(self):
        return self._undo_valid

    def undo(self):
        self.bse = self.previous.copy()

    def reset(self):
        self.bse = self.orig_bse.copy()
        self.set_previous()

    def set_previous(self):
        self.previous = self.bse.copy()

    def CLAHE(self, **kwargs):
        self.set_previous()
        self.bse = equalize_adapthist(self.bse, **kwargs)
        self._set_undo()

    def equalize(self, **kwargs):
        self.set_previous()
        self.bse = equalize_hist(self.bse, **kwargs)
        self._set_undo()

    def rescale_intensity(self, smin, smax):
        self.set_previous()
        self.bse = rescale_intensity(self.bse, in_range=(smin, smax), out_range=(0.0,1.0))
        self._set_undo()

    def correct_background(self, radius):
        self.set_previous()
        background = gaussian(self.bse, sigma=radius)
        bse = self.bse-background
        self.bse = rescale_intensity(bse, out_range=(0.0,1.0))
        self._set_undo()

    def resize_bse(self, new_shape):
        self.set_previous()
        self.bse = transform.resize(self.bse, new_shape)
        self._set_undo()


class BSEPreview(FigureCanvas):
    palette = mpl_cm.gray
    def __init__(self, parent=None):
        fig = Figure()

        super().__init__(fig)
        self.setParent(parent)


        self.ax1 = fig.add_subplot(1, 2, 1)
        self.ax2 = fig.add_subplot(1, 2, 2) #, sharex=self.ax1, sharey=self.ax1)

        self.ax1.set_aspect("equal")
        self.ax2.set_aspect("equal")

        fig.tight_layout()

    def draw_orig_bse(self, array):
        self.ax1.clear()
        self.ax1.imshow(array, cmap=self.palette, vmin=0, vmax=1.0)

        self.draw_idle()
        self.flush_events()

    def update_bse(self, array):
        self.ax2.clear()
        self.ax2.imshow(array, cmap=self.palette, vmin=0, vmax=1)

        self.draw_idle()
        self.flush_events()

class HistBSE(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()

        super().__init__(fig)
        self.setParent(parent)

        self.ax = fig.add_subplot(1,1,1)

        ax = self.ax
        ax.set_xlim([0,1])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_ticks([])

        fig.subplots_adjust(left=0, top=1, bottom=0.1, right=1)
        self.figure.tight_layout()

    def draw_histogram(self, bse_array):
        ax = self.ax

        ax.clear()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_ticks([])
        _, _, self.hist_patches = ax.hist(bse_array.flatten(), bins=200)

        self.figure.tight_layout()
        self.draw_idle()
        self.flush_events()

        self.cache = self.copy_from_bbox(ax.bbox)

        self.min_slider = ax.axvline(0.0, color="black")
        self.max_slider = ax.axvline(1.0, color="black")

    def draw_sliders(self, smin, smax):
        self.restore_region(self.cache)
        #for patch in self.hist_patches:
        #    self.ax.draw_artist(patch)
        self.min_slider.set_xdata([smin,smin])
        self.ax.draw_artist(self.min_slider)
        self.max_slider.set_xdata([smax,smax])
        self.ax.draw_artist(self.max_slider)
        self.blit(self.ax.bbox)



class BSEEditorDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ui = load_ui('bse_editor.ui', self,
            directory=os.path.dirname(__file__))

        self.bse_editor = None
        self.set_preview()


        ui = self._ui
        ui.browse_in_button.clicked.connect(self.browse)
        ui.filepath_in_edit.editingFinished.connect(self.load_bse)
        ui.clahe_button.clicked.connect(self.clahe)
        ui.reset_button.clicked.connect(self.reset_edition)
        ui.undo_button.clicked.connect(self.undo_edition)

        ui.min_slider.valueChanged.connect(self.draw_sliders)
        ui.max_slider.valueChanged.connect(self.draw_sliders)

        ui.rescale_button.clicked.connect(self.rescale_intensity)
        ui.background_button.clicked.connect(self.correct_background)
        ui.resize_button.clicked.connect(self.resize_bse)

        ui.save_button.clicked.connect(self.save_edited)

    def set_label(self):
        if self.bse_editor is not None:
            shape = self.bse_editor.bse.shape
            self._ui.resolution_label.setText("Resolution: {0} x {1}".format(shape[1], shape[0]))
        else:
            self._ui.resolution_label.setText("Resolution _ x _")

    def set_preview(self):
        self.preview = BSEPreview()
        navbar = NavigationToolbar(self.preview, self)
        layout = qtw.QVBoxLayout()
        layout.addWidget(navbar)
        layout.addWidget(self.preview)

        self._ui.plot_container.setLayout(layout)


        self.hist= HistBSE()
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.hist)

        self._ui.hist_container.setLayout(layout)


    def browse(self):
        path, _ = qtw.QFileDialog.getOpenFileName(None, "Open BSE file", ".","text image (*.csv *txt);;All Files (*)")

        if path == "":
            return

        else:
            self._ui.filepath_in_edit.setText(path)
            self._ui.filepath_in_edit.editingFinished.emit()

    def load_bse(self):
        filename = self._ui.filepath_in_edit.text()
        if filename == "":
            return

        with SetBusyApp():
            self.guessed_format = raw_io.guess_format(filename)
            bse = raw_io.load_txt_map(filename, self.guessed_format)

            self.set_bse_editor(bse)
            self.redraw_all()
            self.enable_buttons()
            self.set_label()

    def set_bse_editor(self, bse):
        self.bse_editor = BSEEditor(bse)

    def undo_edition(self):
        if self.bse_editor.undo_valid:
            self.bse_editor.undo()
            self.draw_bse()

    def reset_edition(self):
        with SetBusyApp():
            self.bse_editor.reset()
            self.redraw_all()

    def redraw_all(self):
        self.preview.draw_orig_bse(self.bse_editor.orig_bse)
        bse = self.bse_editor.bse
        self.preview.update_bse(bse)
        self.hist.draw_histogram(bse)
        self._ui.min_slider.setValue(0)
        self._ui.max_slider.setValue(100)
        self.hist.draw_sliders(0.0, 1.0)

    def draw_bse(self):
        bse = self.bse_editor.bse
        self.preview.update_bse(bse)
        self.hist.draw_histogram(bse)

    def equalize(self):
        self.bse_editor.equalize()
        self.draw_bse()

    def clahe(self):
        self.bse_editor.CLAHE()
        self.draw_bse()

    def rescale_intensity(self):
        mins = self.min_slider.value()/100
        maxs = self.max_slider.value()/100

        self.bse_editor.rescale_intensity(mins, maxs)
        self.draw_bse()
        self.min_slider.setValue(0)
        self.max_slider.setValue(100)


    def enable_buttons(self, enable=True):
        ui = self._ui
        for widget in [
                ui.save_button,
                ui.min_slider,
                ui.max_slider,
                ui.rescale_button,
                ui.equalization_button,
                ui.clahe_button,
                ui.undo_button,
                ui.reset_button,
                ui.background_button,
                ui.background_param_box,
                ui.resize_button,
                ui.resize_row_box,
                ui.resize_col_box
                ]:
            widget.setEnabled(enable)

    def save_edited(self):
        new_path, _ = qtw.QFileDialog.getSaveFileName(None, "Save BSE", ".","csv files (*csv *txt);;All Files (*)")

        if new_path != "":
            write_format = self.guessed_format.copy()
            write_format.max_value = 255
            raw_io.save_txt_map(new_path, self.bse_editor.bse, write_format)

    def draw_sliders(self):

        mins = self.min_slider.value()/100
        maxs = self.max_slider.value()/100

        self.hist.draw_sliders(mins, maxs)

    def correct_background(self):
        param = self._ui.background_param_box.value()
        with SetBusyApp():
            self.bse_editor.correct_background(param)
            self.draw_bse()

    def resize_bse(self):
        rows = self._ui.resize_row_box.value()
        cols = self._ui.resize_col_box.value()
        with SetBusyApp():
            self.bse_editor.resize_bse((rows, cols))
            self.set_label()
            self.draw_bse()

@menubar_plugin("edxia: BSE Editor")
def bse_editor(session, data_collection):
    """The menubar action to analyse the subsets"""
    dialog = BSEEditorDialog() #session, data_collection)
    dialog.exec_()

    return
