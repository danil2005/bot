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

async def add_questionnaire_db(data: dict):
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

async def check_name_workout(id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Workout_types
        WHERE id_user = %s AND name = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_workout(id: int, name: str):
    if await check_name_workout(id, name):
        return False
    query = '''
        INSERT INTO Workout_types (id_user, name, is_active)
        VALUES (%s, %s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id, name, True))
        await cursor.connection.commit()
    return True

async def get_active_workouts(id: int) -> tuple:
    query = '''
        SELECT id, name FROM Workout_types
        WHERE id_user = %s AND is_active = 1
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows

async def get_deactive_workouts(id: int) -> tuple:
    query = '''
        SELECT id, name FROM Workout_types
        WHERE id_user = %s AND is_active = 0
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows

async def get_all_workouts(id: int) -> tuple:
    query = '''
        SELECT id, name FROM Workout_types
        WHERE id_user = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows

async def deactive_workout(workout: str):
    query = '''
        UPDATE Workout_types SET is_active = 0
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(workout),))
        await cursor.connection.commit()

async def active_workout(workout: str):
    query = '''
        UPDATE Workout_types SET is_active = 1
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(workout),))
        await cursor.connection.commit()

async def delete_workout(workout: str):
    query = '''
        DELETE FROM Workout_types
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(workout),))
        await cursor.connection.commit()

async def get_name_workout(id: int) -> str:
    query = '''
        SELECT name FROM Workout_types
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows[0][0]

async def check_name_exercise(id: int, name: str) -> bool:
    query = '''
        SELECT * FROM Exercise_types
        WHERE id_user = %s AND name = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id, name))
        rows = await cursor.fetchall()
    return bool(rows)

async def add_new_exercise(id: int, name: str):
    if await check_name_exercise(id, name):
        return False
    query = '''
        INSERT INTO Exercise_types (id_user, name)
        VALUES (%s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id, name))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def get_name_exercise(id: int) -> str:
    query = '''
        SELECT name FROM Exercise_types
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows[0][0]

async def start_workout(id_user, id_type):
    date = datetime.today().strftime("%Y-%m-%d")
    start = datetime.now().strftime("%H:%M:%S")
    query = '''
        INSERT INTO Workouts (id_user, id_type, date, start)
        VALUES (%s, %s, %s, %s)
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id_user, id_type, date, start))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def start_exercise(exercise_type, workout):
    query = '''
        INSERT INTO Exercises (id_type, id_workout, weight)
        VALUES (%s, %s, "")
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (exercise_type, workout))
        last_id = cursor.lastrowid
        await cursor.connection.commit()
    return last_id

async def get_weight_workout(id):
    query = '''
        SELECT Exercise_types.name, Exercises.weight, Exercises.id
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
        WHERE Exercises.id_workout = %s
        ORDER BY Exercises.id ASC
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id,))
        rows = await cursor.fetchall()
    return rows

async def end_workout(workout_id: int):
    query_get_workout = '''
        SELECT date, start FROM Workouts
        WHERE id = %s
    '''
    query_update_workout = '''
        UPDATE Workouts SET end = %s, duration = %s
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_workout, (workout_id,))
        rows = await cursor.fetchall()
    start = datetime.combine(rows[0][0], datetime.min.time()) + rows[0][1]
    end = datetime.now()
    duration = (end - start).total_seconds() // 60
    end_str = end.strftime("%H:%M:%S")
    async with get_db_cursor() as cursor:
        await cursor.execute(query_update_workout, (end_str, duration, workout_id))
        await cursor.connection.commit()

async def get_workout_exercises(type_workout: int):
    query_get_latest_workout = '''
        SELECT id
        FROM Workouts
        WHERE id_type = %s AND end IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    '''
    query_get_exercises = '''
        SELECT Exercises.id_type, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
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
        WHERE id_type = %s
        ORDER BY id DESC
        LIMIT 3
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (type_workout,))
        rows = await cursor.fetchall()
    return [row[0] for row in rows]

async def get_date_workout(workout_id: int):
    query = '''
        SELECT date FROM Workouts
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout_id,))
        rows = await cursor.fetchall()
    return rows[0][0].strftime("%d-%m-%Y")

async def update_exercise(id_exercise, weight):
    query_get_weight = '''
        SELECT weight FROM Exercises
        WHERE id = %s
    '''
    query_update_weight = '''
        UPDATE Exercises SET weight = %s
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query_get_weight, (id_exercise,))
        rows = await cursor.fetchall()
    old_weight = rows[0][0].split(' | ') if rows[0][0] else []
    old_weight.append(weight)
    text_weight = ' | '.join(old_weight)
    async with get_db_cursor() as cursor:
        await cursor.execute(query_update_weight, (text_weight, id_exercise))
        await cursor.connection.commit()

async def get_all_exercises(chat_id: int):
    query = '''
        SELECT Exercise_types.id, Exercise_types.name
        FROM Exercise_types
        WHERE Exercise_types.id_user = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (chat_id,))
        rows = await cursor.fetchall()
    return [(str(row[0]), row[1]) for row in rows]

async def get_info_workout(workout_id: int):
    query = '''
        SELECT date, start, duration, id_type FROM Workouts
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (workout_id,))
        row = await cursor.fetchone()
    return row

async def get_history(exercise_type: int):
    query = '''
        SELECT Workout_types.name, Workouts.date, Workouts.start, Exercises.weight
        FROM Exercises
        JOIN Workouts ON Exercises.id_workout = Workouts.id
        JOIN Workout_types ON Workouts.id_type = Workout_types.id
        WHERE Exercises.id_type = %s
        LIMIT 5
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (exercise_type,))
        rows = await cursor.fetchall()
    return rows

async def delete_exercise(exercise: int):
    exercise_del = await get_type_exercise(exercise)
    query = '''
        DELETE FROM Exercises
        WHERE id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (int(exercise),))
        await cursor.connection.commit()
    return exercise_del

async def get_type_exercise(id_exercise: int):
    query = '''
        SELECT Exercises.id_type, Exercise_types.name
        FROM Exercises
        INNER JOIN Exercise_types ON Exercises.id_type = Exercise_types.id
        WHERE Exercises.id = %s
    '''
    async with get_db_cursor() as cursor:
        await cursor.execute(query, (id_exercise,))
        row = await cursor.fetchone()
    return row