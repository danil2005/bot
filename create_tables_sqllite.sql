BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Exercise_types" (
	"id"	INTEGER,
	"id_user"	INTEGER,
	"name"	TEXT,
	"sets"	INTEGER,
	"reps"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_user") REFERENCES "Users"("chat_id")
);
CREATE TABLE IF NOT EXISTS "Exercises" (
	"id"	INTEGER,
	"id_type"	INTEGER,
	"weight"	TEXT,
	"id_workout"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_type") REFERENCES "Exercise_types"("id"),
	FOREIGN KEY("id_workout") REFERENCES "Workouts"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Users" (
	"chat_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"age"	INTEGER NOT NULL,
	"gender"	TEXT NOT NULL,
	"height"	INTEGER NOT NULL,
	"weight"	INTEGER NOT NULL,
	PRIMARY KEY("chat_id")
);
CREATE TABLE IF NOT EXISTS "Workout_types" (
	"id"	INTEGER,
	"id_user"	INTEGER,
	"name"	TEXT NOT NULL,
	"is_active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_user") REFERENCES "Users"("chat_id")
);
CREATE TABLE IF NOT EXISTS "Workouts" (
	"id"	INTEGER,
	"id_user"	INTEGER,
	"id_type"	INTEGER,
	"data"	TEXT,
	"start"	TEXT,
	"end"	TEXT,
	"duration"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_type") REFERENCES "Workout_types"("id"),
	FOREIGN KEY("id_user") REFERENCES "Users"("chat_id")
);
COMMIT;
