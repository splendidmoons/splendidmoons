from typing import Dict

# Whether to apply the (adhikavāra) exceptions where the official calendar
# differed from the formulas. Default is false, to generate calendar data that
# is "pure" in its consistency. Set to true if you want to match official past
# calendars which differed from the regular pattern.
USE_HISTORICAL_EXCEPTIONS: bool = False

ADHIKAVARA_HISTORICAL_EXCEPTIONS: Dict[int, bool] = {
    1994: False,
    1997: True,
}

# TODO: use env var verbose
verbose: bool = False
