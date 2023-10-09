import datetime
from typing import Self
from splendidmoons.calendar_year import CalendarYear

from splendidmoons.helpers import SEASON_NAME
from splendidmoons.ical import HasIcalEvent

class UposathaMoon(HasIcalEvent):
    date:           datetime.date = datetime.date.fromtimestamp(0)
    phase:          str = "" # only new or full. waxing and waning will be derived.
    event:          str = "" # magha, vesakha, asalha, pavarana
    s_number:       int = 0  # 1 of 8 in Hemanta
    s_total:        int = 0  # total number of uposathas in the season, 8 in Hemanta
    u_days:         int = 0  # uposatha days, 14 or 15
    m_days:         int = 0  # month days, 29 or 30
    lunar_month:    int = 0  # 1-12, 13 is 2nd Asalha (adhikamasa). Odd numbers are 30 day months.
    lunar_season:   int = 0  # 1-3, an int code to an []string array of names
    lunar_year:     int = 0
    has_adhikavara: bool = False
    source:         str = ""
    comments:       str = ""

    def __init__(self):
        pass

    def next_uposatha(self) -> Self:
        lu = self # last uposatha
        nu = UposathaMoon() # next uposatha

        cal_year = CalendarYear(lu.date.year)

        is_adhikamasa_year = cal_year.is_adhikamasa()
        is_adhikavara_year = cal_year.is_adhikavara()

        # Alternating New Moon and Full Moon uposathas.

        if lu.phase == "new":
            nu.phase = "full"
        else:
            nu.phase = "new"

        if nu.phase == "full":

            # A Full Moon uposatha is always 15 days in the same month, season and year as the last uposatha.

            nu.s_number = lu.s_number + 1
            nu.s_total = lu.s_total
            nu.u_days = 15
            nu.m_days = lu.m_days
            nu.lunar_month = lu.lunar_month
            nu.lunar_season = lu.lunar_season
            nu.lunar_year = lu.lunar_year
            nu.has_adhikavara = False # Adhikavara is only added to New Moons

            # Event: magha, vesakha, asalha, pavarana

            # In Adhikamāsa Years the major moons shift with one month
            if is_adhikamasa_year:
                if nu.lunar_month == 4:
                    nu.event = "magha"
                elif nu.lunar_month == 7:
                    nu.event = "vesakha"
                elif nu.lunar_month == 13:
                    nu.event = "asalha"
                elif nu.lunar_month == 11:
                    nu.event = "pavarana"
                else:
                    nu.event = ""

            else:
                # Common Year and Adhikavara Year
                if nu.lunar_month == 3:
                    nu.event = "magha"
                elif nu.lunar_month == 6:
                    nu.event = "vesakha"
                elif nu.lunar_month == 8:
                    nu.event = "asalha"
                elif nu.lunar_month == 11:
                    nu.event = "pavarana"
                else:
                    nu.event = ""

        else:
            # The New Moon uposatha begins a new month.

            if lu.lunar_month == 13:
                nu.lunar_month = 9 # Savana after 2nd Asalha
            elif lu.lunar_month == 8 and is_adhikamasa_year:
                nu.lunar_month = 13 # 2nd Asalha
            elif lu.lunar_month == 12:
                nu.lunar_month = 1
            else:
                nu.lunar_month = lu.lunar_month + 1

            # Odd numbered months are 30 days, except in adhikavāra years when the 8th month is 30 days.

            if is_adhikavara_year and nu.lunar_month == 8:
                nu.has_adhikavara = True
                nu.m_days = 30
            else:
                if nu.lunar_month%2 == 1:
                    nu.m_days = 30
                else:
                    nu.m_days = 29

            if nu.m_days == 29:
                nu.u_days = 14
            else:
                nu.u_days = 15

            # Season

            # In an adhikamāsa year the Hot Season is 10 uposatha long

            if is_adhikamasa_year and ((nu.lunar_month >= 5 and nu.lunar_month <= 8) or nu.lunar_month == 13):
                nu.s_total = 10
            else:
                nu.s_total = 8

            # If the last uposatha was not the last of the season, increment

            if lu.s_number < lu.s_total:
                nu.s_number = lu.s_number + 1
                nu.lunar_season = lu.lunar_season
                nu.lunar_year = lu.lunar_year

            else:
                # Else, it is the first uposatha of the season

                nu.s_number = 1
                # is it a new lunar year?
                if lu.lunar_month == 12:
                    nu.lunar_season = 1
                    nu.lunar_year = lu.lunar_year + 1
                else:
                    nu.lunar_season = lu.lunar_season + 1
                    nu.lunar_year = lu.lunar_year

        nu.date = lu.date + datetime.timedelta(days=nu.u_days)

        return nu

    def __str__(self) -> str:
        if self.phase == "":
            return ""

        return "{} Moon - {} day {} {}/{}".format(self.phase.title(),
                                                  self.u_days,
                                                  SEASON_NAME[self.lunar_season],
                                                  self.s_number,
                                                  self.s_total)
