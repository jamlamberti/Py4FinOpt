"""
The data_handler module handles mixing data stored in a local cache
 with the data we fetch from yahoo finance
It uses the config file to decided which cache implementation
 to use (e.g. MySQL, sqlite3)
"""

from __future__ import print_function
import datetime

from common import config, errors, credential_manager
from . import downloader

CACHE_CONFIG = config.Section('cache')
DB_CONFIG = None

from common.db_manager import *

TIME_FMT = '%Y-%m-%d'

# Just doing some overloading of private built-ins
# pylint: disable=too-few-public-methods


class MemoizedTable(object):

    """
    A class for wrapping a function with memoization
    - memoization leverages a database implementation
    """

    def __init__(self, table, use_cache=True):
        self.use_cache = use_cache
        cred_mgr = credential_manager.CredentialManager(
            host=DB_CONFIG.get('db_host'),
            user=DB_CONFIG.get('username'),
            passwd=DB_CONFIG.get('passwd'),
            name=DB_CONFIG.get('db_name'),
        )
        self.db_access = db_mgr.DatabaseAccess(cred_mgr)
        self.db_access.connect()
        self.table = table

    def __call__(self, func, *args, **kargs):
        def new_func(*args):
            """
            Checks cache for a prior call, returns it
            if found o.w. looks up and writes back
            """
            res = None
            if self.use_cache:
                try:
                    res = self.__check_cache(args)
                    print("Found in cache!!!")
                except errors.CacheMiss:
                    print("Cache Miss..."
                          " be patient as we populate the database")
                    res = func(*args)
                    self.__write_cache(res, args)
            else:
                res = func(*args)
            return res
        return new_func

    def __check_cache(self, args):
        """
        Check the sql table for a cache hit,
        raise cache miss execption if not in cache
        """
        try:
            sql = "SELECT ticker, timestamp, open, " \
                "high, low, close, volume, adjclose from " \
                + self.table \
                + " where ticker = ? and" \
                " timestamp >= ? and timestamp <= ?"
            res = self.db_access.execute_all(sql, *args)
            data = []
            for row in res:
                temp = {}
                try:
                    temp['Date'] = row[1].strftime(TIME_FMT)
                except AttributeError:
                    # SQLite doesn't return datetimes as a
                    # datetime object but rather a string
                    temp['Date'] = row[1]

                temp['Open'] = row[2]
                temp['High'] = row[3]
                temp['Low'] = row[4]
                temp['Close'] = row[5]
                temp['Volume'] = row[6]
                temp['Adj_Close'] = row[7]
                data.append(temp)
            if len(data) == 0:
                raise errors.CacheMiss()
            return data

        except Exception as err:
            print(err)
            raise errors.CacheMiss()

    def __write_cache(self, res, args):
        """
        Write the result of the function back to the
        cache
        """
        ticker = args[0]
        for row in res:
            sql = "INSERT into " \
                + self.table \
                + " VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?);"
            sqlarg = (
                ticker,
                row['Date'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'],
                row['Adj_Close'])

            self.db_access.execute_all(sql, *sqlarg)


@MemoizedTable(table='dailyCacheStocks')
def get_data(ticker, start_date, end_date):
    """
    A memoized function which queries a ticker for daily
    historical data between start_date and end_date
    """
    return downloader.main(ticker, start_date, end_date)


def convert_to_weekly(data):
    """
    Utility function for converting daily data to weekly
    """
    data = sorted(
        data,
        key=lambda row: datetime.datetime.strptime(row['Date'], TIME_FMT))
    weeks = {}
    for row in data:
        d_temp = datetime.datetime.strptime(row['Date'], TIME_FMT)
        d_start = d_temp - datetime.timedelta(d_temp.weekday())
        d_start = d_start.strftime(TIME_FMT)
        if d_start not in weeks:
            weeks[d_start] = row
            weeks[d_start]['Volume'] = [row['Volume']]
        else:
            weeks[d_start]['Volume'].append(row['Volume'])
            weeks[d_start]['Close'] = row['Close']
            weeks[d_start]['Adj_Close'] = row['Adj_Close']
            if float(weeks[d_start]['High']) < float(row['High']):
                weeks[d_start]['High'] = row['High']
            if float(weeks[d_start]['Low']) > float(row['Low']):
                weeks[d_start]['Low'] = row['Low']
    rows = []
    for val in weeks.values():
        v_vol = sum([int(x) for x in val['Volume']]) / len(val['Volume'])
        val['Volume'] = v_vol
        rows.append(val)
    return rows


def convert_to_monthly(data):
    """
    Utility function for converting daily data to monthly
    """
    data = sorted(
        data,
        key=lambda row: datetime.datetime.strptime(row['Date'], TIME_FMT))

    months = {}
    for row in data:
        d_temp = datetime.datetime.strptime(row['Date'], TIME_FMT)
        d_start = d_temp.strftime('%Y-%m')
        if d_start not in months:
            months[d_start] = row
            months[d_start]['Volume'] = [row['Volume']]
        else:
            months[d_start]['Volume'].append(row['Volume'])
            months[d_start]['Close'] = row['Close']
            months[d_start]['Adj_Close'] = row['Adj_Close']
            if float(months[d_start]['High']) < float(row['High']):
                months[d_start]['High'] = row['High']
            if float(months[d_start]['Low']) > float(row['Low']):
                months[d_start]['Low'] = row['Low']
    rows = []
    for val in months.values():
        v_vol = sum([int(x) for x in val['Volume']]) / len(val['Volume'])
        val['Volume'] = v_vol
        rows.append(val)
    return rows


def convert_to_daily(data):
    """
    Stub for consistency
        - see convert_to_weekly and convert_to_monthly
    """
    return data


def main(tickers, start_date, end_date, freq='daily'):
    """
    Fetches historical data for a list of tickers
     from start_date to end_date
    Data frequency can be specified in the freq optional
     parameter (either daily, weekly or monthly)
    """
    data = {}
    freqs = {
        'daily': convert_to_daily,
        'weekly': convert_to_weekly,
        'monthly': convert_to_monthly
    }

    if freq not in freqs:
        raise errors.InvalidParameterValue(
            "freq must be one of the following: %s" %
            ", ".join(freqs.keys()))

    for ticker in set(tickers):
        data[ticker] = freqs[freq](get_data(ticker, start_date, end_date))
    return data
