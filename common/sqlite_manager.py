"""SQLite Database Wrapper"""
from __future__ import print_function
import sqlite3
import os
def init_database(db_access):
    """Create all the tables"""
    db_access.connect()
    db_access.execute("""
    CREATE TABLE IF NOT EXISTS `dailyCacheStocks`(
        `ROWID` integer primary key autoincrement,
        `ticker` VARCHAR(7) NOT NULL,
        `timestamp` DATE NOT NULL,
        `open` DOUBLE(8,2),
        `high` DOUBLE(8,2),
        `low` DOUBLE(8,2),
        `close` DOUBLE(8,2),
        `volume` INT(11) NOT NULL,
        `adjclose` DOUBLE(8,2),
        CONSTRAINT uc_ticker_tstamp UNIQUE (ticker, timestamp)
    );""")
    db_access.close()
    print(" [+] Initialized DB")

# TODO: Split me out into another file and convert to NamedTuple
class CredentialManager(object):
    """Creds for sqlite (e.g. filename)"""
    # pylint: disable=too-many-arguments, too-few-public-methods
    def __init__(
            self,
            host=None,
            user=None,
            passwd=None,
            name='example.db',
            port=3306):
        self.db_host = host
        self.db_user = user
        self.db_pass = passwd
        self.db_name = os.path.abspath(name)
        self.port = port

class DatabaseAccess(object):
    """Database Access Wrapper for SQLite3"""
    def __init__(self, cred_manager):
        self.creds = cred_manager
        self.conn = None
        self.cursor = None
        self.lr_id = None
        if not os.path.exists(self.creds.db_name):
            init_database(self)

    def __connect(self):
        """Low level connection"""
        db = sqlite3.connect(self.creds.db_name)
        return db

    def connect(self):
        """
        Connects to db
            will close connection and reopen if already connected
        """
        if self.conn is not None or self.cursor is not None:
            self.close()

        self.conn = self.__connect()
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the db connection if it is open"""
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None

            if self.conn is not None:
                # Make sure all the changes go through
                self.conn.commit()
                self.conn.close()
                self.conn = None
                print(" [+] Closed SQLite connection")

        except sqlite3.OperationalError as err:
            print(" [-] DB connection already closed... maybe timeout?")
            print(err)

    def execute(self, sql, *args):
        """
        Execute a SQL statement and fetch a single row
            use get_next_result to fetch subsequent rows
        """
        try:
            if self.cursor is None:
                self.close()
                self.connect()

            self.cursor.execute(sql, args)
            self.conn.commit()

        except sqlite3.OperationalError as err:
            print("database connection went away, reconnecting...")
            print(err)
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()

        except sqlite3.Error:
            self.conn.rollback()
            raise

        row = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return row

    def get_next_result(self):
        """Fetch the next row from a prior query"""
        row = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return row

    def execute_all(self, sql, *args):
        """Execute a SQL statement and fetch all of the rows"""
        try:
            if self.cursor is None:
                self.close()
                self.connect()
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.OperationalError, err:
            print("database connection went away, reconnecting...")
            print(err)
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

        rows = self.cursor.fetchall()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return rows

def test_connect():
    """A simple smoke test"""
    cred_mgr = CredentialManager(
        host=None,
        user=None,
        passwd=None,
        name='test.db',
    )
    db = DatabaseAccess(cred_mgr)
    db.connect()
    print(db.execute_all("SELECT * from sqlite_master where type='table'"))
    db.close()

if __name__ == '__main__':
    test_connect()
