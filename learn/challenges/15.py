# http://www.pythonchallenge.com/pc/return/uzi.html

from datetime import date

for year in range(1000, 2000):
    date1 = date(year=year, month=1, day=26)
    day_of_week = date1.isoweekday()
    try:
        date2 = date(year=year, month=2, day=29)
    except:
        date2 = None

    if date2 and day_of_week == 1 and str(year)[3] == '6':
        print(date1)
