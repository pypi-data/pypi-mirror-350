"""Multiple choice Question implementation."""

from typing import ClassVar

import lxml.etree as ET

import excel2moodle.core.etHelpers as eth
from excel2moodle.core import stringHelpers
from excel2moodle.core.exceptions import InvalidFieldException
from excel2moodle.core.globals import (
    DFIndex,
    TextElements,
    XMLTags,
    feedbackStr,
)
from excel2moodle.core.parser import QuestionParser
from excel2moodle.core.question import Picture, Question
from excel2moodle.core.settings import SettingsKey


class MCQuestion(Question):
    """Multiple-choice Question Implementation."""

    standardTags: ClassVar[dict[str, str | float]] = {
        "single": "false",
        "shuffleanswers": "true",
        "answernumbering": "abc",
        "showstandardinstruction": "0",
        "shownumcorrect": "",
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.AnsStyles = ["math", "unit", "text", "picture"]


class MCQuestionParser(QuestionParser):
    """Parser for the multiple choice Question."""

    def __init__(self) -> None:
        super().__init__()
        self.genFeedbacks = [
            XMLTags.CORFEEDB,
            XMLTags.PCORFEEDB,
            XMLTags.INCORFEEDB,
        ]

    def setup(self, question: MCQuestion) -> None:
        self.question: MCQuestion = question
        super().setup(question)

    def getAnsElementsList(
        self,
        answerList: list,
        fraction: float = 50,
        format="html",
    ) -> list[ET.Element]:
        elementList: list[ET.Element] = []
        for i, ans in enumerate(answerList):
            p = TextElements.PLEFT.create()
            if self.answerType == "picture":
                p.append(ans)
            else:
                p.text = str(ans)
            text = eth.getCdatTxtElement(p)
            elementList.append(
                ET.Element(XMLTags.ANSWER, fraction=str(fraction), format=format),
            )
            elementList[-1].append(text)
            if fraction < 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["wrong"],
                        style=TextElements.SPANRED,
                    ),
                )
                if self.answerType == "picture":
                    elementList[-1].append(self.falseImgs[i].element)
            elif fraction > 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["right"],
                        style=TextElements.SPANGREEN,
                    ),
                )
                if self.answerType == "picture":
                    elementList[-1].append(self.trueImgs[i].element)
        return elementList

    def setAnswers(self) -> list[ET.Element]:
        self.answerType = self.rawInput[DFIndex.ANSTYPE]
        true = stringHelpers.getListFromStr(self.rawInput[DFIndex.TRUE])
        false = stringHelpers.getListFromStr(self.rawInput[DFIndex.FALSE])
        if self.answerType not in self.question.AnsStyles:
            msg = f"The Answer style: {self.answerType} is not supported"
            raise InvalidFieldException(msg, self.question.id, DFIndex.ANSTYPE)
        if self.answerType == "picture":
            f = self.settings.get(SettingsKey.PICTUREFOLDER)
            imgFolder = (f / self.question.katName).resolve()
            w = self.settings.get(SettingsKey.ANSPICWIDTH)
            self.trueImgs: list[Picture] = [
                Picture(t, imgFolder, self.question.id, width=w) for t in true
            ]
            self.falseImgs: list[Picture] = [
                Picture(t, imgFolder, self.question.id, width=w) for t in false
            ]
            trueAnsList: list[str] = [pic.htmlTag for pic in self.trueImgs]
            falseAList: list[str] = [pic.htmlTag for pic in self.falseImgs]
        else:
            trueAnsList: list[str] = stringHelpers.texWrapper(
                true, style=self.answerType
            )
            self.logger.debug(f"got the following true answers \n {trueAnsList=}")
            falseAList: list[str] = stringHelpers.texWrapper(
                false, style=self.answerType
            )
            self.logger.debug(f"got the following false answers \n {falseAList=}")
        truefrac = 1 / len(trueAnsList) * 100
        falsefrac = 1 / len(falseAList) * (-100)
        self.tmpEle.find(XMLTags.PENALTY).text = str(round(truefrac / 100, 4))
        ansList = self.getAnsElementsList(trueAnsList, fraction=round(truefrac, 4))
        ansList.extend(
            self.getAnsElementsList(falseAList, fraction=round(falsefrac, 4)),
        )
        return ansList
