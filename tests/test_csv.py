import csv
from pathlib import Path
from typing import Dict, List
from splendidmoons.event_helpers import (CalendarEvent, CalendarAssocEvent, parse_annual_events_csv, year_moondays,
                                         year_moondays_associated_events)

TEST_ASSOC_EVENTS: Dict[str, List[CalendarAssocEvent]] = {
    "magha": [
        CalendarAssocEvent(
            note = "\\xMaghaPuja",
            label = "magha",
            day_text = "\\FullMoon",
        )
    ],

    "vesakha": [
        CalendarAssocEvent(
            note = "\\xVesakhaPuja",
            label = "vesakha",
            day_text = "\\FullMoon",
        )
    ],

    "asalha": [
        CalendarAssocEvent(
            note = "\\xAsalhaPuja",
            label = "asalha",
            day_text = "\\FullMoon"
        ),
        CalendarAssocEvent(
            note = "\\xFirstDayOfVassa",
            label = "first-day",
            day_text = "",
        ),
    ],

    "pavarana": [
        CalendarAssocEvent(
            note = "\\xPavarana",
            label = "pavarana",
            day_text = "\\FullMoon",
        ),
        CalendarAssocEvent(
            note = "\\xLastDayOfVassa",
            label = "last-day",
            day_text = "\\FullMoon",
        ),
    ]
}

TEST_MOON_PHASE_DAY_TEXT: Dict[str, str] = {
    "new": "\\NewMoon",
    "waxing": "\\FirstQuarter",
    "full": "\\FullMoon",
    "waning": "\\LastQuarter",
}

def _collect_events(from_year: int, to_year: int) -> List[CalendarEvent]:
    events: List[CalendarEvent] = []

    year = from_year
    while year <= to_year:
        events.extend(year_moondays(year, TEST_MOON_PHASE_DAY_TEXT))
        events.extend(year_moondays_associated_events(year, TEST_ASSOC_EVENTS))
        events.extend(parse_annual_events_csv(year, "./tests/data/fs-calendar-annual-events.csv"))

        year += 1

    events = sorted(events, key=lambda x: x['date'])

    return events

def test_generating_year_events_csv():
    for year in [1978, # Adhikavara
                 2019, # Normal
                 2020, # Adhikavara
                 2021, # Adhikamasa
                 2022, # Normal
                 2023, # Adhikamasa
                 ]:

        events = _collect_events(year, year)
        csv_path = Path("events.csv")

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=events[0].keys(),
                                    delimiter=';')

            writer.writeheader()
            for row in events:
                writer.writerow(row)


        expected = ""
        result = "sth"

        with open(Path(f"./tests/data/events-{year}.csv"), 'r', encoding='utf-8') as f:
            expected = f.read()

        with open(csv_path, 'r', encoding='utf-8') as f:
            result = f.read()

        assert result == expected

        csv_path.unlink()
