from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Sequence, TypeVar

from typing_extensions import Protocol

from task_script_utils.parse import to_int


class InvalidWellLabelError(ValueError):
    """Invalid well label error"""


@dataclass(frozen=True)
class WellPosition:
    """Dataclass to represent well position for a well in a plate reader"""

    row: int
    column: int

    class LabelFormat(str, Enum):
        MIXED = "mixed"  # A->Z, a->z
        DOUBLE = "double"  # A->Z, AA->AZ

    @staticmethod
    def _parse_letter_to_index(char: str) -> int:
        """
        This function takes a single letter string and turns it into an index.

        The string must be in A-Z or a-z.
        """

        if char.isupper():
            # Map A-Z to 1-26
            return 1 + ord(char) - ord("A")
        # Map a-z to 27-52
        return 27 + ord(char) - ord("a")

    @staticmethod
    def from_well_label(well_label: str) -> WellPosition:
        """
        For an alphanumeric well_label, return the corresponding well position.
        A well_label must satisfy following conditions:
        1. It must start with a letter
        2. It can contain at max two letters
            - When it contains two letters, they must both be upper case
        3. Letter(s) my be followed by at least one and at max two digits

        If the label cannot be parsed, `InvalidWellLabelError` is raised.

        Parsing for well_label containing single letter is case sensitive.
        ie. well labels A02 and a02 represent different wells on the plate

        And Parsing for well_label containing two letters is limited to uppercase only.
        ie. AB01 is supported but ab01, Ab01 and aB01 are not supported

        The following are the only supported sequence of rows for a plate

        1. A -> Z then a -> z
        2. A -> Z then AA -> AZ

        Args:
            well_label (str): Alphanumeric string representing the well label.

        Returns:
            WellPositions: Return the corresponding WellPosition for well_label. eg:
            A01 -> WellPosition(row=1, column=1)
            A45 -> WellPosition(row=1, column=45)
            Z12 -> WellPosition(row=26, column=12)
            a12 -> WellPosition(row=27, column=12)
            z34 -> WellPosition(row=62, column=34)
            BD34 -> WellPosition(row=56, column=34)
            AA01 -> WellPosition(row=27, column=34)
        """

        single_letter_pattern = r"^[a-zA-Z]{1,1}\d{1,2}$"
        two_letter_pattern = r"^[A-Z]{2,2}\d{1,2}$"

        if re.match(single_letter_pattern, well_label):
            row = WellPosition._parse_letter_to_index(well_label[0])
            return WellPosition(row, int(well_label[1:]))
        if re.match(two_letter_pattern, well_label):
            row_position_0 = WellPosition._parse_letter_to_index(well_label[0])
            row_position_1 = WellPosition._parse_letter_to_index(well_label[1])
            return WellPosition(
                row_position_0 * 26 + row_position_1, int(well_label[2:])
            )

        raise InvalidWellLabelError(
            f"Well label {well_label} can't be parsed. "
            "It must match one of the following patterns: "
            f"{single_letter_pattern} or {two_letter_pattern}"
        )

    def to_label(self, label_format: LabelFormat = LabelFormat.DOUBLE):
        """Convert WellPosition to a label"""
        if self.row > 48:
            # The max number of rows is 48, for a 3456 well plate (48*72)
            raise InvalidWellLabelError(
                "The max number of rows that is supported is 48, found the row "
                f"number: {self.row}"
            )
        if self.row < 27:
            row = chr(ord("A") + self.row - 1)
            return f"{row}{self.column:02d}"

        if label_format is self.LabelFormat.DOUBLE:
            row_position_0 = chr(ord("A") + (self.row - 1) // 26 - 1)
            row_position_1 = chr(ord("A") + (self.row - 1) % 26)
            return f"{row_position_0}{row_position_1}{self.column:02d}"

        row = chr(ord("a") + (self.row - 1) % 26)
        return f"{row}{self.column:02d}"


class Location(Protocol):
    """Protocol for location"""

    row: Optional[float]
    column: Optional[float]


# Here we use a TypeVar to indicate that the generic type T must be a subclass of
# Location. We cannot use Location directly because Location is a Protocol and
# Pylance warns: "location" is invariant because it is mutable
T = TypeVar("T", bound=Location)


class SampleWithPk(Protocol[T]):
    """Protocol for samples with pk"""

    pk: Any  # Here we use Any to avoid a dependency on ts-ids-core
    location: T


def create_well_to_pk_map(samples: Sequence[SampleWithPk]) -> Dict[str, str]:
    """Create a map of wells to pk for samples"""
    well_to_pk_map = {}
    for sample in samples:
        if not hasattr(sample, "pk"):
            raise ValueError("Sample must have a pk attribute, and it must be non-null")
        if (
            to_int(str(sample.location.row)) is None
            or to_int(str(sample.location.column)) is None
        ):
            raise ValueError("Sample row and column must be integers")
        well_to_pk_map[
            WellPosition(row=sample.location.row, column=sample.location.column)
        ] = sample.pk
    return well_to_pk_map
