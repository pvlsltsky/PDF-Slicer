from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                               QHeaderView, QLabel, QPushButton,
                               QFileDialog, QSpinBox)
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QRect
import sys
import os.path
from pdf_controller import checkPdfDonor, compose_to_file
from functools import partial
from pdf_view import PDFPanel

user_dir = os.path.expanduser("~")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.realpath(os.path.join(base_path, relative_path))

class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None, pdf_panel=None):
        super().__init__(parent)
        # Set column count and headers
        self.setColumnCount(6)
        self.setHeaderLabels(["", "", "", "From", "To", "Total"])
        self.header().setStretchLastSection(False) 
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  
        self.setStyleSheet("QHeaderView::section { border: 0px; }")
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 30)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 70)

        # Populate the tree with initial header row and ADD input row
        self.setupTreeData()

        # Enable drag-and-drop functionality
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)

        self.pdf_panel = pdf_panel

        # To prevent header line and input line from selection
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)

        self.itemPressed.connect(self.onItemPressed)
        # drag-drop asistance
        self.drop_item = None
        self.drop_position = None
        self.pressed_item_index = None
        self.drop_shift = None

    def setupTreeData(self):
        # Add first row (new PDF file section with controls)
        self.addTitleRow()
        # Add initial ADD child row 
        self.addInitialRow()
    
    def addTitleRow(self) -> None:
        self.new_pdf_row = QTreeWidgetItem(self, ["", "New awesome PDF file", "", "", "", ""])
        self.new_pdf_row.setExpanded(True)
        self.itemCollapsed.connect(self.handleItemCollapsed)
        # PDF icon
        # image_dir = os.path.dirname(__file__)
        # image_path = os.path.relpath(os.path.join(image_dir, "../resources/pdf_color_2.png"))
        image_path = resource_path("./resources/pdf_color_2.png")
        print(image_path)
        pixmap = QPixmap(image_path)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(pixmap.scaledToWidth(30, Qt.TransformationMode.FastTransformation))
        self.setItemWidget(self.new_pdf_row, 0, icon_lbl)
        # save button
        self.save_btn = QPushButton(chr(10515))
        self.save_btn.setToolTip("Save file")
        self.save_btn.setEnabled(False)
        self.setItemWidget(self.new_pdf_row, 2, self.save_btn)
        self.save_btn.clicked.connect(self.handleSaveBtnClicked)
        # total pages in file
        self.new_total = QLabel()
        self.new_total.setMargin(5)
        self.new_total_int = 0
        self.new_total.setText(f"{self.new_total_int} pages")
        self.setItemWidget(self.new_pdf_row, 5, self.new_total)

    def addDonorRow(self, fullpath : str, from_p : int, to_p : int) -> None:
        total_p = to_p - from_p + 1
        donor_row = QTreeWidgetItem(["", fullpath, "", 
                                    str(from_p), str(to_p), 
                                    f"{total_p} page" + ("" if total_p == 1 else "s") ])
        self.new_pdf_row.insertChild(self.new_pdf_row.childCount() - 1, donor_row)
        self.setupDonorButtons(donor_row)
        donor_row.setToolTip(1, fullpath)

    def addInitialRow(self):
        self.init_dir = user_dir
        self.init_row = QTreeWidgetItem(self.new_pdf_row, ["", "", "", "", "", ""])
        # the elements added to instance because of usability
        # button to add file
        self.init_add_btn = QPushButton(chr(10004))
        self.setItemWidget(self.init_row, 0, self.init_add_btn)
        self.init_add_btn.clicked.connect(self.initDonorRow)
        # label with name of the file
        self.init_fullpath = QLabel()
        self.init_fullpath.setMargin(5)
        self.setItemWidget(self.init_row, 1, self.init_fullpath)
        # search file button
        self.init_file_dlg_btn = QPushButton(chr(8230))
        self.init_file_dlg_btn.setToolTip("Select file")
        self.init_file_dlg_btn.clicked.connect(self.handleSelectFileClicked)
        self.setItemWidget(self.init_row, 2, self.init_file_dlg_btn)
        # pages from selector
        self.init_pages_from = QSpinBox(self)
        self.init_pages_from.valueChanged.connect(self.updateTo)
        self.setItemWidget(self.init_row, 3, self.init_pages_from)
        # pages to selector
        self.init_pages_to = QSpinBox(self)
        self.setItemWidget(self.init_row, 4, self.init_pages_to)
        self.init_pages_to.valueChanged.connect(self.calculateInitTotal)
        # total label
        self.init_total = QLabel()
        self.init_total.setMargin(5)
        self.init_total_int = 0 
        self.setItemWidget(self.init_row, 5, self.init_total)
        self.resetInitialRow()

    def resetInitialRow(self):
        self.dir = user_dir
        # Update elements
        self.init_fullpath.setText("Select donor PDF file...")
        self.init_fullpath.setToolTip("Select valid donor PDF file")
        self.init_add_btn.setEnabled(False)
        self.init_pages_from.setMinimum(0)
        self.init_pages_from.setValue(0)
        self.init_pages_from.setEnabled(False)
        self.init_pages_to.setMinimum(0)
        self.init_pages_to.setValue(0)
        self.init_pages_to.setEnabled(False)
        self.init_total.setText("")

    def setFile(self, fullpath : str) -> bool:
        fullpath = fullpath.strip()
        available_pages = checkPdfDonor(fullpath)
        if available_pages > 0:
            # Update data
            self.init_fullpath.setText(fullpath)
            self.init_fullpath.setToolTip(fullpath)
            self.init_dir, _ = os.path.split(fullpath)
            # Update elements
            self.init_add_btn.setEnabled(True)
            self.init_pages_from.setMaximum(available_pages)
            self.init_pages_from.setMinimum(1)
            self.init_pages_from.setValue(1)
            self.init_pages_from.setEnabled(True)
            self.init_pages_to.setMaximum(available_pages)
            self.init_pages_to.setMinimum(1)
            self.init_pages_to.setValue(1)
            self.init_pages_to.setEnabled(True)
        else:
            self.resetInitialRow()

    def handleItemCollapsed(self, item : QTreeWidgetItem):
        # Ensure the item remains expanded
        item.setExpanded(True)

    def handleSelectFileClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Add file', self.init_dir, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            self.setFile(fname[0])
    
    def handleSaveBtnClicked(self):
        fname = QFileDialog.getSaveFileName(self, '*.pdf', self.init_dir, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            compose_to_file(self.buildList(), fname[0])

    def updateTo(self):
        self.init_pages_to.setMinimum(self.init_pages_from.value())
        self.calculateInitTotal()   

    def calculateInitTotal(self):
        pages_diff = int(self.init_pages_to.value()) - int(self.init_pages_from.value())
        self.init_total_int = 0 if self.init_pages_to.value() == 0 else pages_diff + 1
        self.init_total.setText(f"{self.init_total_int} page" + ("" if self.init_total_int == 1 else "s"))

    def handleSelectionChange(self, selected, deselected):
        self.new_pdf_row.setSelected(False)
        self.init_row.setSelected(False)
       
    def updateNewFilePages(self):
        self.new_total.setText(f"{self.new_total_int} page" + ("" if self.init_total_int == 1 else "s"))
        self.save_btn.setEnabled(self.new_total_int > 0)
        self.refreshView()

    def initDonorRow(self):
        self.addDonorRow(self.init_fullpath.text(),
                         self.init_pages_from.value(), 
                         self.init_pages_to.value())
        self.new_total_int += self.init_total_int
        self.updateNewFilePages()
        self.resetInitialRow()

    def handleCopyDataClicked(self, donor_row : QTreeWidgetItem) -> None:
        self.setFile(donor_row.text(1))

    def handleRemoveRowClicked(self, donor_row : QTreeWidgetItem) -> None:
        # handle for remove button clicked event
        pages = [int(s) for s in donor_row.text(5).split() if s.isdigit()]
        self.new_total_int -= int(pages[0])
        self.new_pdf_row.removeChild(donor_row)
        self.updateNewFilePages()

    def onItemPressed(self, item, column):
        self.clicked_id = id(item)
        if isinstance(item, QTreeWidgetItem) and  item.isSelected():
            self.pressed_item_index = self.new_pdf_row.indexOfChild(item)
        else:
            self.pressed_item_index = None

    def detachWidgets(self, index : int):
        # detach widgets before the move opration
        item = self.new_pdf_row.child(index)
        if item:
            self.setItemWidget(item, 0, None)
            self.setItemWidget(item, 2, None)

    def setupDonorButtons(self, item):
        # remove button
        donor_del_btn = QPushButton(chr(10008))
        donor_del_btn.setToolTip("Remove slice")
        donor_del_btn.clicked.connect(partial(self.handleRemoveRowClicked, item))
        self.setItemWidget(item, 0, donor_del_btn)
        # copy button
        donor_cpy_btn = QPushButton(chr(9901))
        donor_cpy_btn.setToolTip("Copy data to initial row")
        donor_cpy_btn.clicked.connect(partial(self.handleCopyDataClicked, item))
        self.setItemWidget(item, 2, donor_cpy_btn)
    
    def dragMoveEvent(self, event):
        # Determine the drop position and item
        self.drop_item = self.itemAt(event.position().x(), event.position().y())
        self.drop_position = event.position().y()
        # Trigger a repaint of the viewport
        self.viewport().repaint()

    def paintEvent(self, event):
        # Call the base class paintEvent to ensure proper drawing of the tree
        super().paintEvent(event)
        # Manually draw a custom drop indicator if applicable
        if self.drop_item and not (self.drop_item == self.init_row or self.drop_item == self.new_pdf_row):
            self.customDrawDropIndicator()

    def customDrawDropIndicator(self):
        # Moves drop indicator only between items 
        # Check if the drop position is on an item
        if self.drop_item:
            drop_item_idx = self.new_pdf_row.indexOfChild(self.drop_item)
            # Get the visual rectangle for the target item
            target_rect = self.visualItemRect(self.drop_item)
            # Create a custom indicator rectangle
            indicator_rect = QRect(target_rect)
            if (target_rect.center().y() < self.drop_position):
                # insert after the item
                indicator_rect.setTop(target_rect.bottom() + 1)
                self.drop_shift = 1
                drop_between = (drop_item_idx, drop_item_idx + 1)
            else:
                # insert before the item
                indicator_rect.setTop(target_rect.top() - 1)
                self.drop_shift = 0
                drop_between = (drop_item_idx, drop_item_idx - 1)

            # ignore when index is out of range
            if (self.pressed_item_index in drop_between
                or drop_item_idx >= self.new_pdf_row.childCount() - 1
                or drop_item_idx < 0):

                self.drop_item = None
                self.drop_shift = None
                self.drop_position = None
                return
                
            indicator_rect.setHeight(2)
            # Use a custom color for the drop indicator
            painter = QPainter(self.viewport())
            painter.fillRect(indicator_rect, QColor(Qt.GlobalColor.darkGreen))
            painter.end()

    def dropEvent(self, event):
        if (self.drop_item 
            and self.drop_shift is not None
            and self.pressed_item_index is not None):

            self.detachWidgets(self.pressed_item_index) 
            dragged_item = self.new_pdf_row.takeChild(self.pressed_item_index)
            target_index = self.new_pdf_row.indexOfChild(self.drop_item) + self.drop_shift
            self.new_pdf_row.insertChild(target_index, dragged_item)
            self.setupDonorButtons(dragged_item)
            self.refreshView()

        self.drop_item = None
        self.drop_position = None
        self.drop_shift = None
        self.pressed_item_index = None
        self.viewport().repaint()

    def buildList(self):
        donor_list = []
        for idx in range(self.new_pdf_row.childCount() - 1):
            donor = self.new_pdf_row.child(idx)
            donor_list.append((donor.text(1), 
                               int(donor.text(3)),
                               int(donor.text(4))))
        return donor_list

    def refreshView(self):
        if isinstance(self.pdf_panel, PDFPanel):
                self.pdf_panel.refreshView(self.buildList())        

# For test purposes only
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_tree_widget = MyTreeWidget()
    my_tree_widget.show()
    sys.exit(app.exec())
