# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'myWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pyqtgraph import PlotWidget
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 1000))
        self.frame.setMinimumSize(QSize(0, 300))

        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame.setStyleSheet("""QFrame {background-color: black; color: white; font-size: 25px } """)
        self.order = QLabel(self.frame)
        self.order.setObjectName(u"order")
        self.order.setStyleSheet("""QLabel {background-color: black; color: white; font-size: 25px } """)
        #self.order.setMinimumSize(QSize(400, 400))




        self.gridLayout_2.addWidget(self.order, 0, 0, 1, 1)

        self.pay = QLabel(self.frame)
        self.pay.setObjectName(u"pay")
        self.pay.setMinimumSize(QSize(400, 0))
        self.pay.setStyleSheet("""QLabel {background-color: black; color: white; font-size: 24px } """)


        self.gridLayout_2.addWidget(self.pay, 1, 2, 1, 1)

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet("""QLineEdit {background-color: black; color: white } """)

        self.gridLayout_2.addWidget(self.lineEdit, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.priceList = QListWidget(self.frame)
        self.priceList.setObjectName(u"priceList")
        self.priceList.setMinimumSize(QSize(800, 100))
        self.priceList.setStyleSheet("""QListWidget {background-color: black; color: red; font-size: 30px } """)


        self.gridLayout_2.addWidget(self.priceList, 0, 3, 2, 1)


        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)

        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.order.setText(QCoreApplication.translate("MainWindow", u"Bestellung:", None))
        self.pay.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

