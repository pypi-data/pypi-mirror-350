"""Helper Module which aids in creating XML-Elements for the Questions.

This module host different functions. All of them will return an ``lxml.etree.Element``
"""

import lxml.etree as ET

import excel2moodle.core.etHelpers as eth
from excel2moodle.core.globals import TextElements, feedbackStr, feedBElements

from .globals import DFIndex, XMLTags


def getElement(eleName: str, text: str, **attribs) -> ET.Element:
    """Creates an XML-Element with text.

    If ``type(text)``is a ``QuestionFields``, the specific field is directly read.
    Otherwise it will include whatever is ``text`` as a string
    :param **kwargs: are treated as attributes for the Element
    raises:
        NanException if the spreadsheet cell of text:QuestionFields is ``nan``
    """
    toEle = ET.Element(eleName)
    toEle.text = str(text)
    for k, v in attribs.items():
        toEle.set(k, v)
    return toEle


def getTextElement(eleName: str, text: str | DFIndex, **attribs) -> ET.Element:
    """Creates two nested elements: ``eleName`` with child ``text`` which holds the text."""
    toEle = ET.Element(eleName, **attribs)
    child = getElement("text", text)
    toEle.append(child)
    return toEle


def getCdatTxtElement(subEle: ET._Element | list[ET._Element]) -> ET.Element:
    """Puts all ``subEle`` as ``str`` into a ``<text><![CDATA[...subEle...]]</text>`` element."""
    textEle = ET.Element(XMLTags.TEXT)
    if isinstance(subEle, list):
        elementString: list = []
        for i in subEle:
            elementString.append(ET.tostring(i, encoding="unicode", pretty_print=True))
        textEle.text = ET.CDATA("".join(elementString))
        return textEle
    textEle.text = ET.CDATA(
        ET.tostring(subEle, encoding="unicode", pretty_print=True),
    )
    return textEle


def getFeedBEle(
    feedback: XMLTags,
    text: str | None = None,
    style: TextElements | None = None,
) -> ET.Element:
    """Gets ET Elements with the feedback for the question."""
    span = feedBElements[feedback] if style is None else style.create()
    if text is None:
        text = feedbackStr[feedback]
    ele = ET.Element(feedback, format="html")
    par = TextElements.PLEFT.create()
    span.text = text
    par.append(span)
    ele.append(eth.getCdatTxtElement(par))
    return ele
