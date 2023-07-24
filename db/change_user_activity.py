from db.run import cur,db

async def change_activity(tg_id,is_active:int=0):
    cur.execute(f"UPDATE users SET is_active = {is_active} WHERE tg_id='{tg_id}'")
    db.commit()