from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                               QHeaderView, QLabel, QPushButton, QStyle,
                               QFileDialog, QSpinBox)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PySide6.QtCore import Qt
import sys
import os.path
from controller import checkPdfDonor


user_dir = os.path.expanduser("~")

class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set column count and headers
        self.setColumnCount(2)
        self.setHeaderLabels(["Item", "Data", "Buttons1", "Pages from", "Pages to", "Total"])
        self.header().setStretchLastSection(False) 
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 30)
        self.setColumnWidth(3, 115)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 130)
        self.header().setHidden(True)
        # Populate the tree with data
        self.setupTreeData()

    def setupTreeData(self):
        # Add first row (new PDF file section with controls)
        self.addTitleRow()
        # Add initial emmpty child row 
        self.addInitialRow()
    
    def addTitleRow(self):
        self.new_pdf_row = QTreeWidgetItem(self, ["", "", "", "", "", "", ""])
        self.new_pdf_row.setExpanded(True)
        # PDF icon
        image_path = "./resources/pdf_color_2.png"
        pixmap = QPixmap(image_path)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(pixmap.scaledToWidth(30, Qt.TransformationMode.FastTransformation))
        self.setItemWidget(self.new_pdf_row, 0, icon_lbl)
        # frase
        str_lbl = QLabel()
        str_lbl.setText("New awesome PDF file")
        self.setItemWidget(self.new_pdf_row, 1, str_lbl)
        # save button
        btn_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        self.save_btn = QPushButton("&Save")
        self.save_btn.setIcon(btn_icon)
        self.setItemWidget(self.new_pdf_row, 3, self.save_btn)
        # total pages in file
        self.new_total = QLabel()
        self.new_total.setMargin(5)
        self.new_total_int = 0
        self.new_total.setText(f"Total: {self.new_total_int} pages")
        self.setItemWidget(self.new_pdf_row, 5, self.new_total)


    def addInitialRow(self):
        self.init_dir = user_dir
        self.init_fullpath = ""
        self.init_row = QTreeWidgetItem(self.new_pdf_row, ["", "", "", "", "", "", ""])
        # the elements added to instance because of usability
        # button to add file
        self.init_add_button = QPushButton("+")
        self.setItemWidget(self.init_row, 0, self.init_add_button)
        # label with name of the file
        self.init_str_lbl = QLabel()
        self.init_str_lbl.setMargin(5)
        self.setItemWidget(self.init_row, 1, self.init_str_lbl)
        # search file button
        self.init_file_dlg_btn = QPushButton(chr(8230))
        self.init_file_dlg_btn.clicked.connect(self.chooseFile)
        self.setItemWidget(self.init_row, 2, self.init_file_dlg_btn)
        # pages from selector
        self.init_pages_from = QSpinBox(self)
        self.init_pages_from.setPrefix("Pages from: ")
        self.init_pages_from.valueChanged.connect(self.updateTo)
        self.setItemWidget(self.init_row, 3, self.init_pages_from)
        # pages to selector
        self.init_pages_to = QSpinBox(self)
        self.init_pages_to.setPrefix("to: ")
        self.setItemWidget(self.init_row, 4, self.init_pages_to)
        self.init_pages_to.valueChanged.connect(self.calculateTotal)
        # total label
        self.init_total = QLabel()
        self.init_total.setMargin(5)
        self.init_total_int = 0 
        self.setItemWidget(self.init_row, 5, self.init_total)
        self.resetInitialRow()

    def resetInitialRow(self):
        # Update data
        self.init_fullpath = ""
        self.dir = user_dir
        # Update elements
        self.init_str_lbl.setText("Select donor PDF file...")
        self.init_str_lbl.setToolTip("Select donor PDF file")
        self.init_add_button.setEnabled(False)
        self.init_pages_from.setValue(0)
        self.init_pages_from.setEnabled(False)
        self.init_pages_to.setValue(0)
        self.init_pages_to.setEnabled(False)
        self.calculateTotal()

    def setFile(self, fullpath : str) -> bool:
        fullpath = fullpath.strip()
        available_pages = checkPdfDonor(fullpath)
        if len(fullpath) > 0 \
               and os.path.exists(fullpath) \
               and os.path.isfile(fullpath) \
               and os.path.splitext(fullpath)[-1].lower() == ".pdf":
            # Update data
            self.init_fullpath = fullpath
            self.init_str_lbl.setToolTip(fullpath)
            self.init_dir, filename = os.path.split(fullpath)
            self.init_str_lbl.setText(filename)
            # Update elements
            self.init_add_button.setEnabled(True)
            self.init_pages_from.setMaximum(available_pages)
            self.init_pages_from.setMinimum(1)
            self.init_pages_from.setValue(0)
            self.init_pages_from.setEnabled(True)
            self.init_pages_to.setMaximum(available_pages)
            self.init_pages_to.setMinimum(1)
            self.init_pages_to.setValue(0)
            self.init_pages_to.setEnabled(True)
        else:
            self.resetInitialRow()

    def chooseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Add file', self.init_dir, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            self.setFile(fname[0])

    def updateTo(self):
        self.init_pages_to.setMinimum(self.init_pages_from.value())
        self.calculateTotal()   

    def calculateTotal(self):
        pages_diff = int(self.init_pages_to.value()) - int(self.init_pages_from.value())
        self.init_total_int = 0 if self.init_pages_to.value() == 0 else pages_diff + 1
        self.init_total.setText(f"Total: {self.init_total_int} pages")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create your custom tree widget
    my_tree_widget = MyTreeWidget()

    # Show the tree widget
    my_tree_widget.show()

    sys.exit(app.exec())
