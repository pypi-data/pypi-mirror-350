from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from excel2moodle.core.dataStructure import Category
from excel2moodle.core.question import Question


class QuestionItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, question: Question) -> None:
        super().__init__(parent)
        self.setData(2, Qt.UserRole, question)
        self.setText(0, question.id)
        self.setText(1, question.name)
        self.setText(2, str(question.points))
        if hasattr(question, "variants") and question.variants is not None:
            self.setText(3, str(question.variants))

    def getQuestion(self) -> Question:
        """Return the question Object the QTreeWidgetItem represents."""
        return self.data(2, Qt.UserRole)


class CategoryItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, category: Category) -> None:
        super().__init__(parent)
        self.setData(2, Qt.UserRole, category)
        self.setText(0, category.NAME)
        self.setText(1, category.desc)
        self.setText(2, str(category.points))
        var = self.getMaxVariants()
        if var != 0:
            self.setText(3, str(var))

    def iterateChildren(self):
        for child in range(self.childCount()):
            yield self.child(child)

    def getMaxVariants(self) -> int:
        count: int = 0
        for child in self.iterateChildren():
            q = child.getQuestion()
            if hasattr(q, "variants") and q.variants is not None:
                count = q.variants if count <= q.variants else count
        return count

    def getCategory(self) -> Category:
        return self.data(2, Qt.UserRole)


# class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#     def createEditor(self, parent, option, index):
#         # Create a QSpinBox when the item is being edited
#         spinbox = QtWidgets.QSpinBox(parent)
#         spinbox.setMinimum(0)
#         spinbox.setMaximum(100)
#         return spinbox
#
#     def setEditorData(self, editor, index):
#         # Set the current value of the QSpinBox based on the item's data
#         value = index.model().data(index, Qt.EditRole)
#         editor.setValue(value)
#
#     def setModelData(self, editor, model, index):
#         # When editing is done, update the model data with the QSpinBox value
#         model.setData(index, editor.value(), Qt.EditRole)
