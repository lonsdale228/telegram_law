from db.run import cur,db


async def add_user(tg_id:int,fullname:str,is_active:int=1):
    cur.execute(f"INSERT INTO users (tg_id,fullname,is_active) VALUES ({tg_id},'{fullname}',{is_active})")
    db.commit()