import sys
from typing import Optional
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget,  QFormLayout,
                               QGridLayout, QPushButton, QGroupBox, 
                               QLineEdit, QDateEdit, QSplitter, 
                               QListView,QListWidgetItem, QHBoxLayout,
                               QFileDialog, QVBoxLayout, QLineEdit, QComboBox, 
                               QLabel, QScrollArea, QLayout, QFrame, QFormLayout,
                               QSizePolicy)
from PySide6.QtCore import Qt
import os.path

user_dir = os.path.expanduser("~")

# class OneLine(QWidget):
class OneLine(QFrame):
    def __init__(self, parent, filename=""):
        super(OneLine, self).__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # Action button 
        self.action_btn = QPushButton("+")
        # File name
        self.file_name = QLineEdit() 
        fn_policy = QSizePolicy()
        fn_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        self.file_name.setSizePolicy(fn_policy)
        # Select button 
        self.file_dlg_btn = QPushButton(chr(8230))
        self.file_dlg_btn.clicked.connect(self.getFile)
        self.file_name = QLineEdit() 
        # Pages from number
        self.pf_lbl = QLabel("Pages, from:", self)
        self.pages_from = QComboBox(self)
        self.pages_from.addItem("0")
        self.pf_lbl.setBuddy(self.pages_from)
        # Pages to number
        self.pt_lbl = QLabel("to:", self)
        self.pages_to = QComboBox(self)
        self.pages_to.addItem("0")
        self.pt_lbl.setBuddy(self.pages_to)
        # Total pages
        self.p_total = QLabel("0 Pages (0 - 0 on new PDF)")
        # Move up
        # Move down
        # Attach file if exists
        self.setFile(filename)
        self.setMaximumWidth(1200)

        # Layout 
        layout = QHBoxLayout(self)
        layout.addWidget(self.action_btn)
        layout.addWidget(self.file_name)
        layout.addWidget(self.file_dlg_btn)
        layout.addWidget(self.pf_lbl)
        layout.addWidget(self.pages_from)
        layout.addWidget(self.pt_lbl)
        layout.addWidget(self.pages_to)
        layout.addWidget(self.p_total)
        layout.setContentsMargins(5,0,5,0)
        self.setLayout(layout)
    
    def setFile(self, fullpath : str) -> bool:
        fullpath = fullpath.strip()
        if len(fullpath) > 0 \
               and os.path.exists(fullpath) \
               and os.path.isfile(fullpath) \
               and os.path.splitext(fullpath)[-1].lower() == ".pdf":
            # Update data
            self.file_name.setToolTip(fullpath)
            self.dir, self.filename = os.path.split(fullpath)
            self.file_name.setText(self.filename)
            # Update elements
            self.action_btn.setEnabled(True)
        else:
            # Update data
            self.full_filename = ''
            self.dir = user_dir
            self.filename = ""
            # Update elements
            self.file_name.setToolTip("Select PDF file")
            self.action_btn.setEnabled(False)

    def getFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Add file', self.dir, "PDF files (*.pdf)")
        if len(fname[0]) > 0 and len(fname[1]) > 0:
            self.setFile(fname[0])


class DataView(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        dv_layout = QVBoxLayout(self)
        initial_line = OneLine(self)
        self.pdf_lines = [initial_line]
        # for test only ->
        for i in range(5):
            self.pdf_lines.append(OneLine(self))
         # <- for test only
        for line in self.pdf_lines:
            dv_layout.addWidget(line)
        dv_layout.setContentsMargins(2,2,2,2)
        dv_layout.setSpacing(0)
        dv_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.setLayout(dv_layout)


class DataViewerPanel(QGroupBox):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.s_area = QScrollArea(self)
        self.data_view = DataView(self)
        dv_policy = QSizePolicy()
        dv_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        self.data_view.setSizePolicy(dv_policy)
        self.s_area.setWidget(self.data_view)
        self.s_area.setWidgetResizable(True)
        s_area_policy = QSizePolicy()
        s_area_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        s_area_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self.s_area.setSizePolicy(s_area_policy)
        dvp_layout = QFormLayout(self)
        dvp_layout.addWidget(self.s_area)

        dvp_layout.setContentsMargins(2,2,2,2)
        self.setLayout(dvp_layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event)
        diff = self.width() - self.s_area.width()
        if diff > 16:
            self.s_area.setGeometry(self.x() + 8, 
                                    self.s_area.y(),
                                    self.width() - 16,
                                    self.s_area.height()) 


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('One Line')
        mw_layout = QVBoxLayout(self)

        # self.line = OneLine(self)
        # mw_layout.addWidget(self.line)

        # self.data_view = DataView(self)
        # mw_layout.addWidget(self.data_view)

        self.dv_panel = DataViewerPanel(self)
        mw_layout.addWidget(self.dv_panel)
        mw_layout.setContentsMargins(2,2,2,2)
        self.setLayout(mw_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())