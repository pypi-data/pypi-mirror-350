"""Main Function to make the Package executable."""

import logging.config as logConfig
import signal
from pathlib import Path

from PySide6 import QtWidgets, sys

import excel2moodle
from excel2moodle import e2mMetadata, mainLogger
from excel2moodle.core import dataStructure
from excel2moodle.core.settings import Settings, SettingsKey
from excel2moodle.logger import loggerConfig
from excel2moodle.ui import appUi as ui


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    settings = Settings()
    database: dataStructure.QuestionDB = dataStructure.QuestionDB(settings)
    window = ui.MainWindow(settings, database)
    database.window = window
    window.show()
    for k, v in e2mMetadata.items():
        msg = f"{k:^14s}:  {v}"
        mainLogger.info(msg)
    sys.exit(app.exec())


if __name__ == "__main__":
    excel2moodle.isMain = True
    settings = Settings()
    logfile = Path(settings.get(SettingsKey.LOGFILE)).resolve()
    e2mMetadata["logfile"] = logfile
    if logfile.exists() and logfile.is_file():
        logfile.replace(f"{logfile}.old")

    logConfig.dictConfig(config=loggerConfig)
    main()
