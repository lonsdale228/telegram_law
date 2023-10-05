
from db.run import cur,db




async def add_treatment(tg_id:int,service_type,consult_type,treatment_date="",custom_text=""):
    # cur.execute(f"INSERT INTO treatments(tg_id, service_type, consult_type, treatment_date, custom_text) VALUES({tg_id}, '{service_type}', '{consult_type}', datetime('now') , '{custom_text}');")
    query=(f"INSERT INTO treatments(tg_id, service_type, consult_type, treatment_date, custom_text) VALUES(?,?,?, datetime('now'), ?);")
    cur.execute(query,(tg_id,service_type,consult_type,custom_text))
    db.commit()


