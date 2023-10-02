"""Test Calendar Year Calculations
"""

import datetime
from typing import Dict, List, TypedDict
from splendidmoons.calendar_consts import HORAKHUN_REF, HORAKHUN_REF_DATE_TUPLE

from splendidmoons.calendar_day import SURIYA_DAY_VALUES_FMT, CalendarDay
from splendidmoons.calendar_year import SURIYA_YEAR_VALUES_FMT, CalendarYear
from splendidmoons.helpers import degree_to_ral_str, horakhun_to_date

TEST_ADHIKAMASA_YEAR: Dict[int, bool] = {
    # --- T = thaiorc.com, M = myhora.com, F = fs-cal, K = Khemanando
    #              T M F K
    1950: True,  # 0 0
    1951: False, #
    1952: False, #
    1953: True,  # 3 3
    1954: False, #
    1955: False, #
    1956: True,  # 3 3
    1957: False, #
    1958: True,  # 2 2
    1959: False, #
    1960: False, #
    1961: True,  # 3 3
    1962: False, #
    1963: False, #
    1964: True,  # 3 3
    1965: False, #
    1966: True,  # 2 2
    1967: False, #
    1968: False, #
    1969: True,  # 3 3
    1970: False, #
    1971: False, #
    1972: True,  # 3 3
    1973: False, #
    1974: False, #
    1975: True,  # 3 3
    1976: False, #
    1977: True,  # 2 2
    1978: False, #
    1979: False, #
    1980: True,  # 3 3
    1981: False, #
    1982: False, #
    1983: True,  # 3 3
    1984: False, #
    1985: True,  # 2 2    K
    1986: False, #
    1987: False, #
    1988: True,  # 3 3    K
    1989: False, #
    1990: False, #        K
    1991: True,  # 3 3
    1992: False, #
    1993: True,  # 2 2    K
    1994: False, #
    1995: False, #
    1996: True,  # 3 3    K
    1997: False, #
    1998: False, #
    1999: True,  # 3 3    K
    2000: False, #
    2001: False, #        K
    2002: True,  # 3 3    ?
    2003: False, #
    2004: True,  # 2 2 2  K
    2005: False, #
    2006: False, #
    2007: True,  # 3 3 3
    2008: False, #
    2009: False, #
    2010: True,  # 3 3 3
    2011: False, #
    2012: True,  # 2 2 2
    2013: False, #
    2014: False, #
    2015: True,  # 3 3 3
    2016: False, #
    2017: False, #
    2018: True,  # 3 3
}

TEST_ADHIKAVARA_YEAR: Dict[int, bool] = {
    1993: False, #
    1994: True,  # False in past calendar, exception
    1995: False, #
    1996: False, #
    1997: False, # True in past calendar, exception
    1998: False, #
    1999: False, #
    2000: True,  # 6
    2001: False, #
    2002: False, #
    2003: False, #
    2004: False, #
    2005: True,  # 5 fs-cal
    2006: False, #
    2007: False, #
    2008: False, #
    2009: True,  # 4 fs-cal
    2010: False, #
    2011: False, #
    2012: False, #
    2013: False, #
    2014: False, #
    2015: False, #
    2016: True,  # 7 fs-cal
}

TEST_ASALHA_PUJA_YEARS: Dict[int, str] = {
    1950: "1950-07-29", # myhora.com
    1951: "1951-07-18", # myhora.com
    #1952: "1952-07-07", # myhora.com F
    #1953: "1953-07-26", # myhora.com F
    1954: "1954-07-15", # myhora.com
    1955: "1955-07-04", # myhora.com
    1956: "1956-07-22", # myhora.com
    #1957: "1957-07-12", # thaiorc.com, myhora.com F
    #1958: "1958-07-31", # thaiorc.com, myhora.com F
    1959: "1959-07-20", # thaiorc.com, myhora.com
    1960: "1960-07-08", # thaiorc.com, myhora.com
    1961: "1961-07-27", # thaiorc.com, myhora.com
    1962: "1962-07-16", # thaiorc.com, myhora.com
    1963: "1963-07-06", # myhora.com
    1964: "1964-07-24", # myhora.com
    1965: "1965-07-13", # myhora.com
    1966: "1966-08-01", # myhora.com
    1967: "1967-07-21", # myhora.com
    #1968: "1968-07-09", # myhora.com F
    #1969: "1969-07-28", # myhora.com F
    1970: "1970-07-18", # myhora.com
    1971: "1971-07-07", # myhora.com
    1972: "1972-07-25", # myhora.com
    1973: "1973-07-15", # myhora.com
    1974: "1974-07-04", # myhora.com
    1975: "1975-07-23", # myhora.com
    1976: "1976-07-11", # myhora.com
    1977: "1977-07-30", # myhora.com
    1978: "1978-07-20", # exception in calendars: myhora.com, 1978-07-19 (missing adhikavāra)
    1979: "1979-07-09", # myhora.com
    1980: "1980-07-27", # myhora.com
    1981: "1981-07-16", # myhora.com
    1982: "1982-07-05", # myhora.com
    1983: "1983-07-24", # myhora.com
    1984: "1984-07-13", # exception in calendars: myhora.com, 1984-07-12 (missing adhikavāra)
    1985: "1985-08-01", # exception in calendars: myhora.com
    1986: "1986-07-21", # exception in calendars: myhora.com
    1987: "1987-07-10", # thaiorc.com
    1988: "1988-07-28", # thaiorc.com
    1989: "1989-07-18", # exception in calendars: thaiorc.com, 1989-07-17 (missing adhikavāra)
    1990: "1990-07-07", # thaiorc.com
    1991: "1991-07-26", # thaiorc.com
    1992: "1992-07-14", # thaiorc.com NOTE: bot.or.th has 07-15
    1993: "1993-08-02", # thaiorc.com
    1994: "1994-07-23", # exception in calendars: thaiorc.com, myhora.com, 1994-07-22 (missing adhikavāra)
    1995: "1995-07-12", # exception in calendars: thaiorc.com, myhora.com
    1996: "1996-07-30", # exception in calendars: thaiorc.com, myhora.com
    1997: "1997-07-19", # thaiorc.com, myhora.com
    1998: "1998-07-08", # thaiorc.com
    1999: "1999-07-27", # thaiorc.com
    2000: "2000-07-16", # thaiorc.com
    2001: "2001-07-05", # fs-cal, thaiorc.com
    2002: "2002-07-24", # thaiorc.com
    2003: "2003-07-13", # thaiorc.com
    2004: "2004-07-31", # fs-cal
    2005: "2005-07-21", # fs-cal NOTE: bot.or.th has 07-22
    2006: "2006-07-10", # fs-cal NOTE: bot.or.th has 07-11
    2007: "2007-07-29", # fs-cal NOTE: bot.or.th says official date was 07-30, substitution day
    2008: "2008-07-17", # fs-cal, bot.or.th
    2009: "2009-07-07", # fs-cal, bot.or.th
    2010: "2010-07-26", # fs-cal, bot.or.th
    2011: "2011-07-15", # fs-cal, bot.or.th
    2012: "2012-08-02", # fs-cal, bot.or.th
    2013: "2013-07-22", # fs-cal, bot.or.th
    2014: "2014-07-11", # fs-cal, bot.or.th
    2015: "2015-07-30", # fs-cal, bot.or.th
    2016: "2016-07-19", # fs-cal, bot.or.th, myhora.com
    2017: "2017-07-08", # fs-cal, myhora.com
    2018: "2018-07-27", # fs-cal, myhora.com
    2019: "2019-07-16", # fs-cal, myhora.com
    2020: "2020-07-05", # fs-cal
    2021: "2021-07-24", # fs-cal
    2022: "2022-07-13", # fs-cal
    2023: "2023-08-01", # fs-cal
    2024: "2024-07-20", # fs-cal
    2025: "2025-07-10", # fs-cal
}

def test_adhikamasa_years():
    for year, expected in TEST_ADHIKAMASA_YEAR.items():
        assert CalendarYear(year).is_adhikamasa() is expected

def test_adhikavara_years():
    for year, expected in TEST_ADHIKAVARA_YEAR.items():
        assert CalendarYear(year).is_adhikavara() is expected

class CalendarYearData(TypedDict):
    Year: int
    BE_Year: int
    CS_Year: int
    Horakhun: int
    Kammacubala: int
    Uccabala: int
    Avoman: int
    Masaken: int
    Tithi: int

def test_calculate_suriya_values():
    expected_values: List[CalendarYearData] = []

    # Take CE 1963, CS 1325 (as in the paper: "Rules for Interpolation...", JC Eade)
    expected_values.append(
        CalendarYearData(
            Year =        1963,
            BE_Year =     2506,
            CS_Year =     1325,
            Horakhun =    483969,
            Kammacubala = 552,
            Uccabala =    1780,
            Avoman =      61,
            Masaken =     16388,
            Tithi =       23,
        )
    )

    # Take CE 1496, CS 858 (as in "South Asian Ephemeris", JC Eade)
    # https://books.google.com/books?id=g_JEgc5C-OYC
    expected_values.append(
        CalendarYearData(
        Year =        1496,
        BE_Year =     2039,
        CS_Year =     858,
        Horakhun =    313393,
        Kammacubala = 421,
        Uccabala =    2500,
        Avoman =      429,
        Masaken =     10612,
        Tithi =       15,
        )
    )

    for exp_y in expected_values:
        y = CalendarYear(exp_y['Year'])

        y_str = y.suriya_values_str()
        exp_y_str = SURIYA_YEAR_VALUES_FMT.format(exp_y['Year'], exp_y['BE_Year'], exp_y['CS_Year'], exp_y['Horakhun'], exp_y['Kammacubala'], exp_y['Uccabala'], exp_y['Avoman'], exp_y['Masaken'], exp_y['Tithi'])

        assert y_str == exp_y_str

class CalendarDayData(TypedDict):
    Year: int
    Day: int
    BE_Year: int
    CS_Year: int
    Masaken: int
    Avoman: int
    Horakhun: int
    Kammacubala: int
    Uccabala: int
    Tithi: int
    TrueSun: float
    TrueMoon: float

def test_calendar_day_init():
    expected_values: List[CalendarDayData] = []

    expected_values.append(
        CalendarDayData(
            Year =        1963,
            Day =         103, # 1963-07-05, 1 day before adhikavāra Asalha, Full Moon
            BE_Year =     2506,
            CS_Year =     1325,
            Masaken =     16391,
            Avoman =      249,
            Horakhun =    484049,
            Kammacubala = 64552,
            Uccabala =    1860,
            Tithi =       14,
            TrueSun =     79.4832,
            TrueMoon =    247.6955,
        )
    )

    expected_values.append(
        CalendarDayData(
            Year =        2015,
            Day =         103 + 30, # adhikamāsa, 2015-07-30, Asalha, Full Moon
            BE_Year =     2558,
            CS_Year =     1377,
            Masaken =     17035,
            Avoman =      463,
            Horakhun =    503067,
            Kammacubala = 84188,
            Uccabala =    1486,
            Tithi =       14,
            TrueSun =     104.5499,
            TrueMoon =    275.4053,
        )
    )

    expected_values.append(
        CalendarDayData(
            Year =        2015,
            Day =         103 + 30 - 15, # adhikamāsa, 2015-07-15, 15 days before Asalha, New Moon
            BE_Year =     2558,
            CS_Year =     1377,
            Masaken =     17034,
            Avoman =      298,
            Horakhun =    503052,
            Kammacubala = 72188,
            Uccabala =    1471,
            Tithi =       29,
            TrueSun =     89.2166,
            TrueMoon =    86.5874,
        )
    )

    for exp_d in expected_values:
        d = CalendarDay(exp_d['Year'], exp_d['Day'])

        d_str = d.suriya_values_str()
        exp_d_str = SURIYA_DAY_VALUES_FMT.format(exp_d['Year'], exp_d['Day'], exp_d['BE_Year'], exp_d['CS_Year'], exp_d['Masaken'], exp_d['Avoman'], exp_d['Horakhun'], exp_d['Kammacubala'], exp_d['Uccabala'], exp_d['Tithi'], exp_d['TrueSun'], exp_d['TrueMoon'])

        assert d_str == exp_d_str

def test_asalha_puja():
    for year, expected in TEST_ASALHA_PUJA_YEARS.items():
        assert CalendarYear(year).asalha_puja().isoformat() == expected

def test_raek():
    # The expanded example in Eade's paper "Rules for Interpolation in The Thai Calendar"
    # CS 1325, Raek 0; 19 : 34
    # CS 1325 is adhikavāra
    day = CalendarDay(1963, 103)
    expect = "0:19°34'"
    ral = degree_to_ral_str(day.Raek)
    assert ral == expect

    expect = "2:19°28'"
    ral = degree_to_ral_str(day.TrueSun)
    assert ral == expect

    expect = "8:7°41'"
    ral = degree_to_ral_str(day.TrueMoon)
    assert ral == expect

    # CS 1324, Raek 0; 20 : 38
    # CS 1324 is common year
    day = CalendarDay(1962, 103)
    expect = "0:20°39'" # +1 arcmin diff to the value in the paper, probably rounding differences
    ral = degree_to_ral_str(day.Raek)
    assert ral == expect

    # 2015-07-15
    # 15 days before Asalha
    # 2015 is adhikamāsa
    day = CalendarDay(2015, 103+30-15)
    expect = "2:26°35'" # myhora.com: Moon is (2; 26 : 12)
    ral = degree_to_ral_str(day.TrueMoon)
    assert ral == expect

    # 1288-04-14
    # Example cited in Calendrical.
    day = CalendarDay(1288, 41)
    expect = "0:19°58'"
    ral = degree_to_ral_str(day.TrueSun)
    assert ral == expect

    expect = "5:11°27'"
    ral = degree_to_ral_str(day.TrueMoon)
    assert ral == expect

    # 1288-06-15
    # Common year, Asalha Puja. Date is Full Moon on AstroPixels.
    day = CalendarDay(1288, 103)
    expect = "2:19°9'"
    ral = degree_to_ral_str(day.TrueSun)
    assert ral == expect

    expect = "8:19°1'"
    ral = degree_to_ral_str(day.TrueMoon)
    assert ral == expect

TEST_HORAKHUN_TO_DATE_STR: Dict[int, str] = {
    0:      "638 Mar 24",
    205184: "1200 Jan 01",
    237396: "1288 Mar 11", # Citta 1, day 0
    237430: "1288 Apr 14",
    237437: "1288 Apr 21", # Eade has 1288 Apr 14. I'm getting correct Sun and Moon at -7d from his Horakhun
    237499: "1288 Jun 22", # 1288 Jun 15, Eade -7d
    338796: "1565 Oct 26", # 26 October 1565, at -10d from Eade in Mangrai Bhuddha he has 338806
    351281: "1600 Jan 01",
    387806: "1700 Jan 01",
    408625: "1757 Jan 01", # first date on myhora.com
    408805: "1757 Jun 30", # day 103, myhora.com horakhun matches, but he marks it as Asalha Puja, 1 day off b/c it is adhikavāra year
    483946: "1963 Mar 24", # Citta 1, day 0
    484049: "1963 Jul 05", # Asalha 14, day 103, adhikavāra year
    502857: "2015 Jan 01", # myhora.com
}

def test_day():
    # Test HORAKHUN_REF constant
    y, m, d = HORAKHUN_REF_DATE_TUPLE
    expected = datetime.date(y, m, d)
    hor_date = horakhun_to_date(HORAKHUN_REF)
    assert hor_date.isoformat() == expected.isoformat()

    for horakhun, expected in TEST_HORAKHUN_TO_DATE_STR.items():
        assert horakhun_to_date(horakhun).strftime("%Y %b %d") == expected

    # Horakhun 1. First day of the Era.
    day = CalendarDay(638, 1)
    expected = """Horakhun: 1
Date: 638 March 25
True Sun: 0:2°38'
True Moon: 0:20°30'
Tithi: 1
"""

    res = """Horakhun: {}
Date: {}
True Sun: {}
True Moon: {}
Tithi: {}
""".format(day.Horakhun,
           horakhun_to_date(day.Horakhun).strftime("%Y %B %d"),
           degree_to_ral_str(day.TrueSun),
           degree_to_ral_str(day.TrueMoon),
           day.Tithi)
    assert res == expected

    # Casting of the Buddha image at Wat Kiat. Eade has the duang inscription in the Mangrai Buddha paper.
    day = CalendarDay(1565, 298)
    expected = """Day: 298
Date: 1566 Jan 03
Horakhun: 338865
Tithi: 2
True Sun: 8:25°29'
True Moon: 9:20°50'
"""

    res = """Day: {}
Date: {}
Horakhun: {}
Tithi: {}
True Sun: {}
True Moon: {}
""".format(day.Day,
           horakhun_to_date(day.Horakhun).strftime("%Y %b %d"),
           day.Horakhun,
           day.Tithi,
           degree_to_ral_str(day.TrueSun),
           degree_to_ral_str(day.TrueMoon))

    assert res == expected
