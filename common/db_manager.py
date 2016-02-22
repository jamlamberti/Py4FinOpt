import MySQLdb

class CredentialManager(object):
    def __init__(
            self,
            host,
            user,
            passwd,
            name,
            port=3306):
        self.db_host = host
        self.db_user = user
        self.db_pass = passwd
        self.db_name = name
        self.port = port

class DatabaseAccess(object):
    def __init__(self, cred_manager):
        self.creds = cred_manager
        self.conn = None
        self.cursor = None

    def __connect(self):
        try:
            db = MySQLdb.connect(
                    host = self.creds.db_host,
                    port = self.creds.port,
                    user = self.creds.db_user,
                    passwd = self.creds.db_pass,
                    db = self.creds.db_name)
        except MySQLdb.Error, e:
            if e.args[0] == 1049: # Unknown DB
                print(" [-] Error connecting to MySQL, try creating the DB?")
                raise e
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
                print(" [+] Closed MySQLdb connection")

        except MySQLdb.OperationalError, e:
            print(" [-] DB connection already closed... maybe timeout?")

    def execute(self, sql, *args):
        try:
            if self.cursor is None:
                self.close()
                self.connect()

            self.cursor.execute(sql, args)
            self.conn.commit()

        except MySQLdb.OperationalError, e:
            print("database connection went away, reconnecting...")
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql,args)
            self.conn.commit()

        except MySQLdb.Error, ex:
            self.conn.rollback()
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
        except MySQLdb.OperationalError, e:
            print("database connection went away, reconnecting...")
            self.connect()
            print("Trying query again...")
            self.cursor.execute(sql, args)
            self.conn.commit()
        except MySQLdb.OperationalError, e:
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
    from common import config
    mysql_config = config.Section('mysql')
    cm = CredentialManager(
        host = mysql_config.get('db_host'),
        user = mysql_config.get('username'),
        passwd = mysql_config.get('passwd'),
        name = mysql_config.get('db_name'),
    )
    da = DatabaseAccess(cm)
    da.connect()
    da.close()

if __name__ == '__main__':
    test_connect()

