# dateformat

Similar to the [`date` filter](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#date), but instead of using format strings derived from PHP, use the normal format strings for Python's [`strftime`](https://strftime.org).

## Format strings

### Day

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%d** | **d**            | Day of the month, 2 digits with leading zeros.                             | `'01'` to `'31'`                   |
| **%-d** | **j**            | Day of the month without leading zeros.                                    | `'1'` to `'31'`                    |
| **%a** | **D**            | Day of the week, textual, 3 letters.                                       | `'Fri'`                             |
| **%A** | **l**            | Day of the week, textual, long.                                           | `'Friday'`                          |
| -- | **S**            | English ordinal suffix for day of the month, 2 characters.                 | `'st'`, `'nd'`, `'rd'` or `'th'`   |
| **%w** | **w**            | Day of the week, digits without leading zeros.                             | `'0'` (Sunday) to `'6'` (Saturday) |
| **%-j** | **z**            | Day of the year.                                                           | `1` to `366`                        |

### Week

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%-W** | **W**            | ISO-8601 week number of year, with weeks starting on Monday.              | `1`, `53`                           |

### Month

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%m** | **m**            | Month, 2 digits with leading zeros.                                        | `'01'` to `'12'`                   |
| **%-m** | **n**            | Month without leading zeros.                                               | `'1'` to `'12'`                    |
| **%b** | **M**            | Month, textual, 3 letters.                                                | `'Jan'`                             |
| -- | **b**            | Month, textual, 3 letters, lowercase.                                     | `'jan'`                             |
| -- | **E**            | Month, locale specific alternative representation.                         | `'listopada'` (for Polish locale)  |
| **%B** | **F**            | Month, textual, long.                                                     | `'January'`                         |
| -- | **N**            | Month abbreviation in Associated Press style.                              | `'Jan.'`, `'Feb.'`, `'March'`, `'May'` |
| -- | **t**            | Number of days in the given month.                                         | `28` to `31`                        |

### Year

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%y** | **y**            | Year, 2 digits with leading zeros.                                         | `'00'` to `'99'`                   |
| **%Y** | **Y**            | Year, 4 digits with leading zeros.                                         | `'0001'`, …, `'1999'`, …, `'9999'` |
| -- | **L**            | Boolean for whether it’s a leap year.                                      | `True` or `False`                  |
| -- | **o**            | ISO-8601 week-numbering year.                                             | `'1999'`                            |

### Time

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%-I** | **g**            | Hour, 12-hour format without leading zeros.                                | `'1'` to `'12'`                    |
| **%-H** | **G**            | Hour, 24-hour format without leading zeros.                                 | `'0'` to `'23'`                    |
| **%I** | **h**            | Hour, 12-hour format.                                                      | `'01'` to `'12'`                   |
| **%H** | **H**            | Hour, 24-hour format.                                                      | `'00'` to `'23'`                   |
| **%M** | **i**            | Minutes.                                                                    | `'00'` to `'59'`                   |
| **%S** | **s**            | Seconds, 2 digits with leading zeros.                                      | `'00'` to `'59'`                   |
| **%f** | **u**            | Microseconds.                                                               | `000000` to `999999`                |
| -- | **a**            | `'a.m.'` or `'p.m.'` (Note that this is slightly different than PHP’s output, because this includes periods to match Associated Press style.) | `'a.m.'` |
| **%p** | **A**            | `'AM'` or `'PM'`.                                                          | `'AM'`                              |
| -- | **f**            | Time, in 12-hour hours and minutes, with minutes left off if they’re zero. | `'1'`, `'1:30'`                    |
| -- | **P**            | Time, in 12-hour hours, minutes and ‘a.m.’/’p.m.’, with minutes left off if they’re zero and the special-case strings ‘midnight’ and ‘noon’ if appropriate. | `'1 a.m.'`, `'1:30 p.m.'`, `'midnight'`, `'noon'`, `'12:30 p.m.'` |

### Timezone

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| **%Z** | **e**            | Timezone name. Could be in any format, or might return an empty string, depending on the datetime. | `''`, `'GMT'`, `'-500'`, `'US/Eastern'`, etc. |
| -- | **I**            | Daylight saving time, whether it’s in effect or not.                      | `'1'` or `'0'`                     |
| **%z** | **O**            | Difference to Greenwich time in hours.                                     | `'+0200'`                           |
| -- | **T**            | Time zone of this machine.                                                 | `'EST'`, `'MDT'`                   |
| -- | **Z**            | Time zone offset in seconds. The offset for timezones west of UTC is always negative, and for those east of UTC is always positive. | `-43200` to `43200`                 |

### Date/Time

| `dateformat` | `date` | Description                                                                 | Example                      |
|-------------|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| -- | **c**            | ISO 8601 format. (Note: unlike other formatters, such as “Z”, “O” or “r”, the “c” formatter will not add timezone offset if value is a naive datetime.) | `2008-01-02T10:30:00.000123+02:00`, or `2008-01-02T10:30:00.000123` if the datetime is naive |
| -- | **r**            | RFC 5322 formatted date.                                                   | `'Thu, 21 Dec 2000 16:01:07 +0200'` |
|-- | **U**            | Seconds since the Unix Epoch (January 1 1970 00:00:00 UTC).               |                                     |
