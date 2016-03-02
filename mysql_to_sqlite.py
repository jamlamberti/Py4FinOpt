# mysqldump -t --skip-extended-insert -u root -p portmgr > inserts.sql

import sqlite3
db = sqlite3.connect('data/cache.db')
c = db.cursor()
with open('inserts.sql', 'r') as f:
    for line in f.readlines():
        c.execute(line)

