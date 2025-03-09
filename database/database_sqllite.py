import aiosqlite
import os
from datetime import datetime
from config_data.config import config

async def check_db():
    if not os.path.exists("bot_gym_db.db"):
        # Если файл не существует, создаем новую базу данных
        open("bot_gym_db.db", 'w').close()
    else:
        return
    
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        with open('create_tables_sqllite.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        sql_commands = sql_script.split(';')

        cursor = await conn.cursor()
        for command in sql_commands:
            if command.strip():
                await cursor.execute(command)
        await conn.commit()

async def add_questionnaire_db(data: dict):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       INSERT INTO Users
                       VALUES (?,?,?,?,?,?)''',
                       tuple(data.values()))
        await conn.commit()

async def check_name_workout(id: int, name: str) -> bool:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT * FROM Workout_types
                       WHERE id_user = ? AND name = ?''',
                       (id, name))
        rows = await cursor.fetchall()
        await conn.commit()
    return bool(rows)

async def add_new_workout(id: int, name: str):
    if await check_name_workout(id, name):
        return False
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       INSERT INTO Workout_types (id_user, name, is_active)
                       VALUES (?,?,?)''',
                       (id, name, True))
        await conn.commit()
    return True
    
async def get_active_workouts(id: int) -> tuple:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ? AND is_active = 1''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows

async def get_deactive_workouts(id: int) -> tuple:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ? AND is_active = 0''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows

async def get_all_workouts(id: int) -> tuple:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT id, name FROM Workout_types
                       WHERE id_user = ?''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows

async def deactive_workout(workout: str):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       UPDATE Workout_types SET is_active = 0
                       WHERE id = ?''',
                       (int(workout), ))
        await conn.commit()

async def active_workout(workout: str):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       UPDATE Workout_types SET is_active = 1
                       WHERE id = ?''',
                       (int(workout), ))
        await conn.commit()

async def delete_workout(workout: str):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       DELETE FROM Workout_types
                       WHERE id = ?''',
                       (int(workout), ))
        await conn.commit()

######################################################################################

async def get_name_workout(id: int) -> str:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT name FROM Workout_types
                       WHERE id = ?''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows[0][0]

async def check_name_exercise(id: int, name: str) -> bool:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT * FROM Exercise_types
                       WHERE id_user = ? AND name = ?''',
                       (id, name))
        rows = await cursor.fetchall()
        await conn.commit()
    return bool(rows)

async def add_new_exercise(id: int, name: str):
    if await check_name_exercise(id, name):
        return False
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       INSERT INTO Exercise_types (id_user, name)
                       VALUES (?,?)''',
                       (id, name))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def get_name_exercise(id: int) -> str:
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT name FROM Exercise_types
                       WHERE id = ?''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows[0][0]

async def start_workout(id_user, id_type):
    data = datetime.today().strftime("%d-%m-%Y")
    start = datetime.now().strftime("%H:%M:%S")

    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       INSERT INTO Workouts (id_user, id_type, data, start)
                       VALUES (?,?,?,?)''',
                       (id_user, id_type, data, start))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def start_exercise(exercise_type, workout):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       INSERT INTO Exercises (id_type, id_workout, weight)
                       VALUES (?,?,"")''',
                       (exercise_type, workout))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def get_weight_workout(id):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT Exercise_types.name, Exercises.weight, Exercises.id
                       FROM Exercises
                       INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                       WHERE Exercises.id_workout = ?''',
                       (id, ))
        rows = await cursor.fetchall()
        await conn.commit()
    return rows

async def end_workout(workout_id: int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT data, start FROM Workouts
                       WHERE id = ?''',
                       (workout_id, ))
        rows = await cursor.fetchall()

    date_start = datetime.strptime(rows[0][0], "%d-%m-%Y").date()
    time_start = datetime.strptime(rows[0][1], "%H:%M:%S").time()
    start = datetime.combine(date_start, time_start)

    end = datetime.now()
    duration = (end-start).total_seconds()//60
    end_str = end.strftime("%H:%M:%S")

    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       UPDATE Workouts SET end = ?, duration = ?
                       WHERE id = ?''',
                       (end_str, duration, workout_id))
        await conn.commit()

async def get_workout_exercises(type_workout:int):
    #Получаем id последней тренировки
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT id
                       FROM Workouts
                       WHERE id_type = ? AND end IS NOT NULL
                       ORDER BY id DESC
                       LIMIT 1''',
                       (type_workout, ))
        rows = await cursor.fetchall()
    
    #если нет записей в БД
    if not rows:
        return []

    id_workout = rows[0][0]

    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT  Exercises.id_type, Exercise_types.name
                       FROM Exercises
                       INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                       WHERE Exercises.id_workout = ?''',
                       (id_workout, ))
        rows = await cursor.fetchall()
    
    result = [(str(i), j) for i,j in rows]

    return result

async def get_latest_workout_ids(type_workout: int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT id
                       FROM Workouts
                       WHERE id_type = ?
                       ORDER BY id DESC
                       LIMIT ?''',
                       (type_workout, 3))
        rows = await cursor.fetchall()
    return [i[0] for i in rows]

async def get_date_workout(workout_id: int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT data FROM Workouts
                       WHERE id = ?''',
                       (workout_id, ))
        rows = await cursor.fetchall()
    return rows[0][0]

async def update_exercise(id_exercise, weight):
    #получаем вес, уже записанный
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT weight FROM Exercises
                       WHERE id = ?''',
                       (id_exercise, ))
        rows = await cursor.fetchall()
    
    if not rows[0][0]:
        old_weight = []
    else:
        old_weight = rows[0][0].split(' | ')
        
    old_weight.append(weight)
    text_weight = ' | '.join(old_weight)
    #записываем новый вес
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       UPDATE Exercises SET weight = ?
                       WHERE id = ?
                       ''',
                       (text_weight, id_exercise))
        await conn.commit()

async def get_all_exercises(chat_id:int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT  Exercise_types.id, Exercise_types.name
                       FROM Exercise_types
                       WHERE Exercise_types.id_user = ?''',
                       (chat_id, ))
        rows = await cursor.fetchall()

    result = [(str(i), j) for i,j in rows]

    return result

async def get_info_workout(workout_id: int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT data, start, duration, id_type FROM Workouts
                       WHERE id = ?''',
                       (workout_id, ))
        row = await cursor.fetchone()
    return row

async def get_history(exercise_type: int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                        SELECT Workout_types.name, Workouts.data, Workouts.start, Exercises.weight
                        FROM Exercises
                        JOIN Workouts ON Exercises.id_workout = Workouts.id
                        JOIN Workout_types ON Workouts.id_type = Workout_types.id
                        WHERE Exercises.id_type = ?
                        LIMIT 5''',
                        (exercise_type, ))
        rows = await cursor.fetchall()
    return rows

async def delete_exercise(exercise: int):
    exerecise_del = await get_type_exercise(exercise)
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       DELETE FROM Exercises
                       WHERE id = ?''',
                       (exercise,))
        await conn.commit()
    
    return exerecise_del

async def get_type_exercise(id_exercise:int):
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
                       SELECT Exercises.id_type, Exercise_types.name
                       FROM Exercises
                       INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
                       WHERE Exercises.id = ?''',
                       (id_exercise, ))
        row = await cursor.fetchone()
    return row