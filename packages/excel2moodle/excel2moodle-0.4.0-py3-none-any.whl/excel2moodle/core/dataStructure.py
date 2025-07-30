"""Main Module which does the heavy lifting.

At the heart is the class ``xmlTest``
"""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

import lxml.etree as ET  # noqa: N812
import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtCore import QObject, Signal

from excel2moodle.core import stringHelpers
from excel2moodle.core.category import Category
from excel2moodle.core.exceptions import InvalidFieldException, QNotParsedException
from excel2moodle.core.globals import DFIndex
from excel2moodle.core.question import Question
from excel2moodle.core.settings import Settings, SettingsKey
from excel2moodle.core.validator import Validator
from excel2moodle.logger import LogAdapterQuestionID
from excel2moodle.question_types import QuestionTypeMapping
from excel2moodle.question_types.mc import MCQuestion, MCQuestionParser
from excel2moodle.question_types.nf import NFQuestion, NFQuestionParser
from excel2moodle.question_types.nfm import NFMQuestion, NFMQuestionParser
from excel2moodle.ui.dialogs import QuestionVariantDialog
from excel2moodle.ui.treewidget import QuestionItem

if TYPE_CHECKING:
    from PySide6.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)


class QuestionDBSignals(QObject):
    categoryReady = Signal(Category)
    categoryQuestionsReady = Signal(Category)


def processSheet(sheetPath: str, categoryName: str) -> pd.DataFrame:
    """Parse `categoryName` from the file ``sheetPath`` into the dataframe.

    This Function is meant to be run asynchron for increased speed.
    """
    return pd.read_excel(
        Path(sheetPath),
        sheet_name=str(categoryName),
        index_col=0,
        header=None,
    )


class QuestionDB:
    """The QuestionDB is the main class for processing the Spreadsheet.

    It provides the functionality, for setting up the categories and Questions.
    Any interaction with the questions are done by its methods.
    """

    signals = QuestionDBSignals()
    validator: Validator = Validator()
    nfParser: NFQuestionParser = NFQuestionParser()
    nfmParser: NFMQuestionParser = NFMQuestionParser()
    mcParser: MCQuestionParser = MCQuestionParser()

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.window: QMainWindow | None = None
        self.version = None
        self.categoriesMetaData: pd.DataFrame
        self.categories: dict[str, Category]

    def readCategoriesMetadata(self, sheetPath: Path) -> None:
        """Read the metadata and questions from the spreadsheet.

        Get the category data from the spreadsheet and stores it in the
        ``categoriesMetaData`` dataframe
        Setup the categories and store them  in ``self.categories = {}``
        Pass the question data to the categories.
        """
        logger.info("Start Parsing the Excel Metadata Sheet\n")
        with Path(sheetPath).open("rb") as f:
            settingDf = pd.read_excel(
                f,
                sheet_name="settings",
                index_col=0,
            )
            logger.debug("Found the settings: \n\t%s", settingDf)
            self._setProjectSettings(settingDf)
        with Path(sheetPath).open("rb") as f:
            self.categoriesMetaData = pd.read_excel(
                f,
                sheet_name=self.settings.get(SettingsKey.CATEGORIESSHEET),
                index_col=0,
            )
            logger.info(
                "Sucessfully read categoriesMetaData \n %s", self.categoriesMetaData
            )

    def _setProjectSettings(self, settings: pd.DataFrame) -> None:
        for tag, value in settings.iterrows():
            self.settings.set(tag, value.iloc[0], local=True)

    def initAllCategories(self, sheetPath: Path) -> None:
        """Read all category sheets and initialize all Categories."""
        if not hasattr(self, "categoriesMetaData"):
            logger.error("Can't process the Categories without Metadata")
            return
        if hasattr(self, "categories"):
            self.categories.clear()
        else:
            self.categories: dict[str, Category] = {}
        with Path(sheetPath).open("rb") as f:
            excelFile = pd.ExcelFile(f)
            for categoryName in excelFile.sheet_names:
                logger.debug("Starting to read category %s", categoryName)
                if categoryName.startswith("KAT"):
                    self.initCategory(sheetPath, categoryName)

    def asyncInitAllCategories(self, sheetPath: Path) -> None:
        """Read all category sheets asynchron and initialize all Categories.

        It does the same as `initAllCategories` but the parsing of the excelfile
        is done asynchron via `concurrent.futures.ProcessPoolExecutor`
        """
        if not hasattr(self, "categoriesMetaData"):
            logger.error("Can't process the Categories without Metadata")
            return
        if hasattr(self, "categories"):
            self.categories.clear()
        else:
            self.categories: dict[str, Category] = {}
        sheet_names = []
        with Path(sheetPath).open("rb") as f:
            excel_file = pd.ExcelFile(f)
            sheet_names = [
                name for name in excel_file.sheet_names if name.startswith("KAT_")
            ]
        logger.debug("found those caetegory sheets: \n %s ", sheet_names)
        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(processSheet, str(sheetPath), sheet): sheet
                for sheet in sheet_names
            }
            for future in as_completed(futures):
                categoryName = futures[future]
                try:
                    categoryDataF = future.result()
                    categoryNumber = int(categoryName[4:])
                    self._setupCategory(categoryDataF, categoryName, categoryNumber)
                    logger.debug("Finished processing %s", categoryName)
                except Exception as e:
                    logger.exception("Error processing sheet %s: %s", categoryName, e)
                    logger.debug("Future exception: %s", future.exception())

    def initCategory(self, sheetPath: Path, categoryName: str) -> None:
        """Read `categoryName` from the file ``sheetPath`` and initialize the category."""
        categoryNumber = int(categoryName[4:])
        katDf = pd.read_excel(
            sheetPath,
            sheet_name=str(categoryName),
            index_col=0,
            header=None,
        )
        if not katDf.empty:
            logger.debug("Sucessfully read the Dataframe for cat %s", categoryName)
            self._setupCategory(katDf, categoryName, categoryNumber)

    def _setupCategory(
        self, categoryDf: pd.DataFrame, categoryName: str, categoryNumber: int
    ) -> None:
        """Setup the category from the ``dataframe``.
        :emits: categoryReady(self) Signal.
        """  # noqa: D401
        points = (
            self.categoriesMetaData["points"].iloc[categoryNumber - 1]
            if "points" in self.categoriesMetaData
            and not pd.isna(self.categoriesMetaData["points"]).iloc[categoryNumber - 1]
            else self.settings.get(SettingsKey.POINTS)
        )
        version = (
            self.categoriesMetaData["version"].iloc[categoryNumber - 1]
            if "version" in self.categoriesMetaData
            and not pd.isna(self.categoriesMetaData["version"].iloc[categoryNumber - 1])
            else self.settings.get(SettingsKey.VERSION)
        )
        category = Category(
            categoryNumber,
            categoryName,
            self.categoriesMetaData["description"].iloc[categoryNumber - 1],
            dataframe=categoryDf,
            points=points,
            version=version,
        )
        self.categories[categoryName] = category
        logger.debug("Category %s is initialized", categoryName)
        self.signals.categoryReady.emit(category)

    def parseAllQuestions(self) -> None:
        """Parse all question from all categories.

        The categories need to be initialized first.
        """
        for category in self.categories.values():
            self.parseCategoryQuestions(category)

    def parseCategoryQuestions(self, category: Category) -> None:
        """Parse all questions inside ``category``.

        The category has to be initialized first.
        """
        for qNum in category.dataframe.columns:
            try:
                self.setupAndParseQuestion(category, qNum)
            except (InvalidFieldException, QNotParsedException, ValueError) as e:
                logger.exception(
                    "Question %s%02d couldn't be parsed. The Question Data: \n %s",
                    category.id,
                    qNum,
                    category.dataframe[qNum],
                    exc_info=e,
                )
        self.signals.categoryQuestionsReady.emit(category)

    @classmethod
    def setupAndParseQuestion(cls, category: Category, qNumber: int) -> None:
        """Check if the Question Data is valid. Then parse it.

        The Question data is accessed from  `category.dataframe` via its number
        First it is checked if all mandatory fields for the given question type
        are provided.
        Then in checks, weather the data has the correct type.
        If the data is valid, the corresponding parser is fed with the data and run.

        Raises
        ------
        QNotParsedException
            If the parsing of the question is not possible this is raised
        InvalidFieldException
            If the data of the question is invalid.
            This gives more information wheather a missing field, or the invalid type
            caused the Exception.

        """
        locallogger = LogAdapterQuestionID(
            logger, {"qID": f"{category.id}{qNumber:02d}"}
        )
        locallogger.debug("Starting to check Validity")
        qdat = category.dataframe[qNumber]
        if not isinstance(qdat, pd.Series):
            locallogger.error("cannot validate data that isn't a pd.Series")
            msg = "cannot validate data that isn't a pd.Series"
            raise QNotParsedException(msg, f"{category.id}{qNumber}")
        cls.validator.setup(qdat, qNumber)
        cls.validator.validate()
        validData = cls.validator.getQuestionRawData()
        qtype: str = str(validData.get(DFIndex.TYPE))
        category.questions[qNumber] = QuestionTypeMapping[qtype].create(
            category, validData
        )
        question = category.questions[qNumber]
        if question.element is not None:
            locallogger.info("Question already parsed")
            return
        if isinstance(question, NFQuestion):
            cls.nfParser.setup(question)
            cls.nfParser.parse()
            locallogger.debug("setup a new NF parser ")
        elif isinstance(question, MCQuestion):
            cls.mcParser.setup(question)
            cls.mcParser.parse()
            locallogger.debug("setup a new MC parser ")
        elif isinstance(question, NFMQuestion):
            cls.nfmParser.setup(question)
            cls.nfmParser.parse()
            locallogger.debug("setup a new NFM parser ")
        else:
            msg = "couldn't setup Parser"
            raise QNotParsedException(msg, question.id)

    def appendQuestions(
        self, questions: list[QuestionItem], file: Path | None = None
    ) -> None:
        """Append selected question Elements to the tree."""
        tree = ET.Element("quiz")
        catdict: dict[Category, list[Question]] = {}
        for q in questions:
            logger.debug(f"got a question to append {q=}")
            cat = q.parent().getCategory()
            if cat not in catdict:
                catdict[cat] = []
            catdict[cat].append(q.getQuestion())
        for cat, qlist in catdict.items():
            self.appendQElements(
                cat,
                qlist,
                tree=tree,
                includeHeader=self.settings.get(SettingsKey.INCLUDEINCATS),
            )
        stringHelpers.printDom(tree, file=file)

    def appendQElements(
        self,
        cat: Category,
        qList: list[Question],
        tree: ET.Element,
        includeHeader: bool = True,
    ) -> None:
        if includeHeader:
            tree.append(cat.getCategoryHeader())
            logger.debug(f"Appended a new category item {cat=}")
        variant: int = self.settings.get(SettingsKey.QUESTIONVARIANT)
        for q in qList:
            if q.variants is not None:
                if variant == 0 or variant > q.variants:
                    dialog = QuestionVariantDialog(self.window, q)
                    if dialog.exec() == QtWidgets.QDialog.Accepted:
                        variant = dialog.variant
                        logger.debug("Die Fragen-Variante %s wurde gewählt", variant)
                    else:
                        logger.warning("Keine Fragenvariante wurde gewählt.")
                q.assemble(variant)
            else:
                q.assemble()
            tree.append(q.element)
