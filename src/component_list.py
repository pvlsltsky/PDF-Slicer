import sys
import os.path
from functools import partial

from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
                               QHeaderView, QLabel, QPushButton, QStyledItemDelegate,
                               QFileDialog, QSpinBox,QButtonGroup)
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtCore import Qt, Slot, QRect, QItemSelection

from pdf_controller import checkPdfDonor, resource_path
from status_updater import StatusUpdater

class CustomStyleDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        size_hint.setHeight(30)
        return size_hint

class ComponentList(QTreeWidget, StatusUpdater):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set column count and headers
        self.initializeHeader()
        self.setStatusTip("List of donor PDF files")

        # Enable drag-and-drop functionality
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.itemPressed.connect(self.onItemPressed)

        # row height:
        # self.setUniformRowHeights(True)
        # self.setItemDelegate(CustomStyleDelegate(self)) 

        # drag-drop asistance
        self.drop_position = None
        self.drop_to_item = None
        self.drag_row = None
        self.drop_shift = None

        # common tree widget setup
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)
        self.setItemsExpandable(False)
        self.default_text_color = None 
        # delegates
        self.setSaveButtonEnabled = lambda x : None
        self.updatePdfView = lambda x : None
        self.moveFocusToPagePdfView = lambda x: None

    def initializeHeader(self):
        self.setColumnCount(6)
        self.setHeaderLabels(["", "", "Donor file name", "From", "To", "Total"])
        self.header().setStretchLastSection(False) 
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) 
        self.header().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed) 
        self.setStyleSheet(""" * { show-decoration-selected: 0; }
                           QHeaderView::section { border: 0px; } 
                           QTreeView::item {height: 30px;}
                           QTreeView::item:selected {background: grey;}
                           QTreeView::item:selected {color: black;}""")
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 30)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 70)

    def firstPageIndex(self, row_idx : int):
        if row_idx < self.topLevelItemCount():
            pages_till_row_idx = 0
            for i in range(row_idx):
                try: 
                    pages_till_row_idx  += int(self.topLevelItem(i).text(5).split()[0])
                except:
                    self.setStatusText(f"Error in line {i + 1}")
            return pages_till_row_idx
        return None

    @Slot(QItemSelection, QItemSelection)
    def handleSelectionChange(self, selected : QItemSelection, deselected : QItemSelection):
        # if selected.count():
        #     self.attachDonorControls(self.topLevelItem(selected.indexes()[0].row()))
        #     self.moveFocusToPagePdfView(self.firstPageIndex(selected.indexes()[0].row()))
        if self.currentItem():
            self.attachDonorControls(self.topLevelItem(self.currentIndex().row()))
            self.moveFocusToPagePdfView(self.firstPageIndex(self.currentIndex().row()))
        if deselected.count():
            self.detachDonorControls(self.topLevelItem(deselected.indexes()[0].row()))

    @Slot(str)
    def addNewDonor(self, fullpath : str) -> None:
        donor= QTreeWidgetItem(["", "-",  fullpath, "1", "1", "1 page"])
        donor.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
        donor.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
        self.addTopLevelItem(donor)
        donor.setText(0, str(self.indexOfTopLevelItem(donor) + 1))
        donor.setToolTip(2, fullpath)
        self.setSaveButtonEnabled(True)
        self.updateToolTipMsg()
        self.updatePdfView(self.listOfDonors())
        
    def updateToolTipMsg(self):
        count = self.topLevelItemCount()
        if count > 1:
            self.setToolTip("You can drag items to change merging order")
        elif count == 1:
            self.setToolTip("You can add donors and change their order afterwards")
        else:
            self.setToolTip("List is empty")

    @Slot()
    def listOfDonors(self):
        donor_list = [] 
        for idx in range(self.topLevelItemCount()):
            donor = self.topLevelItem(idx)
            donor_list.append((donor.text(2), 
                               self.itemWidget(donor, 3).value() if donor.isSelected() else int(donor.text(3)),
                               self.itemWidget(donor, 4).value() if donor.isSelected() else int(donor.text(4))))
        return donor_list

    def updatePages(self, _donor : QTreeWidgetItem, p_from : QSpinBox, p_to : QSpinBox, new_val):
        p_to.setMinimum(p_from.value())
        total_p = p_to.value() - p_from.value() + 1
        _donor.setText(5, f"{total_p} page" + ("" if total_p == 1 else "s"))
        self.updatePdfView(self.listOfDonors())

    def attachDonorControls(self, _donor : QTreeWidgetItem):
        if __name__ != "__main__":
            max_pages = checkPdfDonor(_donor.text(2))
        else:
            max_pages = 15 # for test purposes
        # remove button
        _donor.setText(0, "")
        donor_del_btn = QPushButton("")
        donor_del_btn.setIcon(QPixmap(resource_path("icons/delete24.png")))
        donor_del_btn.setToolTip("Remove row")
        donor_del_btn.clicked.connect(partial(self.handleRemoveBtnClicked, _donor))
        self.setItemWidget(_donor, 0, donor_del_btn)
        # copy button
        _donor.setText(1, "")
        donor_cpy_btn = QPushButton("")
        donor_cpy_btn.setIcon(QPixmap(resource_path("icons/copy24.png")))
        donor_cpy_btn.setToolTip("Copy row")
        donor_cpy_btn.clicked.connect(partial(self.handleCopyDataClicked, _donor))
        self.setItemWidget(_donor, 1, donor_cpy_btn)
        # pages from selector
        pages_from = QSpinBox(self)
        pages_from.setStyleSheet('background-color: grey; color: black;')
        try:
            pages_from.setValue(int(_donor.text(3)))
        except:
            pages_from.setValue(1)
        _donor.setText(3, "")
        pages_from.setMinimum(1)
        pages_from.setMaximum(max_pages)
        self.setItemWidget(_donor, 3, pages_from)
        # pages to selector
        pages_to = QSpinBox(self)
        pages_to.setStyleSheet('background-color: grey; color: black;')
        try:
            pages_to.setValue(int(_donor.text(4)))
        except:
            pages_to.setValue(1)
        _donor.setText(4, "")
        pages_to.setMinimum(1)
        pages_to.setMaximum(max_pages)
        self.setItemWidget(_donor, 4, pages_to)
        pages_from.valueChanged.connect(partial(self.updatePages, _donor, pages_from, pages_to))
        pages_to.valueChanged.connect(partial(self.updatePages, _donor, pages_from, pages_to))

    def detachDonorControls(self, _donor : QTreeWidgetItem):
        # detach controls of donor line 
        _donor.setText(0, str(self.indexOfTopLevelItem(_donor) + 1))
        _donor.setText(1, "-")
        _donor.setText(3, str(self.itemWidget(_donor, 3).value()))
        _donor.setText(4, str(self.itemWidget(_donor, 4).value()))
        self.setItemWidget(_donor, 0, None)
        self.setItemWidget(_donor, 1, None)
        self.setItemWidget(_donor, 3, None)
        self.setItemWidget(_donor, 4, None)

    def updateIndexes(self):
        for i in range(self.topLevelItemCount()):
            if not self.topLevelItem(i).isSelected():
                self.topLevelItem(i).setText(0, str(i + 1))

    @Slot(QTreeWidgetItem)
    def handleRemoveBtnClicked(self, donor : QTreeWidgetItem) -> None:
        index = self.indexOfTopLevelItem(donor)
        self.takeTopLevelItem(index)
        self.setSaveButtonEnabled(self.topLevelItemCount() != 0)
        self.updateIndexes()
        self.updateToolTipMsg()
        self.updatePdfView(self.listOfDonors())

    @Slot(QTreeWidgetItem)
    def handleCopyDataClicked(self, donor : QTreeWidgetItem) -> None:
        # handling copy button click
        index = self.indexOfTopLevelItem(donor)
        copied_donor = donor.clone()
        copied_donor.setText(1, "-")
        copied_donor.setText(3, str(self.itemWidget(donor, 3).value()))
        copied_donor.setText(4, str(self.itemWidget(donor, 4).value()))
        self.insertTopLevelItem(index + 1, copied_donor)
        copied_donor.setText(0, str(self.indexOfTopLevelItem(copied_donor) + 1))
        self.updateIndexes()
        self.updateToolTipMsg()
        self.updatePdfView(self.listOfDonors())

    # Drag - Drop functionality    

    @Slot(QTreeWidgetItem, int)
    def onItemPressed(self, item, column):
        if isinstance(item, QTreeWidgetItem):
            self.drag_row = self.indexOfTopLevelItem(item)
        else:
            self.drag_row = None 

    def dragMoveEvent(self, event):
        # Determine the drop row
        self.drop_to_item = self.itemAt(event.position().x(), event.position().y())
        if self.drag_row != self.indexOfTopLevelItem(self.drop_to_item):
            self.drop_position = event.position().y()
        else:
            self.drop_to_item = None
            self.drop_position = None
        # Trigger a repaint of the viewport
        self.viewport().repaint()

    def paintEvent(self, event):
        # Call the base class paintEvent to ensure proper drawing of the tree
        super().paintEvent(event)
        # Manually draw a custom drop indicator if applicable
        if self.drop_to_item:
            self.customDrawDropIndicator()

    def customDrawDropIndicator(self):
        # Moves drop indicator only between items 
        if self.drop_to_item:
            # Get the visual rectangle for the target item
            target_rect = self.visualItemRect(self.drop_to_item)
            drop_to_row = self.indexOfTopLevelItem(self.drop_to_item)
            # Create a custom indicator rectangle
            indicator_rect = QRect(target_rect)
            if (target_rect.center().y() < self.drop_position):
                # insert after the item
                indicator_rect.setTop(target_rect.bottom() + 1)
                self.drop_shift = 1
                drop_between = (drop_to_row, drop_to_row + 1)
            else:
                # insert before the item
                indicator_rect.setTop(target_rect.top() - 1)
                self.drop_shift = 0
                drop_between = (drop_to_row, drop_to_row - 1)

            # ignore when index is out of range
            if (self.drag_row in drop_between):
                self.drop_to_item = None
                self.drop_shift = None
                self.drop_position = None
                return
                
            indicator_rect.setHeight(2)
            # Use a custom color for the drop indicator
            painter = QPainter(self.viewport())
            painter.fillRect(indicator_rect, QColor(Qt.GlobalColor.darkGreen))
            painter.end()

    def dropEvent(self, event):
        if (self.drop_to_item 
            and self.drop_shift is not None
            and self.drag_row is not None):

            self.topLevelItem(self.drag_row).setSelected(False)
            dragged_item = self.takeTopLevelItem(self.drag_row)
            target_index = self.indexOfTopLevelItem(self.drop_to_item) + self.drop_shift
            self.insertTopLevelItem(target_index, dragged_item)
            for i in range(self.topLevelItemCount()):
                self.topLevelItem(i).setSelected(False)
            self.updatePdfView(self.listOfDonors())
            dragged_item.setSelected(True)
            self.updateIndexes()

        self.drop_to_item = None
        self.drop_position = None
        self.drop_shift = None
        self.drag_row = None
        self.viewport().repaint()

# For test purposes only
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_tree_widget = ComponentList()
    my_tree_widget.addNewDonor("mypath/blalala.pdf")
    my_tree_widget.addNewDonor("mypath/blalala2.pdf")
    my_tree_widget.addNewDonor("mypath/blalala3.pdf")
    my_tree_widget.show()
    sys.exit(app.exec())