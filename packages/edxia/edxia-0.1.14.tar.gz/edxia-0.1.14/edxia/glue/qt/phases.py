import os.path
import pandas as pd
from glue.config import menubar_plugin


import qtpy.compat as qcompat
import qtpy.QtWidgets as qtw


from glue_qt.utils.helpers import load_ui

from edxia.utils.chemistry import phases_df_from_file, formula_to_composition, normalize_composition
from edxia.glue.phase_data import create_phase_data

from edxia.utils.qt import EditablePandasTableModel

__all__ = ["phases_loader"]

PHASES_LABEL = "Phases"

def get_phases_data(data_collection):
    if "Phases" in data_collection:
        return data_collection[PHASES_LABEL]
    else:
        return None


@menubar_plugin("edxia: load Phases (Experimental !)")
def phases_loader(session, data_collection):
    """The menubar action to load the phases dataset."""
    filename, _ = qcompat.getopenfilename(None, caption="Phase database")

    if filename == "":
        return
    else:
        df = phases_df_from_file(filename)

    phases = get_phases_data(data_collection)
    if phases is None:
        data_collection[PHASES_LABEL] = create_phase_data(df)
    else:
        new_data = create_phase_data(df)
        new_data.label = PHASES_LABEL
        phases.update_values_from_data(new_data)
    return


@menubar_plugin("edxia: edit Phases (Experimental !)")
def phases_editor(session, data_collection):
    phases = get_phases_data(data_collection)
    if phases is None:
        phases_loader(session, data_collection)
        phases = get_phases_data(data_collection)
    if phases is not None:
        dialog = PhasesEditor(phases)
        dialog_result = dialog.exec_()

        if dialog_result != qtw.QDialog.Accepted:
            return
        else:
            phases.update_values_from_data(dialog.results)
    return


class PhasesEditor(qtw.QDialog):
    """Dialog to edit phases in the Glue extension."""

    def __init__(self, phases, parent=None):
        super().__init__(parent)


        self._ui = load_ui('phases.ui', self,
            directory=os.path.dirname(__file__))

        self.set_model(phases)
        self.results = None

        self.add_formula_button.clicked.connect(self.add_phase_by_formula)

    def set_model(self, phases):
        # custom transformation to remove derived components
        df = pd.DataFrame()
        coords = phases.coordinate_components
        derived = phases.derived_components
        for cid in phases.components:
            if cid not in coords and cid not in derived:
                df[cid.label] = phases[cid]

        self.model = EditablePandasTableModel(df, fixed_columns=None)
        self.table.setModel(self.model)

    def add_phase_by_formula(self):
        """Add a phase by formula, rather than adding them by coefficients."""
        dialog = PhaseAddition()
        dialog_result = dialog.exec_()

        if dialog_result != qtw.QDialog.Accepted:
            return

        label, compo = dialog.results
        df = self.model.get_dataframe()
        empty = int(df.index[df["phase"] == ''][0])
        for key, value in compo.items():
            df.loc[empty, key] = float(value)
        df.loc[empty, "phase"] = label


    def _set_data(self):
        df = self.model.get_dataframe()
        df = df.set_index("phase")
        self.results = create_phase_data(df)
        self.results.label = PHASES_LABEL

    def accept(self):
        """Return the data."""
        try:
            self._set_data()
        except Exception as e:
            print(repr(e))
            return self.reject()
        return super().accept()


class PhaseAddition(qtw.QDialog):
    """Dialog to add a phase in the Glue extension."""
    def __init__(self, parent=None):
        super().__init__(parent)


        self._ui = load_ui('phase_add.ui', self,
            directory=os.path.dirname(__file__))

        self.results = None

    def _set_data(self):
        compo = formula_to_composition(self.phase_formula.text())
        compo = normalize_composition(compo)
        label = self.phase_label.text()
        self.results = (label, compo)

    def accept(self):
        """Return the data."""
        try:
            self._set_data()
        except Exception as e:
            print(repr(e))
            return self.reject()
        return super().accept()
