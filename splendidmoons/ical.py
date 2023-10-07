import datetime
from typing import TypedDict, List
import uuid

class IcalVEvent(TypedDict):
    UID: str
    DTSTAMP: str
    DTSTART: str
    DTEND: str
    SUMMARY: str

class HasIcalEvent:
    date: datetime.date
    phase: str

def ical_vevent(date: datetime.date,
                summary: str,
                dtstamp = datetime.datetime.utcnow(),
                ) -> IcalVEvent:
    return IcalVEvent(
        UID = str(uuid.uuid4()),
        # 20160516T153929Z
        DTSTAMP = dtstamp.strftime("%Y%m%dT%H%M%SZ"),
        # 20130126
        DTSTART = date.strftime("%Y%m%d"),
        # 20130127
        DTEND = (date + datetime.timedelta(days=1)).strftime("%Y%m%d"),
        # Full Moon - 15 day Hemanta 4/8
        SUMMARY = summary,
    )

def ical_vevent_to_str(e: IcalVEvent) -> str:
    """
    BEGIN:VEVENT
    DTSTAMP:20160516T153929Z
    UID:1e42915f-0e76-4f27-8ed9-6bbb27a02b44
    SUMMARY:Full Moon - 15 day Hemanta 4/8
    DTSTART;VALUE=DATE:20130126
    DTEND;VALUE=DATE:20130127
    END:VEVENT
    """

    res = f"""BEGIN:VEVENT
DTSTAMP:{e['DTSTAMP']}
UID:{e['UID']}
SUMMARY:{e['SUMMARY']}
DTSTART;VALUE=DATE:{e['DTSTART']}
DTEND;VALUE=DATE:{e['DTEND']}
END:VEVENT
"""

    return res

"""
https://tools.ietf.org/html/draft-ietf-calext-extensions-01

http://stackoverflow.com/a/17187346/195141

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//My Company//NONSGML Event Calendar//EN
URL:http://my.calendar/url
NAME:My Calendar Name
X-WR-CALNAME:My Calendar Name
DESCRIPTION:A description of my calendar
X-WR-CALDESC:A description of my calendar
TIMEZONE-ID:Europe/London
X-WR-TIMEZONE:Europe/London
REFRESH-INTERVAL;VALUE=DURATION:PT12H
X-PUBLISHED-TTL:PT12H
COLOR:34:50:105
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""

MAHANIKAYA_ICAL_HEADER = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:Uposatha Moondays Mahānikāya EN
URL:http://splendidmoons.github.io/ical/mahanikaya.ical
NAME:Uposatha Moondays (Mahānikāya)
X-WR-CALNAME:Uposatha Moondays (Mahānikāya)
DESCRIPTION:Uposatha Moondays (Mahānikāya)
X-WR-CALDESC:Uposatha Moondays (Mahānikāya)
REFRESH-INTERVAL;VALUE=DURATION:PT12H
X-PUBLISHED-TTL:PT12H
COLOR:244:196:48
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""

def write_ical(events: List[IcalVEvent], ical_path: str):
    text = MAHANIKAYA_ICAL_HEADER

    for e in events:
        text += ical_vevent_to_str(e)

    text += "END:VCALENDAR\n"

    with open(ical_path, 'w', encoding = 'utf-8', newline = '\r\n') as f:
        f.write(text)
