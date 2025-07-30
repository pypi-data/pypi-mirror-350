from enum import Enum, StrEnum

import lxml.etree as ET

questionTypes = {
    "NF": "numerical",
    "NFM": "numerical",
    "MC": "multichoice",
}


class DFIndex(StrEnum):
    """The identifier string for for the spreadsheet and the string for the xml-tag.

    Each enum corresponds to a list of two values.
    The first Value is the index in the spreadsheet, the second is the name of the xml-tag
    """

    TEXT = "text"
    BPOINTS = "bulletPoint"
    TRUE = "true"
    FALSE = "false"
    TYPE = "type"
    NAME = "name"
    RESULT = "result"
    PICTURE = "picture"
    NUMBER = "number"
    ANSTYPE = "answerType"
    TOLERANCE = "tolerance"


class TextElements(Enum):
    PLEFT = "p", "text-align: left;"
    SPANRED = "span", "color: rgb(239, 69, 64)"
    SPANGREEN = "span", "color: rgb(152, 202, 62)"
    SPANORANGE = "span", "color: rgb(152, 100, 100)"
    ULIST = (
        "ul",
        "",
    )
    LISTITEM = (
        "li",
        "text-align: left;",
    )

    def create(self, tag: str | None = None):
        if tag is None:
            tag, style = self.value
        else:
            style = self.value[1]
        return ET.Element(tag, dir="ltr", style=style)

    @property
    def style(
        self,
    ) -> str:
        return self.value[1]


class XMLTags(StrEnum):
    def __new__(cls, value: str, dfkey: DFIndex | None = None):
        obj = str.__new__(cls, value)
        obj._value_ = value
        if dfkey is not None:
            obj._dfkey_ = dfkey
        return obj

    def __init__(self, _: str, dfkey: DFIndex | None = None, getEle=None) -> None:
        if isinstance(dfkey, DFIndex):
            self._dfkey_: str = dfkey
        if getEle:
            self._getEle_: object = getEle

    @property
    def dfkey(self) -> str:
        return self._dfkey_

    def set(self, getEle) -> None:
        self._getEle_ = getEle

    def __repr__(self) -> str:
        msg = []
        msg.append(f"XML Tag {self.value=}")
        if hasattr(self, "_dfkey_"):
            msg.append(f"Df Key {self.dfkey=}")
        return "\n".join(msg)

    NAME = "name", DFIndex.NAME
    QTEXT = "questiontext", DFIndex.TEXT
    QUESTION = "question"
    TEXT = "text"
    PICTURE = "file", DFIndex.PICTURE
    GENFEEDB = "generalfeedback"
    CORFEEDB = "correctfeedback"
    PCORFEEDB = "partialcorrectfeedback"
    INCORFEEDB = "incorrectfeedback"
    ANSFEEDBACK = "feedback"
    POINTS = "defaultgrade"
    PENALTY = "penalty"
    HIDE = "hidden"
    ID = "idnumber"
    TYPE = "type"
    ANSWER = "answer"
    TOLERANCE = "tolerance"


feedBElements = {
    XMLTags.CORFEEDB: TextElements.SPANGREEN.create(),
    XMLTags.PCORFEEDB: TextElements.SPANORANGE.create(),
    XMLTags.INCORFEEDB: TextElements.SPANRED.create(),
    XMLTags.ANSFEEDBACK: TextElements.SPANGREEN.create(),
    XMLTags.GENFEEDB: TextElements.SPANGREEN.create(),
}
feedbackStr = {
    XMLTags.CORFEEDB: "Die Frage wurde richtig beantwortet",
    XMLTags.PCORFEEDB: "Die Frage wurde teilweise richtig beantwortet",
    XMLTags.INCORFEEDB: "Die Frage wurde Falsch beantwortet",
    XMLTags.GENFEEDB: "Sie haben eine Antwort abgegeben",
    "right": "richtig",
    "wrong": "falsch",
    "right1Percent": "Gratultaion, die Frage wurde im Rahmen der Toleranz richtig beantwortet",
}
