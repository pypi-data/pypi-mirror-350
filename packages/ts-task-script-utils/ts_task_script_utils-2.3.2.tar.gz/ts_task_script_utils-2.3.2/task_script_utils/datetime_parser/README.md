# Datetime Parser <!-- omit in toc -->

## Table of contents <!-- omit in toc -->

- [DatetimeParser](#datetimeparser)
- [DatetimeParser.to\_tsformat()](#datetimeparserto_tsformat)
- [DatetimeParser.parse()](#datetimeparserparse)
- [Examples](#examples)
  - [No formats](#no-formats)
  - [Single format](#single-format)
  - [Multiple formats](#multiple-formats)
  - [Partial formats](#partial-formats)
- [Supported datetime tokens](#supported-datetime-tokens)
- [Working with fractional seconds](#working-with-fractional-seconds)
- [Working with abbreviated timezones](#working-with-abbreviated-timezones)
- [Working with TSDatetime](#working-with-tsdatetime)
- [Limitations](#limitations)
- [Deprecated parse()](#deprecated-parse)

## DatetimeParser

Available arguments when creating a `DatetimeParser`:

- `formats (Sequence[str], optional)`: List of possible datetime formats. These datetime formats must be built using [supported datetime tokens](#supported-datetime-tokens). Defaults to empty tuple.
- `tz_dict (dict[str, str] | None, optional)`: A python dict that maps abbreviated timezone names to their corresponding offset. Defaults to `None`.
- `fold (int | None, optional)`: Informs how to disambiguate datetimes that fall in the 2h window where the same hour repeats twice. This happens when setting clocks one hour back at the end of daylight savings time. Defaults to `None`.
  - `0`: Datetime is interpreted as the first repeat.
  - `1`: Datetime is interpreted as the second repeat.
  - `None`: Raise `AmbiguousFoldError` for datetimes that fall in the fold.
- `require_unambiguous_formats (bool, optional)`: Whether datetime formats are required to be unambiguous. That is, if multiple formats can parse a datetime string, they must all give the same result. Defaults to `True`.
  - `True`: raise `AmbiguousDatetimeFormatsError` if any of the formats produce conflicting output.
  - `False`: the first format that can parse the datetime string is used.

## DatetimeParser.to_tsformat()

Use the method `DatetimeParser.to_tsformat(datetime_raw_str: str) -> str | None` to parse a datetime string to a TetraScience formatted datetime string.

If the parser does not have any formats configured, `None` is returned.
If formats are configured, the datetime string is parsed and the formatted string returned.

If unable to parse `datetime_raw_str`, `DatetimeParserError` or a derived exception is raised.

## DatetimeParser.parse()

Use the method `DatetimeParser.parse(datetime_raw_str: str) -> TSDatetime` to parse a datetime string to a `TSDatetime` instance.

If unable to parse `datetime_raw_str`, `DatetimeParserError` or a derived exception is raised.

## Examples

### No formats

```python
from task_script_utils.datetime_parser import DatetimeParser

datetime_parser = DatetimeParser(formats=[])

# As no formats are registered, .to_tsformat() always returns None
formatted_datetime_str = datetime_parser.to_tsformat("01/02/2003 04:05:06 AM +00:00")

# formatted_datetime_str: None
```

### Single format

Successful parsing using a single format:

```python
from task_script_utils.datetime_parser import DatetimeParser


formats = ["MM/DD/YYYY hh:mm:ss A Z"]
datetime_parser = DatetimeParser(formats=formats)

formatted_datetime_str = datetime_parser.to_tsformat("01/02/2003 04:05:06 AM +00:00")

# formatted_datetime_str: "2003-01-02T04:05:06Z"
```

An error is raised when the format does not match the datetime string or using the format results in an invalid date:

```python
from task_script_utils.datetime_parser import DatetimeParser


formats = ["MM/DD/YYYY hh:mm:ss A Z"]
datetime_parser = DatetimeParser(formats=formats)

# Parsing a string with the invalid month "14"
formatted_datetime_str = datetime_parser.to_tsformat("14/02/2003 04:05:06 AM +00:00")

# Raises:
# NoValidDatetimeFormatsError: Could not parse: '14/02/2003 04:05:06 AM +00:00' using any of the formats ['MM/DD/YYYY hh:mm:ss A Z']
```

### Multiple formats

In this example, two formats are used that are mutually exclusive, which allows to parse both `MM/DD/YYYY`, and `DD/MM/YYYY` formats.
Note that `require_unambiguous_formats=True` (the default), so an error would be raised if they were not mutually exclusive and both matched a datetime string.

```python
from task_script_utils.datetime_parser import DatetimeParser

formats = [
    "MM/DD/YYYY hh:mm:ss A Z",  # Month first + AM/PM
    "DD/MM/YYYY HH:mm:ss Z"     # Day first + 24h clock
]
datetime_parser = DatetimeParser(formats=formats)

datetime_parser.to_tsformat("01/02/2003 04:05:06 AM -06:00")  # This is January 2nd
# Returns: "2003-01-02T10:05:06Z"

datetime_parser.to_tsformat("01/02/2003 04:05:06 +00:00")  # This is February 1st
# Returns: "2003-02-01T04:05:06Z"
```

If the formats are not mutually exclusive, the datetime parsing will pass/fail depending on wether the date is valid according to both or just one of the formats.
In Task Scripts parsing some dates and not others is considered a bug.

```python
from task_script_utils.datetime_parser import DatetimeParser

formats = [
    "MM/DD/YYYY HH:mm:ss",  # Month first
    "DD/MM/YYYY HH:mm:ss"   # Day first
]
datetime_parser = DatetimeParser(formats=formats)

# 28/02 parse as Feb 28 using DD/MM/YYYY because MM/DD/YYYY would create an invalid date
datetime_parser.to_tsformat("28/02/2003 04:05:06")  # This is Feb 28
# Returns: "2003-02-28T04:05:06"

# 01/28 parse as Jan 31 using MM/DD/YYYY because DD/MM/YYYY would create an invalid date
datetime_parser.to_tsformat("01/31/2003 04:05:06")  # This is Jan 31
# Returns: "2003-01-31T04:05:06"

# This fails parsing as both formats can parse the date and they don't agree on the result
datetime_parser.to_tsformat("01/02/2003 04:05:06")
# Raises: AmbiguousDatetimeFormatsError: Ambiguity found between datetime formats: ['MM/DD/YYYY HH:mm:ss', 'DD/MM/YYYY HH:mm:ss'], the parsed datetimes ['2003-01-02T04:05:06', '2003-02-01T04:05:06'], and the input datetime string '01/02/2003 04:05:06'
```

### Partial formats

It is possible to specify partial formats, for example leaving out the year.
Pendulum will in that case infuse extra information using the value of `now()`.
It may set the year to the current year, or select the next point in time from `now()` that satisfies all the available tokens.

For that reason Task Scripts should use full formats so that the value of `now()`, i.e., when the Task Script runs, does not change the result.

```python
import pendulum
from task_script_utils.datetime_parser import DatetimeParser

formats = ["MM-DD HH"]  # Format without year
datetime_parser = DatetimeParser(formats=formats)

future_now = pendulum.datetime(2050, 11, 25, 21, 45)  # year 2050

with pendulum.travel_to(future_now):
    formatted_datetime_str = datetime_parser.to_tsformat("02-05 22") # Feb 5, year 2050
formatted_datetime_str  # 2050-02-05T22:00:00
```

## Supported datetime tokens

Supported tokens for datetime formats.

|                            | Token  | Output                            |
| -------------------------- | ------ | --------------------------------- |
| **Year**                   | YYYY   | 2000, 2001, 2002 ... 2012, 2013   |
|                            | YY     | 00, 01, 02 ... 12, 13             |
|                            | Y      | 2000, 2001, 2002 ... 2012, 2013   |
| **Quarter**                | Q      | 1 2 3 4                           |
|                            | Qo     | 1st 2nd 3rd 4th                   |
| **Month**                  | MMMM   | January, February, March ...      |
|                            | MMM    | Jan, Feb, Mar ...                 |
|                            | MM     | 01, 02, 03 ... 11, 12             |
|                            | M      | 1, 2, 3 ... 11, 12                |
|                            | Mo     | 1st 2nd ... 11th 12th             |
| **Day of Year**            | DDDD   | 001, 002, 003 ... 364, 365        |
|                            | DDD    | 1, 2, 3 ... 4, 5                  |
| **Day of Month**           | DD     | 01, 02, 03 ... 30, 31             |
|                            | D      | 1, 2, 3 ... 30, 31                |
|                            | Do     | 1st, 2nd, 3rd ... 30th, 31st      |
| **Day of Week**            | dddd   | Monday, Tuesday, Wednesday ...    |
|                            | ddd    | Mon, Tue, Wed ...                 |
|                            | dd     | Mo, Tu, We ...                    |
|                            | d      | 0, 1, 2 ... 6                     |
| **Days of ISO Week**       | E      | 1, 2, 3 ... 7                     |
| **Hour**                   | HH     | 00, 01, 02 ... 23, 24             |
|                            | H      | 0, 1, 2 ... 23, 24                |
|                            | hh     | 01, 02, 03 ... 11, 12             |
|                            | h      | 1, 2, 3 ... 11, 12                |
| **Minute**                 | mm     | 00, 01, 02 ... 58, 59             |
|                            | m      | 0, 1, 2 ... 58, 59                |
| **Second**                 | ss     | 00, 01, 02 ... 58, 59             |
|                            | s      | 0, 1, 2 ... 58, 59                |
| **Fractional Second**      | SSSSSS | All fractional digits             |
| **AM / PM**                | A      | AM, PM                            |
| **Timezone**               | Z      | -07:00, -06:00 ... +06:00, +07:00 |
|                            | ZZ     | -0700, -0600 ... +0600, +0700     |
|                            | z      | Asia/Baku, Europe/Warsaw, GMT ... |
|                            | zz     | EST CST ... MST PST               |
| **Seconds timestamp**      | X      | 1381685817, 1234567890.123        |
| **Milliseconds timestamp** | x      | 1234567890123                     |

**Note: If `zz` token is used in format string, passing `tz_dict` is a must.**

## Working with fractional seconds

You can use `SSSSSS` as a token to parse any number on digits as fractional seconds.
`TSDatetime` object returned by `parse()` helps maintaining the precision of fractional seconds.

For example, in the examples below `result.isoformat()` and `result.tsformat()` maintains the number of digits in fractional seconds.
This is different from python's `datetime` object, which only allows 6 digits for microseconds.
This is visible as the result of `result.datetime.isoformat()`, where `result.datetime` property returns a standard python `datetime` object.

```python
from task_script_utils.datetime_parser import DatetimeParser

datetime_formats = [
    "YYYY-MM-DD HH:mm:ss.SSSSSS z",
]
datetime_parser = DatetimeParser(formats=datetime_formats)

# Example 1
result = datetime_parser.parse("2021-12-13 13:00:12.19368293274 Asia/Kolkata")
result.tsformat()           # 2021-12-13T07:30:12.19368293274Z
result.isoformat()          # 2021-12-13T13:00:12.19368293274+05:30
result.datetime.isoformat() # 2021-12-13T13:00:12.193682+05:30

# Example 2
result = datetime_parser.parse("2021-12-13 13:00:12.1 Asia/Kolkata")
result.tsformat()           # 2021-12-13T07:30:12.1Z
result.isoformat()          # 2021-12-13T13:00:12.1+05:30
result.datetime.isoformat() # 2021-12-13T13:00:12.100000+05:30
```

## Working with abbreviated timezones

Abbreviated timezones are inherently ambiguous as each abbreviation may correspond to multiple different UTC offsets depending on location in the world.
We solve this by mapping abbreviated timezones to fixed UTC offsets.
Note that timezones that use daylight saving time correspond to two different abbreviations depending on the time of year.
Take the IANA zone `America/Chicago` as an example which corresponds to CST for UTC−06:00 and CDT for UTC−05:00.

```python
from task_script_utils.datetime_parser import DatetimeParser

datetime_formats = [
    "YYYY-MM-DD HH:mm:ss Z",
]
tz_dict = {
  "IST": "+05:30",
  "EST": "-05:00",
  "CST": "-06:00",
}

datetime_parser = DatetimeParser(formats=datetime_formats, tz_dict=tz_dict)

result = datetime_parser.parse("2021-12-25 00:00:00 IST")
result.tsformat()   # 2021-12-24T18:30:00Z
result.isoformat()  # 2021-12-25T00:00:00+05:30
```

## Working with TSDatetime

The `TSDatetime` object has the following methods and properties:

- `isoformat()`: return datetime string in ISO format
- `tsformat()`: returns datetime string in TetraScience's ISO8601 format
- `datetime`: return python `datetime` object.
- `change_fold()`: change the fold value

`TSDatetime` allows us to maintain the precision of fractional seconds.
Use `TSDatetime.datetime` to get a regular python `datetime` object which will loose any sub-microsecond precision.

## Limitations

1. It is not possible to map abbreviated timezones to fully named IANA timezones, e.g., `{"EST": "America/New_York"}`

## Deprecated parse()

The function `task_script_utils.datetime_parser.parse()` is deprecated and no longer documented here.
You can find the documentation in a [previous version of this readme](https://github.com/tetrascience/ts-task-script-utils/blob/v2.0.1/task_script_utils/datetime_parser/README.md).
