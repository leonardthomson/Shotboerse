

"""
from PySide6 import QtCore, QtWidgets, QtWidgets
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.horizontalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Filepathselector_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Filepathselector_2)
        self.toolButton_2 = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.toolButton_2)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL("clicked()"), self.Filepathselector_2.clear)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL("clicked()"), self.showDialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        print("Bla")
        #MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, QtWidgets.QApplication.UnicodeUTF8))
        #self.Filepathselector_2.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Select file", None, QtWidgets.QApplication.UnicodeUTF8))
        #self.toolButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, QtWidgets.QApplication.UnicodeUTF8))


    def showDialog(self):
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open file', "", 'MP3 Files (*.mp3)')
            print(fname)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""