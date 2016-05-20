"""Download wrapper for yahoo finance api"""
from __future__ import print_function
import datetime
from yahoo_finance import Share

TIME_FMT = '%Y-%m-%d'


def check_date_format(date):
    """Check if a date is valid using the TIME_FMT string"""
    try:
        datetime.datetime.strptime(date, TIME_FMT)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def check_args(start_date, end_date):
    """Check all user supplied args"""
    res = False
    if not check_date_format(start_date):
        print(' [-] Invalid start date format! Use: %s' % TIME_FMT)
        res = True
    if not check_date_format(end_date):
        print(' [-] Invalid end date format! Use: %s' % TIME_FMT)
        res = True
    if not res:
        s_d = datetime.datetime.strptime(start_date, TIME_FMT)
        e_d = datetime.datetime.strptime(end_date, TIME_FMT)
        if s_d >= e_d:
            print(' [-] Start date must come before end date')
            res = True
    return res


def download_data(stock, s_date, e_date):
    """Downloads daily pricing data for stock,
       between s_date and e_date"""

    ticker = Share(stock)
    return ticker.get_historical(s_date, e_date)


def main(ticker, start_date, end_date):
    """Wraps download data and iterates over a list
    of ticker symbols and downloads data for each of them"""

    if check_args(start_date, end_date):
        return []

    rows = download_data(ticker, start_date, end_date)

    # Remove the symbol entry in the dictionary
    for row in rows:
        del row['Symbol']

    return rows
