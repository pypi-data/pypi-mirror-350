from typing import Dict, Optional, Sequence

import pendulum
from typing_extensions import deprecated

from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError
from task_script_utils.datetime_parser.ts_datetime import TSDatetime

from .datetime_config import DEFAULT_DATETIME_CONFIG, DatetimeConfig
from .datetime_info import LongDateTimeInfo, ShortDateTimeInfo
from .utils.manipulation import replace_z_with_offset
from .utils.parsing import _parse_with_formats, parse_with_formats


class DatetimeParser:
    """Parse datetimes and convert them to TetraScience string format"""

    def __init__(
        self,
        formats: Sequence[str] = (),
        tz_dict: Optional[Dict[str, str]] = None,
        fold: Optional[int] = None,
        require_unambiguous_formats: bool = True,
    ):
        """
        Create a datetime parser

        Args:
            formats: a list of datetime formats used for parsing.

            tz_dict: A python dict that maps abbreviated timezone names to their
            corresponding offset.

            fold: 0, 1 or None. Relevant for datetimes that fall in the 2 hour window
            when clocks are set back in a time zone with daylight savings (such as the
            IANA timezone `Europe/London`). Determines if the datetimes is interpreted
            as the first (0) or second (1) repeat. If set to None, parsing a datetime
            that falls in the 2 hour window will fail with the exception
            `AmbiguousFoldError`.

            require_unambiguous_formats: Whether datetime formats are required to be
            unambiguous. If `True`, `AmbiguousDatetimeFormatsError` is raised when two
            or more formats can parse the datetime, but result in different points in
            time. If `False`, the first format that can parse the datetime successfully
            is used.
        """
        self.formats = formats
        if tz_dict is None:
            tz_dict = {}
        self.config = DatetimeConfig(
            tz_dict=tz_dict,
            fold=fold,
            require_unambiguous_formats=require_unambiguous_formats,
        )

    def parse(self, datetime_raw_str: str) -> TSDatetime:
        """
        Parse a datetime string to `TSDatetime`

        Args:
            datetime_raw_str: Raw datetime string to be parsed

        Raises:
            Raises `DatetimeParserError` or a derived exception when datetime_raw_str
            cannot be parsed to a TSDatetime object.
        """

        return parse_with_formats(
            datetime_raw_str=datetime_raw_str, formats=self.formats, config=self.config
        )

    def to_tsformat(self, datetime_raw_str: str) -> Optional[str]:
        """
        Parse a datetime string to a tetrascience formatted datetime string.

        If the parser does not have any formats configured, None is returned. Otherwise
        the datetime string is parsed and the formatted string returned.

        Raises:
            Raises `DatetimeParserError` or a derived exception when datetime_raw_str
            cannot be parsed to a TSDatetime object.

        Returns:
            Tetrascience formatted datetime string or None.
        """
        if self.formats:
            return self.parse(datetime_raw_str).tsformat()
        return None


@deprecated(
    "Use `task_script_utils.datetime_parser.DatetimeParser instead`", category=None
)
def parse(
    datetime_raw_str: str,
    formats: Sequence[str] = (),
    config: DatetimeConfig = DEFAULT_DATETIME_CONFIG,
) -> TSDatetime:
    """
    **Warning**: Deprecated function. Use `DatetimeParser.parse` from
    `task_script_utils.datetime_parser` instead to parse a datetime string to `TSDatetime`.

    Parse datetime_str and construct a TSDatetime Object

    Args:
        datetime_raw_str (str): Raw datetime string
        formats (Sequence[str], optional): List of possible datetime
        formats. These datetime formats must be built using `pendulum` datetime tokens.
        Defaults to empty tuple.
        config (DatetimeConfig, optional): Datetime Configuration.
        Defaults to DEFAULT_DATETIME_CONFIG.

    Raises:
        DatetimeParserError: When datetime_str can be parsed into TSDatetime object
    Returns:
        TSDatetime
    """
    parsed_datetime = None
    datetime_info = None

    # If the input datetime string contains Z to denote UTC+0,
    # then Z is replaced by +00:00
    datetime_str = replace_z_with_offset(datetime_raw_str)
    # Parse Using formats list
    if formats:
        parsed_datetime, _ = _parse_with_formats(
            datetime_str, config=config, formats=formats
        )

    # Otherwise use DateInfo Parser to parse short dates
    if not parsed_datetime:
        datetime_info = ShortDateTimeInfo(datetime_str, config)
        parsed_datetime = datetime_info.datetime

    # Use long date formats
    if not parsed_datetime:
        datetime_info = LongDateTimeInfo(datetime_str, config)
        parsed_datetime = datetime_info.datetime

    if parsed_datetime is None:
        raise DatetimeParserError(f"Could not parse: {datetime_str}")

    if not isinstance(parsed_datetime, TSDatetime):
        parsed_datetime = pendulum.instance(parsed_datetime)
        parsed_datetime = TSDatetime(datetime_=parsed_datetime)

    parsed_datetime.change_fold(config.fold)
    return parsed_datetime
