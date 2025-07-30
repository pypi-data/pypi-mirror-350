"""This Module checks if the data inside the Spreadsheet is valid.

Those things are considered:

#. The mandatory entries must not be ``Nan``
#. All fields must have the right data-type

If Those checks pass, a question is created,
which can be accessed via ``Validator.question``
"""

import logging
from typing import TYPE_CHECKING

import pandas as pd

from excel2moodle.core.exceptions import InvalidFieldException
from excel2moodle.core.globals import DFIndex

if TYPE_CHECKING:
    from types import UnionType


logger = logging.getLogger(__name__)


class Validator:
    """Validate the question data from the spreadsheet.

    Creates a dictionary with the data, for easier access later.
    """

    def __init__(self) -> None:
        self.allMandatory: dict[DFIndex, type | UnionType] = {
            DFIndex.TEXT: str,
            DFIndex.NAME: str,
            DFIndex.TYPE: str,
        }
        self.allOptional: dict[DFIndex, type | UnionType] = {
            DFIndex.PICTURE: int | str,
        }
        self.nfOpt: dict[DFIndex, type | UnionType] = {
            DFIndex.BPOINTS: str,
        }
        self.nfMand: dict[DFIndex, type | UnionType] = {
            DFIndex.RESULT: float | int,
        }
        self.nfmOpt: dict[DFIndex, type | UnionType] = {}
        self.nfmMand: dict[DFIndex, type | UnionType] = {
            DFIndex.RESULT: str,
            DFIndex.BPOINTS: str,
        }
        self.mcOpt: dict[DFIndex, type | UnionType] = {}
        self.mcMand: dict[DFIndex, type | UnionType] = {
            DFIndex.TRUE: str,
            DFIndex.FALSE: str,
            DFIndex.ANSTYPE: str,
        }

        self.mapper: dict = {
            "NF": (self.nfOpt, self.nfMand),
            "MC": (self.mcOpt, self.mcMand),
            "NFM": (self.nfmOpt, self.nfmMand),
        }

    def setup(self, df: pd.Series, index: int) -> None:
        self.df = df
        self.index = index
        self.mandatory = {}
        self.optional = {}
        typ = self.df.loc[DFIndex.TYPE]
        if typ not in self.mapper:
            msg = f"No valid question type provided. {typ} is not a known type"
            raise InvalidFieldException(msg, "index:02d", DFIndex.TYPE)
        self.mandatory.update(self.allMandatory)
        self.optional.update(self.allOptional)
        self.mandatory.update(self.mapper[typ][1])
        self.optional.update(self.mapper[typ][0])

    def validate(self) -> None:
        qid = f"{self.index:02d}"
        checker, missing = self._mandatory()
        if not checker:
            msg = f"Question {qid} misses the key {missing}"
            if missing is not None:
                raise InvalidFieldException(msg, qid, missing)
        checker, missing = self._typeCheck()
        if not checker:
            msg = f"Question {qid} has wrong typed data {missing}"
            if missing is not None:
                raise InvalidFieldException(msg, qid, missing)

    def getQuestionRawData(self) -> dict[str, str | float | list[str]]:
        """Get the data from the spreadsheet as a dictionary."""
        self.qdata: dict[str, str | float | int | list] = {}
        for idx, val in self.df.items():
            if not isinstance(idx, str):
                continue
            if pd.isna(val):
                continue
            if idx in self.qdata:
                if isinstance(self.qdata[idx], list):
                    self.qdata[idx].append(val)
                else:
                    existing = self.qdata[idx]
                    self.qdata[idx] = [existing, val]
            else:
                self.qdata[idx] = val
        return self.qdata

    def _mandatory(self) -> tuple[bool, DFIndex | None]:
        """Detects if all keys of mandatory are filled with values."""
        checker = pd.Series.notna(self.df)
        for k in self.mandatory:
            try:
                c = checker[k]
            except KeyError:
                return False, k
            if isinstance(c, pd.Series):
                if not c.any():
                    return False, k
            elif not c:
                return False, k
        return True, None

    def _typeCheck(self) -> tuple[bool, list[DFIndex] | None]:
        invalid: list[DFIndex] = []
        for field, typ in self.mandatory.items():
            if field in self.df and isinstance(self.df[field], pd.Series):
                for f in self.df[field]:
                    if pd.notna(f) and not isinstance(f, typ):
                        invalid.append(field)
            elif not isinstance(self.df[field], typ):
                invalid.append(field)
        for field, typ in self.optional.items():
            if field in self.df and isinstance(self.df[field], pd.Series):
                for f in self.df[field]:
                    if pd.notna(f) and not isinstance(f, typ):
                        invalid.append(field)
        if len(invalid) == 0:
            return True, None
        return False, invalid
