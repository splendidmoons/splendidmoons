import csv
from typing import List, TypedDict, Dict, Optional
import datetime
from splendidmoons.calendar_consts import BE_DIFF

from splendidmoons.calendar_year import CalendarYear, YearType
from splendidmoons.helpers import SEASON_NAME
from splendidmoons.json_cal_day import get_json_cal_days
from splendidmoons.uposatha_moon import UposathaMoon

class CalendarEvent(TypedDict):
    date: datetime.date
    day_text: str
    note: str
    label: str
    phase: str
    season: str
    season_number: int
    season_total: int
    days: int

MOON_PHASE_DAY_TEXT: Dict[str, str] = {
    "new": "New Moon",
    "waxing": "Waxing Moon", # First Quarter
    "full": "Full Moon",
    "waning": "Waning Moon", # Last Quarter
}

def calendar_event_to_str(e: CalendarEvent) -> str:
    if e['note'] != "":
        return e['note']

    if e['phase'] == "":
        return ""

    # FIXME adding the half-moons doesn't replace the phase name?
    if e['phase'] == "waxing" \
       or e['phase'] == "waning":
        return MOON_PHASE_DAY_TEXT[e['phase']]

    return "{} Moon - {} day {} {}/{}".format(e['phase'].title(),
                                              e['days'],
                                              e['season'],
                                              e['season_number'],
                                              e['season_total'])

def year_moondays(ce_year: int,
                  moon_phase_day_text: Dict[str, str] = MOON_PHASE_DAY_TEXT,
                  ) -> List[CalendarEvent]:

    from_date = datetime.date(ce_year, 1, 1)
    to_date = datetime.date(ce_year, 12, 31)

    events: List[CalendarEvent] = []

    days = get_json_cal_days(from_date, to_date)

    for d in days:
        phase, label, season = "", "", ""
        season_number, season_total, days = 0, 0, 0

        if d.uposatha_moon is not None:
            u = d.uposatha_moon
            phase = u.phase
            label = u.event
            season_number = u.s_number
            season_total = u.s_total
            days = u.u_days

            if u.lunar_season == 1:
                season = "Hemanta"
            elif u.lunar_season == 2:
                season = "Gimha"
            elif u.lunar_season == 3:
                season = "Vassāna"

        elif d.half_moon is not None:
            phase = d.half_moon.phase

        else:
            continue

        if phase in moon_phase_day_text.keys():
            day_text = moon_phase_day_text[phase]
        else:
            day_text = ""

        events.append(
            CalendarEvent(
                date = d.date,
                day_text = day_text,
                note = "",
                label = label,
                phase = phase,
                season = season,
                season_number = season_number,
                season_total = season_total,
                days = days,
            )
        )

    return events

class CalendarAssocEvent(TypedDict):
    day_text: str
    note: str
    label: str

ASSOC_EVENTS: Dict[str, List[CalendarAssocEvent]] = {
    "magha": [
        CalendarAssocEvent(
            note = "Māgha Pūjā",
            label = "magha",
            day_text = "Full Moon",
        )
    ],

    "vesakha": [
        CalendarAssocEvent(
            note = "Visākha Pūjā",
            label = "vesakha",
            day_text = "Full Moon",
        )
    ],

    "asalha": [
        CalendarAssocEvent(
            note = "Āsāḷha Pūjā",
            label = "asalha",
            day_text = "Full Moon"
        ),
        CalendarAssocEvent(
            note = "First Day of Vassa",
            label = "first-day",
            day_text = "",
        ),
    ],

    "pavarana": [
        CalendarAssocEvent(
            note = "Pavāraṇā Day",
            label = "pavarana",
            day_text = "Full Moon",
        ),
        CalendarAssocEvent(
            note = "Last Day of Vassa",
            label = "last-day",
            day_text = "Full Moon",
        ),
    ]
}

def year_moondays_associated_events(ce_year: int,
                                    assoc_events: Optional[Dict[str, List[CalendarAssocEvent]]] = None,
                                    show_adhikamasa_adhikamasa = False,
                                    ) -> List[CalendarEvent]:
    """
    Collect the major moondays and add associated events.

    Associated events can be specified, defaults are in ASSOC_EVENTS.
    """

    events: List[CalendarEvent] = []
    if assoc_events is None:
        assoc_events = ASSOC_EVENTS

    cal_year = CalendarYear(ce_year)

    prev_kattika = cal_year.calculate_previous_kattika()

    lu = UposathaMoon()
    lu.date =         prev_kattika
    lu.phase =        "full"
    lu.s_number =     8
    lu.s_total =      8
    lu.u_days =       15
    lu.m_days =       29
    lu.lunar_month =  12
    lu.lunar_season = 3
    lu.lunar_year =   prev_kattika.year + BE_DIFF

    last_uposatha = lu

    while last_uposatha.date.year <= ce_year:
        uposatha: UposathaMoon = last_uposatha.next_uposatha()
        last_uposatha = uposatha

        # Add associated events for each major event.

        if uposatha.date.year == ce_year:

            for k in ["magha", "vesakha", "asalha", "pavarana"]:
                if uposatha.event == k \
                   and k in assoc_events.keys():

                    for e in assoc_events[k]:
                        if e['label'] == 'first-day':
                            e = CalendarEvent(
                                date = uposatha.date + datetime.timedelta(days=1),
                                day_text = e['day_text'],
                                note = e['note'],
                                label = e['label'],
                                phase = "",
                                season = "",
                                season_number = 0,
                                season_total = 0,
                                days = 0,
                            )

                        else:
                            e = CalendarEvent(
                                date = uposatha.date,
                                day_text = e['day_text'],
                                note = e['note'],
                                label = e['label'],
                                phase = uposatha.phase,
                                season = SEASON_NAME[uposatha.lunar_season],
                                season_number = uposatha.s_number,
                                season_total = uposatha.s_total,
                                days = uposatha.u_days,
                            )

                        events.append(e)

        # Add Adhikamasa and Adhikavara events.

        if show_adhikamasa_adhikamasa:
            if cal_year.year_type() == YearType.Adhikamasa:
                # Full Moon of 2nd Asalha, 10th Uposatha of Gimha (10/10)
                # New Moon of 2nd Asalha, 1st Uposatha of Vassana (1/8)
                if (uposatha.lunar_season == 2 and uposatha.s_number == 10) \
                   or (uposatha.lunar_season == 3 and uposatha.s_number == 1):
                    e = CalendarEvent(
                        date = uposatha.date,
                        day_text = "Adhikamāsa",
                        note = "Adhikamāsa",
                        label = "adhikamasa",
                        phase = uposatha.phase,
                        season = SEASON_NAME[uposatha.lunar_season],
                        season_number = uposatha.s_number,
                        season_total = uposatha.s_total,
                        days = uposatha.u_days,
                    )
                    events.append(e)

            elif cal_year.year_type() == YearType.Adhikavara:
                if uposatha.has_adhikavara:
                    e = CalendarEvent(
                        date = uposatha.date,
                        day_text = "Adhikavāra",
                        note = "Adhikavāra",
                        label = "adhikavara",
                        phase = uposatha.phase,
                        season = SEASON_NAME[uposatha.lunar_season],
                        season_number = uposatha.s_number,
                        season_total = uposatha.s_total,
                        days = uposatha.u_days,
                    )
                    events.append(e)

    return events

def parse_annual_events_csv(ce_year: int, csv_path: str) -> List[CalendarEvent]:
    events: List[CalendarEvent] = []

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
            e = CalendarEvent(
                date = datetime.date(ce_year, d.month, d.day),
                note = row['note'],
                label = row['label'],
                day_text = row['day_text'],
                phase = row['phase'],
                season = row['season'],
                season_number = int(row['season_number']),
                season_total = int(row['season_total']),
                days = int(row['days']),
            )
            events.append(e)

    return events
