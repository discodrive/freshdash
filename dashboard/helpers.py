import calendar

from datetime import date
from math import ceil


def month_first_day():
    y, m = date.today().year, date.today().month
    a, m = divmod(m-1, 12)

    return date(y+a, m+1, 1)

def month_last_day():
    return calendar.monthrange(date.today().year, date.today().month)[1]

def week_of_month():
    today = date.today()
    first_day = today.replace(day=1)

    dom = today.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))
