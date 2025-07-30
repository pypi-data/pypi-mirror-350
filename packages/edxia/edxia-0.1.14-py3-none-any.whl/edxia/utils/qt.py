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

"""This module provides qt helpers and tools
"""

from contextlib import AbstractContextManager

import numpy as np
import pandas as pd

import qtpy.QtWidgets as qtw
import qtpy.QtGui as qtg
import qtpy.QtCore as qtc

__all__ = ["NumpyTableModel", "PandasTableModel", "EditablePandasTableModel", "SetBusyApp", "set_busy_app"]

class NumpyTableModel(qtc.QAbstractTableModel):
    """Simple model for numpy numerical data to be used in QTableView"""
    def __init__(self, row_labels, column_labels, data, factor=1, parent=None, fmt=None):
        """
        :param row_labels: headers for the rows
        :param column_labels: headers for the columns
        :param data: the numpy array to display
        :param fmt: format to use for the display
        """
        super().__init__(parent)

        self._row_labels = row_labels
        self._column_labels = column_labels
        self._data = data
        self._factor = factor
        if fmt is None:
            fmt = ".2f"
        self._fmt = fmt

    def rowCount(self, parent=None):
        return len(self._row_labels)

    def columnCount(self, parent=None):
        return len(self._column_labels)

    def data(self, index, role=qtc.Qt.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.DisplayRole:
                fmt = "{0:"+self._fmt+"}"
                return fmt.format(
                        self._data[index.row(),index.column()]*self._factor)
        return None

    def appendColumn(self, name, new_col=None):
        """Add a new column to the end of the table

        :param name: the header of the column
        :param new_col: (optional) the new column
        """
        ncol = self._data.shape[1]
        if new_col is None:
            new_col = np.zeros(self._data.shape[0], 1)
        if new_col.shape[0] != self._data.shape[0]:
            raise ValueError("Inconsistent shape for the columns '{0} != {1}'".format(
                   new_col.shape[0],  self._data.shape[0]))
        self.beginInsertColumns(qtc.QModelIndex(),ncol,ncol)
        self._column_labels.append(name)
        if self._data.shape[1] == 0:
            self._data = new_col
        else:
            self._data = np.hstack((self._data,  new_col))
        self.endInsertColumns()

    def headerData(self, rowcol, orientation, role=qtc.Qt.DisplayRole):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._column_labels[rowcol]
        if orientation == qtc.Qt.Vertical and role == qtc.Qt.DisplayRole:
            return self._row_labels[rowcol]
        return None

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= qtc.Qt.ItemIsSelectable
        flags |= qtc.Qt.ItemIsEnabled
        flags |= qtc.Qt.ItemIsDragEnabled
        return flags


class PandasTableModel(qtc.QAbstractTableModel):
    """Simple model for pandas dataframe to be used in QTableView"""
    def __init__(self, dataframe, parent=None):
        """
        :param dataframe: the pandas dataframe to display
        """
        super().__init__(parent)

        self._data = dataframe

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=qtc.Qt.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.DisplayRole:
                value = self._data.iloc[index.row(),index.column()]
                if isinstance(value, str):
                    return value
                else:
                    return "{0:.4f}".format(value)
        return None

    def appendColumn(self, name, new_col=None):
        """Add a new column to the end of the table

        :param name: the header of the column
        :param new_col: (optional) the new column
        """
        if new_col is None:
            new_col = np.zeros((self._data.shape[0], 1))
        self._data[name] = new_col


    def headerData(self, rowcol, orientation, role=qtc.Qt.DisplayRole):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._data.columns[rowcol]
        if orientation == qtc.Qt.Vertical and role == qtc.Qt.DisplayRole:
            return self._data.index[rowcol]
        return None

    def flags(self, index):
        flags = super().flags(index)
        flags |= qtc.Qt.ItemIsSelectable
        flags |= qtc.Qt.ItemIsEnabled
        flags |= qtc.Qt.ItemIsDragEnabled
        return flags

    def get_dataframe(self):
        return self._data

class EditablePandasTableModel(PandasTableModel):

    def __init__(self, dataframe, fixed_columns=None):
        super().__init__(dataframe)
        if fixed_columns is None:
            fixed_columns = []
        self.fixed_columns = fixed_columns

    def setData(self, index, value, role=qtc.Qt.EditRole):
        if role == qtc.Qt.EditRole:
            if isinstance(self._data.iloc[index.row(),index.column()], str):
                try:
                    self._data.iloc[index.row(),index.column()] = value
                except ValueError:
                    return False
                else:
                    return True
            else:
                try:
                    self._data.iloc[index.row(),index.column()] = float(value)
                except ValueError:
                    return False
                else:
                    return True

    def flags(self, index):
        flags = super().flags(index)
        if index.column() not in self.fixed_columns:
            flags |= qtc.Qt.ItemIsEditable
        return flags

class SetBusyApp(AbstractContextManager):
    """A context manager to use the busy cursor in the Qt application"""
    def __enter__(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.WaitCursor))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        qtw.QApplication.restoreOverrideCursor()
        return False

class set_busy_app(object):
    """A decorator to use the busy cursor in the Qt application"""
    def __init__(self, func):
        self.func=func

    def __call__(self, *args, **kwargs):
        with SetBusyApp():
            res = self.func(*args, **kwargs)
        return res