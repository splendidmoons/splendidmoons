from math import floor, sin, pi
from datetime import date

from splendidmoons.calendar_consts import (BE_DIFF, CS_DIFF, CYCLE_DAILY, CYCLE_SOLAR, ERA_AVOMAN, ERA_MASAKEN,
                                           KAMMACUBALA_DAILY, ERA_DAYS, ERA_HORAKHUN, ERA_YEARS, ERA_UCCABALA,
                                           MONTH_LENGTH)
from splendidmoons.calendar_year import CalendarYear
from splendidmoons.helpers import degree_to_ral, normalize_degree, ral_to_degree

SURIYA_DAY_VALUES_FMT = """Year: {}
Day: {}
BE_Year: {}
CS_Year: {}
Masaken: {}
Avoman: {}
Horakhun: {}
Kammacubala: {}
Uccabala: {}
Tithi: {}
TrueSun: {}
TrueMoon: {}
"""

# Steps resolved with the answers at:
# http://astronomy.stackexchange.com/questions/12052/from-mean-moon-to-true-moon-in-an-old-procedural-calendar
# http://astronomy.stackexchange.com/questions/11753/how-to-interpret-this-old-degree-notation

class CalendarDay:
    Year:         int # Common Era
    BE_Year:      int # Buddhist Era, CE + 543
    CS_Year:      int # Chulasakkarat Era, CE - 638
    Day:          int # nth day in the Lunar Year
    Date:         date
    Horakhun:     int
    Kammacubala:  int
    Uccabala:     int
    Avoman:       int
    Masaken:      int
    Tithi:        int
    MeanSun:      float # position in degrees
    TrueSun:      float
    MeanMoon:     float
    TrueMoon:     float
    Raek:         float

    def __init__(self, ce_year: int, lunar_year_day: int):

        # === A. Find the relevant values for the astronomical New Year ===

        cal_year = CalendarYear(ce_year)

        self.Year = ce_year
        self.BE_Year = ce_year + BE_DIFF
        self.CS_Year = ce_year - CS_DIFF
        self.Day = lunar_year_day

        # This is elapsedDays = self.Horakhun - cal_year.Horakhun, but the meaning is
        # perhaps clearer as below.
        elapsedDays = self.Day - cal_year.Tithi

        # Horakhun of the day
        self.Horakhun = cal_year.Horakhun + elapsedDays

        # Kammacubala of the day
        self.Kammacubala = KAMMACUBALA_DAILY - (self.CS_Year * ERA_DAYS + ERA_HORAKHUN) % ERA_YEARS  + elapsedDays * KAMMACUBALA_DAILY

        # Uccabala of the day
        self.Uccabala = (self.Horakhun + ERA_UCCABALA) % 3232

        # helper values
        ai: int
        bi: int

        # Avoman of the day
        ai = (self.Horakhun * CYCLE_DAILY) + ERA_AVOMAN
        self.Avoman = ai % CYCLE_SOLAR

        # Masaken of the day
        bi = int(floor(float(ai) / CYCLE_SOLAR)) + ERA_MASAKEN + self.Horakhun
        self.Masaken = int(floor(float(bi / MONTH_LENGTH)))

        # Tithi of the day
        self.Tithi = bi % MONTH_LENGTH

        # helper values
        a: float
        b: float

        # === B. Find the position of the Mean and true Sun on Asalha 15 ===

        # Sample values in the comments are for lunar_year_day = 103, Asalha 15
        #
        # Length of the months, Thai months ending on New Moon:
        # Citta   Full + New = 15+14
        # Vesakha Full + New = 15+15
        # Jettha  Full + New = 15+14
        # Asalha  Full       = 15
        # ---------------------------
        #                    = 103

        # interval from 1 Caitra (aka Citta) to Asalha Full Moon, minus New Year day

        a = float((elapsedDays * ERA_YEARS) + cal_year.Kammacubala)
        # a = 64552

        b = (a / ERA_DAYS) * 360
        # b = 79.5282796100025

        # The -3 arcmin is a geographical correction. Mentioned in "Interpolation..." and "Calendrical".

        # (x; y : z) in Eade's notation means 30*60*x + 60*y + z in arcmins, so x and y are deg originally
        x, y, z = degree_to_ral(b)
        z -= 3

        # Do convert the degree to Ral and back. If we only do b -= 3/60, we get
        # slightly different results than in Eade's papers.

        self.MeanSun = ral_to_degree(x, y, z)
        # MeanSun = 2; 19 : 28
        # MeanSun = 79.4666

        # The -80 degree is mentioned in Calendrical, sth to do with the Sun's Apogee?

        a = abs(self.MeanSun - 80)

        # math.sin() takes radians
        radconv = pi / 180
        b = floor(134 * sin(a*radconv))
        # b = floor(1.2473)
        # b = 1

        # Floor it to get degree only to 4th decimal place, to avoid results such as TrueSun: 79.48326666666667
        self.TrueSun = floor(self.MeanSun*10000+(b*10000)/60) / 10000
        # TrueSun = 2; 19 : 29

        # === C. Find the Mean and True Moon on Asalha 15 ===

        # step 12.

        # divide with 60 to covert value in degrees from minutes
        a = (float(self.Avoman) + floor(float(self.Avoman)/25)) / 60
        # 0; 4 : 17
        # b = 4.3

        # step 13.

        # The -40 arcmin is a geographical correction. In "Interpolation...": The
        # routine subtraction of 3 arcmins is a geographical longitude correction for
        # the sun, as is the subtraction of 40 arcmins for the moon (sec. C13).

        # Use ral_to_degree() instead of 40/60. ral_to_degree() gives only a four decimal
        # place value, which produces results closer to Eade's papers.

        self.MeanMoon = normalize_degree(self.TrueSun + a + (float(self.Tithi) * 12) - ral_to_degree(0, 0, 40))
        # Mean Moon: 8; 11 : 7
        # Mean Moon: 251.116666

        # step 14.

        meanUccabala: float

        # all in one, see below for step-by-step
        meanUccabala = ((((float(cal_year.Uccabala + elapsedDays) * 3 * 30) / 808) * 60) + 2) / 60
        # Mean Uccabala = 6; 27 : 12
        # Mean Uccabala = 207.2115

        """
        Multiply with 30 to conform with (x; y : z) = 30*60*x + 60*y + z

        808 / 30 is 26.9333, perhaps reproducing the length of the lunar month.

        meanUccabala *= 30

        Which gives Mean Uccabala = 6; 27 : 10

        Convert to arcmin:

        meanUccabala *= 60

        Add 2, possibly correction for geographical position

        meanUccabala += 2

        Convert back to degree:

        meanUccabala = meanUccabala / 60

        Mean Uccabala = 6; 27 : 12
        """

        # step 15.

        a = self.MeanMoon - meanUccabala
        # b = 1; 13 : 54
        # b = 43.9051

        # NOTE: Eade has 1; 3 : 55, but that doesn't work. This is a typo in the paper.

        # step 16.

        b = (296 * sin(a*radconv)) / 60
        # d = 0; 3 : 24
        # d = 3.4

        # step 17.

        self.TrueMoon = floor((self.MeanMoon-b)*10000) / 10000
        # True Moon = 8; 7 : 43
        # True Moon = 247.716666

        # (0; 13:20) = 13.33 degree is one raek, i.e. 360 deg / 27 mansions
        a = ral_to_degree(0, 13, 20)
        # Raek aka Mula
        self.Raek = self.TrueMoon/a + 1
        # Raek = 0; 19 : 34
        # Raek = 19.5771

    def suriya_values_str(self) -> str:
        return SURIYA_DAY_VALUES_FMT.format(self.Year, self.Day, self.BE_Year, self.CS_Year, self.Masaken,
                                            self.Avoman, self.Horakhun, self.Kammacubala, self.Uccabala,
                                            self.Tithi, self.TrueSun, self.TrueMoon)
