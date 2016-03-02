# mysqldump -t --skip-extended-insert -u root -p portmgr > inserts.sql
from common import sqlite_manager as db_manager

cm = db_manager.CredentialManager(name='data/cache.db')
db = db_manager.DatabaseAccess(cm)
with open('inserts.sql', 'r') as f:
    for line in f.readlines():
        if line.startswith('INSERT INTO'):
            db.execute(line)

