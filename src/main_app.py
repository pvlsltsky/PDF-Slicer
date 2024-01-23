import sys
import os.path
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from splitted_area import MainWindowSplitted

user_dir = os.path.expanduser("~")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PDFMergerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__status_label = QLabel('Initializing...', self)
        self.statusBar().addPermanentWidget(self.__status_label)
        splitted_area = MainWindowSplitted(self)
        self.setCentralWidget(splitted_area)
        self.setWindowTitle('PDF Merger')
        self.setStatusText("Ready")
        self.setWindowIcon(QIcon(QPixmap(resource_path("logo200.ico"))))
    
    @Slot(str)
    def setStatusText(self, msg : str):
        self.__status_label.setText(msg)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = PDFMergerMainWindow()
    window.resize(800, 400)
    window.show()
    sys.exit(app.exec())