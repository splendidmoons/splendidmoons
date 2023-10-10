from enum import Enum
from math import floor
import datetime
from splendidmoons import ADHIKAVARA_HISTORICAL_EXCEPTIONS, USE_HISTORICAL_EXCEPTIONS

from splendidmoons.calendar_consts import (BE_DIFF, CS_DIFF, CYCLE_DAILY, CYCLE_SOLAR, ERA_AVOMAN, ERA_DAYS, ERA_HORAKHUN, ERA_MASAKEN, ERA_UCCABALA, KAMMACUBALA_DAILY, MONTH_LENGTH)

class YearType(int, Enum):
    Normal = 0
    Adhikamasa = 1
    Adhikavara = 2

YEAR_TYPE_NAME = {
    YearType.Normal: "Normal",
    YearType.Adhikamasa: "Adhikamāsa",
    YearType.Adhikavara: "Adhikavāra",
}

SURIYA_YEAR_VALUES_FMT = """CE: {}
BE: {}
CS: {}
Horakhun: {}
Kammacubala: {}
Uccabala: {}
Avoman: {}
Masaken: {}
Tithi: {}
"""

class CalendarYear:
    year:        int # Common Era
    be_Year:     int # Buddhist Era, CE + 543
    cs_Year:     int # Chulasakkarat Era, CE - 638
    horakhun:    int # Elapsed days of the era, aka Ahargana or Sawana
    kammacubala: int # Remaining 800ths of a day
    uccabala:    int # Age of the moon's Apogee
    avoman:      int # For the Moon's mean motion
    masaken:     int # Elapsed months of the era
    tithi:       int # Age of the moon at the start of the year, aka Thaloengsok or New Year's Day
    first_day:    datetime.date

    def __init__(self, ce_year: int):
        self.year = ce_year
        self.be_year = self.year + BE_DIFF
        self.cs_year = self.year - CS_DIFF

        # helper variables
        a: int
        b: int

        # Take CE 1963, CS 1325 (as in the paper: "Rules for Interpolation...")

        # === A. Find the relevant values for the astronomical New Year ===

        # +1 is another constant correction, H3
        a = (self.cs_year * ERA_DAYS) + ERA_HORAKHUN
        self.horakhun = int(floor(float(a/KAMMACUBALA_DAILY + 1)))
        # Horakhun = 483969

        self.kammacubala = KAMMACUBALA_DAILY - (a % KAMMACUBALA_DAILY)
        # Kammacubala = 552

        self.uccabala = (self.horakhun + ERA_UCCABALA) % 3232
        # Uccabala = 1780

        a = (self.horakhun * CYCLE_DAILY) + ERA_AVOMAN
        self.avoman = a % CYCLE_SOLAR
        # Avoman = 61

        b = int(floor(float(a) / CYCLE_SOLAR))
        self.masaken = int(floor(float((b + ERA_MASAKEN + self.horakhun) / MONTH_LENGTH)))
        # Masaken = 16388

        self.tithi = (b + self.horakhun) % MONTH_LENGTH
        # Tithi = 23

    def year_type(self) -> YearType:
        if self.is_adhikamasa():
            return YearType.Adhikamasa
        elif self.is_adhikavara():
            return YearType.Adhikavara
        else:
            return YearType.Normal

    def is_adhikamasa(self) -> bool:
        # If next year also qualifies for adhikamāsa, then this year isn't
        next_year = CalendarYear(self.year + 1)
        return (not next_year.would_be_adhikamasa() and self.would_be_adhikamasa())

    def would_be_adhikamasa(self) -> bool:
        t = self.tithi
        # Eade says t >= 25, but then 2012 (t=24) would not be adhikamāsa.
        return ((t >= 24 and t <= 29) or (t >= 0 and t <= 5))

    def is_adhikavara(self) -> bool:
        if USE_HISTORICAL_EXCEPTIONS \
           and self.year in ADHIKAVARA_HISTORICAL_EXCEPTIONS.keys():
                return ADHIKAVARA_HISTORICAL_EXCEPTIONS[self.year]

        if self.is_adhikamasa():
            return False

        elif self.has_carried_adhikavara():
            return True

        else:
            return self.would_be_adhikavara()

    def suriya_values_str(self) -> str:
        return SURIYA_YEAR_VALUES_FMT.format(self.year, self.be_year, self.cs_year, self.horakhun, self.kammacubala,
                                        self.uccabala, self.avoman, self.masaken, self.tithi)

    def is_suriya_leap(self) -> bool:
        return (self.kammacubala <= 207)

    def would_be_adhikavara(self) -> bool:
        """
        Eade, in Rules for Interpolation...:

        > if the kammacubala value is 207 or less, then the year is a leap year.
        > in a leap year, if the avoman is 126 or less, the year will have an extra day
        > in a normal year, if the avoman is 137 or less the year will have an extra day.
        """

        if self.is_suriya_leap():
            # Both <= and < seems to work. Eade phrases it as <=.
            return self.avoman <= 126
        else:
            # Eade says Avoman <= 137, but that doesn't work.
            return self.avoman < 137

    def has_carried_adhikavara(self) -> bool:
        last_year = CalendarYear(self.year - 1)
        return (last_year.is_adhikamasa() and last_year.would_be_adhikavara())

    def adhikavara_cycle_pos(self) -> int:
        """Determine the position in the 57 year cycle. Assume 1984 = 1, 2040 = 57, 2041 = 1."""
        return int(abs(float(1984-57*10-self.year)))%57 + 1

    def adhikamasa_cycle_pos(self) -> int:
        """Determine the position in the 19 year cycle."""
        return int(abs(float(1984-19*10-self.year)))%19 + 1

    def delta_adhikamasa(self) -> int:
        """Years since last adhikamāsa."""

        year = self.year - 1
        while True:
            check = CalendarYear(year)
            if check.is_adhikamasa():
                return self.year - check.year
            # Avoid looking forever.
            if self.year-check.year > 6:
                break
            year -= 1

        return -1

    def delta_adhikavara(self) -> int:
        """Years since last adhikavāra."""

        year = self.year - 1
        while True:
            check = CalendarYear(year)
            if check.is_adhikavara():
                return self.year - check.year
            # Avoid looking forever.
            if self.year-check.year > 12:
                break

            year -= 1

        return -1

    def year_length(self) -> int:
        """Length of the lunar year in days."""

        # In a common year, there are six alternating 29 and 30 day lunar months.
        days = 6 * (30 + 29)

        if self.is_adhikamasa():
            # In an adhikamāsa year, there is an extra 30 day month.
            days = days + 30
        elif self.is_adhikavara():
            # In an adhikavāra year, there is an extra day.
            days = days + 1

        return days

    def asalha_puja(self) -> datetime.date:
        """Date of Asalha Puja"""

        # In a common year, Asalha Puja is the last day of the 8th month.
        days = 4 * (29 + 30)

        if self.is_adhikamasa():
            # In an adhikamāsa year, the extra month (2nd Asalha) is a 30 day month.
            days = days + 30
        elif self.is_adhikavara():
            # In an adhikavāra year, the 8th month (Asalha) is 30 days instead of 29 days.
            days = days + 1

        prev_kattika = self.calculate_previous_kattika()
        date = prev_kattika + datetime.timedelta(days=days)

        return date

    def calculate_previous_kattika(self) -> datetime.date:
        """Calculate the kattika full moon before this year"""

        # Step from a known Kattika date as epoch date
        kattika_date = datetime.date.fromisoformat("2015-11-25")

        # Determine the direction of stepping
        direction: int
        if kattika_date.year < self.year-1:
            direction = 1
        else:
            direction = -1

        # Step in direction until the Kattika in the prev. solar year
        y = kattika_date.year
        while y != self.year-1:
            check_year: CalendarYear
            n: int

            if direction == 1:
                check_year = CalendarYear(y + 1)

            else:
                check_year = CalendarYear(y)

            n = 6*29 + 6*30

            if check_year.is_adhikamasa():
                n += 30
            elif check_year.is_adhikavara():
                n += 1

            kattika_date = kattika_date + datetime.timedelta(days = (n*direction))

            y += direction

        return kattika_date
