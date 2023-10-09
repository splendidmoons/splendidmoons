import datetime

from splendidmoons.ical import HasIcalEvent

"""
Events are notes for a date in a calendar.
They may be anniversaries, Kathinas or occasional notes.
"""

class Event(HasIcalEvent):
    date: datetime.date = datetime.date.fromtimestamp(0)
    summary: str = ""
    description: str = ""

    def __init__(self):
        pass

"""
Type for major calendar events for convenience.

- Magha Puja
- Vesakha Puja
- Asalha Puja
- Vassa begins
- Pavarana Day
- Vassa ends
"""

MajorEvent = Event
