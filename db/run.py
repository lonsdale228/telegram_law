import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER UNIQUE, phone_number TEXT DEFAULT null,fullname TEXT,is_active INTEGER DEFAULT 1)")
    cur.execute("CREATE TABLE IF NOT EXISTS treatments(id INTEGER PRIMARY KEY AUTOINCREMENT,tg_id INTEGER, service_type TEXT,consult_type TEXT,treatment_date TEXT,custom_text TEXT DEFAULT null)")
    db.commit()

