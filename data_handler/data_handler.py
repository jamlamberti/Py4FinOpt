import functools
import downloader

from common import config, db_manager, memoize


class MemoizedTable(object):
    def __init__(self, table, use_cache=True):
        mysql_config = config.Section('mysql')
        #self.func = func
        self.use_cache = use_cache

        cm = db_manager.CredentialManager(
            host = mysql_config.get('db_host'),
            user = mysql_config.get('username'),
            passwd = mysql_config.get('passwd'),
            name = mysql_config.get('db_name'),
        )
        self.db = db_manager.DatabaseAccess(cm)
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
                temp['Date']  = row[1].strftime('%Y-%m-%d')
                temp['Open']  = row[2]
                temp['High']  = row[3]
                temp['Low']   = row[4]
                temp['Close'] = row[5]
                temp['Volume'] = row[6]
                temp['Adj_Close'] = row[7]
                data.append(temp)
            if len(data) == 0:
                raise memoize.CacheMiss()
            return data
        except:
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

def main(tickers, start_date, end_date):
    data = {}
    for ticker in set(tickers):
        data[ticker] = get_data(ticker, start_date, end_date)
    return data

if __name__ == '__main__':
    print main(['YHOO'], '2016-02-01', '2016-02-15')
