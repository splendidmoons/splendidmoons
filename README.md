# Splendid Moons

*calculates uposatha moonday calendar data for Mahanikaya*

Python library

Generates the calendar data for <http://splendidmoons.github.io/>

(This is a Python port and replacement of the older [suriya-go](https://github.com/splendidmoons/suriya-go) GoLang package.)

``` shell
$ pip install splendidmoons
$ splendidmoons asalha-puja 2023
2023-08-01
$ splendidmoons year-events-csv 2020 2030 moondays.csv
```

``` python
from splendidmoons.calendar_year import CalendarYear
for year in [2023, 2024, 2025]:
    print(f"{year}: {CalendarYear(year).year_type()}")
# 2023: YearType.Adhikamasa
# 2024: YearType.Normal
# 2025: YearType.Adhikavara
```

