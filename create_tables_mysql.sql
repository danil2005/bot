-- Начало транзакции
START TRANSACTION;

-- Создание таблицы Users
CREATE TABLE IF NOT EXISTS Users (
    chat_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,
    height INT NOT NULL,
    weight INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Создание таблицы Exercise_types
CREATE TABLE IF NOT EXISTS Exercise_types (
    id INT AUTO_INCREMENT,
    id_user BIGINT,
    name VARCHAR(255),
    sets INT,
    reps INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES Users(chat_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Создание таблицы Workout_types
CREATE TABLE IF NOT EXISTS Workout_types (
    id INT AUTO_INCREMENT,
    id_user BIGINT,
    name VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES Users(chat_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Создание таблицы Workouts
CREATE TABLE IF NOT EXISTS Workouts (
    id INT AUTO_INCREMENT,
    id_user BIGINT,
    id_type INT,
    data DATE,
    start_time DATETIME,
    end_time DATETIME,
    duration INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_type) REFERENCES Workout_types(id) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES Users(chat_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Создание таблицы Exercises
CREATE TABLE IF NOT EXISTS Exercises (
    id INT AUTO_INCREMENT,
    id_type INT,
    weight DECIMAL(5,2),
    id_workout INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_type) REFERENCES Exercise_types(id) ON DELETE CASCADE,
    FOREIGN KEY (id_workout) REFERENCES Workouts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Завершение транзакции
COMMIT;