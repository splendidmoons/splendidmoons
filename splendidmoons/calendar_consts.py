# Eade, p.10. South Asian traditional number of days in 800 years

ERA_DAYS          = 292207
ERA_YEARS         = 800
ERA_HORAKHUN      = 373 # The Horakhun at the beginning of the CS Era, Ephemeris p.15, H2 element
ERA_UCCABALA      = 2611
ERA_AVOMAN        = 650
ERA_MASAKEN       = 0
MONTH_LENGTH      = 30
CYCLE_TITHI       = 703 # For every 692 solar days that elapse there are also 703 tithi = 692 + 11 / 692
CYCLE_SOLAR       = 692
CYCLE_DAILY       = 11
KAMMACUBALA_DAILY = 800 # Daily increase
CS_DIFF           = 638 # Absolute of CE - CS Era difference
BE_DIFF           = 543 # Absolute of BE - CS Era difference

# 1963 July 5, adhikavāra year, day 103, 1 day before Asalha Full Moon.
# Eade uses this example in "Interpolation".
HORAKHUN_REF     = 484049
HORAKHUN_REF_STR = "1963 Jul 5"
HORAKHUN_REF_DATE_TUPLE = (1963, 7, 5)

# NOTE: recreate from the tuple to avoid getting a pointer instead of a new variable.
# HORAKHUN_REF_DATE = datetime.date(1963, 7, 5)
