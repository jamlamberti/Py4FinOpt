"""A is-it-up test for YF"""
import yahoo_finance as yf


def test_yahoo_finance():
    """A simple smoke test"""
    share = yf.Share('AAPL')
    assert len(share.get_historical('2015-01-01', '2016-01-01')) > 0
