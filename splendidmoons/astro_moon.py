import datetime

from splendidmoons.ical import HasIcalEvent

class AstroMoon(HasIcalEvent):
    date: datetime.date = datetime.date.fromtimestamp(0)
    phase: str = ""

    def __str__(self) -> str:
        if self.phase == "":
            return ""

        return "{} Moon".format(self.phase.title())
