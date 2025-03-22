from datetime import datetime
from config_data.config import config
import aiomysql
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_cursor():
    conn = await aiomysql.connect(
        host=config.data_base.host,
        user=config.data_base.user,
        password=config.data_base.password,
        db=config.data_base.name_db
    )
    cursor = await conn.cursor()
    try:
        yield cursor
    finally:
        await cursor.close()
        conn.close()

async def add_questionnaire(data: dict):
    query = '''
        INSERT INTO Users
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, tuple(data.values()))
        await cursor.connection.commit()

async def check_db():
    config_db = {
        'host': config.data_base.host,
        'user': config.data_base.user,
        'password': config.data_base.password,
    }
    conn = await aiomysql.connect(**config_db)
    check_db_query = f"SHOW DATABASES LIKE '{config.data_base.name_db}'"
    create_db_query = f"CREATE DATABASE {config.data_base.name_db}"
    
    async with conn.cursor() as cursor:
        await cursor.execute(check_db_query)
        result = await cursor.fetchone()
        if not result:
            await cursor.execute(create_db_query)
        else:
            return
    
    await conn.select_db(config.data_base.name_db)
    with open('create_tables_mysql.sql', 'r', encoding='utf-8') as file:
        sql_script = file.read()
    sql_commands = sql_script.split(';')
    
    async with conn.cursor() as cursor:
        for command in sql_commands:
            if command.strip():
                await cursor.execute(command)
    await conn.commit()
    conn.close()

async def check_name_workout_type(user_id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Workout_types
        WHERE user_id = %s AND name = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (user_id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_workout_type(user_id: int, name: str):
    if await check_name_workout_type(user_id, name):
        return False
    query = '''
        INSERT INTO Workout_types (user_id, name, is_active)
        VALUES (%s, %s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (user_id, name, True))
        await cursor.connection.commit()
    return True

async def get_workout_types(user_id: int, is_active = None) -> tuple:
    query = '''
        SELECT id, name FROM Workout_types
        WHERE user_id = %s
    '''
    query_is_active = 'AND is_active = %s'

    async with get_db_cursor() as cursor:
        if is_active == 'active':
            await cursor.execute(query + query_is_active, (user_id, 1))
        elif is_active == 'deactive':
            await cursor.execute(query + query_is_active, (user_id, 0))
        else:
            await cursor.execute(query, (user_id,))
        rows = await cursor.fetchall()
    return rows

async def set_active_workout_type(workout_type: str, is_active: bool):
    query = '''
        UPDATE Workout_types SET is_active = %s
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (is_active, int(workout_type)))
        await cursor.connection.commit()

async def delete_workout_type(workout_type: str):
    query = '''
        DELETE FROM Workout_types
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(workout_type),))
        await cursor.connection.commit()

async def get_name_workout_type(workout_type: int) -> str:
    query = '''
        SELECT name FROM Workout_types
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout_type,))
        rows = await cursor.fetchall()
    return rows[0][0]

async def check_name_exercise_type(user_id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Exercise_types
        WHERE user_id = %s AND name = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (user_id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_exercise_type(user_id: int, name: str):
    if await check_name_exercise_type(user_id, name):
        return False
    query = '''
        INSERT INTO Exercise_types (user_id, name)
        VALUES (%s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (user_id, name))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def start_workout(user_id, workout_type):
    date = datetime.today().strftime("%Y-%m-%d")
    start = datetime.now().strftime("%H:%M:%S")
    query = '''
        INSERT INTO Workouts (user_id, type_id, date, start)
        VALUES (%s, %s, %s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (user_id, workout_type, date, start))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def start_exercise(exercise_type, workout):
    query = '''
        INSERT INTO Exercises (type_id, id_workout, weight)
        VALUES (%s, %s, "")
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (exercise_type, workout))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def get_weight_workout(workout):
    query = '''
        SELECT Exercise_types.name, Exercises.weight, Exercises.id
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id_workout = %s
        ORDER BY Exercises.id ASC
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout,))
        rows = await cursor.fetchall()
    return rows

async def end_workout(workout: int):
    query_get_workout = '''
        SELECT date, start FROM Workouts
        WHERE id = %s
    '''
    query_update_workout = '''
        UPDATE Workouts SET end = %s, duration = %s
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_workout, (workout,))
        rows = await cursor.fetchall()
    start = datetime.combine(rows[0][0], datetime.min.time()) + rows[0][1]
    end = datetime.now()
    duration = (end - start).total_seconds() // 60
    end_str = end.strftime("%H:%M:%S")
    async with get_db_cursor() as cursor:
        await cursor.execute(query_update_workout, (end_str, duration, workout))
        await cursor.connection.commit()

async def get_workout_exercises(type_workout: int):
    query_get_latest_workout = '''
        SELECT id
        FROM Workouts
        WHERE type_id = %s AND end IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    '''
    query_get_exercises = '''
        SELECT Exercises.type_id, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id_workout = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_latest_workout, (type_workout,))
        rows = await cursor.fetchall()
    if not rows:
        return []
    id_workout = rows[0][0]
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_exercises, (id_workout,))
        rows = await cursor.fetchall()
    return [(str(row[0]), row[1]) for row in rows]

async def get_latest_workout_ids(type_workout: int):
    query = '''
        SELECT id
        FROM Workouts
        WHERE type_id = %s
        ORDER BY id DESC
        LIMIT 3
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (type_workout,))
        rows = await cursor.fetchall()
    return [row[0] for row in rows]

async def get_date_workout(workout: int):
    query = '''
        SELECT date FROM Workouts
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout,))
        rows = await cursor.fetchall()
    return rows[0][0].strftime("%d-%m-%Y")

async def update_exercise(exercise, weight):
    query_get_weight = '''
        SELECT weight FROM Exercises
        WHERE id = %s
    '''
    query_update_weight = '''
        UPDATE Exercises SET weight = %s
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_weight, (exercise,))
        rows = await cursor.fetchall()
    old_weight = rows[0][0].split(' | ') if rows[0][0] else []
    old_weight.append(weight)
    text_weight = ' | '.join(old_weight)
    async with get_db_cursor() as cursor:
        await cursor.execute(query_update_weight, (text_weight, exercise))
        await cursor.connection.commit()

async def get_all_exercise_types(chat_id: int):
    query = '''
        SELECT Exercise_types.id, Exercise_types.name
        FROM Exercise_types
        WHERE Exercise_types.user_id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (chat_id,))
        rows = await cursor.fetchall()
    return [(str(row[0]), row[1]) for row in rows]

async def get_info_workout(workout: int):
    query = '''
        SELECT date, start, duration, type_id FROM Workouts
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout,))
        row = await cursor.fetchone()
    return row

async def get_exercise_history(exercise_type: int):
    query = '''
        SELECT Workout_types.name, Workouts.date, Workouts.start, Exercises.weight
        FROM Exercises
        JOIN Workouts ON Exercises.id_workout = Workouts.id
        JOIN Workout_types ON Workouts.type_id = Workout_types.id
        WHERE Exercises.type_id = %s
        LIMIT 5
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (exercise_type,))
        rows = await cursor.fetchall()
    return rows

async def delete_exercise(exercise: int):
    exercise_del = await get_exercise_type(exercise)
    query = '''
        DELETE FROM Exercises
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(exercise),))
        await cursor.connection.commit()
    return exercise_del

async def get_exercise_type(exercise: int):
    query = '''
        SELECT Exercises.type_id, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.type_id = Exercise_types.id
        WHERE Exercises.id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (exercise,))
        row = await cursor.fetchone()
    return row