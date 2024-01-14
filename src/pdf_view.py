import sys
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget, QFormLayout,
                               QGroupBox, QVBoxLayout)

from PySide6.QtCore import Qt, QBuffer, QByteArray, QIODevice
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument

from controller import compose_to_buffer

class PDFPanel(QGroupBox):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.doc = QPdfDocument(self)
        self.pdf_view = QPdfView(self)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.pdf_view.setDocument(self.doc)
        layout = QFormLayout(self)
        layout.addWidget(self.pdf_view)
        layout.setContentsMargins(2,2,2,2)
        self.setLayout(layout) 
        self.refreshView([])
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event)
        diff = self.width() - self.pdf_view.width()
        if diff > 16:
            self.pdf_view.setGeometry(self.x() + 8, 
                                    self.pdf_view.y(),
                                    self.width() - 16,
                                    self.pdf_view.height()) 
            
    def refreshView(self, list_of_donors):
        barr = compose_to_buffer(list_of_donors)
        if barr is not None:
            ba = QByteArray(barr)
            buffer = QBuffer(ba)
            buffer.open(QIODevice.OpenModeFlag.ReadOnly)
            self.doc.load(buffer)
        else:
            self.doc.close()

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('One Line')
        mw_layout = QVBoxLayout(self)

        self.dv_panel = PDFPanel(self)
        mw_layout.addWidget(self.dv_panel)
        mw_layout.setContentsMargins(2,2,2,2)
        self.setLayout(mw_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
