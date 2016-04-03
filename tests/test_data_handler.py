"""Tests for the data_handler component"""
import pytest


def test_downloader():
    """Check if we can download data correctly"""
    from data_handler import downloader
    # Invalid stock test
    res = downloader.main('refhurwefhurwefhwe', '2006-02-12', '2016-02-12')
    assert len(res) == 0

    # Invalid start date, passing in as int
    res = downloader.main('WMT', 2006, '2016-02-12')
    assert len(res) == 0

    # Invalid end date, passing in too large a month
    res = downloader.main('WMT', '2006-02-12', '2016-32-12')
    assert len(res) == 0

    # Start date comes after end date
    res = downloader.main('WMT', '2016-02-12', '2016-02-12')
    assert len(res) == 0

    # Valid case
    res = downloader.main('WMT', '2006-02-12', '2016-02-12')
    assert len(res) > 0


def test_fetch_data():
    """Test fetching and the cache"""
    from common import errors
    from data_handler import data_handler
    daily = data_handler.main(['WMT'],
                              '2006-02-12', '2016-02-12', freq='daily')
    assert len(daily) > 0 and len(daily['WMT']) > 0

    # Invalid freq, should raise error
    with pytest.raises(errors.InvalidParameterValue):
        _ = data_handler.main(['WMT'],
                              '2006-02-12', '2016-02-12', freq='asdf')

    weekly = data_handler.main(['WMT'],
                               '2006-02-12', '2016-02-12', freq='weekly')
    assert len(weekly) > 0 and len(weekly['WMT']) > 0
    assert len(weekly['WMT']) < len(daily['WMT'])

    monthly = data_handler.main(['WMT'],
                                '2006-02-12', '2016-02-12', freq='monthly')
    assert len(monthly) > 0 and len(monthly['WMT']) > 0
    assert len(monthly['WMT']) < len(weekly['WMT'])

    # Make sure TSLA isn't in the db
    daily = data_handler.main(['TSLA'],
                              '2016-01-12', '2016-02-12', freq='daily')
    assert len(daily) > 0 and len(daily['TSLA']) > 0


def test_memoizetable_no_cache():
    """Shut off caching and see what happens"""
    import timeit
    from data_handler import data_handler
    from data_handler import downloader

    @data_handler.MemoizedTable(table='dailyCacheStocks', use_cache=False)
    def get_data_without_cache(ticker, start_date, end_date):
        """Similar to get_data in data_handler, but with caching turned off"""
        return downloader.main(ticker, start_date, end_date)

    # Time the tsla lookup against the new version
    t_cache = timeit.default_timer()
    data_handler.get_data('WMT', '2006-02-12', '2016-02-12')
    t_cache = timeit.default_timer() - t_cache

    t_no_cache = timeit.default_timer()
    get_data_without_cache('WMT', '2006-02-12', '2016-02-12')
    t_no_cache = timeit.default_timer() - t_no_cache

    assert t_cache < t_no_cache
