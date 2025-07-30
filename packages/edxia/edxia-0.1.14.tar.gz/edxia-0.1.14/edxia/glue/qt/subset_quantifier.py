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

"""This module provides interfaces to analyse image datasets

Implemented options so far:
    - Point fractions
    - Surface fractions
    - S2 correlations functions
    - Lineal paths/chord lengths
"""

import os.path

import qtpy.QtWidgets as qtw
import qtpy.QtGui as qtg
import qtpy.QtCore as qtc

import numpy as np

from glue_qt.utils.helpers import load_ui
from glue.config import menubar_plugin
from glue.core.subset import SubsetState, InvertState


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from edxia.analysis.helpers import find_image_datasets, find_points_datasets
from edxia.analysis.correlation import two_point_correlation_function, lineal_path
from edxia.analysis.point_counting import multiple_counts
from edxia.utils.qt import NumpyTableModel

class QuantifySubsets(qtw.QDialog):
    """The main dialog to quantify all the subsets, should be replaced by a submenu if possible"""
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)

        self.session = session
        self.dc = data_collection

        self._ui = load_ui('main_quantifier.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))

        self._ui.surface_fraction_button.clicked.connect(self.run_surface_fraction)
        self._ui.s2_correlation_button.clicked.connect(self.run_s2_correlation)
        self._ui.chord_button.clicked.connect(self.run_chord_lineal)
        self._ui.point_fraction_button.clicked.connect(self.run_point_fraction)
        self._ui.composition_button.clicked.connect(self.run_composition)

    def run_surface_fraction(self):
        dialog = SurfaceFractionQuantifier(self.session, self.dc)
        dialog.exec_()
        return

    def run_s2_correlation(self):
        dialog = S2CorrelationQuantifier(self.session, self.dc)
        dialog.exec_()
        return

    def run_chord_lineal(self):
        dialog = ChordCorrelationQuantifier(self.session, self.dc)
        dialog.exec_()
        return

    def run_point_fraction(self):
        dialog = PointFractions(self.session, self.dc)
        dialog.exec_()
        return

    def run_composition(self):
        dialog = CompositionQuantifier(self.session, self.dc)
        dialog.exec_()
        return


@menubar_plugin("edxia: Analyse phase subsets")
def subset_quantifier(session, data_collection):
    """The menubar action to analyse the subsets"""
    dialog = QuantifySubsets(session, data_collection)
    dialog.exec_()

    return

######################
# Surface fractions  #
######################

class TableMixin:
    """This is a mixin class for dialog containing a main table

    It allows to copy multiple selection to the clipboard.

    Requirements: the table should be accessible as self.table
    """
    def set_event_filter(self):

        self.table.installEventFilter(self)

    def keyPressEvent(self, event):
        """Filter for the table events."""
        if len(self.table.selectedIndexes()) > 0:
            if event.matches(qtg.QKeySequence.Copy):
                self.copy_selection()
        else:
            super().keyPressEvent(event);

    def eventFilter(self, source, event):
        if (event.type() == qtc.QEvent.KeyPress and
            event.matches(qtg.QKeySequence.Copy)):
            self.copy_selection()
            return True
        return qtw.QDialog.eventFilter(self,source, event)

    def copy_selection(self):
        """Copy the selection into a csv format to be paste in spreadheets."""
        selection = self.table.selectionModel()

        # Copy one value
        if len(selection.selectedIndexes()) == 1:
            index = selection.selectedIndexes()[0]

            sys_clip = qtw.QApplication.clipboard()
            sys_clip.setText(index.data())
        # Copy several values: add headers
        elif len(selection.selectedIndexes()) > 1:

            # Find the row/columns and the correspondign headers
            row_labels = ["",]
            row_ind = [-1,]

            column_labels = ["",]
            column_ind = [-1,]


            tmp_rows = []
            tmp_cols = []
            for index in selection.selectedIndexes():
                tmp_rows.append(index.row())
                tmp_cols.append(index.column())
            tmp_rows = list(set(tmp_rows))
            tmp_cols = list(set(tmp_cols))
            tmp_rows.sort()
            tmp_cols.sort()

            for row in tmp_rows:
                row_ind.append(row)
                row_labels.append(self.model.headerData(row,qtc.Qt.Vertical))

            for col in tmp_cols:
                column_ind.append(col)
                column_labels.append(self.model.headerData(col,qtc.Qt.Horizontal))


            nrows = len(row_labels)
            ncols = len(column_labels)

            # prepare data
            data = np.zeros((len(row_labels),len(column_labels)))

            for index in selection.selectedIndexes():
                r = index.row()
                c = index.column()
                new_r = row_ind.index(r)
                new_c = column_ind.index(c)
                data[new_r,new_c] = self.model._data[r,c]

            # Set to the correct format
            to_copy = "\t".join(column_labels)
            to_copy += '\n'

            for r in range(1,nrows):
                to_copy += row_labels[r] + '\t'
                for c in range(1,ncols):
                    to_copy += "{:.6f}".format(data[r, c])
                    if c != (ncols-1):
                        to_copy += '\t'
                to_copy += '\n'

            # copy to the system clipboard
            sys_clip = qtw.QApplication.clipboard()
            sys_clip.setText(to_copy)


class SurfaceFractionQuantifier(qtw.QDialog, TableMixin):
    """Compute and display the surface fractions."""
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)
        self._ui = load_ui('surface_fractions.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))

        self.set_event_filter()

        self.session = session
        self.dc = data_collection



        self.model = None
        self.fill_table()

    def compute_surface_fractions(self):
        """Compute the surface fractions for all available image datasets and
        all subsets."""
        # find datasets
        datas = find_image_datasets(self.dc)
        datas_labels = [data.label for data in datas]

        # normalisation values
        all_state = InvertState(SubsetState())
        norms = []
        for data in datas:
            norms.append(np.count_nonzero(data.get_mask(all_state)))

        surface_fractions = []
        subset_labels = []
        for subset_grp in self.dc.subset_groups:
            state = subset_grp.subset_state
            subset_labels.append(subset_grp.label)
            frac = []
            for ind, data in enumerate(datas):
                frac.append(np.count_nonzero(data.get_mask(state))/norms[ind])
            surface_fractions.append(frac)

        surface_fractions = np.array(surface_fractions)

        return datas_labels, subset_labels, surface_fractions

    def fill_table(self):
        """Fill the table widget."""
        datas_labels, subset_labels, surface_fractions = self.compute_surface_fractions()

        self.model = NumpyTableModel(subset_labels, datas_labels, surface_fractions, factor=100)
        self.table.setModel(self.model)



###################
#   Composition   #
###################

class CompositionQuantifier(qtw.QDialog, TableMixin):
    """Compute and display the composition (average and standard deviation),
    for a chosen subset."""
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)
        self._ui = load_ui('composition.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))

        self.set_event_filter()

        self.session = session
        self.dc = data_collection

        for subset in self.dc.subset_groups:
            self._ui.subset_box.addItem(subset.label, subset)
        for data in self.dc.data:
            self._ui.data_box.addItem(data.label, data)

        self._ui.compute_button.clicked.connect(self.compute_composition)

        self.model = None

    def compute_composition(self):
        """Compute the average and standard deviations of the components."""
        subset_grp = self._ui.subset_box.currentData()
        subset_state = subset_grp.subset_state
        data = self._ui.data_box.currentData()

        indexes = subset_state.to_index_list(data)

        col_labels = ["E", "sigma"]
        row_labels = []
        npdata = np.zeros((len(data.components), 2))

        for ind, comp in enumerate(data.components):
            row_labels.append(comp.label)
            npa = data[comp].flat[indexes]
            npdata[ind,0] = npa.mean()
            npdata[ind,1] = npa.std()

        self.model = NumpyTableModel(row_labels, col_labels, npdata, fmt=".3f")
        self.table.setModel(self.model)




############################
# S2 Correlation functions #
############################

class S2Plot(FigureCanvas):
    """Figure canvas for the S2 function plot"""
    def __init__(self, parent=None):
        fig = Figure(constrained_layout=True)
        self.ax = fig.add_subplot(1,1,1)
        self.ax.set_xlabel(r"$r$ (pixel)")
        self.ax.set_ylabel(r"$S_2(r)$")

        self.ax.set_ylim([0,1])
        self.ax.set_xlim([0,200])

        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)

    def set_ylim(self, size):
        self.ax.set_xlim([0,size])

    def plot(self, xs, ys, label=None):
        self.ax.plot(xs, ys, label=label)
        if label is not None:
            self.ax.legend()
        self.draw()
        self.flush_events()

class S2Display(qtw.QWidget):
    """The plot area for the correlation functions"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = S2Plot(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def set_ylim(self, size):
        self.canvas.set_size(size)

    def plot(self, data, label):
        size = data.shape[0]
        xs = np.arange(0,size)
        self.canvas.plot(xs, data, label)


class S2CorrelationQuantifier(qtw.QDialog):
    """Compute the S2 correlation functions, and display it"""
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)

        self.session = session
        self.dc = data_collection

        self._ui = load_ui('s2_correlation.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))
        self.setWindowTitle("S2 correlation function")
        self.plot_widget = S2Display()
        container_layout = qtw.QVBoxLayout()
        container_layout.addWidget(self.plot_widget)
        self._ui.plot_container.setLayout(container_layout)

        self._ui.compute_button.clicked.connect(self.compute)
        self._ui.save_button.clicked.connect(self.save_to_file)
        self._ui.clipboard_button.clicked.connect(self.copy_to_clipboard)

        self.fill_combo_boxes()

        self.all_data = np.zeros((1,1))
        self.all_data_labels = ["pixel",]

    def fill_combo_boxes(self):
        """Fill the options in the combo box"""
        # fill dataset combo box
        datas = find_image_datasets(self.dc)
        cb = self._ui.dataset_box
        cb.clear()
        for ds in datas:
            cb.addItem(ds.label, ds)

        # fill subset combo box
        cb = self._ui.subset_box
        cb.clear()
        for subset_grp in self.dc.subset_groups:
            cb.addItem(subset_grp.label, subset_grp)

    def compute(self):
        """ Compute the S2-correlation functions"""
        ui = self._ui
        data = ui.dataset_box.currentData()
        subset_grp = ui.subset_box.currentData()

        mask = data.get_mask(subset_grp.subset_state)

        size =  ui.size_box.value()
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            s2f = two_point_correlation_function(mask, size)
            label = "{0}-{1}".format(data.label,subset_grp.label)
            self.plot_widget.plot(s2f, label)
            self.add_to_data(s2f, label)
        finally:
            qtw.QApplication.restoreOverrideCursor()

    def add_to_data(self, s2f, label):
        """Add the correlation function to the numerical data cache, to be saved"""
        size = s2f.shape[0]

        current_shape = self.all_data.shape
        if size > current_shape[0]:
            tmp = np.zeros((size, current_shape[1]+1))
            tmp[:,0] = np.arange(0,size)
            if current_shape[1] > 1:
                tmp[:current_shape[0],1:] = self.all_data[:,1:]
            tmp[:s2f.shape[0],-1] = s2f
            self.all_data = tmp
        else:
            tmp = np.zeros((current_shape[0], current_shape[1]+1))
            tmp[:,:-1] = self.all_data[:,:]
            tmp[:,-1] = s2f
            self.all_data = tmp

        self.all_data_labels.append(label)

    def copy_to_clipboard(self):
        """Copy the numerical data to the system clipdoard"""
        to_copy = "\t".join(self.all_data_labels)
        to_copy += '\n'

        data = self.all_data
        for r in range(data.shape[0]):
            for c in range(data.shape[1]):
                to_copy += "{:.6f}".format(data[r, c])
                if c != data.shape[1]:
                    to_copy += '\t'
            to_copy += '\n'

            # copy to the system clipboard
            sys_clip = qtw.QApplication.clipboard()
            sys_clip.setText(to_copy)

    def save_to_file(self):
        """Save the numerical data to the clipboard"""
        path, _ = qtw.QFileDialog.getSaveFileName(None, "Save dataset", ".","csv file (*.csv *.txt *.dat);;All Files (*)")

        if path != "":
            np.savetxt(path, self.all_data, "%.6f",delimiter="\t", header="\t".join(self.all_data_labels))




#############################
#  LinealPath/chord lengths #
#############################

class ChordPlot(FigureCanvas):
    """Figure canvas for the S2 function plot"""
    def __init__(self, parent=None):
        fig = Figure(constrained_layout=True)

        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)


        self.ax1, self.ax2 = fig.subplots(1,2)
        self.ax1.set_xlabel(r"$r$ (pixel)")
        self.ax1.set_ylabel(r"Lineal path")
        self.ax2.set_xlabel(r"$r$ (pixel)")
        self.ax2.set_ylabel(r"chord_lengths")

        self.ax1.set_ylim([0,1])
        self.ax1.set_xlim([0,200])
        self.ax2.set_ylim([0,1])
        self.ax2.set_xlim([0,200])

    def plot(self, xs, lp, cs, label=None):
        line, = self.ax1.plot(xs, lp, label=label)
        if label is not None:
            self.ax1.legend()

        self.ax2.plot(xs, cs, ".", label=label, color=line.get_color())
        if label is not None:
            self.ax2.legend()


        self.ax1.set_xlim([0,xs[-1]])
        self.ax2.set_xlim([0,xs[-1]])

        self.draw()
        self.flush_events()

class ChordDisplay(qtw.QWidget):
    """The plot area for the correlation functions"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = ChordPlot(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)


    def plot(self, lp, cs, label):
        size = lp.shape[0]
        xs = np.arange(1,size+1)
        self.canvas.plot(xs, lp, cs, label)


class ChordCorrelationQuantifier(qtw.QDialog):
    """Compute the S2 correlation functions, and display it"""
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)

        self.session = session
        self.dc = data_collection

        self._ui = load_ui('s2_correlation.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))
        self.setWindowTitle("Chord lengths / Lineal paths")
        self.plot_widget = ChordDisplay()
        container_layout = qtw.QVBoxLayout()
        container_layout.addWidget(self.plot_widget)
        self._ui.plot_container.setLayout(container_layout)

        self._ui.compute_button.clicked.connect(self.compute)
        self._ui.save_button.clicked.connect(self.save_to_file)
        self._ui.clipboard_button.clicked.connect(self.copy_to_clipboard)

        self.fill_combo_boxes()

        self.all_data = np.zeros((1,1))
        self.all_data_labels = ["pixel",]

    def fill_combo_boxes(self):
        """Fill the options in the combo box"""
        # fill dataset combo box
        datas = find_image_datasets(self.dc)
        cb = self._ui.dataset_box
        cb.clear()
        for ds in datas:
            cb.addItem(ds.label, ds)

        # fill subset combo box
        cb = self._ui.subset_box
        cb.clear()
        for subset_grp in self.dc.subset_groups:
            cb.addItem(subset_grp.label, subset_grp)

    def compute(self):
        """ Compute the lineal path function"""
        ui = self._ui
        data = ui.dataset_box.currentData()
        subset_grp = ui.subset_box.currentData()

        mask = data.get_mask(subset_grp.subset_state)

        size =  ui.size_box.value()
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            lp, cs = lineal_path(mask, size)
            label = "{0}-{1}".format(data.label,subset_grp.label)
            self.plot_widget.plot(lp,cs,label)
            self.add_to_data(lp, cs, label)
        finally:
            qtw.QApplication.restoreOverrideCursor()

    def add_to_data(self, lp, cs, label):
        """Add the correlation function to the numerical data cache, to be saved"""
        size = lp.shape[0]

        current_shape = self.all_data.shape
        if size > current_shape[0]:
            tmp = np.zeros((size, current_shape[1]+2))
            tmp[:,0] = np.arange(1,size+1)
            if current_shape[1] > 1:
                tmp[:current_shape[0],1:] = self.all_data[:,1:]
            tmp[:lp.shape[0],-2] = lp
            tmp[:lp.shape[0],-1] = cs
            self.all_data = tmp
        else:
            tmp = np.zeros((current_shape[0], current_shape[1]+2))
            tmp[:,:-2] = self.all_data[:,:]
            tmp[:,-2] = lp
            tmp[:,-1] = cs
            self.all_data = tmp

        self.all_data_labels.append(label+"-lineal path")
        self.all_data_labels.append(label+"-chord length")

    def copy_to_clipboard(self):
        """Copy the numerical data to the system clipdoard"""
        to_copy = "\t".join(self.all_data_labels)
        to_copy += '\n'

        data = self.all_data
        for r in range(data.shape[0]):
            for c in range(data.shape[1]):
                to_copy += "{:.6f}".format(data[r, c])
                if c != data.shape[1]:
                    to_copy += '\t'
            to_copy += '\n'

            # copy to the system clipboard
            sys_clip = qtw.QApplication.clipboard()
            sys_clip.setText(to_copy)

    def save_to_file(self):
        """Save the numerical data to the clipboard"""
        path, _ = qtw.QFileDialog.getSaveFileName(None, "Save dataset", ".","csv file (*.csv *.txt *.dat);;All Files (*)")

        if path != "":
            np.savetxt(path, self.all_data, "%.6f",delimiter="\t", header="\t".join(self.all_data_labels))


##################
# Point counting #
##################


class PointPlot(FigureCanvas):
    """Figure canvas for the point fractions boxplots"""
    def __init__(self, parent=None):
        fig = Figure(constrained_layout=True)
        self.ax = fig.add_subplot(1,1,1)
        self.ax.set_ylabel(r"Point fraction")

        #self.ax.set_ylim([0,1])

        self._data = []
        self._labels = []


        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)

    def plot(self, frac, label=None):
        """Plot the boxplot

        :param frac: array of point fractions
        :param label: label of the serie of points
        """
        if label is None:
            label = ""

        self._data.append(frac)
        self._labels.append(label)

        self.ax.clear()
        self.ax.set_ylabel(r"Point fraction")
        self.ax.boxplot(self._data, labels=self._labels)

        self.draw()
        self.flush_events()

class PointDisplay(qtw.QWidget):
    """The plot area for the point fractions"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = PointPlot(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)


    def plot(self, frac, label):
        self.canvas.plot(frac, label)


class PointFractions(qtw.QDialog, TableMixin):
    def __init__(self, session, data_collection, parent=None):
        super().__init__(parent)
        self._ui = load_ui('point_fractions.ui', self,
            directory=os.path.join(os.path.dirname(__file__), "quantifier"))
        self.set_event_filter()


        self.session = session
        self.dc = data_collection


        self.plot_widget = PointDisplay()
        container_layout = qtw.QVBoxLayout()
        container_layout.addWidget(self.plot_widget)
        self._ui.plot_container.setLayout(container_layout)

        self._ui.compute_button.clicked.connect(self.compute)
        self._ui.compute_all_button.clicked.connect(self.compute_all)


        self.fill_combo_boxes()

        data = np.zeros((3,0))
        column_labels = []
        row_labels = ["<Pi/Pn>", "stdev", "Si/Sn"]

        self.model = NumpyTableModel(row_labels, column_labels, data, factor=100)
        self.table.setModel(self.model)

    def fill_combo_boxes(self):
        """Fill the options in the combo box"""
        # fill dataset combo box
        datas = find_image_datasets(self.dc)
        cb = self._ui.dataset_box
        cb.clear()
        for ds in datas:
            cb.addItem(ds.label, ds)

        # fill subset combo box
        cb = self._ui.subset_box
        cb.clear()
        for subset_grp in self.dc.subset_groups:
            cb.addItem(subset_grp.label, subset_grp)

    def _compute(self, data, subset_grp, frac, rep):
        """Compute point fractions for a subset of a dataset

        :param data: The glue dataset
        :param subset_grp: The glue subset group
        :param frac: fraction of total points to use
        :param rep: The number of repetitions
        """
        mask = data.get_mask(subset_grp.subset_state)
        pts, frac = multiple_counts(mask, frac, rep)

        col = np.zeros((3,1))
        col[0,0] = np.mean(frac)
        col[1,0] = np.std(frac)
        col[2,0] = np.count_nonzero(mask)/data.size

        label = "{0}-{1}".format(data.label,subset_grp.label)
        self.model.appendColumn(label, new_col=col)
        self.plot_widget.plot(frac, label)

    def compute(self):
        """Compute the point fractions for the current subset and the current dataset"""
        ui = self._ui
        data = ui.dataset_box.currentData()
        subset_grp = ui.subset_box.currentData()

        frac = ui.fraction_box.value()
        rep = ui.repetitions_box.value()

        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            self._compute(data, subset_grp, frac, rep)
        finally:
            qtw.QApplication.restoreOverrideCursor()

    def compute_all(self):
        """Compute the point fractions for all subsets and all datasets available."""
        ui = self._ui
        frac = ui.fraction_box.value()
        rep = ui.repetitions_box.value()

        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        try:
            ds = ui.dataset_box
            ss = ui.subset_box
            for j in range(ss.count()):
                for i in range(ds.count()):
                    self._compute(ds.itemData(i), ss.itemData(j), frac, rep)
        finally:
            qtw.QApplication.restoreOverrideCursor()



