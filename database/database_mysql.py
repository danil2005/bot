from datetime import datetime
from config_data.config import config
import pymysql

# Подключение к базе данных MySQL
def get_db_connection():
    return pymysql.connect(
        host=config.data_base.host,
        user=config.data_base.user,
        password=config.data_base.password,
        database=config.data_base.name_db
    )

def check_db ():
    config_db = {
        'host': config.data_base.host,
        'user': config.data_base.user,
        'password': config.data_base.password,
    }

    with pymysql.connect(**config_db) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{config.data_base.name_db}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(f"CREATE DATABASE {config.data_base.name_db}")
            else:
                return
            
        conn.select_db(config.data_base.name_db)

        with open('create_tables_mysql.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        sql_commands = sql_script.split(';')

        with conn.cursor() as cursor:
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            
def add_questionnaire_db(data: dict):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           INSERT INTO Users
                           VALUES (%s, %s, %s, %s, %s, %s)''',
                           tuple(data.values()))
            conn.commit()

def check_name_workout(id: int, name: str) -> bool:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT * FROM Workout_types
                           WHERE id_user = %s AND name = %s''',
                           (id, name))
            rows = cursor.fetchall()
            conn.commit()
    return bool(rows)

def add_new_workout(id: int, name: str):
    if check_name_workout(id, name):
        return False
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           INSERT INTO Workout_types (id_user, name, is_active)
                           VALUES (%s, %s, %s)''',
                           (id, name, True))
            conn.commit()
    return True

def get_active_workouts(id: int) -> tuple:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT id, name FROM Workout_types
                           WHERE id_user = %s AND is_active = 1''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows

def get_deactive_workouts(id: int) -> tuple:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT id, name FROM Workout_types
                           WHERE id_user = %s AND is_active = 0''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows

def get_all_workouts(id: int) -> tuple:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT id, name FROM Workout_types
                           WHERE id_user = %s''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows

def deactive_workout(workout: str):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           UPDATE Workout_types SET is_active = 0
                           WHERE id = %s''',
                           (int(workout),))
            conn.commit()

def active_workout(workout: str):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           UPDATE Workout_types SET is_active = 1
                           WHERE id = %s''',
                           (int(workout),))
            conn.commit()

def delete_workout(workout: str):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           DELETE FROM Workout_types
                           WHERE id = %s''',
                           (int(workout),))
            conn.commit()

def get_name_workout(id: int) -> str:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT name FROM Workout_types
                           WHERE id = %s''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows[0][0]  # Обращение по индексу

def check_name_exercise(id: int, name: str) -> bool:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT * FROM Exercise_types
                           WHERE id_user = %s AND name = %s''',
                           (id, name))
            rows = cursor.fetchall()
            conn.commit()
    return bool(rows)

def add_new_exercise(id: int, name: str):
    if check_name_exercise(id, name):
        return False
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           INSERT INTO Exercise_types (id_user, name)
                           VALUES (%s, %s)''',
                           (id, name))
            last_id = cursor.lastrowid
            conn.commit()
    return last_id

def get_name_exercise(id: int) -> str:
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT name FROM Exercise_types
                           WHERE id = %s''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows[0][0]  # Обращение по индексу

def start_workout(id_user, id_type):
    # Получаем текущую дату и время
    date = datetime.today().strftime("%Y-%m-%d")  # Формат YYYY-MM-DD
    start = datetime.now().strftime("%H:%M:%S")   # Формат времени HH:MM:SS

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Вставляем данные в таблицу Workouts
            cursor.execute('''
                INSERT INTO Workouts (id_user, id_type, date, start)
                VALUES (%s, %s, %s, %s)''',
                (id_user, id_type, date, start))
            
            # Получаем ID последней вставленной записи
            last_id = cursor.lastrowid
            conn.commit()  # Фиксируем изменения в базе данных
    
    return last_id

def start_exercise(exercise_type, workout):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           INSERT INTO Exercises (id_type, id_workout, weight)
                           VALUES (%s, %s, "")''',
                           (exercise_type, workout))
            last_id = cursor.lastrowid
            conn.commit()
    return last_id

def get_weight_workout(id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT Exercise_types.name, Exercises.weight, Exercises.id
                           FROM Exercises
                           INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                           WHERE Exercises.id_workout = %s
                           ORDER BY Exercises.id ASC''',
                           (id,))
            rows = cursor.fetchall()
            conn.commit()
    return rows

def end_workout(workout_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT date, start FROM Workouts
                           WHERE id = %s''',
                           (workout_id,))
            rows = cursor.fetchall()

    # date_start = datetime.strptime(rows[0][0], "%Y-%m-%d").date()  # Обращение по индексу
    # time_start = datetime.strptime(rows[0][1], "%H:%M:%S").time()  # Обращение по индексу
    # start = datetime.combine(date_start, time_start)

    start = datetime.combine(rows[0][0], datetime.min.time()) + rows[0][1]

    end = datetime.now()
    duration = (end - start).total_seconds() // 60
    end_str = end.strftime("%H:%M:%S")

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           UPDATE Workouts SET end = %s, duration = %s
                           WHERE id = %s''',
                           (end_str, duration, workout_id))
            conn.commit()

def get_workout_exercises(type_workout: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT id
                           FROM Workouts
                           WHERE id_type = %s AND end IS NOT NULL
                           ORDER BY id DESC
                           LIMIT 1''',
                           (type_workout,))
            rows = cursor.fetchall()

    if not rows:
        return []

    id_workout = rows[0][0]  # Обращение по индексу

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT Exercises.id_type, Exercise_types.name
                           FROM Exercises
                           INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                           WHERE Exercises.id_workout = %s''',
                           (id_workout,))
            rows = cursor.fetchall()

    result = [(str(row[0]), row[1]) for row in rows]  # Обращение по индексу
    return result

def get_latest_workout_ids(type_workout: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT id
                           FROM Workouts
                           WHERE id_type = %s
                           ORDER BY id DESC
                           LIMIT 3''',
                           (type_workout,))
            rows = cursor.fetchall()
    return [row[0] for row in rows]  # Обращение по индексу

def get_date_workout(workout_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT date FROM Workouts
                           WHERE id = %s''',
                           (workout_id,))
            rows = cursor.fetchall()
    return rows[0][0].strftime("%d-%m-%Y")  # Обращение по индексу


def update_exercise(id_exercise, weight):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT weight FROM Exercises
                           WHERE id = %s''',
                           (id_exercise,))
            rows = cursor.fetchall()

    if not rows[0][0]:  # Обращение по индексу
        old_weight = []
    else:
        old_weight = rows[0][0].split(' | ')  # Обращение по индексу

    old_weight.append(weight)
    text_weight = ' | '.join(old_weight)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           UPDATE Exercises SET weight = %s
                           WHERE id = %s''',
                           (text_weight, id_exercise))
            conn.commit()

def get_all_exercises(chat_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT Exercise_types.id, Exercise_types.name
                           FROM Exercise_types
                           WHERE Exercise_types.id_user = %s''',
                           (chat_id,))
            rows = cursor.fetchall()

    result = [(str(row[0]), row[1]) for row in rows]  # Обращение по индексу
    return result

def get_info_workout(workout_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT date, start, duration, id_type FROM Workouts
                           WHERE id = %s''',
                           (workout_id,))
            row = cursor.fetchone()
    return row

def get_history(exercise_type: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT Workout_types.name, Workouts.date, Workouts.start, Exercises.weight
                           FROM Exercises
                           JOIN Workouts ON Exercises.id_workout = Workouts.id
                           JOIN Workout_types ON Workouts.id_type = Workout_types.id
                           WHERE Exercises.id_type = %s
                           LIMIT 5''',
                           (exercise_type,))
            rows = cursor.fetchall()
    return rows

def delete_exercise(exercise: int):
    exerecise_del = get_type_exercise(exercise)
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           DELETE FROM Exercises
                           WHERE id = %s''',
                           (int(exercise),))
            conn.commit()
    
    return exerecise_del

def get_type_exercise(id_exercise:int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           SELECT Exercises.id_type, Exercise_types.name
                           FROM Exercises
                           INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                           WHERE Exercises.id = %s''',
                           (id_exercise,))
            row = cursor.fetchone()
    return row
            