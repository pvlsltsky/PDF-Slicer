from PySide6.QtWidgets import QErrorMessage, QMessageBox

class StatusUpdater():

    def setStatusText(self, text : str):
        try:
            self.__status_label.setText(text)
        except:
            if self.parent():
                self.parent().setStatusText(text)
            else:
                self.showInfoMessage(text)

    def showInfoMessage(self, text : str):            
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Info")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setText(text)
        dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
        dialog.show()

    def showErrorMessage(self, text):
        error_message = QErrorMessage(self)
        error_message.setWindowTitle("Error")
        error_message.showMessage(f"An error has occurred. \nDetails: {text}")