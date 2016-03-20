"""A is-it-up test for YF"""
import yahoo_finance as yf

if __name__ == '__main__':
    # not going to make share a constant
    # pylint: disable=invalid-name
    share = yf.Share('AAPL')
    assert len(share.get_historical('2015-01-01', '2016-01-01')) > 0
