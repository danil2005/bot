import sqlite3

def add_questionnaire_db(data: dict):
    d = data.values()
    d = tuple(d)
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO users
                       VALUES (?,?,?,?,?,?)''',
                       d)
        conn.commit()
