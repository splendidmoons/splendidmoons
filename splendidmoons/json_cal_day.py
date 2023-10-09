import datetime
from typing import List, Optional, Dict
from splendidmoons.calendar_consts import BE_DIFF
from splendidmoons.calendar_year import CalendarYear
from splendidmoons.ical import HasIcalEvent

from splendidmoons.uposatha_moon import UposathaMoon
from splendidmoons.half_moon import HalfMoon
from splendidmoons.astro_moon import AstroMoon
from splendidmoons.event import Event, MajorEvent

class JsonCalDay():
    date: datetime.date = datetime.date.fromtimestamp(0)
    uposatha_moon: Optional[UposathaMoon] = None
    half_moon: Optional[HalfMoon] = None
    astro_moon: Optional[AstroMoon] = None
    major_events: List[MajorEvent] = []
    events: List[Event] = []

    def __init__(self):
        pass

    def to_dict(self) -> Dict:
        return {
            "date": self.date.isoformat(),
            "uposatha_moon": None if not self.uposatha_moon else self.uposatha_moon.__dict__,
            "half_moon": self.half_moon,
            "astro_moon": self.astro_moon,
            "major_events": self.major_events,
            "events": self.events,
        }

    def __str__(self) -> str:
        return str(self.to_dict())

def find_json_cal_day_idx(cal_days: List[JsonCalDay],
                          date: datetime.date) -> Optional[int]:
    for idx, d in enumerate(cal_days):
        if d.date == date:
            return idx
    return None

def add_half_moon_days(cal_days: List[JsonCalDay]) -> List[JsonCalDay]:
    half_moon_days: List[JsonCalDay] = []

    for day in cal_days:
        # If there is no uposatha on the day, skip
        if day.uposatha_moon is None:
            continue

        # Eight days from its date
        eighth_day = JsonCalDay()
        eighth_day.date = day.date + datetime.timedelta(days=8)

        # determine the phase of the half moon
        phase = ""
        if day.uposatha_moon.phase == "new":
            phase = "waxing"
        elif day.uposatha_moon.phase == "full":
            phase = "waning"
        else:
            # just skip in case of an invalid phase
            continue

        # add a new half-moon
        eighth_day.half_moon = HalfMoon(
            date = eighth_day.date,
            phase = phase,
        )

        half_moon_days.append(eighth_day)

    cal_days.extend(half_moon_days)

    return cal_days

def merge_event_into_cal_days(cal_days: List[JsonCalDay],
                              event: HasIcalEvent) -> List[JsonCalDay]:
    day_idx = find_json_cal_day_idx(cal_days, event.date)
    if day_idx is None:
        day = JsonCalDay()
    else:
        day = cal_days[day_idx]

    add_event_to_json_cal_day(event, day)

    if day_idx is None:
        cal_days.append(day)
    else:
        cal_days[day_idx] = day

    return cal_days

def get_astro_moons(from_date: datetime.date,
                    to_date: datetime.date) -> List[AstroMoon]:
    # FIXME
    return []

def get_json_cal_days(from_date: datetime.date,
                      to_date: datetime.date) -> List[JsonCalDay]:
    cal_days: List[JsonCalDay] = []

    for d in get_astro_moons(from_date, to_date):
        merge_event_into_cal_days(cal_days, d)

    year = from_date.year
    while year <= to_date.year:

        for d in generate_solar_year(year):
            if d.date < from_date or d.date > to_date:
                continue
            else:
                merge_event_into_cal_days(cal_days, d)

        year += 1

    return cal_days

def generate_solar_year(ce_year: int) -> List[HasIcalEvent]:
    events: List[HasIcalEvent] = []

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

        # Add the Uposatha
        if uposatha.date.year == ce_year:
            events.append(uposatha)

        # Half Moon
        phase = ""
        if uposatha.phase == "new":
            phase = "waxing"
        elif uposatha.phase == "full":
            phase = "waning"

        half_moon = HalfMoon(
            date = uposatha.date + datetime.timedelta(days=8),
            phase = phase,
        )

        if half_moon.date.year == ce_year:
            events.append(half_moon)

        # Major Events

        if uposatha.date.year == ce_year:

            if uposatha.event == "magha":
                e = MajorEvent()
                e.date = uposatha.date
                e.summary = "Māgha Pūjā"
                e.description = "Māgha Pūjā"
                events.append(e)

            elif uposatha.event == "vesakha":
                e = MajorEvent()
                e.date = uposatha.date
                e.summary = "Vesākha Pūjā"
                e.description = "Vesākha Pūjā"
                events.append(e)

            elif uposatha.event == "asalha":
                e = MajorEvent()
                e.date = uposatha.date
                e.summary = "Āsāḷha Pūjā"
                e.description = "Āsāḷha Pūjā"
                events.append(e)

                e = MajorEvent()
                e.date = uposatha.date + datetime.timedelta(days=1)
                e.summary = "First day of Vassa"
                e.description = "First day of Vassa"
                events.append(e)

            elif uposatha.event == "pavarana":
                e = MajorEvent()
                e.date = uposatha.date
                e.summary = "Pavāraṇā Day"
                e.description = "Pavāraṇā Day"
                events.append(e)

                e = MajorEvent()
                e.date = uposatha.date
                e.summary = "Last Day of Vassa"
                e.description = "Last Day of Vassa"
                events.append(e)

    return events

def add_event_to_json_cal_day(event: HasIcalEvent, day: JsonCalDay) -> JsonCalDay:
    type_self = str(type(event))

    day.date = event.date

    if type_self == "<class 'splendidmoons.uposatha_moon.UposathaMoon'>" \
       and isinstance(event, UposathaMoon):
        day.uposatha_moon = event
        return day

    elif type_self == "<class 'splendidmoons.half_moon.HalfMoon'>" \
       and isinstance(event, HalfMoon):
        day.half_moon = event
        return day

    elif type_self == "<class 'splendidmoons.astro_moon.AstroMoon'>" \
       and isinstance(event, AstroMoon):
        day.astro_moon = event
        return day

    elif type_self == "<class 'splendidmoons.event.MajorEvent'>" \
       and isinstance(event, MajorEvent):
        day.major_events.append(event)
        return day

    elif type_self == "<class 'splendidmoons.event.Event'>" \
       and isinstance(event, Event):
        day.events.append(event)
        return day

    raise Exception(f"add_event_to_json_cal_day() can't handle type: {type(event)}")
