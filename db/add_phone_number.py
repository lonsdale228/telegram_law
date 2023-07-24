from db.run import cur,db

async def add_phone(tg_id,phone_number):
    cur.execute(f"UPDATE users SET phone_number = '{phone_number}' WHERE tg_id='{tg_id}'")
    db.commit()