import sqlite3
from datetime import datetime, timezone
import random

db_path = "../filmsBot/db.sqlite3"

def get_film_by_code_from_db(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_film WHERE id=?"
    cursor.execute(sql, [(id)])
    result = cursor.fetchone()
    conn.close()
    return result

def get_random_film_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_film ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    return result

def initiate_user_start(user, chat_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql_verify = "SELECT * from bot_admin_botuser WHERE user_id=?"
    username = user.username
    if username == None:
        username = 'NoInfo'
    cursor.execute(sql_verify, [(user.id)])
    print(cursor.fetchone())
    if cursor.fetchone() == None:
        datas = [user.id, username, datetime.now(timezone.utc), '', datetime.now(timezone.utc), chat_id]
        sql = "INSERT INTO bot_admin_botuser (user_id, nickname, date_started, phone_number, last_day_active, chat_id) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, datas)
        conn.commit()
    conn.close()
    

def update_last_day_active(id, chat_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    datas = [datetime.now(timezone.utc), chat_id, id]
    sql = "UPDATE bot_admin_botuser SET last_day_active = ?, chat_id = ? WHERE user_id = ?"
    cursor.execute(sql, datas)
    conn.commit()
    conn.close()

def get_all_genres():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * from bot_admin_genre"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

def get_random_film_by_genre_from_db(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_genre WHERE name=?"
    cursor.execute(sql, [(name)])
    id = cursor.fetchone()[0]
    sql = "SELECT * FROM bot_admin_film_genre WHERE genre_id=?"
    cursor.execute(sql, [(id)])
    films = cursor.fetchall()
    film = random.choice(films)
    sql = "SELECT * FROM bot_admin_film WHERE id=?"
    cursor.execute(sql, [(film[1])])
    result = cursor.fetchone()
    conn.close()
    return result

def get_random_ad_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_ad ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    return result

def get_last_ad_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_ad ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    return result

def get_film_by_name(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM bot_admin_film WHERE name like  '%'||?||'%';"
    cursor.execute(sql, [(name)])
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_users():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "SELECT DISTINCT user_id FROM bot_admin_botuser"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result