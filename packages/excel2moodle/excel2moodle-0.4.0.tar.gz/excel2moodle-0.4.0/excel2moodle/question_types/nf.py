"""Numerical question implementation."""

import lxml.etree as ET

from excel2moodle.core.globals import (
    DFIndex,
    XMLTags,
)
from excel2moodle.core.parser import QuestionParser
from excel2moodle.core.question import Question


class NFQuestion(Question):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class NFQuestionParser(QuestionParser):
    """Subclass for parsing numeric questions."""

    def __init__(self) -> None:
        super().__init__()
        self.genFeedbacks = [XMLTags.GENFEEDB]

    def setAnswers(self) -> list[ET.Element]:
        result = self.rawInput[DFIndex.RESULT]
        ansEle: list[ET.Element] = []
        ansEle.append(self.getNumericAnsElement(result=result))
        return ansEle
