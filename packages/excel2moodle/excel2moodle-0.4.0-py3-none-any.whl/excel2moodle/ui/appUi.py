"""AppUi holds the extended  class mainWindow() and any other main Windows.

It needs to be seperated from ``windowMain.py`` because that file will be changed by the
``pyside6-uic`` command, which generates the python code from the ``.ui`` file
"""

import logging
from pathlib import Path

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QRunnable, Qt, QThreadPool

from excel2moodle import mainLogger
from excel2moodle.core.category import Category
from excel2moodle.core.dataStructure import QuestionDB
from excel2moodle.core.settings import Settings, SettingsKey
from excel2moodle.extra import equationVerification as eqVerif
from excel2moodle.logger import LogWindowHandler
from excel2moodle.ui import dialogs
from excel2moodle.ui.treewidget import CategoryItem, QuestionItem
from excel2moodle.ui.windowDoc import DocumentationWindow
from excel2moodle.ui.windowMain import Ui_MoodleTestGenerator

from .windowEquationChecker import Ui_EquationChecker

logger = logging.getLogger(__name__)

loggerSignal = LogWindowHandler()
mainLogger.addHandler(loggerSignal)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, settings: Settings, testDB: QuestionDB) -> None:
        super().__init__()
        self.settings = settings
        self.excelPath: Path | None = None
        self.mainPath = self.excelPath.parent if self.excelPath is not None else None
        self.exportFile = Path()
        self.testDB = testDB
        self.ui = Ui_MoodleTestGenerator()
        self.ui.setupUi(self)
        self.exportDialog = dialogs.ExportDialog(self)
        self.questionPreview = dialogs.QuestionPreview(self)
        self.connectEvents()
        logger.info("Settings are stored under: %s", self.settings.fileName())
        self.ui.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.ui.treeWidget.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents,
        )
        self.exportDialog.ui.checkBoxIncludeCategories.setChecked(
            self.settings.get(SettingsKey.INCLUDEINCATS),
        )
        self.exportDialog.ui.spinBoxDefaultQVariant.setValue(
            self.settings.get(SettingsKey.QUESTIONVARIANT)
        )
        self.ui.pointCounter.setReadOnly(True)
        self.ui.questionCounter.setReadOnly(True)
        self.setStatus(
            "Wählen Sie eine Excel Tabelle mit den Fragen aus",
        )
        try:
            self.resize(self.settings.value("windowSize"))
            self.move(self.settings.value("windowPosition"))
        except Exception:
            pass
        self.threadPool = QThreadPool()

    def connectEvents(self) -> None:
        self.ui.treeWidget.itemSelectionChanged.connect(self.onSelectionChanged)
        self.ui.checkBoxQuestionListSelectAll.checkStateChanged.connect(
            self.toggleQuestionSelectionState,
        )
        loggerSignal.emitter.signal.connect(self.updateLog)
        self.ui.actionEquationChecker.triggered.connect(self.openEqCheckerDlg)
        self.exportDialog.ui.checkBoxIncludeCategories.checkStateChanged.connect(
            self.setIncludeCategoriesSetting,
        )
        self.ui.actionParseAll.triggered.connect(self.parseSpreadsheetAll)
        self.testDB.signals.categoryQuestionsReady.connect(self.treeRefreshCategory)
        self.ui.actionSpreadsheet.triggered.connect(self.actionSpreadsheet)
        self.ui.actionExport.triggered.connect(self.onButGenTest)
        self.ui.buttonSpreadsheet.clicked.connect(self.actionSpreadsheet)
        self.ui.buttonExport.clicked.connect(self.onButGenTest)
        self.ui.treeWidget.itemClicked.connect(self.updateQuestionPreview)
        self.ui.actionAbout.triggered.connect(self.openAboutDlg)
        self.ui.actionDocumentation.triggered.connect(self.openDocumentation)
        self.settings.shPathChanged.connect(self.onSheetPathChanged)
        self.exportDialog.ui.spinBoxDefaultQVariant.valueChanged.connect(
            self.setQVariantDefault
        )

    @QtCore.Slot()
    def setQVariantDefault(self, value: int) -> None:
        self.settings.set(SettingsKey.QUESTIONVARIANT, value)

    @QtCore.Slot()
    def parseSpreadsheetAll(self) -> None:
        """Event triggered by the *Tools/Parse all Questions* Event.

        It parses all the Questions found in the spreadsheet
        and then refreshes the list of questions.
        If successful it prints out a list of all exported Questions
        """
        self.ui.treeWidget.clear()
        process = ParseAllThread(self.testDB, self)
        self.threadPool.start(process)

    @QtCore.Slot(Path)
    def onSheetPathChanged(self, sheet: Path) -> None:
        logger.debug("Slot, new Spreadsheet triggered")
        self.spreadSheetPath = sheet
        self.mainPath = sheet.parent
        svgFolder = self.mainPath / self.settings.get(SettingsKey.PICTURESUBFOLDER)
        svgFolder.resolve()
        self.settings.set(SettingsKey.PICTUREFOLDER, svgFolder)
        self.ui.buttonSpreadsheet.setText(f"../{sheet.name}")
        self.parseSpreadsheetAll()

    def updateLog(self, log) -> None:
        self.ui.loggerWindow.append(log)

    def setIncludeCategoriesSetting(self) -> None:
        if self.exportDialog.ui.checkBoxIncludeCategories.isChecked():
            self.settings.set(SettingsKey.INCLUDEINCATS, True)
        else:
            self.settings.set(SettingsKey.INCLUDEINCATS, False)

    def closeEvent(self, event) -> None:
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowPosition", self.pos())

    @QtCore.Slot()
    def onSelectionChanged(self, **args) -> None:
        """Whenever the selection changes the total of selected points needs to be recalculated."""
        count: int = 0
        questions: int = 0
        selection = self.ui.treeWidget.selectedItems()
        for q in selection:
            questions += 1
            count += q.getQuestion().points
        self.ui.pointCounter.setValue(count)
        self.ui.questionCounter.setValue(questions)

    @QtCore.Slot()
    def toggleQuestionSelectionState(self, state) -> None:
        setter = state == Qt.Checked
        root = self.ui.treeWidget.invisibleRootItem()
        childN = root.childCount()
        for i in range(childN):
            qs = root.child(i).childCount()
            for q in range(qs):
                root.child(i).child(q).setSelected(setter)

    @QtCore.Slot()
    def onButGenTest(self) -> None:
        """Open a file Dialog so the export file may be choosen."""
        self.exportDialog.exec()
        path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Select Output File",
            dir=f"{self.mainPath / 'Testfile.xml'}",
            filter="xml Files (*.xml)",
        )
        self.exportFile = Path(path[0])
        logger.info("New Export File is set %s", self.exportFile)
        selection: list[QuestionItem] = self.ui.treeWidget.selectedItems()
        self.testDB.appendQuestions(selection, self.exportFile)

    @QtCore.Slot()
    def actionSpreadsheet(self) -> None:
        file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open Spreadsheet"),
            dir=str(self.mainPath),
            filter=self.tr("Spreadsheet(*.xlsx *.ods)"),
            selectedFilter=("*.ods"),
        )
        path = Path(file[0]).resolve(strict=True)
        if path.is_file():
            self.excelPath = path
            self.settings.setSpreadsheet(self.excelPath)
            self.setStatus("[OK] Excel Tabelle wurde eingelesen")
        else:
            self.setStatus("[ERROR] keine Tabelle angegeben")

    @QtCore.Slot(Category)
    def treeRefreshCategory(self, cat: Category) -> None:
        """Append Category with its Questions to the treewidget."""
        catItem = CategoryItem(self.ui.treeWidget, cat)
        catItem.setFlags(catItem.flags() & ~Qt.ItemIsSelectable)
        for q in cat.questions.values():
            QuestionItem(catItem, q)
        self.ui.treeWidget.sortItems(0, Qt.SortOrder.AscendingOrder)

    @QtCore.Slot()
    def updateQuestionPreview(self) -> None:
        item = self.ui.treeWidget.currentItem()
        if isinstance(item, QuestionItem):
            self.questionPreview.setupQuestion(item.getQuestion())
        else:
            logger.info("current Item is not a Question, can't preview")

    def setStatus(self, status) -> None:
        self.ui.statusbar.clearMessage()
        self.ui.statusbar.showMessage(self.tr(status))

    @QtCore.Slot()
    def openEqCheckerDlg(self) -> None:
        logger.debug("opening wEquationChecker \n")
        self.uiEqChecker = EqCheckerWindow()
        self.uiEqChecker.excelFile = self.excelPath
        self.uiEqChecker.show()

    @QtCore.Slot()
    def openAboutDlg(self) -> None:
        about = dialogs.AboutDialog(self)
        about.exec()

    @QtCore.Slot()
    def openDocumentation(self) -> None:
        if hasattr(self, "documentationWindow"):
            self.documentationWindow.show()
        else:
            self.documentationWindow = DocumentationWindow(self)
            self.documentationWindow.show()


class ParseAllThread(QRunnable):
    """Parse the whole Spreadsheet.
    Start by reading the spreadsheet asynchron.
    When finished parse all Categories subsequently.
    """

    def __init__(self, questionDB: QuestionDB, mainApp: MainWindow) -> None:
        super().__init__()
        self.testDB = questionDB
        self.mainApp = mainApp

    @QtCore.Slot()
    def run(self) -> None:
        self.testDB.readCategoriesMetadata(self.mainApp.spreadSheetPath)
        self.testDB.asyncInitAllCategories(self.mainApp.spreadSheetPath)
        self.mainApp.setStatus("[OK] Tabellen wurde eingelesen")
        self.testDB.parseAllQuestions()


class EqCheckerWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.excelFile = Path()
        self.ui = Ui_EquationChecker()
        self.ui.setupUi(self)
        self.ui.buttonRunCheck.clicked.connect(
            lambda: self.onButRunCheck(
                self.ui.catNumber.value(),
                self.ui.qNumber.value(),
            ),
        )

    def onButRunCheck(self, catN: int, qN: int) -> None:
        """Is Triggered by the ``Run Check now`` Button and runs the Equation Check."""
        self.ui.textResultsOutput.clear()
        bullets, results, firstResult = eqVerif.equationChecker(
            f"KAT_{catN}",
            qN,
            self.excelFile,
        )
        check = False
        self.ui.lineFirstResult.setText(f"{firstResult}")
        for i, calculation in enumerate(results):
            if i == 0 and firstResult != 0:
                check = eqVerif.checkResult(firstResult, calculation)
                self.ui.lineCalculatedRes.setText(f"{calculation}")
            self.ui.textResultsOutput.append(
                f"Ergebnis {i + 1}: \t{calculation}\n\tMit den Werten: \n{bullets[i]}\n",
            )

        if check:
            self.ui.lineCheckResult.setText("[OK]")
            logger.info(
                "Das erste berechnete Ergebnis stimmt mit dem Wert in 'firstResult' überein\n",
            )
        else:
            self.ui.lineCheckResult.setText("[ERROR]")
