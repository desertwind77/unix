#!/usr/bin/env python
# pylint: disable=all

def print_leading_zero():
    # Displaying numbers with leading zeros
    print( "{:06d}".format( 99 ) )      # 000099
    print( f"{67 :07d}" )               # 0000067
    str( 73 ).rjust( 7, '0' )           # 0000073
    '37'.zfill( 6 )                     # 000037

def enumerate_example():
    # https://realpython.com/python-enumerate/
    values = [ 'a', 'b', 'c', 'd', 'e' ]
    for count, value in enumerate( values ):
        print( count, value )

from datetime import date, datetime
from dateutil.relativedelta import *
import calendar
def dateutil_example():
    # dateutil package
    #   https://dev.to/ejbarba/python-dateutil-module-4m03
    #   install: pip3 install python-dateutil
    #
    #   use cases
    #   - Computing of relative deltas (next Monday, next week, last week of
    #     the previous month, next five years, etc).
    #   - Computing of relative deltas between two given dates and/or datetime
    #     objects.
    now = datetime.now()
    today = date.today()
    last_week = today + relativedelta( weeks=-1 )
    next_week = today + relativedelta( weeks=+1 )
    last_month = today + relativedelta( months=-1 )
    next_month = today + relativedelta( months=+1 )
    next_month_plus_one_week = today + relativedelta( months=+1, weeks=+1 )
    added_time = today + relativedelta( months=+1, weeks=+1, hour=13 )
    one_month_before_one_year = today + relativedelta( years=+1, months=-1 )

    # Adding one month will never cross the month boundary:
    print(date(2020, 1, 27) + relativedelta(months=+1))
    # 2020-02-27
    print(date(2020, 1, 31) + relativedelta(months=+1))
    # 2020-02-29 (2020 is a leap year!)
    print(date(2020, 1, 31) + relativedelta(months=+2))
    # 2020-03-31
    # This logic also applies for years, even on leap years
    print(date(2020, 2, 28) + relativedelta(years=+1))
    # 2021-02-28
    print(date(2020, 2, 29) + relativedelta(years=+1))
    # 2021-02-28
    # Subtracting 1 year from Feb 29 2020 will print Feb 28 2019
    print(date(2020, 2, 29) + relativedelta(years=-1))
    # 2019-02-28

    # Assumming today is a Monday
    coming_friday = today + relativedelta( weekday=FR )
    next_tueday = today + relativedelta( weeks=+1, weekday=TU )
    # Making use of the calendar import
    next_tueday_calendar = today + relativedelta( weeks=+1, weekday=calendar.TUESDAY )

    # Get the 237th day of 2020
    print( date( 2020, 1, 1 ) + relativedelta( yearday=237 ) )
    # 2020-08-24

    # Getting the difference of two dates
    nasa_birthday = datetime( 1958, 7, 29, 0, 0 )
    age_of_nasa = relativedelta( today, nasa_birthday )
    print( age_of_nasa )
    print( 'It has been {} years, {} months and {} days since the birth of NASA.'
           .format( age_of_nasa.years, age_of_nasa.months, age_of_nasa.days ) )


print_leading_zero()
enumerate_example()
dateutil_example()
