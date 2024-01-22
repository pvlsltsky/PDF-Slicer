import sys
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget, QSizePolicy,
                               QGroupBox, QVBoxLayout, QLabel,
                               QHBoxLayout,QPushButton)

from PySide6.QtCore import Qt, Slot, QBuffer, QByteArray, QIODevice
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument, QPdfLink

from pdf_controller import composeToBuffer

# class PDFPanel(QGroupBox):
class PDFPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.__doc = QPdfDocument(self)
        self.__path = ""
        self.__elide_mode = Qt.TextElideMode.ElideRight
        # PDF view ->
        self.__pdf_view = QPdfView(self)
        self.__pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__pdf_view.setDocument(self.__doc)

        # Control panel ->
        cntrl_box = QGroupBox(self)

        self.__file_name_lbl = QLabel(cntrl_box)
        self.__file_name_lbl.setWordWrap(True)
        self.__file_name_lbl.setFixedHeight(self.__file_name_lbl.height())
        self.__file_name_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.__page_lbl = QLabel(cntrl_box)
        self.__page_lbl.setText("Page:")
        self.__current_page = QLabel(cntrl_box)
        cp_size = self.__current_page.fontMetrics().size(Qt.TextFlag.TextSingleLine ,"999 / 999")
        self.__current_page.setFixedWidth(cp_size.width())

        ctrl_box_layout = QHBoxLayout()
        ctrl_box_layout.addWidget(self.__file_name_lbl)
        ctrl_box_layout.addWidget(self.__page_lbl)
        ctrl_box_layout.addWidget(self.__current_page)
        ctrl_box_layout.setContentsMargins(3,3,3,3)
        cntrl_box.setLayout(ctrl_box_layout)
        self.__pdf_view.pageNavigator().currentPageChanged.connect(self.setCurrentPage)
        
        # For tests only -> 
        if __name__ == "__main__":
            cntrl_btn = QPushButton(cntrl_box)
            cntrl_btn.pressed.connect(self.testAction)
            ctrl_box_layout.addWidget(cntrl_btn)
        # <- for test purpose

        # Layouts ->
        vert_layout = QVBoxLayout(self)
        vert_layout.addWidget(cntrl_box)
        vert_layout.addWidget(self.__pdf_view)
        vert_layout.setContentsMargins(2,2,2,2)
        
        self.setLayout(vert_layout) 
        self.refreshView([])

    @Slot(str)
    def updatePath(self, path):
        self.__path = path 
        self.setFNameLabel(self.__path)

    @Slot(int)
    def setCurrentPage(self, page : int):
        self.__current_page.setText(f"{page + 1} / {self.__doc.pageCount()}")

    @Slot(str)
    def clearViewerData(self, msg : str):
        self.__doc.close()
        self.updatePath(msg)
        self.__current_page.clear()
        self.__current_page.hide()
        self.__page_lbl.hide()

    @Slot(str)
    def showViewerData(self, msg : str):
        self.__current_page.show()
        self.__page_lbl.show()
        self.setCurrentPage(0)
        self.updatePath(msg)
        self.__file_name_lbl.setToolTip(self.__path)

    @Slot(str)
    def setPdfDoc(self, path : str):
        self.updatePath(path)
        try:
            self.__doc.load(self.__path)
            self.__elide_mode = Qt.TextElideMode.ElideLeft
            self.showViewerData(self.__path)
        except Exception as ex:
            self.clearViewerData("Invalid PDF file")

    @Slot(str)
    def setFNameLabel(self, text : str):
        lbl_width = self.__file_name_lbl.width()
        metrics = self.__file_name_lbl.fontMetrics()
        elided_text = metrics.elidedText(text, self.__elide_mode, lbl_width)
        self.__file_name_lbl.setText(elided_text)

    @Slot(QResizeEvent)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        diff = self.width() - self.__pdf_view.width()
        if diff > 16:
            self.__pdf_view.setGeometry(self.x() + 8, 
                                      self.__pdf_view.y(),
                                      self.width() - 16,
                                      self.__pdf_view.height())
            
        self.setFNameLabel(self.__path)

    @Slot(list)        
    def refreshView(self, list_of_donors):
        self.__elide_mode = Qt.TextElideMode.ElideRight
        barr = composeToBuffer(list_of_donors)
        if barr is not None:
            try:
                ba = QByteArray(barr)
                buffer = QBuffer(ba)
                buffer.open(QIODevice.OpenModeFlag.ReadOnly)
                self.__doc.load(buffer)
                self.showViewerData("Result of merging")
            except:
                self.clearViewerData("Invalid PDF data received")
        else:
            self.clearViewerData("No PDF data to preview")
    
    @Slot(int)
    def jumpToPage(self, targetPage : int):
        navigator = self.__pdf_view.pageNavigator()
        if navigator.currentPage() != targetPage:
            navigator.jump(targetPage, navigator.currentLocation(), navigator.currentZoom())

    # For test purpose only ->
    @Slot()
    def testAction(self):  
        navigator = self.__pdf_view.pageNavigator()
        self.jumpToPage(navigator.currentPage() + 2)
    # <- for test purpose

# For test purpose only ->
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('One Line')
        mw_layout = QVBoxLayout(self)
        self.dv_panel = PDFPanel(self)
        mw_layout.addWidget(self.dv_panel)
        mw_layout.setContentsMargins(2,2,2,2)
        self.setLayout(mw_layout)
        # self.dv_panel.setPdfDoc("/Users/pavelslutsky/Library/CloudStorage/GoogleDrive-pvlsltsky@gmail.com/My Drive/Documents/Medical docs/Finger break/Med_case.pdf")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
# <- For test purpose only