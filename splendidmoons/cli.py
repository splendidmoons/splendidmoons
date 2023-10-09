import csv, json
from typing import List, Optional, TypedDict
import typer

from splendidmoons.event_helpers import CalendarEvent, parse_annual_events_csv, year_moondays, year_moondays_associated_events
from splendidmoons.calendar_year import CalendarYear
from splendidmoons.ical import IcalVEvent, ical_vevent, write_ical

app = typer.Typer()

@app.command()
def year_type(common_era_year: int):
    cal_year = CalendarYear(common_era_year)
    print(cal_year.year_type())

@app.command()
def asalha_puja(common_era_year: int):
    cal_year = CalendarYear(common_era_year)
    print(cal_year.asalha_puja())

def _collect_events(from_year: int,
                    to_year: int,
                    annual_events_csv_path: Optional[str] = None,
                    ) -> List[CalendarEvent]:



    events: List[CalendarEvent] = []

    year = from_year
    while year <= to_year:
        events.extend(year_moondays(year))
        events.extend(year_moondays_associated_events(year))
        if annual_events_csv_path is not None:
            events.extend(parse_annual_events_csv(year, annual_events_csv_path))

        year += 1

    events = sorted(events, key=lambda x: x['date'])

    return events

@app.command()
def year_events_csv(from_year: int,
                    to_year: int,
                    csv_path: str,
                    delimiter = ',',
                    annual_events_csv_path: Optional[str] = None):

    events = _collect_events(from_year, to_year, annual_events_csv_path)

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f,
                                fieldnames=events[0].keys(),
                                delimiter=delimiter)

        writer.writeheader()
        for row in events:
            writer.writerow(row)

@app.command()
def year_events_ical(from_year: int,
                    to_year: int,
                    ical_path: str,
                    annual_events_csv_path: Optional[str] = None):

    events = _collect_events(from_year, to_year, annual_events_csv_path)

    def _to_vevent(x: CalendarEvent) -> IcalVEvent:
        return ical_vevent(x['date'], x['note'])

    ical_vevents = [_to_vevent(x) for x in events]

    write_ical(ical_vevents, ical_path)

@app.command()
def year_events_json(from_year: int,
                     to_year: int,
                     json_path: str,
                     annual_events_csv_path: Optional[str] = None):

    events = _collect_events(from_year, to_year, annual_events_csv_path)

    class JsonEvent(TypedDict):
        date: str
        day_text: str
        note: str
        label: str
        phase: str
        season: str
        season_number: int
        season_total: int
        days: int

    def _to_json_event(x: CalendarEvent) -> JsonEvent:
        return JsonEvent(
            date = x['date'].isoformat(),
            day_text = x['day_text'],
            note = x['note'],
            label = x['label'],
            phase = x['phase'],
            season = x['season'],
            season_number = x['season_number'],
            season_total = x['season_total'],
            days = x['days'],
        )

    json_events = [_to_json_event(x) for x in events]

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_events))
