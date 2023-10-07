import re
from pathlib import Path
import datetime
from typing import List
from splendidmoons.event_helpers import (CalendarEvent, calendar_event_to_str, year_moondays,
                                         year_moondays_associated_events)
from splendidmoons.ical import IcalVEvent, ical_vevent, write_ical

def _collect_events(from_year: int, to_year: int) -> List[CalendarEvent]:
    events: List[CalendarEvent] = []

    year = from_year
    while year <= to_year:
        events.extend(year_moondays(year))
        events.extend(year_moondays_associated_events(year))

        year += 1

    events = sorted(events, key=lambda x: x['date'])

    return events

def test_generating_ical():
    # DTSTAMP:20160516T155437Z
    #
    # Starting from:
    #
    # 2010-01-08: Waning Moon
    # 2010-01-15: New Moon - 15 day Hemanta 5/8
    #
    # Until:
    #
    # 2030-12-24: New Moon - 14 day Hemanta 3/8

    events = _collect_events(2010, 2030)

    dtstamp = datetime.datetime(2016, 5, 16, 15, 54, 37)

    def _to_vevent(x: CalendarEvent) -> IcalVEvent:
        summary = calendar_event_to_str(x)
        return ical_vevent(x['date'], summary, dtstamp)

    ical_vevents = [_to_vevent(x) for x in events]

    ical_path = "mahanikaya.ical"

    write_ical(ical_vevents, ical_path)

    with open(ical_path, 'rb') as f:
        # write_ical() should write CRLF line endings
        #
        # Use a slice, .startswith() doesn't create string diff when assert fails
        result = f.read()
        assert result[0:17] == b'BEGIN:VCALENDAR\r\n'

    with open(ical_path, 'r', encoding='utf-8') as f:
        result = f.read()
        result = re.sub(r'UID:[^ \n]+\n', '', result)

    with open(ical_path, 'w', encoding='utf-8', newline = '\r\n') as f:
        f.write(result)

    with open(Path("./tests/data/mahanikaya-2010-2030.no-uid.ical"), 'r', encoding='utf-8') as f:
        expected = f.read()

    assert result == expected

    Path(ical_path).unlink()
