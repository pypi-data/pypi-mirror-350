"""Numeric Multi Questions Module to calculate results from a formula.

This module calculates a series of results from al matrix of variables.
For each column in the matrix there will be one result.
As well it returns a bullet points string that shows the numerical values corresponding to the set of variables
"""

import re

import pandas as pd
from asteval import Interpreter

astEval = Interpreter()


def getVariablesDict(df: pd.DataFrame, keyList: list, index: int) -> dict:
    """Liest alle Variablen-Listen deren Name in ``keyList`` ist aus dem DataFrame im Column[index]."""
    dic = {}
    for k in keyList:
        val = df.loc[str(k)][index]
        if isinstance(val, str) and val is not None:
            li = val.split(";")
            dic[str(k)] = li
        else:
            dic[str(k)] = [str(val)]
    return dic


def setParameters(parameters: dict, index: int) -> None:
    """Ubergibt die Parameter mit entsprechenden Variablen-Namen an den asteval-Interpreter.

    Dann kann dieser die equation loesen.
    """
    for k, v in parameters.items():
        comma = re.compile(r",")
        value = comma.sub(".", v[index])
        astEval.symtable[k] = float(value)


def insertVariablesToBPoints(varDict: dict, bulletPoints: str, index: int) -> str:
    """Für jeden Eintrag im varDict, wird im bulletPoints String der
    Substring "{key}" durch value[index] ersetzt.
    """
    for k, v in varDict.items():
        s = r"{" + str(k) + r"}"
        matcher = re.compile(s)
        bulletPoints = matcher.sub(str(v[index]), bulletPoints)
    return bulletPoints


def getVarsList(bps: str) -> list:
    """Durchsucht den bulletPoints String nach den Variablen `{var}`."""
    vars = re.findall(r"\{\w\}", str(bps))
    variablen = []
    for v in vars:
        variablen.append(v.strip("{}"))
    return variablen


def parseNumericMultiQuestion(
    datFrame: pd.DataFrame,
    bulletPoints: str,
    equation: str,
    questionIndex: int,
) -> tuple[list[str], list[float]]:
    """Berechnet die Ergebnisse anhand der Variablen in *bulletPoints*.

    Gibt eine Liste mit allen Ergebnissen zurück
    und eine Liste mit den bulletPoints-Strings, die die Numerischen Variablen enthalten
    """
    results = []
    bps = []
    varNames = getVarsList(bulletPoints)
    variables = getVariablesDict(datFrame, varNames, questionIndex)
    length = len(next(iter(variables.values())))
    for n in range(length):
        setParameters(variables, n)
        results.append(astEval(equation))
        bps.append(insertVariablesToBPoints(variables, bulletPoints, n))
    return bps, results
