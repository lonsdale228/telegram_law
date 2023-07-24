from db.run import cur,db




async def add_treatment(tg_id:int,service_type,consult_type,treatment_date="",custom_text=""):
    cur.execute(f"INSERT INTO treatments(tg_id, service_type, consult_type, treatment_date, custom_text) VALUES({tg_id}, '{service_type}', '{consult_type}', strftime('%s','now') , '{custom_text}');")
    db.commit()
    #strftime('%s','now')