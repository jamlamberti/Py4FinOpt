"""A set of test cases for common"""
from __future__ import print_function
import os
import pytest

# Used for tracking memoized code
CALL_CNT = 0


def test_sqlite_connection():
    """A simple smoke test"""
    from common import credential_manager, sqlite_manager
    cred_mgr = credential_manager.CredentialManager(
        host=None,
        user=None,
        passwd=None,
        name='test.db'
    )

    db = sqlite_manager.DatabaseAccess(cred_mgr)
    db.connect()
    print(db.execute_all("SELECT * from sqlite_master where type='table'"))
    db.close()
    assert 'test.db' in os.listdir('.')
    os.remove('test.db')


def test_dependency_planning():
    """A simple smoke test"""
    from common import dependency_planning
    depr = dependency_planning.DependencyResolver()
    depr.add_task('arithmetic mean')
    depr.add_task('geometric mean')
    depr.add_task('median')
    depr.add_task('quartiles')
    depr.add_task('standard deviation')
    depr.add_dep('downside standard deviation', 'arithmetic mean')
    depr.add_dep('MAD', 'arithmetic mean')
    depr.add_dep('sharpe ratio', 'standard deviation')
    depr.add_dep('sortino ratio', 'downside standard deviation')
    depr.visualize('out.png')
    assert 'out.png' in os.listdir('.')
    os.remove('out.png')

    depr.generate_solution('MAD')
    print(depr.sol)

    assert depr.validate_solution(depr.sol, [])
    assert not depr.validate_solution(['MAD'])
    assert depr.validate_solution([
        'arithmetic mean',
        'arithmetic mean',
        'MAD'])

    # Test circular
    depr.add_dep('arithmetic mean', 'MAD')
    with pytest.raises(Exception) as circular_excep:
        depr.generate_solution('MAD')
        assert 'Circular reference detected: ' in str(circular_excep)

    assert not depr.validate_solution(['arithmetic mean', 'MAD'])

    # Self-reference test
    depr.add_dep('median', 'median')
    assert not depr.validate_solution(['median'])


def test_config_section():
    """Run tests over the testing section of the config file"""
    from common import config
    test_config = config.Section('testing')
    str_test = test_config.get('s')
    assert str_test == 'abc'
    assert isinstance(str_test, str) or isinstance(str_test, unicode)

    int_test = test_config.getint('x')
    assert isinstance(int_test, int)
    assert int_test == 1

    float_test = test_config.getfloat('f')
    assert isinstance(float_test, float)
    assert float_test == -0.05

    true_test = test_config.getboolean('bt')
    assert true_test
    assert isinstance(true_test, bool)

    false_test = test_config.getboolean('bf')
    assert not false_test
    assert isinstance(false_test, bool)

    list_test = test_config.getlist('li')
    assert len(list_test) == 3
    assert isinstance(list_test, list)


def test_memoized():
    """Verify simple memoization code works"""
    from common import memoize

    global CALL_CNT  # pylint: disable=global-statement

    @memoize.MemoizedDict()
    def simple_test(arg):
        """Check if dict storage works"""
        global CALL_CNT  # pylint: disable=global-statement
        CALL_CNT += 1
        return 2 * arg

    for i in range(10):
        for _ in range(2):
            assert 2 * i == simple_test(i)
    assert CALL_CNT == 10
    CALL_CNT = 0

    @memoize.MemoizedDict(use_cache=False)
    def simple_test2(arg):
        """Check if we can shut off caching"""
        global CALL_CNT  # pylint: disable=global-statement
        CALL_CNT += 1
        return 2 * arg

    for i in range(10):
        for _ in range(2):
            assert 2 * i == simple_test2(i)
    assert CALL_CNT == 20
