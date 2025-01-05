import sqlite3
from datetime import date, time, datetime

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
    
def get_active_workouts(id: int) -> tuple:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ? AND is_active = 1''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows

def get_deactive_workouts(id: int) -> tuple:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ? AND is_active = 0''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows

def get_all_workouts(id: int) -> tuple:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ?''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows

def deactive_workout(workout: str):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE Workout_types SET is_active = 0
                       WHERE id = ?''',
                       (int(workout), ))
        conn.commit()

def active_workout(workout: str):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE Workout_types SET is_active = 1
                       WHERE id = ?''',
                       (int(workout), ))
        conn.commit()

def delite_workout(workout: str):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       DELETE FROM Workout_types
                       WHERE id = ?''',
                       (int(workout), ))
        conn.commit()

def get_name_workout(id: int) -> str:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT name FROM Workout_types
                       WHERE id = ?''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows[0][0]

def check_name_exercise(id: int, name: str) -> bool:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT * FROM Exercise_types
                       WHERE id_user = ? AND name = ?''',
                       (id, name))
        rows = cursor.fetchall()
        conn.commit()
    return bool(rows)

def add_new_exercise (id: int, name: str):
    if check_name_exercise(id, name):
        return False
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Exercise_types (id_user, name)
                       VALUES (?,?)''',
                       (id, name))
        last_id = cursor.lastrowid
        conn.commit()
    return last_id

def get_name_exercise(id: int) -> str:
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT name FROM Exercise_types
                       WHERE id = ?''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows[0][0]

def start_workout(id_user, id_type):
    data = datetime.today().strftime("%d-%m-%Y")
    start = datetime.now().strftime("%H:%M:%S")

    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Workouts (id_user, id_type, data, start)
                       VALUES (?,?,?,?)''',
                       (id_user, id_type, data, start))
        last_id = cursor.lastrowid
        conn.commit()
    return last_id

def end_exercise(exercise_type, workout, weight):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Exercises (id_type, id_workout, weight)
                       VALUES (?,?,?)''',
                       (exercise_type, workout, ' | '.join(weight)))
        last_id = cursor.lastrowid
        conn.commit()
    return last_id

def get_weight_workout(id):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT Exercise_types.name, Exercises.weight 
                       FROM Exercises
                       INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                       WHERE Exercises.id_workout = ?''',
                       (id, ))
        rows = cursor.fetchall()
        conn.commit()
    return rows

def end_workout(workout_id: int):
    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT data, start FROM Workouts
                       WHERE id = ?''',
                       (workout_id, ))
        rows = cursor.fetchall()

    date_start = datetime.strptime(rows[0][0], "%d-%m-%Y").date()
    time_start = datetime.strptime(rows[0][1], "%H:%M:%S").time()
    start = datetime.combine(date_start, time_start)

    end = datetime.now()
    duration = (end-start).total_seconds()//60
    end_str = end.strftime("%H:%M:%S")

    with sqlite3.connect("bot_gym_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE Workouts SET end = ?, duration = ?
                       WHERE id = ?''',
                       (end_str, duration, workout_id))
        conn.commit()


