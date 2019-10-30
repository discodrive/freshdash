from datetime import date


def monthFirstDay():
    y, m = date.today().year, date.today().month
    a, m = divmod(m-1, 12)

    return date(y+a, m+1, 1)
