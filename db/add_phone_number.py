from db.run import cur,db

async def add_phone(tg_id,phone_number):
    query="UPDATE users SET phone_number = ? WHERE tg_id=?"
    cur.execute(query,(phone_number,tg_id))
    db.commit()