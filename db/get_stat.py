import datetime

import pytz

from db.run import cur, db


async def local_to_utc(dt, tz_name='Europe/Kiev'):
    local_tz = pytz.timezone(tz_name)
    dt = local_tz.localize(dt)
    return dt.astimezone(pytz.utc)

async def utc_to_local(dt, tz_name='Europe/Kiev'):
    utc_dt = pytz.utc.localize(dt)
    local_tz = pytz.timezone(tz_name)
    return utc_dt.astimezone(local_tz)


async def get_click_stat(btn_name,time_period):
    if time_period!=0:
        start_date = await local_to_utc(datetime.datetime.now() - datetime.timedelta(days=time_period))
        # start_date = datetime.datetime.now() - datetime.timedelta(days=time_period)
        date_from = start_date.strftime('%Y-%m-%d %H:%M:%S')
        query="SELECT click_count FROM click_stat WHERE btn_name=? and DATETIME(click_date) BETWEEN DATETIME(?) AND DATETIME('now')"
        click_nums=cur.execute(query,(btn_name,date_from)).fetchall()
    else:
        query="SELECT click_count FROM click_stat WHERE btn_name=?"
        click_nums = cur.execute(query,(btn_name,)).fetchall()
    db.commit()
    total_clicks=0
    for click in click_nums:
        total_clicks+=click[0]
    return total_clicks

async def get_new_users(days_ago):
    if days_ago != 0:
        start_date = await local_to_utc(datetime.datetime.now() - datetime.timedelta(days=days_ago))
        # start_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        date_from = start_date.strftime('%Y-%m-%d %H:%M:%S')
        new_users = cur.execute(
            f"SELECT COUNT(*) FROM users WHERE DATETIME(start_date) BETWEEN DATETIME('{date_from}') AND DATETIME('now')").fetchall()
    else:
        new_users = cur.execute(f"SELECT COUNT(*) FROM users").fetchall()
    db.commit()
    total_users = 0
    for user in new_users:
        total_users += user[0]
    return total_users



async def get_treatments_from_day(days_ago):

    if days_ago!=0:
        start_date = await local_to_utc(datetime.datetime.now() - datetime.timedelta(days=days_ago))
        # start_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        date_from = start_date.strftime('%Y-%m-%d %H:%M:%S')
        click_nums=cur.execute(f"SELECT COUNT(*) FROM treatments WHERE DATETIME(treatment_date) BETWEEN DATETIME('{date_from}') AND DATETIME('now')").fetchall()
    else:
        click_nums=cur.execute(f"SELECT COUNT(*) FROM treatments").fetchall()
    db.commit()
    total_clicks=0
    for click in click_nums:
        total_clicks+=click[0]
    return total_clicks