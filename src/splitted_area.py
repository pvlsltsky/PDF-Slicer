from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QWidget, QGridLayout, QErrorMessage , QGroupBox, 
                               QVBoxLayout, QSplitter, QLabel,
                               QListView)
from PySide6.QtCore import Qt

from list_composer_panel import ListComposerPanel
from pdf_view import PDFPanel

from status_updater import StatusUpdater

class MainBox(QGroupBox, StatusUpdater):
    def __init__(self, parent : QWidget):
        QGroupBox.__init__(self, 'List of PDF donor files for merge', parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.inner_widget = ListComposerPanel(self)
        layout.addWidget(self.inner_widget)
        layout.setContentsMargins(2,2,2,2)
        self.setStatusTip("Main box")
        self.setStatusText("Main box initialized")

class PDFViewerBox(QGroupBox, StatusUpdater):
    def __init__(self, parent):
        QGroupBox.__init__(self, 'PDF preview', parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.inner_widget = PDFPanel(self)
        layout.addWidget(self.inner_widget)
        layout.setContentsMargins(2,2,2,2)
        self.setStatusTip("PDF preview")
        self.setStatusText("PDF viewer box initialized")
    
    def getInnerWidget(self):
        # return self.inner_widget
        return None

class MainWindowSplitted(QWidget, StatusUpdater):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStatusText("Splitted area initializing...")
        d_layout = QGridLayout()
        self.setLayout(d_layout)

        self.splitter = QSplitter(self)
        self.pdf_box = PDFViewerBox(self)
        self.main_box = MainBox(self, self.pdf_box.getInnerWidget())
        self.splitter.addWidget(self.main_box)
        self.splitter.addWidget(self.pdf_box)

        d_layout.addWidget(self.splitter)
        d_layout.setContentsMargins(0,0,0,0)

        # set delegates
        self.main_box.inner_widget.setRefreshPdfDelegate(self.pdf_box.inner_widget.refreshView)
        self.main_box.inner_widget.setMovePdfViewFocus(self.pdf_box.inner_widget.jumpToPage)
        self.main_box.inner_widget.setPreviewPdfDelegate(self.pdf_box.inner_widget.setPdfDoc)

        # # for test >
        # pdfViewSetPdf = self.pdf_box.inner_widget.setPdfDoc
        # pdfViewSetPdf("/Users/pavelslutsky/Library/CloudStorage/GoogleDrive-pvlsltsky@gmail.com/My Drive/Documents/Medical docs/Finger break/Med_case.pdf")
        # # < for test

    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event) 
        orientation = self.splitter.orientation()
        width = self.width()
        if width < 700 and orientation != Qt.Orientation.Vertical:
            self.splitter.setOrientation(Qt.Orientation.Vertical)
        elif width > 700 and orientation != Qt.Orientation.Horizontal:
            self.splitter.setOrientation(Qt.Orientation.Horizontal)
        return res