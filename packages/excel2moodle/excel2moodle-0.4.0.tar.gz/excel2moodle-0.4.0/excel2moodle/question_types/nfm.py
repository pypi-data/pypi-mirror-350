"""Numerical question multi implementation."""

import re
from typing import TYPE_CHECKING

import lxml.etree as ET
from asteval import Interpreter

from excel2moodle.core import stringHelpers
from excel2moodle.core.globals import (
    DFIndex,
    XMLTags,
)
from excel2moodle.core.parser import QuestionParser
from excel2moodle.core.question import Question

if TYPE_CHECKING:
    import lxml.etree as ET


class NFMQuestion(Question):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class NFMQuestionParser(QuestionParser):
    def __init__(self) -> None:
        super().__init__()
        self.genFeedbacks = [XMLTags.GENFEEDB]
        self.astEval = Interpreter()

    def setAnswers(self) -> None:
        equation = self.rawInput[DFIndex.RESULT]
        bps = str(self.rawInput[DFIndex.BPOINTS])
        ansElementsList: list[ET.Element] = []
        varNames: list[str] = self._getVarsList(bps)
        self.question.variables, number = self._getVariablesDict(varNames)
        for n in range(number):
            self._setupAstIntprt(self.question.variables, n)
            result = self.astEval(equation)
            if isinstance(result, float):
                ansElementsList.append(
                    self.getNumericAnsElement(result=round(result, 3)),
                )
        self.question.answerVariants = ansElementsList
        self.setVariants(len(ansElementsList))

    def setVariants(self, number: int) -> None:
        self.question.variants = number
        mvar = self.question.category.maxVariants
        if mvar is None:
            self.question.category.maxVariants = number
        else:
            self.question.category.maxVariants = min(number, mvar)

    def _setupAstIntprt(self, var: dict[str, list[float | int]], index: int) -> None:
        """Setup the asteval Interpreter with the variables."""
        for name, value in var.items():
            self.astEval.symtable[name] = value[index]

    def _getVariablesDict(self, keyList: list) -> tuple[dict[str, list[float]], int]:
        """Liest alle Variablen-Listen deren Name in ``keyList`` ist aus dem DataFrame im Column[index]."""
        dic: dict = {}
        num: int = 0
        for k in keyList:
            val = self.rawInput[k]
            if isinstance(val, str):
                li = stringHelpers.getListFromStr(val)
                num = len(li)
                variables: list[float] = [float(i.replace(",", ".")) for i in li]
                dic[str(k)] = variables
            else:
                dic[str(k)] = [str(val)]
                num = 1
        self.logger.debug("The following variables were provided: %s", dic)
        return dic, num

    @staticmethod
    def _getVarsList(bps: str | list[str]) -> list:
        """Durchsucht den bulletPoints String nach den Variablen ``{var}``.

        It only finds variables after the ``=`` sign, to not catch LaTex.
        """
        varNames = []
        regexFinder = re.compile(r"=\s*\{(\w+)\}")
        if isinstance(bps, list):
            for _p in bps:
                varNames.extend(regexFinder.findall(str(_p)))
        else:
            varNames = regexFinder.findall(str(bps))
        return varNames
