# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportSettingsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpinBox, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.resize(572, 217)
        self.horizontalLayout = QHBoxLayout(ExportDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_10 = QLabel(ExportDialog)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.spinBoxDefaultQVariant = QSpinBox(ExportDialog)
        self.spinBoxDefaultQVariant.setObjectName(u"spinBoxDefaultQVariant")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spinBoxDefaultQVariant)

        self.label_9 = QLabel(ExportDialog)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.checkBoxIncludeCategories = QCheckBox(ExportDialog)
        self.checkBoxIncludeCategories.setObjectName(u"checkBoxIncludeCategories")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.checkBoxIncludeCategories)


        self.horizontalLayout.addLayout(self.formLayout_2)

        self.buttonBox = QDialogButtonBox(ExportDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ExportDialog)
        self.buttonBox.accepted.connect(ExportDialog.accept)
        self.buttonBox.rejected.connect(ExportDialog.reject)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Dialog", None))
        self.label_10.setText(QCoreApplication.translate("ExportDialog", u"Default Question Variant", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("ExportDialog", u"If enabled, all questions will be categorized, when importing into moodle. Otherwise they will all be imported into one category", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("ExportDialog", u"Include Questions in Categories", None))
        self.checkBoxIncludeCategories.setText("")
    # retranslateUi

