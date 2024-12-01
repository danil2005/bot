import sqlite3

def add_questionnaire(data: dict):
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
