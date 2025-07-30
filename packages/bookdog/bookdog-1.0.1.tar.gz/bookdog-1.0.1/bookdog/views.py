# -*- coding: utf-8 -*-

"""This module provides views to manage the books table."""

from PyQt5.QtCore import Qt, pyqtSlot, QDate
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from .model import BooksModel


class TestDelegate(QStyledItemDelegate):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def createEditor(self, parent, option, index):
        series = [""]
        series.extend(sorted(self.model.model.series))
        box = QComboBox(parent)
        edit = QLineEdit(parent)
        box.setLineEdit(edit)
        box.setFrame(False)
        box.addItems(series)
        return box

    # def setEditorData(self, editor, index):
    # return super().setEditorData(editor, index)
    # def setModelData(self, editor, model, index):
    # return super().setModelData(editor, model, index)
    # def updateEditorGeometry(self, editor, option, index):
    # return super().updateEditorGeometry(editor, option, index)


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Bookdog")
        self.resize(
            1550, 1250
        )  # jha todo - this is bigger than my screen - figure out what to do there
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.booksModel = BooksModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setModel(self.booksModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.setColumnHidden(0, True)
        self.table.setItemDelegateForColumn(3, TestDelegate(self.booksModel))
        # Sort by the date column (assumed to be column 4, index 3)
        self.table.sortByColumn(4, Qt.DescendingOrder)
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.addButton.setShortcut("Ctrl+A")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteBook)
        self.deleteButton.setShortcut("Ctrl+D")
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    # JHA not sure what this
    @pyqtSlot()
    def on_add(self):
        pass
        # print("in slot")

    def openAddDialog(self):
        """Open the Add Book dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.booksModel.addBook(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteBook(self):
        """Delete the selected book from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected book?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if messageBox == QMessageBox.Ok:
            self.booksModel.deleteBook(row)


class AddDialog(QDialog):
    """Add Book dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Book")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Add Book dialog's GUI."""
        # Create line edits for data fields
        self.titleField = QLineEdit()
        self.titleField.setObjectName("Title")
        self.authorField = QLineEdit()
        self.authorField.setObjectName("Author")
        self.seriesField = QLineEdit()
        self.seriesField.setObjectName("Series")
        self.dateField = QDateEdit(calendarPopup=True)
        self.dateField.setDisplayFormat("yyyy/MM/dd")
        self.dateField.setDate(QDate.currentDate())
        self.dateField.setObjectName("Date")
        self.audioField = QCheckBox()
        self.audioField.setObjectName("Audio")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Title:", self.titleField)
        layout.addRow("Author:", self.authorField)
        layout.addRow("Series:", self.seriesField)
        layout.addRow("Date:", self.dateField)
        layout.addRow("Audiobook:", self.audioField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.titleField, self.authorField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a book's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return
            self.data.append(field.text())
        # add non-required fields as well
        self.data.append(self.seriesField.text())
        self.data.append(self.dateField.text())
        self.data.append(self.audioField.isChecked())
        if not self.data:
            return
        super().accept()
