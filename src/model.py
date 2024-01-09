import sys
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtCore import (QAbstractListModel, QObject)


class MyObj:

    def __init__(self, fname, lname):
        self.__fname = fname
        self.__lname = lname

class PdfPagesModel(QAbstractListModel):
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self._pdf_files = []

def main():

    model = QStandardItemModel()
    parentItem = model.invisibleRootItem()
    for i in range(0, 4):
        item = QStandardItem(MyObj("Hui", "Viter"))
        # item = QStandardItem(f"item {i}")
        parentItem.appendRow(item)
        parentItem = item


    print(model.item(0).type())

    sys.exit(print("Done"))
    pass


if __name__ == "__main__":
    main()    