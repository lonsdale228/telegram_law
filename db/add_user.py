from db.run import cur,db


async def add_user(tg_id:int,fullname:str,is_active:int=1):
    query="INSERT INTO users (tg_id,fullname,is_active,start_date) VALUES (?,?,?, datetime('now'))"
    cur.execute(query,(tg_id,fullname,is_active))
    db.commit()


