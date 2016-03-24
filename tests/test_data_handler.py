"""Tests for the data_handler component"""
from data_handler import downloader, data_handler

def test_downloader():
    """Check if we can download data correctly"""
    # Invalid stock test
    res = downloader.main('refhurwefhurwefhwe', '2006-02-12', '2016-02-12')
    assert len(res) == 0

    # Invalid start date, passing in as int
    res = downloader.main('WMT', 2006, '2016-02-12')
    assert len(res) == 0

    # Invalid end date, passing in too large a month
    res = downloader.main('WMT', '2006-02-12', '2016-32-12')
    assert len(res) == 0

    # Valid case
    res = downloader.main('WMT', '2006-02-12', '2016-02-12')
    assert len(res) > 0


def test_fetch_data():
    """Test fetching and the cache"""
    daily = data_handler.main(['WMT'], \
            '2006-02-12', '2016-02-12', freq='daily')
    assert len(daily['WMT']) > 0

    weekly = data_handler.main(['WMT'], \
            '2006-02-12', '2016-02-12', freq='weekly')
    assert len(weekly) > 0 and len(weekly['WMT']) > 0
    assert len(weekly['WMT']) < len(daily['WMT'])

    monthly = data_handler.main(['WMT'], \
            '2006-02-12', '2016-02-12', freq='monthly')
    assert len(monthly) > 0 and len(monthly['WMT']) > 0
    assert len(monthly['WMT']) < len(weekly['WMT'])

    # Make sure TSLA isn't in the db
    daily = data_handler.main(['TSLA'], \
            '2016-01-12', '2016-02-12', freq='daily')
    assert len(daily) > 0 and len(daily['TSLA']) > 0
