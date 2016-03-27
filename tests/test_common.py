"""A set of test cases for common"""
from __future__ import print_function
import os
from common import credential_manager, dependency_planning


def test_sqlite_connection():
    """A simple smoke test"""
    from common import sqlite_manager
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

def test_case():
    """A simple smoke test"""
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
