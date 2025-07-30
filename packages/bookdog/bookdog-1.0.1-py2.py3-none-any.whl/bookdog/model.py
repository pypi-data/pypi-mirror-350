# -*- coding: utf-8 -*-
# bookdog/model.py

"""This module provides a model to manage the books table."""

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class ImportSqlTableModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.booleanSet = [5]  # column with checkboxes
        self.setTable("books")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.select()
        self.series = self.populateSeries()

    def populateSeries(self):
        s = set()
        query = QSqlQuery()
        query.exec("select series from books")
        while query.next():
            value = query.value(0)
            if len(value):
                s.add(value)
        return s

    def data(self, index, role=Qt.DisplayRole):
        value = super().data(index)
        if index.column() in self.booleanSet:
            if role == Qt.CheckStateRole:
                return Qt.Unchecked if value == 2 else Qt.Checked
            else:
                return QVariant()
        return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if index.column() == 3:  # JHA TODO fix the magic number
            self.series.add(value)
        if index.isValid():
            if index.column() not in self.booleanSet:
                return QSqlTableModel.setData(self, index, value, role)
            if role in (Qt.CheckStateRole, Qt.EditRole):
                val = 0 if value else 2
                return QSqlTableModel.setData(self, index, val, Qt.EditRole)
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() in self.booleanSet:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return QSqlTableModel.flags(self, index)


class BooksModel:
    def __init__(self):
        """Create and set up the model."""
        tableModel = ImportSqlTableModel()
        headers = ("ID", "Title", "Author", "Series", "Date", "Audiobook")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        self.model = tableModel

    def sort(self, column, order):
        """Sort the books by the specified column (default: Date)."""
        self.model.sort(column, order)
        self.model.select()

    def addBook(self, data):
        """Add a book to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def deleteBook(self, row):
        """Remove a book from the Database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
