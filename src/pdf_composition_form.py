from typing import Optional
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                               QHeaderView, QLabel, QPushButton,
                               QFileDialog, QSpinBox, QWidget,QGroupBox)
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QRect
import sys
import os.path
from pdf_controller import checkPdfDonor, composeToFile
from functools import partial
from pdf_view import PDFPanel

class InputBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setTitle("Please choose donor PDF file to merge")

class CompositorForm(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.input_box = QGroupBox(self)
