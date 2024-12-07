import sqlite3

def add_questionnaire_db(data: dict):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO users
                       VALUES (?,?,?,?,?,?)''',
                       tuple(data.values()))
        conn.commit()
