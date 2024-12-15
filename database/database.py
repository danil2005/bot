import sqlite3

def add_questionnaire_db(data: dict):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Users
                       VALUES (?,?,?,?,?,?)''',
                       tuple(data.values()))
        conn.commit()

def check_name_workout(id: int, name: str) -> bool:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT * FROM Workout_types
                       WHERE id_user = ? AND name = ?''',
                       (id, name))
        rows = cursor.fetchall()
        conn.commit()
    return bool(rows)

def add_new_workout (id: int, name: str):
    if check_name_workout(id, name):
        return False
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Workout_types (id_user, name, is_active)
                       VALUES (?,?,?)''',
                       (id, name, True))
        conn.commit()
    return True
    
def get_active_workout(id: int) -> tuple:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ? AND is_active = 1''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows
    


