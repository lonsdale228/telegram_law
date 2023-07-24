from db.run import cur,db


async def get_user(tg_id:int):
    user=cur.execute(f"SELECT tg_id FROM USERS WHERE tg_id={tg_id}").fetchall()
    db.commit()
    return user



async def get_all_users():
    users=cur.execute("SELECT tg_id FROM USERS").fetchall()
    db.commit()
    return users