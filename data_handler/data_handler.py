import functools
import downloader
import datetime
from common import config, memoize
cache_config = config.Section('cache')
db_config = None
if cache_config.get('cache-impl') == 'mysql':
    try:
        from common import db_manager as db_mgr
        db_config = config.Section('mysql')

    except:
        from common import sqlite_manager as db_mgr
        db_config = config.Section('sqlite')
else:
    from common import sqlite_manager as db_mgr
    db_config = config.Section('sqlite')

TIME_FMT = '%Y-%m-%d'

class MemoizedTable(object):
    def __init__(self, table, use_cache=True):
        self.use_cache = use_cache
        cm = db_mgr.CredentialManager(
            host = db_config.get('db_host'),
            user = db_config.get('username'),
            passwd = db_config.get('passwd'),
            name = db_config.get('db_name'),
        )
        self.db = db_mgr.DatabaseAccess(cm)
        self.db.connect()
        self.table = table
            

    def __call__(self, func, *args, **kargs):
        def new_func(*args, **kargs):
            res = None
            if self.use_cache:
                try:
                    res = self.__check_cache(args)
                    print("Found in cache!!!")
                except memoize.CacheMiss, e:
                    print("Cache Miss... be patient as we populate the database")
                    res = func(*args)
                    self.__write_cache(res, args)
            else:
                res = func(*args)
            return res
        return new_func

    def __check_cache(self, args):
        try:
            sql = "SELECT ticker, timestamp, open, high, low, close, volume, adjclose from " + self.table + " where ticker = '%s' and timestamp >= '%s' and timestamp <= '%s'"
            res = self.db.execute_all(sql%args)
            data = []
            for row in res:
                temp = {}
                try:
                    temp['Date']  = row[1].strftime('%Y-%m-%d')
                except:
                    # SQLite doesn't return datetimes as a datetime object but rather a string
                    temp['Date'] = row[1]
                temp['Open']  = row[2]
                temp['High']  = row[3]
                temp['Low']   = row[4]
                temp['Close'] = row[5]
                temp['Volume'] = row[6]
                temp['Adj_Close'] = row[7]
                data.append(temp)
            if len(data) == 0:
                print "here"
                raise memoize.CacheMiss()
            return data
        except Exception, e:
            print(e)
            raise memoize.CacheMiss()

    def __write_cache(self, res, args):
        ticker = args[0]
        for row in res:
            sql = "INSERT into " + self.table + " VALUES (null, '%s', '%s', %s, %s, %s, %s, %s, %s);"
            sqlarg = (ticker, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Adj_Close'])
            self.db.execute_all(sql%sqlarg)

@MemoizedTable(table='dailyCacheStocks')
def get_data(ticker, start_date, end_date):
    return downloader.main(ticker, start_date, end_date)

def convert_to_weekly(data):
    data = sorted(data, key=lambda row: datetime.datetime.strptime(row['Date'], TIME_FMT))
    weeks = {}
    for row in data:
        d = datetime.datetime.strptime(row['Date'], TIME_FMT)
        d_start = d-datetime.timedelta(d.weekday())
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
    for k,v in weeks.items():
        v_vol = sum(map(int, v['Volume']))/len(v['Volume'])
        v['Volume'] = v_vol
        rows.append(v)
    return rows


def convert_to_monthly(data):
    data = sorted(data, key=lambda row: datetime.datetime.strptime(row['Date'], TIME_FMT))
    months = {}
    for row in data:
        d = datetime.datetime.strptime(row['Date'], TIME_FMT)
        d_start = d.strftime('%Y-%m')
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
    for k,v in months.items():
        v_vol = sum(map(int, v['Volume']))/len(v['Volume'])
        v['Volume'] = v_vol
        rows.append(v)
    return rows


def convert_to_daily(data):
    return data


def main(tickers, start_date, end_date, freq='daily'):
    data = {}
    freqs = {
        'daily': convert_to_daily,
        'weekly': convert_to_weekly,
        'monthly': convert_to_monthly
    }
    if freq not in freqs:
        print "Unknown frequency, defaulting to daily"
        freq = daily

    for ticker in set(tickers):
        data[ticker] = freqs[freq](get_data(ticker, start_date, end_date))
    return data

if __name__ == '__main__':
    print main(['YHOO'], '2016-02-01', '2016-02-15')
