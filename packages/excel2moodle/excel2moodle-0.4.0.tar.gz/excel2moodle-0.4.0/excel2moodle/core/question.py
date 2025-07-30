import base64
import logging
import re
import typing
from pathlib import Path
from re import Match

import lxml.etree as ET

from excel2moodle.core import etHelpers
from excel2moodle.core.category import Category
from excel2moodle.core.exceptions import QNotParsedException
from excel2moodle.core.globals import (
    DFIndex,
    TextElements,
    XMLTags,
    questionTypes,
)
from excel2moodle.core.settings import Settings, SettingsKey
from excel2moodle.logger import LogAdapterQuestionID

loggerObj = logging.getLogger(__name__)
settings = Settings()


class Question:
    standardTags: typing.ClassVar[dict[str, str | float]] = {
        "hidden": 0,
    }

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        subclassTags = getattr(cls, "standartTags", {})
        superclassTags = super(cls, cls).standardTags
        mergedTags = superclassTags.copy()
        mergedTags.update(subclassTags)
        cls.standardTags = mergedTags

    @classmethod
    def addStandardTags(cls, key, value) -> None:
        cls.standardTags[key] = value

    def __init__(
        self,
        category: Category,
        rawData: dict[str, float | str | int | list[str]],
        parent=None,
        points: float = 0,
    ) -> None:
        self.rawData = rawData
        self.category = category
        self.katName = self.category.name
        self.name: str = self.rawData.get(DFIndex.NAME)
        self.number: int = self.rawData.get(DFIndex.NUMBER)
        self.parent = parent
        self.qtype: str = self.rawData.get(DFIndex.TYPE)
        self.moodleType = questionTypes[self.qtype]
        self.points = points if points != 0 else self.category.points
        self.element: ET.Element | None = None
        self.picture: Picture
        self.id: str
        self.qtextParagraphs: list[ET.Element] = []
        self.bulletList: ET.Element | None = None
        self.answerVariants: list[ET.Element] = []
        self.variants: int | None = None
        self.variables: dict[str, list[float | int]] = {}
        self.setID()
        self.logger = LogAdapterQuestionID(loggerObj, {"qID": self.id})
        self.logger.debug("Sucess initializing")

    def __repr__(self) -> str:
        li: list[str] = []
        li.append(f"Question v{self.id}")
        li.append(f"{self.qtype}")
        li.append(f"{self.parent=}")
        return "\t".join(li)

    def assemble(self, variant: int = 1) -> None:
        textElements: list[ET.Element] = []
        textElements.extend(self.qtextParagraphs)
        self.logger.debug("Starting assembly, (variant %s)", variant)
        if self.element is not None:
            mainText = self.element.find(XMLTags.QTEXT)
            self.logger.debug(f"found existing Text in element {mainText=}")
            txtele = mainText.find("text")
            if txtele is not None:
                mainText.remove(txtele)
                self.logger.debug("removed previously existing questiontext")
        else:
            msg = "Cant assamble, if element is none"
            raise QNotParsedException(msg, self.id)
        if self.variants is not None:
            textElements.append(self.getBPointVariant(variant - 1))
        elif self.bulletList is not None:
            textElements.append(self.bulletList)
        if hasattr(self, "picture") and self.picture.ready:
            textElements.append(self.picture.htmlTag)
            mainText.append(self.picture.element)
        mainText.append(etHelpers.getCdatTxtElement(textElements))
        self.logger.debug("inserted MainText to element")
        if len(self.answerVariants) > 0:
            ans = self.element.find(XMLTags.ANSWER)
            if ans is not None:
                self.element.remove(ans)
                self.logger.debug("removed previous answer element")
            self.element.insert(5, self.answerVariants[variant - 1])

    def setID(self, id=0) -> None:
        if id == 0:
            self.id: str = f"{self.category.id}{self.number:02d}"
        else:
            self.id: str = str(id)

    def getBPointVariant(self, variant: int) -> ET.Element:
        if self.bulletList is None:
            return None
        # matches {a}, {some_var}, etc.
        varPlaceholder = re.compile(r"{(\w+)}")

        def replaceMatch(match: Match[str]) -> str | int | float:
            key = match.group(1)
            if key in self.variables:
                value = self.variables[key][variant]
                return f"{value}".replace(".", ",\\!")
            return match.group(0)  # keep original if no match

        unorderedList = TextElements.ULIST.create()
        for li in self.bulletList:
            listItemText = li.text or ""
            bullet = TextElements.LISTITEM.create()
            bullet.text = varPlaceholder.sub(replaceMatch, listItemText)
            self.logger.debug(f"Inserted Variables into List: {bullet}")
            unorderedList.append(bullet)
        return unorderedList


class Picture:
    def __init__(
        self, picKey: str, imgFolder: Path, questionId: str, width: int = 0
    ) -> None:
        self.logger = LogAdapterQuestionID(loggerObj, {"qID": questionId})
        self.picID: str
        w: int = width if width > 0 else settings.get(SettingsKey.PICTUREWIDTH)
        self.size: dict[str, str] = {"width": str(w)}
        self.ready: bool = False
        self.imgFolder = imgFolder
        self.htmlTag: ET.Element
        self.path: Path
        self.questionId: str = questionId
        self.logger.debug("Instantiating a new picture in %s", picKey)
        if self.getImgId(picKey):
            self.ready = self.__getImg()
        else:
            self.ready = False

    def getImgId(self, imgKey: str) -> bool:
        """Get the image ID and width based on the given key.
        The key should either be the full ID (as the question) or only the question Num.
        If only the number is given, the category.id is prepended.
        The width should be specified by `ID:width:XX`. where xx is the px value.
        """
        width = re.findall(r"\:width\:(\d+)", str(imgKey))
        height = re.findall(r"\:height\:(\d+)", str(imgKey))
        if len(width) > 0 and width[0]:
            self.size["width"] = width[0]
        elif len(height) > 0 and height[0]:
            self.size["height"] = height[0]
            self.size.pop("width")
        self.logger.debug("Size of picture is %s", self.size)
        if imgKey in ("true", "True", "yes"):
            self.picID = self.questionId
            return True
        num: list[int | str] = re.findall(r"^\d+", str(imgKey))
        app: list[int | str] = re.findall(r"^\d+([A-Za-z_\-]+)", str(imgKey))
        if imgKey in ("false", "nan", False) or len(num) == 0:
            return False
        imgID: int = int(num[0])
        if imgID < 10:
            picID = f"{self.questionId[:3]}{imgID:02d}"
        elif imgID < 10000:
            picID = f"{self.questionId[:1]}{imgID:04d}"
        elif imgID <= 100000:
            picID = str(imgID)
        if len(app) > 0 and app[0]:
            self.picID = f"{picID}{app[0]}"
        else:
            self.picID = str(picID)
        self.logger.debug("Evaluated the imgID %s from %s", self.picID, imgKey)
        return True

    def _getBase64Img(self, imgPath: Path):
        with imgPath.open("rb") as img:
            return base64.b64encode(img.read()).decode("utf-8")

    def __getImg(self) -> bool:
        suffixes = ["png", "svg", "jpeg", "jpg"]
        paths = [
            path
            for suf in suffixes
            for path in self.imgFolder.glob(f"{self.picID}.{suf}")
        ]
        self.logger.debug("Found the following paths %s", paths)
        try:
            self.path = paths[0]
        except IndexError as e:
            msg = f"The Picture from key {self.picID} is not found"
            # raise InvalidFieldException(msg, self.questionId, DFIndex.PICTURE)
            self.logger.warning(
                msg=f"Bild {self.picID} konnte nicht gefunden werden ",
                exc_info=e,
            )
            self.element = None
            return False
        base64Img = self._getBase64Img(self.path)
        self.element: ET.Element = ET.Element(
            "file",
            name=f"{self.path.name}",
            path="/",
            encoding="base64",
        )
        self.element.text = base64Img
        self.htmlTag = ET.Element(
            "img",
            src=f"@@PLUGINFILE@@/{self.path.name}",
            alt=f"Bild {self.path.name}",
            **self.size,
        )
        return True
