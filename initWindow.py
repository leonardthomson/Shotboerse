from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 300)
        Dialog.setMaximumSize(QSize(500, 300))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.select_shots = QGroupBox(Dialog)
        self.select_shots.setObjectName(u"select_shots")
        self.gridLayout_2 = QGridLayout(self.select_shots)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.mex = QCheckBox(self.select_shots)
        self.mex.setObjectName(u"mex")

        self.gridLayout_2.addWidget(self.mex, 0, 0, 1, 1)

        self.gim = QCheckBox(self.select_shots)
        self.gim.setObjectName(u"gim")

        self.gridLayout_2.addWidget(self.gim, 0, 1, 1, 1)

        self.blu = QCheckBox(self.select_shots)
        self.blu.setObjectName(u"blu")

        self.gridLayout_2.addWidget(self.blu, 0, 2, 1, 1)

        self.fis = QCheckBox(self.select_shots)
        self.fis.setObjectName(u"fis")

        self.gridLayout_2.addWidget(self.fis, 1, 0, 1, 1)

        self.teq = QCheckBox(self.select_shots)
        self.teq.setObjectName(u"teq")

        self.gridLayout_2.addWidget(self.teq, 1, 1, 1, 1)

        self.vod = QCheckBox(self.select_shots)
        self.vod.setObjectName(u"vod")

        self.gridLayout_2.addWidget(self.vod, 1, 2, 1, 1)

        self.ber = QCheckBox(self.select_shots)
        self.ber.setObjectName(u"ber")

        self.gridLayout_2.addWidget(self.ber, 2, 0, 1, 1)

        self.pfe = QCheckBox(self.select_shots)
        self.pfe.setObjectName(u"pfe")

        self.gridLayout_2.addWidget(self.pfe, 2, 1, 1, 1)

        self.jos = QCheckBox(self.select_shots)
        self.jos.setObjectName(u"jos")

        self.gridLayout_2.addWidget(self.jos, 2, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.select_shots)

        self.settings = QGroupBox(Dialog)
        self.settings.setObjectName(u"settings")
        self.settings.setMaximumSize(QSize(16777215, 60))
        self.verticalLayout = QVBoxLayout(self.settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.log = QCheckBox(self.settings)
        self.log.setObjectName(u"log")

        self.verticalLayout.addWidget(self.log)


        self.verticalLayout_2.addWidget(self.settings)

        self.dialogButtonBox = QDialogButtonBox(Dialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.dialogButtonBox)


        self.retranslateUi(Dialog)
        self.dialogButtonBox.accepted.connect(Dialog.accept)
        self.dialogButtonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Start shot-stock", None))
        self.select_shots.setTitle(QCoreApplication.translate("Dialog", u"Select shots:", None))
        self.mex.setText(QCoreApplication.translate("Dialog", u"Mexikaner", None))
        self.gim.setText(QCoreApplication.translate("Dialog", u"Gimlet", None))
        self.blu.setText(QCoreApplication.translate("Dialog", u"Blue shot", None))
        self.fis.setText(QCoreApplication.translate("Dialog", u"Fish shot", None))
        self.teq.setText(QCoreApplication.translate("Dialog", u"Tequila", None))
        self.vod.setText(QCoreApplication.translate("Dialog", u"Vodka", None))
        self.ber.setText(QCoreApplication.translate("Dialog", u"Berentzen", None))
        self.pfe.setText(QCoreApplication.translate("Dialog", u"Pfeffi", None))
        self.jos.setText(QCoreApplication.translate("Dialog", u"Joster", None))
        self.settings.setTitle(QCoreApplication.translate("Dialog", u"Settings:", None))
        self.log.setText(QCoreApplication.translate("Dialog", u"Log sells", None))

    def extract_checks(self):
        ls = [self.mex.isChecked(), self.gim.isChecked(), self.blu.isChecked(),
              self.fis.isChecked(), self.teq.isChecked(), self.vod.isChecked(),
              self.ber.isChecked(), self.jos.isChecked(), self.pfe.isChecked()]
        return ls, self.log.isChecked() 


