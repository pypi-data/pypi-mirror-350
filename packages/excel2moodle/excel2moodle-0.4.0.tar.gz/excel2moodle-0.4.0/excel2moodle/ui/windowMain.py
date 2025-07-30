# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QDoubleSpinBox, QFormLayout, QFrame, QGraphicsView,
    QGridLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSplitter, QStatusBar,
    QTextEdit, QToolBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MoodleTestGenerator(object):
    def setupUi(self, MoodleTestGenerator):
        if not MoodleTestGenerator.objectName():
            MoodleTestGenerator.setObjectName(u"MoodleTestGenerator")
        MoodleTestGenerator.resize(1101, 1010)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogQuestion))
        MoodleTestGenerator.setWindowIcon(icon)
        self.actionSpreadsheet = QAction(MoodleTestGenerator)
        self.actionSpreadsheet.setObjectName(u"actionSpreadsheet")
        icon1 = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionSpreadsheet.setIcon(icon1)
        self.actionEquationChecker = QAction(MoodleTestGenerator)
        self.actionEquationChecker.setObjectName(u"actionEquationChecker")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ToolsCheckSpelling))
        self.actionEquationChecker.setIcon(icon2)
        self.actionParseAll = QAction(MoodleTestGenerator)
        self.actionParseAll.setObjectName(u"actionParseAll")
        icon3 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.actionParseAll.setIcon(icon3)
        self.actionSetting = QAction(MoodleTestGenerator)
        self.actionSetting.setObjectName(u"actionSetting")
        icon4 = QIcon(QIcon.fromTheme(u"preferences-system"))
        self.actionSetting.setIcon(icon4)
        self.actionExport = QAction(MoodleTestGenerator)
        self.actionExport.setObjectName(u"actionExport")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        self.actionExport.setIcon(icon5)
        self.actionAbout = QAction(MoodleTestGenerator)
        self.actionAbout.setObjectName(u"actionAbout")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.actionAbout.setIcon(icon6)
        self.actionDocumentation = QAction(MoodleTestGenerator)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionDocumentation.setIcon(icon6)
        self.mainWidget = QWidget(MoodleTestGenerator)
        self.mainWidget.setObjectName(u"mainWidget")
        self.verticalLayout_3 = QVBoxLayout(self.mainWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter_2 = QSplitter(self.mainWidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.splitter_2.setHandleWidth(3)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(3)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 4, 4)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.line_4 = QFrame(self.layoutWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 1, 3, 1, 1)

        self.checkBoxQuestionListSelectAll = QCheckBox(self.layoutWidget)
        self.checkBoxQuestionListSelectAll.setObjectName(u"checkBoxQuestionListSelectAll")

        self.gridLayout.addWidget(self.checkBoxQuestionListSelectAll, 1, 0, 1, 1)

        self.questionCounter = QDoubleSpinBox(self.layoutWidget)
        self.questionCounter.setObjectName(u"questionCounter")
        self.questionCounter.setMaximumSize(QSize(120, 16777215))
        font = QFont()
        font.setPointSize(13)
        self.questionCounter.setFont(font)
        self.questionCounter.setReadOnly(True)
        self.questionCounter.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.questionCounter.setDecimals(0)
        self.questionCounter.setMaximum(300.000000000000000)

        self.gridLayout.addWidget(self.questionCounter, 1, 1, 1, 1)

        self.pointCounter = QDoubleSpinBox(self.layoutWidget)
        self.pointCounter.setObjectName(u"pointCounter")
        self.pointCounter.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pointCounter.sizePolicy().hasHeightForWidth())
        self.pointCounter.setSizePolicy(sizePolicy)
        self.pointCounter.setMaximumSize(QSize(120, 16777215))
        self.pointCounter.setBaseSize(QSize(190, 0))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(False)
        self.pointCounter.setFont(font1)
        self.pointCounter.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pointCounter.setAutoFillBackground(False)
        self.pointCounter.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.pointCounter.setWrapping(False)
        self.pointCounter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.pointCounter.setReadOnly(True)
        self.pointCounter.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pointCounter.setDecimals(1)
        self.pointCounter.setMaximum(9999.899999999999636)

        self.gridLayout.addWidget(self.pointCounter, 1, 2, 1, 1)

        self.buttonSpreadsheet = QPushButton(self.layoutWidget)
        self.buttonSpreadsheet.setObjectName(u"buttonSpreadsheet")

        self.gridLayout.addWidget(self.buttonSpreadsheet, 0, 0, 1, 1)

        self.buttonExport = QPushButton(self.layoutWidget)
        self.buttonExport.setObjectName(u"buttonExport")

        self.gridLayout.addWidget(self.buttonExport, 0, 2, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.treeWidget = QTreeWidget(self.layoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignLeading|Qt.AlignVCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setBaseSize(QSize(0, 60))
        self.treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setMinimumSectionSize(8)

        self.verticalLayout_4.addWidget(self.treeWidget)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.verticalLayout_2.setContentsMargins(4, 0, 0, 4)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(True)
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_3.setHorizontalSpacing(20)
        self.formLayout_3.setVerticalSpacing(5)
        self.formLayout_3.setContentsMargins(10, 6, 10, -1)
        self.questionNameLabel = QLabel(self.layoutWidget1)
        self.questionNameLabel.setObjectName(u"questionNameLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.questionNameLabel)

        self.qNameLine = QLineEdit(self.layoutWidget1)
        self.qNameLine.setObjectName(u"qNameLine")
        self.qNameLine.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.qNameLine)


        self.verticalLayout_2.addLayout(self.formLayout_3)

        self.questionText = QLabel(self.layoutWidget1)
        self.questionText.setObjectName(u"questionText")
        self.questionText.setWordWrap(True)
        self.questionText.setMargin(10)

        self.verticalLayout_2.addWidget(self.questionText)

        self.line_6 = QFrame(self.layoutWidget1)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_6)

        self.answersLabel = QLabel(self.layoutWidget1)
        self.answersLabel.setObjectName(u"answersLabel")
        self.answersLabel.setMargin(10)

        self.verticalLayout_2.addWidget(self.answersLabel)

        self.graphicsView = QGraphicsView(self.layoutWidget1)
        self.graphicsView.setObjectName(u"graphicsView")
        brush = QBrush(QColor(231, 243, 245, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)

        self.verticalLayout_2.addWidget(self.graphicsView)

        self.splitter.addWidget(self.layoutWidget1)
        self.splitter_2.addWidget(self.splitter)
        self.layoutWidget2 = QWidget(self.splitter_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.verticalLayout = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 3, 0, 0)
        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setBaseSize(QSize(0, 20))
        self.label_4.setIndent(8)

        self.verticalLayout.addWidget(self.label_4)

        self.loggerWindow = QTextEdit(self.layoutWidget2)
        self.loggerWindow.setObjectName(u"loggerWindow")
        self.loggerWindow.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.loggerWindow.sizePolicy().hasHeightForWidth())
        self.loggerWindow.setSizePolicy(sizePolicy2)
        self.loggerWindow.setMinimumSize(QSize(0, 0))
        self.loggerWindow.setMaximumSize(QSize(16777215, 800))
        self.loggerWindow.setBaseSize(QSize(0, 29))
        self.loggerWindow.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout.addWidget(self.loggerWindow)

        self.splitter_2.addWidget(self.layoutWidget2)

        self.verticalLayout_3.addWidget(self.splitter_2)

        MoodleTestGenerator.setCentralWidget(self.mainWidget)
        self.menubar = QMenuBar(MoodleTestGenerator)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1101, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MoodleTestGenerator.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MoodleTestGenerator)
        self.statusbar.setObjectName(u"statusbar")
        MoodleTestGenerator.setStatusBar(self.statusbar)
        self.toolBar_3 = QToolBar(MoodleTestGenerator)
        self.toolBar_3.setObjectName(u"toolBar_3")
        MoodleTestGenerator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_3)
        self.toolBar = QToolBar(MoodleTestGenerator)
        self.toolBar.setObjectName(u"toolBar")
        MoodleTestGenerator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionSpreadsheet)
        self.menuTools.addAction(self.actionParseAll)
        self.menuTools.addAction(self.actionEquationChecker)
        self.menuTools.addAction(self.actionSetting)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionDocumentation)
        self.toolBar_3.addAction(self.actionEquationChecker)
        self.toolBar_3.addAction(self.actionDocumentation)
        self.toolBar_3.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionSpreadsheet)
        self.toolBar.addAction(self.actionParseAll)
        self.toolBar.addAction(self.actionExport)

        self.retranslateUi(MoodleTestGenerator)

        QMetaObject.connectSlotsByName(MoodleTestGenerator)
    # setupUi

    def retranslateUi(self, MoodleTestGenerator):
        MoodleTestGenerator.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"excel 2 moodle", None))
        self.actionSpreadsheet.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Input Spreadsheet", None))
#if QT_CONFIG(tooltip)
        self.actionSpreadsheet.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"Open the question spreadsheet", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSpreadsheet.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionEquationChecker.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Equation Checker", None))
        self.actionParseAll.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Parse all Questions", None))
#if QT_CONFIG(tooltip)
        self.actionParseAll.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"Parse all questions inside the spreadsheet", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionParseAll.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionSetting.setText(QCoreApplication.translate("MoodleTestGenerator", u"Settings", None))
        self.actionExport.setText(QCoreApplication.translate("MoodleTestGenerator", u"Export the question selection ", None))
#if QT_CONFIG(shortcut)
        self.actionExport.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MoodleTestGenerator", u"About", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MoodleTestGenerator", u"Documentation", None))
#if QT_CONFIG(tooltip)
        self.actionDocumentation.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"Open the documentation for excel2moodle", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionDocumentation.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.checkBoxQuestionListSelectAll.setText(QCoreApplication.translate("MoodleTestGenerator", u"Select all", None))
#if QT_CONFIG(tooltip)
        self.questionCounter.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"The number of selected questions", None))
#endif // QT_CONFIG(tooltip)
        self.questionCounter.setPrefix("")
        self.questionCounter.setSuffix(QCoreApplication.translate("MoodleTestGenerator", u"  Qst.", None))
#if QT_CONFIG(tooltip)
        self.pointCounter.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"The total number of points of all selected questions.", None))
#endif // QT_CONFIG(tooltip)
        self.pointCounter.setPrefix("")
        self.pointCounter.setSuffix(QCoreApplication.translate("MoodleTestGenerator", u"  Pts.", None))
        self.buttonSpreadsheet.setText(QCoreApplication.translate("MoodleTestGenerator", u"Open Spreadsheet", None))
#if QT_CONFIG(tooltip)
        self.buttonExport.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"Export the selected questions  to a xml file", None))
#endif // QT_CONFIG(tooltip)
        self.buttonExport.setText(QCoreApplication.translate("MoodleTestGenerator", u"Export", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MoodleTestGenerator", u"Variants", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MoodleTestGenerator", u"Points", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MoodleTestGenerator", u"Description", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MoodleTestGenerator", u"Question ID", None));
        self.label.setText(QCoreApplication.translate("MoodleTestGenerator", u"Question Preview", None))
        self.questionNameLabel.setText(QCoreApplication.translate("MoodleTestGenerator", u"Question:", None))
        self.questionText.setText(QCoreApplication.translate("MoodleTestGenerator", u"QuestionText", None))
        self.answersLabel.setText(QCoreApplication.translate("MoodleTestGenerator", u"Answers", None))
        self.label_4.setText(QCoreApplication.translate("MoodleTestGenerator", u"Logging Messages", None))
        self.menuFile.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"Help", None))
        self.toolBar_3.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"toolBar_3", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"toolBar", None))
    # retranslateUi

