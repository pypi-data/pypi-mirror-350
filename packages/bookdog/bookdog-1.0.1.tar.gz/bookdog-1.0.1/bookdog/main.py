# -*- coding: utf-8 -*-
# bookdog/main.py

"""This module provides bookdog application."""

import pathlib
import shutil
import sys
import time

from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .views import Window


def find_data_file():
    # look for json file in currenct dir first
    filename = "books.sqlite"
    database_file = pathlib.Path(filename)
    if not database_file.exists():
        database_file = pathlib.Path.home() / filename

    if database_file.is_file():
        backup_dir = database_file.parent / ".bookdogBACKUP"
        backup_dir.mkdir(exist_ok=True)
        backup_name = time.strftime("%Y_%m_%d_%H_%M_%S_") + str(database_file)
        backup_file = backup_dir / backup_name
        shutil.copy(database_file, backup_file)

    return database_file


def main():
    """Bookdog main function."""
    app = QApplication(sys.argv)
    database_file = find_data_file()
    if not createConnection(database_file):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())
