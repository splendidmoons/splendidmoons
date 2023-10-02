import typer

from splendidmoons.calendar_year import CalendarYear

app = typer.Typer()

@app.command()
def year_type(common_era_year: int):
    cal_year = CalendarYear(common_era_year)
    print(cal_year.year_type())

@app.command()
def asalha_puja(common_era_year: int):
    cal_year = CalendarYear(common_era_year)
    print(cal_year.asalha_puja())
