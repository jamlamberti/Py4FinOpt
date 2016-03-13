import yahoo_finance as yf
s = yf.Share('AAPL')
assert len(s.get_historical('2015-01-01', '2016-01-01')) > 0
