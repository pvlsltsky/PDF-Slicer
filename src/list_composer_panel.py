import sys
import os.path
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QApplication, QGroupBox, QWidget, 
                               QPushButton, QLineEdit, QLabel, 
                               QHBoxLayout, QVBoxLayout,QFileDialog) 
from status_updater import StatusUpdater
from component_list import ComponentList
from pdf_controller import checkPdfDonor, composeToFile

USER_DIR = os.path.expanduser("~")

class InputBox(QGroupBox, StatusUpdater):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setTitle("Please choose donor PDF file to merge")
        self.__init_dir = USER_DIR
        self.__file_path_txt = QLineEdit(self)
        self.__file_path_txt.textEdited.connect(self.checkFile)
        self.__select_file_btn = QPushButton(chr(8230), self)
        self.__select_file_btn.clicked.connect(self.handleSelectFileClicked)
        self.__preview_btn = QPushButton("Preview", self)
        self.__preview_btn.setEnabled(False)
        self.__preview_btn.clicked.connect(self.handlePreviewClicked)
        self.__add_to_list_btn = QPushButton("Add to list", self)
        self.__add_to_list_btn.setEnabled(False)
        self.__add_to_list_btn.clicked.connect(self.handleAddToListClicked)
        layout = QHBoxLayout(self)
        layout.addWidget(self.__file_path_txt)
        layout.addWidget(self.__select_file_btn)
        layout.addWidget(self.__preview_btn)
        layout.addWidget(self.__add_to_list_btn)
        self.setLayout(layout)
        # define delegates
        self.previewPDF = lambda x : None
        self.addToList = lambda x : None

    @Slot()
    def checkFile(self):
        enabled = checkPdfDonor(self.__file_path_txt.text()) > 0
        self.__add_to_list_btn.setEnabled(enabled)
        self.__preview_btn.setEnabled(enabled)

    @Slot()
    def handleSelectFileClicked(self):
        # self.setStatusText("Selection of donor file...")
        fname = QFileDialog.getOpenFileName(self, 'Add file', self.__init_dir, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            self.__file_path_txt.setText(fname[0])
            self.checkFile()

    @Slot() 
    def handlePreviewClicked(self):
        self.previewPDF(self.__file_path_txt.text())

    @Slot()
    def handleAddToListClicked(self):
        self.addToList(self.__file_path_txt.text())

# class ListComposerPanel(QGroupBox, StatusUpdater):
class ListComposerPanel(QWidget, StatusUpdater):
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel(self)
        label.setText("List of donors")
        self.__save_btn = QPushButton(self)
        self.__save_btn.setText("Save as PDF")
        self.__save_btn.setEnabled(False)
        self.__save_btn.setFixedWidth(100)
        self.__save_btn.clicked.connect(self.handleSaveBtnClicked)
        self.__comp_list = ComponentList(self)
        self.__input_box = InputBox(self)

        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(self.__save_btn)
        hlayout.setContentsMargins(0,0,0,0)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.__comp_list)
        vlayout.addWidget(self.__input_box)
        vlayout.setContentsMargins(2,2,2,2)
        vlayout.setSpacing(2)
        self.setLayout(vlayout)

        # care of delegates
        self.__comp_list.setSaveButtonEnabled = self.setSaveButtonEnabled
        self.__input_box.addToList = self.__comp_list.addNewDonor
        self.setStatusText("Composer panel initialized")
    
    @Slot()
    def handleSaveBtnClicked(self):
        fname = QFileDialog.getSaveFileName(self, '*.pdf', USER_DIR, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            self.setStatusText(composeToFile(self.__comp_list.listOfDonors(), fname[0]))
    
    @Slot(bool)
    def setSaveButtonEnabled(self, bool):
        self.__save_btn.setEnabled(bool)      

    def setPreviewPdfDelegate(self, pdfViewPrevieMethod):
        self.__input_box.previewPDF = pdfViewPrevieMethod

    def setRefreshPdfDelegate(self, pdfViewRefreshMethod):
        self.__comp_list.updatePdfView = pdfViewRefreshMethod

    def setMovePdfViewFocus(self, pdfViewMoveFocusMethod):
        self.__comp_list.moveFocusToPagePdfView = pdfViewMoveFocusMethod

# For test purposes only
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_tree_widget = ListComposerPanel()
    my_tree_widget.show()
    sys.exit(app.exec())