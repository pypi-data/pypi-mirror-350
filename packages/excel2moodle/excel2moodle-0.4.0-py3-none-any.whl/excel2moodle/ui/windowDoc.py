import sys

from PySide6 import QtCore, QtWebEngineWidgets, QtWidgets

from excel2moodle import e2mMetadata


class DocumentationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Load the HTML documentation
        url = QtCore.QUrl(e2mMetadata["documentation"])
        print(f"Opening URL {url}")
        self.web_view.setUrl(url)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = DocumentationWindow()
    window.show()

    sys.exit(app.exec())
