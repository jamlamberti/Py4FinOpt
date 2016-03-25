"""A set of test cases for common"""
from __future__ import print_function
from common import credential_manager


def test_sqlite_connection():
    """A simple smoke test"""
    import os
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
