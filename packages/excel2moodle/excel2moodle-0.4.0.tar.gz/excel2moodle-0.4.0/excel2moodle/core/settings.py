"""Settings module provides the adjusted subclass of ``PySide6.QtCore.QSettings``."""

import logging
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Literal, overload

from PySide6.QtCore import QSettings, QTimer, Signal

import excel2moodle

logger = logging.getLogger(__name__)


class SettingsKey(StrEnum):
    """Settings Keys are needed to always acess the correct Value.

    As the QSettings settings are accesed via strings, which could easily gotten wrong.
    Further, this Enum defines, which type a setting has to be.
    """

    def __new__(
        cls,
        key: str,
        place: str,
        typ: type,
        default: str | float | Path | bool | None,
    ):
        """Define new settings class."""
        obj = str.__new__(cls, key)
        obj._value_ = key
        obj._place_ = place
        obj._default_ = default
        obj._typ_ = typ
        return obj

    def __init__(
        self, _, place: str, typ: type, default: str | float | Path | None
    ) -> None:
        self._typ_ = typ
        self._place_ = place
        self._default_ = default
        self._full_ = f"{self._place_}/{self._value_}"

    @property
    def default(self) -> str | int | float | Path | bool | None:
        """Get default value for the key."""
        return self._default_

    @property
    def place(self) -> str:
        return self._place_

    @property
    def full(self) -> str:
        return self._full_

    def typ(self) -> type:
        """Get default value for the key."""
        return self._typ_

    QUESTIONVARIANT = "defaultQuestionVariant", "testgen", int, 0
    INCLUDEINCATS = "includeCats", "testgen", bool, False
    TOLERANCE = "tolerance", "parser/nf", int, 1
    PICTUREFOLDER = "pictureFolder", "core", Path, None
    SPREADSHEETFOLDER = "spreadsheetFolder", "core", Path, None
    LOGLEVEL = "loglevel", "core", str, "INFO"
    LOGFILE = "logfile", "core", str, "excel2moodleLogFile.log"
    CATEGORIESSHEET = "categoriesSheet", "core", str, "Kategorien"
    VERSION = "version", "project", int, 1
    POINTS = "points", "project", float, 1.0
    PICTURESUBFOLDER = "imgFolder", "project", str, "Abbildungen"
    PICTUREWIDTH = "imgWidth", "project", int, 500
    ANSPICWIDTH = "answerImgWidth", "project", int, 120


class Settings(QSettings):
    """Settings for Excel2moodle."""

    shPathChanged = Signal(Path)
    localSettings: ClassVar[dict[str, str | float | Path]] = {}

    def __init__(self) -> None:
        """Instantiate the settings."""
        super().__init__("jbosse3", "excel2moodle")
        if excel2moodle.isMainState():
            logger.info("Settings are stored under: %s", self.fileName())
            if self.contains(SettingsKey.SPREADSHEETFOLDER.full):
                self.sheet = self.get(SettingsKey.SPREADSHEETFOLDER)
                if self.sheet.is_file():
                    QTimer.singleShot(300, self._emitSpreadsheetChanged)

    def _emitSpreadsheetChanged(self) -> None:
        self.shPathChanged.emit(self.sheet)

    @overload
    def get(
        self,
        key: Literal[
            SettingsKey.QUESTIONVARIANT,
            SettingsKey.TOLERANCE,
            SettingsKey.VERSION,
            SettingsKey.POINTS,
            SettingsKey.PICTUREWIDTH,
            SettingsKey.ANSPICWIDTH,
        ],
    ) -> int: ...
    @overload
    def get(self, key: Literal[SettingsKey.INCLUDEINCATS]) -> bool: ...
    @overload
    def get(
        self,
        key: Literal[
            SettingsKey.PICTURESUBFOLDER,
            SettingsKey.LOGLEVEL,
            SettingsKey.LOGFILE,
            SettingsKey.CATEGORIESSHEET,
        ],
    ) -> str: ...
    @overload
    def get(
        self,
        key: Literal[SettingsKey.PICTUREFOLDER, SettingsKey.SPREADSHEETFOLDER],
    ) -> Path: ...

    def get(self, key: SettingsKey):
        """Get the typesafe settings value.

        If local Settings are stored, they are returned.
        If no setting is made, the default value is returned.
        """
        if key in self.localSettings:
            val = key.typ()(self.localSettings[key])
            logger.debug("Returning project setting: %s = %s", key, val)
            return val
        if not excel2moodle.isMainState():
            logger.warning("No GUI: Returning default value.")
            return key.default
        if key.typ() is Path:
            path: Path = self.value(key.full, defaultValue=key.default)
            try:
                path.resolve(strict=True)
            except ValueError:
                logger.warning(
                    f"The settingsvalue {key} couldn't be fetched with correct typ",
                )
                return key.default
            logger.debug("Returning path setting: %s = %s", key, path)
            return path
        raw = self.value(key.full, defaultValue=key.default, type=key.typ())
        logger.debug("read a settings Value: %s of type: %s", key, key.typ())
        try:
            logger.debug("Returning global setting: %s = %s", key, raw)
            return key.typ()(raw)
        except (ValueError, TypeError):
            logger.warning(
                f"The settingsvalue {key} couldn't be fetched with correct typ",
            )
            return key.default

    def set(
        self,
        key: SettingsKey | str,
        value: float | bool | Path | str,
        local: bool = False,
    ) -> None:
        """Set the setting to value.

        Parameters
        ----------
        local
            True saves local project specific settings.
            Defaults to False
            The local settings are meant to be set in the first sheet `settings`

        """
        if not excel2moodle.isMainState():
            local = True
        if local:
            if key in SettingsKey:
                self.localSettings[key] = value
                logger.info("Saved the project setting %s = %s", key, value)
            else:
                logger.warning("got invalid local Setting %s = %s", key, value)
            return
        if not local and isinstance(key, SettingsKey):
            if not isinstance(value, key.typ()):
                logger.error("trying to save setting with wrong type not possible")
                return
            self.setValue(key.full, value)
            logger.info("Saved the global setting %s = %s", key, value)

    def setSpreadsheet(self, sheet: Path) -> None:
        """Save spreadsheet path and emit the changed event."""
        if isinstance(sheet, Path):
            self.sheet = sheet.resolve(strict=True)
            logpath = str(self.sheet.parent / "excel2moodleLogFile.log")
            self.set(SettingsKey.LOGFILE, logpath)
            self.set(SettingsKey.SPREADSHEETFOLDER, self.sheet)
            self.shPathChanged.emit(sheet)
            return
