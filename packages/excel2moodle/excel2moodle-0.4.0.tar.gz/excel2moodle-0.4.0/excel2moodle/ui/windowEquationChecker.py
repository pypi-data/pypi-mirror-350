# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equationChecker.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget)

class Ui_EquationChecker(object):
    def setupUi(self, EquationChecker):
        if not EquationChecker.objectName():
            EquationChecker.setObjectName(u"EquationChecker")
        EquationChecker.resize(1213, 898)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        EquationChecker.setWindowIcon(icon)
        EquationChecker.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(EquationChecker)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(EquationChecker)
        self.label_6.setObjectName(u"label_6")
        font = QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)

        self.qNumber = QSpinBox(EquationChecker)
        self.qNumber.setObjectName(u"qNumber")
        self.qNumber.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.qNumber, 2, 1, 1, 1)

        self.lineFirstResult = QLineEdit(EquationChecker)
        self.lineFirstResult.setObjectName(u"lineFirstResult")
        self.lineFirstResult.setEnabled(True)
        font1 = QFont()
        font1.setBold(True)
        self.lineFirstResult.setFont(font1)
        self.lineFirstResult.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineFirstResult.setReadOnly(True)

        self.gridLayout.addWidget(self.lineFirstResult, 1, 4, 1, 1)

        self.label_2 = QLabel(EquationChecker)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(200, 0))

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.catNumber = QSpinBox(EquationChecker)
        self.catNumber.setObjectName(u"catNumber")

        self.gridLayout.addWidget(self.catNumber, 1, 1, 1, 1)

        self.label_3 = QLabel(EquationChecker)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 3, 1, 1)

        self.label_5 = QLabel(EquationChecker)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.buttonRunCheck = QPushButton(EquationChecker)
        self.buttonRunCheck.setObjectName(u"buttonRunCheck")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.buttonRunCheck.setFont(font2)

        self.gridLayout.addWidget(self.buttonRunCheck, 4, 1, 1, 1)

        self.label_8 = QLabel(EquationChecker)
        self.label_8.setObjectName(u"label_8")
        font3 = QFont()
        font3.setPointSize(12)
        self.label_8.setFont(font3)

        self.gridLayout.addWidget(self.label_8, 4, 3, 1, 1)

        self.lineCheckResult = QLineEdit(EquationChecker)
        self.lineCheckResult.setObjectName(u"lineCheckResult")
        font4 = QFont()
        font4.setBold(True)
        font4.setItalic(True)
        self.lineCheckResult.setFont(font4)
        self.lineCheckResult.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineCheckResult.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineCheckResult.setReadOnly(True)

        self.gridLayout.addWidget(self.lineCheckResult, 4, 4, 1, 1)

        self.lineCalculatedRes = QLineEdit(EquationChecker)
        self.lineCalculatedRes.setObjectName(u"lineCalculatedRes")
        self.lineCalculatedRes.setFont(font1)
        self.lineCalculatedRes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineCalculatedRes.setReadOnly(True)
        self.lineCalculatedRes.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.lineCalculatedRes, 3, 4, 1, 1)

        self.label_4 = QLabel(EquationChecker)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 3, 1, 1)

        self.label = QLabel(EquationChecker)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_7 = QLabel(EquationChecker)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font3)

        self.verticalLayout.addWidget(self.label_7)

        self.line = QFrame(EquationChecker)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textResultsOutput = QTextEdit(EquationChecker)
        self.textResultsOutput.setObjectName(u"textResultsOutput")

        self.verticalLayout_2.addWidget(self.textResultsOutput)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(EquationChecker)

        QMetaObject.connectSlotsByName(EquationChecker)
    # setupUi

    def retranslateUi(self, EquationChecker):
        EquationChecker.setWindowTitle(QCoreApplication.translate("EquationChecker", u"Equation Checker", None))
        self.label_6.setText(QCoreApplication.translate("EquationChecker", u"Output", None))
        self.lineFirstResult.setText(QCoreApplication.translate("EquationChecker", u"0.00", None))
        self.lineFirstResult.setPlaceholderText(QCoreApplication.translate("EquationChecker", u"waiting", None))
        self.label_2.setText(QCoreApplication.translate("EquationChecker", u"Question Number", None))
        self.label_3.setText(QCoreApplication.translate("EquationChecker", u"firstResult from spreadsheet", None))
        self.label_5.setText(QCoreApplication.translate("EquationChecker", u"Input", None))
        self.buttonRunCheck.setText(QCoreApplication.translate("EquationChecker", u"Run Check now", None))
        self.label_8.setText(QCoreApplication.translate("EquationChecker", u"Check", None))
        self.lineCheckResult.setText("")
        self.lineCheckResult.setPlaceholderText(QCoreApplication.translate("EquationChecker", u"waiting for check", None))
        self.lineCalculatedRes.setText(QCoreApplication.translate("EquationChecker", u"0.00", None))
        self.label_4.setText(QCoreApplication.translate("EquationChecker", u"calculated first Result", None))
        self.label.setText(QCoreApplication.translate("EquationChecker", u"Category Number", None))
        self.label_7.setText(QCoreApplication.translate("EquationChecker", u"Calculated Values with corresponding properties", None))
    # retranslateUi

