import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER UNIQUE, phone_number TEXT DEFAULT null,fullname TEXT,is_active INTEGER DEFAULT 1)")
    cur.execute("CREATE TABLE IF NOT EXISTS treatments(id INTEGER PRIMARY KEY AUTOINCREMENT,tg_id INTEGER, service_type TEXT,consult_type TEXT,treatment_date TEXT,custom_text TEXT DEFAULT null)")
    cur.execute("CREATE TABLE IF NOT EXISTS click_stat(id INTEGER PRIMARY KEY AUTOINCREMENT, btn_name TEXT, click_count INT, click_date TEXT, CONSTRAINT unique_button_date UNIQUE (btn_name, click_date))")
    db.commit()

