from db.run import cur,db


async def add_user(tg_id:int,fullname:str):
    cur.execute(f"INSERT INTO users (tg_id,fullname) VALUES ({tg_id},'{fullname}')")
    db.commit()