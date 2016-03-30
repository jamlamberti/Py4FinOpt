# Seems to struggle on exception classes in MySQLdb
# pylint: disable=no-member
"""MySQL Database Access wrapper"""
from __future__ import print_function
import MySQLdb
from . import credential_manager


class DatabaseAccess(object):

    """Database access wrapper for MySQL"""

    def __init__(self, cred_manager):
        self.creds = cred_manager
        self.conn = None
        self.cursor = None
        self.lr_id = None

    def __connect(self):
        """Connect to db"""
        try:
            db = MySQLdb.connect(
                host=self.creds.db_host,
                port=self.creds.port,
                user=self.creds.db_user,
                passwd=self.creds.db_pass,
                db=self.creds.db_name)

        except MySQLdb.Error as err:
            # Check if issue is due to an unknown db
            if err.args[0] == 1049:
                print(" [-] Error connecting to MySQL, try creating the DB?")
                raise
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
        """Close the connection and cursor if they are open"""
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None

            if self.conn is not None:
                # Make sure all the changes go through
                self.conn.commit()
                self.conn.close()
                self.conn = None
                print(" [+] Closed MySQLdb connection")

        except MySQLdb.OperationalError:
            print(" [-] DB connection already closed... maybe timeout?")

    def execute(self, sql, *args):
        """
        Execute a sql statement and fetch a single row
            use get_next_result to fetch subsequent rows
        """
        try:
            if self.cursor is None:
                self.close()
                self.connect()

            self.cursor.execute(sql, args)
            self.conn.commit()

        except MySQLdb.OperationalError:
            print("database connection went away, reconnecting...")
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()

        except MySQLdb.Error:
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
        """Execute a sql statement and return all rows"""
        try:
            if self.cursor is None:
                self.close()
                self.connect()
            self.cursor.execute(sql, args)
            self.conn.commit()
        except MySQLdb.OperationalError:
            print("database connection went away, reconnecting...")
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()
        except MySQLdb.OperationalError:
            self.conn.rollback()
            raise

        except:
            print(sql)
            print(args)
            raise

        rows = self.cursor.fetchall()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return rows


def test_connect():
    """A smoke test for both CredentialManager and DatabaseAccess"""
    from common import config
    mysql_config = config.Section('mysql')
    cred_mgr = credential_manager.CredentialManager(
        host=mysql_config.get('db_host'),
        user=mysql_config.get('username'),
        passwd=mysql_config.get('passwd'),
        name=mysql_config.get('db_name'),
    )
    dba = DatabaseAccess(cred_mgr)
    dba.connect()
    dba.close()

if __name__ == '__main__':
    test_connect()
