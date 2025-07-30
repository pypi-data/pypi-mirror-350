"""This Module hosts the various Dialog Classes, that can be shown from main Window."""

import lxml.etree as ET
from PySide6 import QtGui, QtWidgets
from PySide6.QtSvgWidgets import QGraphicsSvgItem

from excel2moodle import e2mMetadata
from excel2moodle.core.globals import XMLTags
from excel2moodle.core.question import Question
from excel2moodle.ui.exportSettingsDialog import Ui_ExportDialog
from excel2moodle.ui.variantDialog import Ui_Dialog


class QuestionVariantDialog(QtWidgets.QDialog):
    def __init__(self, parent, question: Question) -> None:
        super().__init__(parent)
        self.setWindowTitle("Question Variant Dialog")
        self.maxVal = question.variants
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.spinBox.setRange(1, self.maxVal)
        self.ui.catLabel.setText(f"{question.katName}")
        self.ui.qLabel.setText(f"{question.name}")
        self.ui.idLabel.setText(f"{question.id}")

    @property
    def variant(self):
        return self.ui.spinBox.value()

    @property
    def categoryWide(self):
        return self.ui.checkBox.isChecked()


class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export question Selection")
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)


class QuestionPreview:
    def __init__(self, parent) -> None:
        self.ui = parent.ui
        self.parent = parent

    def setupQuestion(self, question: Question) -> None:
        self.question: Question = question
        self.ui.qNameLine.setText(f"{self.question.qtype} - {self.question.name}")
        self.picScene = QtWidgets.QGraphicsScene(self.parent)
        self.ui.graphicsView.setScene(self.picScene)
        self.setText()
        self.setAnswers()
        if hasattr(self, "picItem"):
            self.picScene.removeItem(self.picItem)
        self.setPicture()

    def setPicture(self) -> None:
        if hasattr(self.question, "picture") and self.question.picture.ready:
            path = self.question.picture.path
            if path.suffix == ".svg":
                self.picItem = QGraphicsSvgItem(str(self.question.picture.path))
            else:
                pic = QtGui.QPixmap(self.question.picture.path)
                aspRat = pic.height() // pic.width()
                width = 400
                scaleHeight = aspRat * width
                self.picItem = QtWidgets.QGraphicsPixmapItem(
                    pic.scaled(
                        width, scaleHeight, QtGui.Qt.AspectRatioMode.KeepAspectRatio
                    )
                )
            self.picScene.addItem(self.picItem)
        # else:
        #     self.ui.graphicsView.setFixedHeight(1)

    def setText(self) -> None:
        t = []
        for text in self.question.qtextParagraphs:
            t.append(ET.tostring(text, encoding="unicode"))
        if self.question.bulletList is not None:
            t.append(ET.tostring(self.question.bulletList, encoding="unicode"))
        self.ui.questionText.setText("\n".join(t))

    def setAnswers(self) -> None:
        if self.question.qtype == "NFM":
            list = ET.Element("ol")
            for ans in self.question.answerVariants:
                textEle = ET.Element("li")
                textEle.text = f"Result: {ans.find('text').text}"
                list.append(textEle)
            self.ui.answersLabel.setText(ET.tostring(list, encoding="unicode"))
        elif self.question.qtype == "NF":
            ans = self.question.element.find(XMLTags.ANSWER)
            self.ui.answersLabel.setText(f" Result: {ans.find('text').text}")
        elif self.question.qtype == "MC":
            list = ET.Element("ol")
            for ans in self.question.element.findall(XMLTags.ANSWER):
                textEle = ET.Element("li")
                pEle = ans.find("text").text
                frac = ans.get("fraction")
                anstext = ET.fromstring(pEle).text
                text = f"Fraction {frac}: {anstext}"
                textEle.text = text
                list.append(textEle)
            self.ui.answersLabel.setText(ET.tostring(list, encoding="unicode"))


class AboutDialog(QtWidgets.QMessageBox):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"About {e2mMetadata['name']}")
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close)

        self.aboutMessage: str = f"""
        <h1> About {e2mMetadata["name"]} v {e2mMetadata["version"]}</h1><br>
        <p style="text-align:center">

                <b><a href="{e2mMetadata["homepage"]}">{e2mMetadata["name"]}</a> - {e2mMetadata["description"]}</b>
        </p>
        <p style="text-align:center">
            A <b>
            <a href="{e2mMetadata["documentation"]}">documentation</a></b>
            is also available.
            </br>
        </p>
        <p style="text-align:center">
        This project is maintained by {e2mMetadata["author"]}.
        <br>
        Development takes place at <a href="{e2mMetadata["homepage"]}"> GitLab: {e2mMetadata["homepage"]}</a>
        contributions are very welcome
        </br>
        If you encounter any issues please report them under the repositories issues page.
        </br>
        </p>
        <p style="text-align:center">
        <i>This project is published under {e2mMetadata["license"]}, you are welcome, to share, modify and reuse the code.</i>
        </p>
        """
        self.setText(self.aboutMessage)
