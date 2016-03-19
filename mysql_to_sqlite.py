"""Takes a mysql dump and converts it into a sqlite3 db"""
# Run this command
# mysqldump -t --skip-extended-insert -u root -p pyfinopt > inserts.sql
from common import sqlite_manager as db_manager

def converter(mysql_dump='inserts.sql', sqlite_db='data/cache.db'):
    """Converts a MySQL export to a sqlite3 db
        - mysql_dump - Mysql dump file
        - sqlite_db  - Output db"""

    cred_mgr = db_manager.CredentialManager(name=sqlite_db)
    db_conn = db_manager.DatabaseAccess(cred_mgr)

    with open(mysql_dump, 'r') as f_handler:
        for line in f_handler.readlines():
            if line.startswith('INSERT INTO'):
                db_conn.execute(line)

    db_conn.close()

if __name__ == '__main__':
    converter()
