import sys
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget,  QFormLayout,
                               QGridLayout, QPushButton, QGroupBox, 
                               QLineEdit, QDateEdit, QSplitter, 
                               QListView,QListWidgetItem, QHBoxLayout,
                               QFileDialog)
from PySide6.QtCore import Qt

class PdfFilesListView(QListView):
    def __init__(self, parent):
        QListView.__init__(self, parent)

class PDFFileLine(QListWidgetItem):
    def __init__(self, parent):
        QListWidgetItem.__init__()

class MainBox(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, 'Personal Information', parent)
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        form_layout.addRow('First Name:', QLineEdit(self))
        form_layout.addRow('Last Name:', QLineEdit(self))
        form_layout.addRow('DOB:', QDateEdit(self))

class PDFViewerBox(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, 'Contact Information', parent)
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        form_layout.addRow('Phone Number:', QLineEdit(self))
        form_layout.addRow('Email Address:', QLineEdit(self))

class MainWindowSplitted(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt QGroupBox')

        d_layout = QGridLayout(self)
        self.setLayout(d_layout)

        self.splitter = QSplitter(self)
        self.main_box = MainBox(self)
        self.pdf_box = PDFViewerBox(self)

        self.splitter.addWidget(self.main_box)
        self.splitter.addWidget(self.pdf_box)

        d_layout.addWidget(self.splitter)


    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event) 
        orientation = self.splitter.orientation()
        width = self.width()
        if width < 500 and orientation != Qt.Orientation.Vertical:
            self.splitter.setOrientation(Qt.Orientation.Vertical)
        elif width > 500 and orientation != Qt.Orientation.Horizontal:
            self.splitter.setOrientation(Qt.Orientation.Horizontal)
        return res

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowSplitted()
    window.show()
    sys.exit(app.exec())