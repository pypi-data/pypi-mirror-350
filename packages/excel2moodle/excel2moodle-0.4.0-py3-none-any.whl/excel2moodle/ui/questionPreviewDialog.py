# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'questionPreviewDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QGraphicsView, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_QuestionPrevDialog(object):
    def setupUi(self, QuestionPrevDialog):
        if not QuestionPrevDialog.objectName():
            QuestionPrevDialog.setObjectName(u"QuestionPrevDialog")
        QuestionPrevDialog.resize(577, 620)
        self.verticalLayout = QVBoxLayout(QuestionPrevDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(5)
        self.formLayout.setContentsMargins(10, 6, 10, -1)
        self.questionNameLabel = QLabel(QuestionPrevDialog)
        self.questionNameLabel.setObjectName(u"questionNameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.questionNameLabel)

        self.qNameLine = QLineEdit(QuestionPrevDialog)
        self.qNameLine.setObjectName(u"qNameLine")
        self.qNameLine.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.qNameLine)

        self.label = QLabel(QuestionPrevDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.qTypeLine = QLineEdit(QuestionPrevDialog)
        self.qTypeLine.setObjectName(u"qTypeLine")
        self.qTypeLine.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.qTypeLine)


        self.verticalLayout.addLayout(self.formLayout)

        self.line = QFrame(QuestionPrevDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.questionText = QLabel(QuestionPrevDialog)
        self.questionText.setObjectName(u"questionText")
        self.questionText.setWordWrap(True)
        self.questionText.setMargin(10)

        self.verticalLayout.addWidget(self.questionText)

        self.graphicsView = QGraphicsView(QuestionPrevDialog)
        self.graphicsView.setObjectName(u"graphicsView")
        brush = QBrush(QColor(231, 243, 245, 255))
        brush.setStyle(Qt.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)

        self.verticalLayout.addWidget(self.graphicsView)

        self.answersLabel = QLabel(QuestionPrevDialog)
        self.answersLabel.setObjectName(u"answersLabel")

        self.verticalLayout.addWidget(self.answersLabel)

        self.answersFormLayout = QFormLayout()
        self.answersFormLayout.setObjectName(u"answersFormLayout")
        self.answersFormLayout.setContentsMargins(-1, 3, -1, -1)

        self.verticalLayout.addLayout(self.answersFormLayout)

        self.buttonBox = QDialogButtonBox(QuestionPrevDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(QuestionPrevDialog)
        self.buttonBox.accepted.connect(QuestionPrevDialog.accept)
        self.buttonBox.rejected.connect(QuestionPrevDialog.reject)

        QMetaObject.connectSlotsByName(QuestionPrevDialog)
    # setupUi

    def retranslateUi(self, QuestionPrevDialog):
        QuestionPrevDialog.setWindowTitle(QCoreApplication.translate("QuestionPrevDialog", u"Dialog", None))
        self.questionNameLabel.setText(QCoreApplication.translate("QuestionPrevDialog", u"Question Name", None))
        self.label.setText(QCoreApplication.translate("QuestionPrevDialog", u"Question Type", None))
        self.questionText.setText(QCoreApplication.translate("QuestionPrevDialog", u"QuestionText", None))
        self.answersLabel.setText(QCoreApplication.translate("QuestionPrevDialog", u"Answers", None))
    # retranslateUi

