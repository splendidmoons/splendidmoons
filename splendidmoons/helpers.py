from typing import Tuple
from math import floor
import datetime

from splendidmoons.calendar_consts import HORAKHUN_REF, HORAKHUN_REF_DATE_TUPLE

def degree_to_ral(degree: float) -> Tuple[int, int, int]:
    """
    (x; y : z) in Rasi, Angsa (degree), Lipda (minute) means 30*60*x + 60*y + z
    in arcmins, so x and y are deg originally
    """

    # how many times 30 degrees
    x = int(floor(degree / 30))

    # the remainder degrees
    y = int(floor(degree)) % 30

    # plus the arcmins
    z = int(floor((degree - floor(degree)) * 60))

    # This is rasi, angsa, lipda
    return (x, y, z)

def degree_to_ral_str(degree: float) -> str:
    u, v, t = degree_to_ral(degree)
    return "%d:%d°%d'" % (u, v, t)

def ral_to_degree(x: int, y: int, z: int) -> float:
    """
    Multiply up and divide down by 10000 for better arcmin (z) accuracy
    Floor to keep only 4 decimal places
    """
    return floor(float(30*x+y)*10000+float(z*10000)/60) / 10000

def normalize_degree(deg: float) -> float:
    """Keep it within 360 deg"""
    if deg <= 360:
        return deg

    return deg - floor(deg/360)*360

def horakhun_to_date(horakhun: int) -> datetime.date:
    # Make sure it is not a pointer to HORAKHUN_REF_DATE, but is the same time.
    y, m, d = HORAKHUN_REF_DATE_TUPLE
    hor_date = datetime.date(y, m, d)

    delta: int
    step_days: int
    direction: int

    # Duration is max 290 solar years. Increment the date in 290 year steps.

    delta = horakhun - HORAKHUN_REF
    if delta == 0:
        return hor_date
    elif delta < 0:
        direction = -1
    else:
        direction = 1

    step_days = 290 * 356

    while abs(delta) > step_days:
        days = direction*step_days
        hor_date += datetime.timedelta(days=days)
        delta += days * -1

    # Add any remaining delta.
    hor_date += datetime.timedelta(days=delta)

    return hor_date
