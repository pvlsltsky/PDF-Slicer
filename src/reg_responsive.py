import sys
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (QApplication, QWidget,  QFormLayout,
                               QGridLayout, QPushButton, QGroupBox, 
                               QLineEdit, QDateEdit, QSplitter)
from PySide6.QtCore import Qt

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

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt QGroupBox')

        # layout = QFormLayout(self)
        d_layout = QGridLayout(self)
        self.setLayout(d_layout)

        self.main_box = MainBox(self)
        self.pdf_box = PDFViewerBox(self)

        d_layout.addWidget(self.main_box, 0, 0)
        d_layout.addWidget(self.pdf_box, 0, 1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        res = super().resizeEvent(event) 
        pdf_box_column = self.layout().getItemPosition(self.layout().indexOf(self.pdf_box))[1]
        width = self.width()
        if width < 500 and pdf_box_column != 0:
            # self.layout().removeItem(self.layout().takeAt(self.layout().indexOf(self.contact_groupbox)))
            self.layout().removeWidget(self.pdf_box)
            self.layout().addWidget(self.pdf_box, 1, 0)
        elif width > 500 and  pdf_box_column != 1:
            self.layout().removeWidget(self.pdf_box)
            self.layout().addWidget(self.pdf_box, 0, 1)
        return res

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
    # window = MainWindow()
    window = MainWindowSplitted()
    window.show()
    sys.exit(app.exec())