import datetime

from splendidmoons.ical import HasIcalEvent

class HalfMoon(HasIcalEvent):
    date: datetime.date
    phase: str

    def __init__(self, date: datetime.date, phase: str):
        self.date = date
        self.phase = phase

    def __str__(self) -> str:
        if self.phase == "":
            return ""

        return "{} Moon".format(self.phase.title())
