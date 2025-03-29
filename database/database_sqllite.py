import aiosqlite
import os
from datetime import datetime
from config_data.config import config

async def check_db() -> None:
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

async def add_questionnaire(data: dict) -> None:
    query = '''
        INSERT INTO Users
        VALUES (?,?,?,?,?,?)
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, tuple(data.values()))
        await conn.commit()

async def check_name_workout_type(user_id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Workout_types
        WHERE user_id = ? AND name = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (user_id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_workout_type(user_id: int, name: str) -> None:
    if await check_name_workout_type(user_id, name):
        return False
    query = '''
        INSERT INTO Workout_types (user_id, name, is_active)
        VALUES (?,?,?)
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (user_id, name, True))
        await conn.commit()
    return True

async def get_workout_types(user_id: int, is_active = None) -> list[tuple]:
    query = '''
        SELECT id, name FROM Workout_types
        WHERE user_id = ?
    '''
    query_is_active = 'AND is_active = ?'

    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        if is_active == 'active':
            await cursor.execute(query + query_is_active, (user_id, 1))
        elif is_active == 'deactive':
            await cursor.execute(query + query_is_active, (user_id, 0))
        else:
            await cursor.execute(query, (user_id,))
        rows = await cursor.fetchall()
    return rows

async def set_active_workout_type(workout_type: int, is_active: bool)-> None:
    query = '''
        UPDATE Workout_types SET is_active = ?
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (is_active, workout_type))
        await conn.commit()

async def delete_workout_type(workout_type: int) -> None:
    query = '''
        DELETE FROM Workout_types
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout_type,))
        await conn.commit()

async def get_name_workout_type(workout_type: int) -> str:
    query = '''
        SELECT name FROM Workout_types
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout_type,))
        rows = await cursor.fetchall()
    return rows[0][0]

async def check_name_exercise_type(user_id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Exercise_types
        WHERE user_id = ? AND name = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (user_id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_exercise_type(user_id: int, name: str) -> int:
    if await check_name_exercise_type(user_id, name):
        return False
    query = '''
        INSERT INTO Exercise_types (user_id, name)
        VALUES (?,?)
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (user_id, name))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def start_workout(user_id: int, workout_type: int) -> int:
    data = datetime.today().strftime("%d-%m-%Y")
    start = datetime.now().strftime("%H:%M:%S")
    query = '''
        INSERT INTO Workouts (user_id, type_id, data, start)
        VALUES (?,?,?,?)
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (user_id, workout_type, data, start))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def start_exercise(exercise_type: int, workout: int) -> int:
    query = '''
        INSERT INTO Exercises (type_id, id_workout, weight)
        VALUES (?,?,"")
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (exercise_type, workout))
        last_id = cursor.lastrowid
        await conn.commit()
    return last_id

async def get_weight_workout(workout: int) -> list[tuple]:
    query = '''
        SELECT Exercise_types.name, Exercises.weight, Exercises.id
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id_workout = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout,))
        rows = await cursor.fetchall()
    return rows

async def end_workout(workout: int) -> None:
    query_select = '''
        SELECT data, start FROM Workouts
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_select, (workout,))
        rows = await cursor.fetchall()
    date_start = datetime.strptime(rows[0][0], "%d-%m-%Y").date()
    time_start = datetime.strptime(rows[0][1], "%H:%M:%S").time()
    start = datetime.combine(date_start, time_start)
    end = datetime.now()
    duration = (end - start).total_seconds() // 60
    end_str = end.strftime("%H:%M:%S")

    query_update = '''
        UPDATE Workouts SET end = ?, duration = ?
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_update, (end_str, duration, workout))
        await conn.commit()

async def get_workout_exercises(workout_type: int) -> list[tuple]:
    query_last_workout = '''
        SELECT id
        FROM Workouts
        WHERE type_id = ? AND end IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_last_workout, (workout_type,))
        rows = await cursor.fetchall()

    if not rows:
        return []

    id_workout = rows[0][0]
    query_exercises = '''
        SELECT Exercises.type_id, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id_workout = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_exercises, (id_workout,))
        rows = await cursor.fetchall()

    # result = [(i, j) for i, j in rows]
    return rows #result

async def get_latest_workout_ids(workout_type: int) -> list[int]:
    query = '''
        SELECT id
        FROM Workouts
        WHERE type_id = ?
        ORDER BY id DESC
        LIMIT ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout_type, 3))
        rows = await cursor.fetchall()
    return [i[0] for i in rows]

async def get_date_workout(workout: int) -> str:
    query = '''
        SELECT data FROM Workouts
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout,))
        rows = await cursor.fetchall()
    return rows[0][0]

async def update_exercise(exercise: int, weight: str) -> None:
    query_select = '''
        SELECT weight FROM Exercises
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_select, (exercise,))
        rows = await cursor.fetchall()
    if not rows[0][0]:
        old_weight = []
    else:
        old_weight = rows[0][0].split(' | ')
    old_weight.append(weight)
    text_weight = ' | '.join(old_weight)

    query_update = '''
        UPDATE Exercises SET weight = ?
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query_update, (text_weight, exercise))
        await conn.commit()

async def get_all_exercise_types(chat_id: int) -> list[tuple]:
    query = '''
        SELECT Exercise_types.id, Exercise_types.name
        FROM Exercise_types
        WHERE Exercise_types.user_id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (chat_id,))
        rows = await cursor.fetchall()
    #result = [(str(i), j) for i, j in rows]
    return rows #result

async def get_info_workout(workout: int) -> tuple:
    query = '''
        SELECT data, start, duration, type_id FROM Workouts
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (workout,))
        row = await cursor.fetchone()
    return row


async def get_exercise_history(exercise_type: int) -> list[tuple]:
    query = '''
        SELECT Workout_types.name, Workouts.data, Workouts.start, Exercises.weight
        FROM Exercises
        JOIN Workouts ON Exercises.id_workout = Workouts.id
        JOIN Workout_types ON Workouts.type_id = Workout_types.id
        WHERE Exercises.type_id = ?
        LIMIT 5
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (exercise_type,))
        rows = await cursor.fetchall()
    return rows

async def delete_exercise(exercise: int) -> tuple:
    exerecise_del = await get_exercise_type(exercise)
    query = '''
        DELETE FROM Exercises
        WHERE id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (exercise,))
        await conn.commit()
    return exerecise_del

async def get_exercise_type(exercise: int) -> tuple:
    query = '''
        SELECT Exercises.type_id, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id = ?
    '''
    async with aiosqlite.connect("bot_gym_db.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, (exercise,))
        row = await cursor.fetchone()
    return row