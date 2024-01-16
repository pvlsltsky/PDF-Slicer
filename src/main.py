import sys
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget,  QFormLayout,
                               QGridLayout, QGroupBox, QVBoxLayout,
                               QLineEdit, QDateEdit, QSplitter, 
                               QListView,QListWidgetItem)
from PySide6.QtCore import Qt

from list_panel import MyTreeWidget
from pdf_view import PDFPanel

class PdfFilesListView(QListView):
    def __init__(self, parent):
        QListView.__init__(self, parent)

class PDFFileLine(QListWidgetItem):
    def __init__(self, parent):
        QListWidgetItem.__init__()

class MainBox(QGroupBox):
    def __init__(self, parent, viewer):
        QGroupBox.__init__(self, 'Donor files list', parent)
        form_layout = QVBoxLayout()
        self.setLayout(form_layout)
        self.inner_widget = MyTreeWidget(self, viewer)
        form_layout.addWidget(self.inner_widget)
        form_layout.setContentsMargins(2,2,2,2)

class PDFViewerBox(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, 'PDF preview', parent)
        form_layout = QVBoxLayout()
        self.setLayout(form_layout)
        self.inner_widget = PDFPanel(self)
        form_layout.addWidget(self.inner_widget)
        form_layout.setContentsMargins(2,2,2,2)
    
    def getInnerWidget(self):
        return self.inner_widget

class MainWindowSplitted(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PDF Slicer')

        d_layout = QGridLayout(self)
        self.setLayout(d_layout)

        self.splitter = QSplitter(self)
        self.pdf_box = PDFViewerBox(self)

        self.main_box = MainBox(self, self.pdf_box.getInnerWidget())

        self.splitter.addWidget(self.main_box)
        self.splitter.addWidget(self.pdf_box)

        d_layout.addWidget(self.splitter)
        d_layout.setContentsMargins(0,0,0,0)

    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event) 
        orientation = self.splitter.orientation()
        width = self.width()
        if width < 700 and orientation != Qt.Orientation.Vertical:
            self.splitter.setOrientation(Qt.Orientation.Vertical)
        elif width > 700 and orientation != Qt.Orientation.Horizontal:
            self.splitter.setOrientation(Qt.Orientation.Horizontal)
        return res

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowSplitted()
    window.show()
    sys.exit(app.exec())