import sqlite3
import os
def init_database(da):
    da.connect()
    da.execute("""
    CREATE TABLE IF NOT EXISTS `dailyCacheStocks`(
        `ROWID` INT NOT NULL,
        `ticker` VARCHAR(7) NOT NULL,
        `timestamp` DATE NOT NULL,
        `open` DOUBLE(8,2),
        `high` DOUBLE(8,2),
        `low` DOUBLE(8,2),
        `close` DOUBLE(8,2),
        `volume` INT(11) NOT NULL,
        `adjclose` DOUBLE(8,2),
        PRIMARY KEY(`ROWID`),
        CONSTRAINT uc_ticker_tstamp UNIQUE (ticker, timestamp)
    );""")
    da.close()
    print(" [+] Initialized DB")


class CredentialManager(object):
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
    def __init__(self, cred_manager):
        self.creds = cred_manager
        self.conn = None
        self.cursor = None
        if not os.path.exists(self.creds.db_name):
            init_database(self)

    def __connect(self):
        db = sqlite3.connect(self.creds.db_name)
        return db

    def connect(self):
        if self.conn is not None or self.cursor is not None:
            self.close()

        self.conn = self.__connect()
        self.cursor = self.conn.cursor()

    def close(self):
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

        except Exception, e:
            print(" [-] DB connection already closed... maybe timeout?")
            print(e)

    def execute(self, sql, *args):
        try:
            if self.cursor is None:
                self.close()
                self.connect()

            self.cursor.execute(sql, args)
            self.conn.commit()

        except sqlite3.OperationalError, e:
            print("database connection went away, reconnecting...")
            print(e)
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql,args)
            self.conn.commit()

        except sqlite3.OperationalError, e:
            self.conn.rollback()
            raise

        except:
            print(sql)
            print(args)
            raise

        r = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

    def get_next_result(self):
        r = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

    def execute_all(self, sql, *args):
        try:
            if self.cursor is None:
                self.close()
                self.connect()
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.OperationalError, e:
            print("database connection went away, reconnecting...")
            print(e)
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.OperationalError, e:
            self.conn.rollback()
            raise

        except:
            print(sql)
            print(args)
            raise
        
        r = self.cursor.fetchall()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

def test_connect():
    cm = CredentialManager(
        host = None,
        user = None,
        passwd = None,
        name = 'test.db',
    )
    da = DatabaseAccess(cm)
    da.connect()
    print da.execute_all("SELECT * from sqlite_master where type='table'")
    da.close()

if __name__ == '__main__':
    test_connect()

