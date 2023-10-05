
from db.run import cur,db


async def add_click(btn_name):

    current_stat=cur.execute(f"SELECT click_count FROM click_stat WHERE btn_name='{btn_name}' and click_date=strftime('%Y-%m-%d', 'now')").fetchone()

    if current_stat:
        times_clicked=current_stat[0]+1
        cur.execute(f"UPDATE click_stat SET click_count={times_clicked} WHERE btn_name='{btn_name}' AND click_date=strftime('%Y-%m-%d', 'now')")
    else:
        cur.execute(f"INSERT INTO click_stat (btn_name,click_count,click_date) VALUES ('{btn_name}',1,strftime('%Y-%m-%d', 'now'))")

    db.commit()




# async def get_clicks(btn_name):
#     query = f"""
#         SELECT
#             COALESCE(t1.click_count, 0) AS date0,
#             COALESCE(t2.click_count, 0) AS date1,
#             COALESCE(t3.click_count, 0) AS date7,
#             COALESCE(t4.click_count, 0) AS date30
#         FROM
#             (SELECT SUM(click_count) AS click_count FROM click_stat
#             WHERE btn_name='{btn_name}') t1
#         LEFT JOIN
#             (SELECT SUM(click_count) AS click_count FROM click_stat
#             WHERE btn_name='{btn_name}' AND DATETIME(click_date) BETWEEN DATETIME('now', '-1 day') AND DATETIME('now')) t2
#         ON 1=1
#         LEFT JOIN
#             (SELECT SUM(click_count) AS click_count FROM click_stat
#             WHERE btn_name='{btn_name}' AND DATETIME(click_date) BETWEEN DATETIME('now', '-7 day') AND DATETIME('now')) t3
#         ON 1=1
#         LEFT JOIN
#             (SELECT SUM(click_count) AS click_count FROM click_stat
#             WHERE btn_name='{btn_name}' AND DATETIME(click_date) BETWEEN DATETIME('now', '-30 day') AND DATETIME('now')) t4
#         ON 1=1
#     """
#     data = cur.execute(query).fetchone()
#     db.commit()
#     click_count={
#         "day":data[1],
#         "week":data[2],
#         "month":data[3],
#         "all_time":data[0]
#     }
#
#
#     return click_count