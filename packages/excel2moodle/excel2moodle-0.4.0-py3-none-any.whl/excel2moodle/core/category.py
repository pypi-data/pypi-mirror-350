import logging
from typing import TYPE_CHECKING

import lxml.etree as ET
import pandas as pd

if TYPE_CHECKING:
    from excel2moodle.core.question import Question

loggerObj = logging.getLogger(__name__)


class Category:
    """Category stores a list of question. And holds shared information for all."""

    def __init__(
        self,
        n: int,
        name: str,
        description: str,
        dataframe: pd.DataFrame,
        points: float = 0,
        version: int = 0,
    ) -> None:
        """Instantiate a new Category object."""
        self.n = n
        self.NAME = name
        self.desc = str(description)
        self.dataframe: pd.DataFrame = dataframe
        self.points = points
        self.version = int(version)
        self.questions: dict[int, Question] = {}
        self.maxVariants: int | None = None
        loggerObj.info("initializing Category %s", self.NAME)

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def id(self) -> str:
        return f"{self.version}{self.n:02d}"

    def __hash__(self) -> int:
        return hash(self.NAME)

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Category):
            return self.NAME == other.NAME
        return False

    def getCategoryHeader(self) -> ET.Element:
        """Insert an <question type='category'> before all Questions of this Category."""
        header = ET.Element("question", type="category")
        cat = ET.SubElement(header, "category")
        info = ET.SubElement(header, "info", format="html")
        ET.SubElement(cat, "text").text = f"$module$/top/{self.NAME}"
        ET.SubElement(info, "text").text = str(self.desc)
        ET.SubElement(header, "idnumber").text = str(self.n)
        ET.indent(header)
        return header
