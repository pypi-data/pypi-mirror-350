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

"""This module loads EDS points analysis into Glue
"""

import os.path

from glue_qt.utils.helpers import load_ui
from glue.config import importer

import qtpy.QtWidgets as qtw

import pandas as pd

from edxia.glue.create_data import gluedata_from_points
from edxia.utils.qt import PandasTableModel, SetBusyApp

# edxia import

from edxia.point_analysis.points import EDSPoints
from edxia.core.experiment import PointsExperiment

class LoadEDSPointsData(qtw.QDialog):
    """Dialog to load EDS points dataset into the glue interface"""
    def __init__(self, parent=None):
        super().__init__(parent)


        self._ui = load_ui('points_loader.ui', self,
            directory=os.path.dirname(__file__))

        ui = self._ui
        ui.browse_button.clicked.connect(self.browse)

    def browse(self):
        """Browse the filepath to find the dataset"""
        filepath, _ = qtw.QFileDialog.getOpenFileName(None, "Open EDS points", ".","csv files (*.txt *.csv *.dat);;All Files (*)")

        if filepath is None:
            return
        if not os.path.exists(filepath):
            return

        self.set_preview(filepath)
        self._ui.filepath_edit.setText(filepath)

        test_label = os.path.splitext(os.path.basename(filepath))[0]
        self._ui.label_edit.setText(test_label)

    def set_preview(self, path):
        """Set the preview table"""
        with SetBusyApp():
            df = pd.read_csv(path)
            model = PandasTableModel(df)
            self.table.setModel(model)

    def _set_data(self):
        """Read adn transform the data"""
        ui = self._ui

        path = ui.filepath_edit.text()
        if path is None:
            return RuntimeError("No filepath defined")

        data = pd.read_csv(path)
        all_components = list(data.columns)

        exp = PointsExperiment(all_components, label=os.path.basename(path))

        points = EDSPoints(data, exp)

        # non-negativity
        if ui.output_non_negative_box.isEnabled():
            points.set_non_negative()
        # sum of oxide
        if ui.output_sox_box.isEnabled() and ui.output_sox_box.isChecked():
            points.add_sox()
        # mass to atomic
        if ui.input_mass_box.isChecked() or ui.input_mass_norm_box.isChecked():
            if ui.output_atomic_box.isChecked:
                points.to_atomic(copy=False)
        if ui.output_normalize_box.isChecked():
            points.normalize()


        self.results = [gluedata_from_points(ui.label_edit.text(), points),]

    def accept(self):
        """Return the data"""
        with SetBusyApp():
            try:
                self._set_data()
            except Exception as e:
                print(str(e))
                return self.reject()
        return super().accept()

@importer("edxia: Import EDS points")
def load_points():
    """Load EDS points in the glue interface"""
    dialog = LoadEDSPointsData()

    dialog_result = dialog.exec_()
    if dialog_result != qtw.QDialog.Accepted:
        return []

    return dialog.results
