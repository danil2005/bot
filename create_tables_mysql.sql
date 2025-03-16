-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: db
-- Время создания: Фев 22 2025 г., 09:05
-- Версия сервера: 9.2.0
-- Версия PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `gymbot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `exercises`
--

CREATE TABLE `exercises` (
  `id` int NOT NULL,
  `id_type` int NOT NULL,
  `weight` varchar(255) NOT NULL,
  `id_workout` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `exercise_types`
--

CREATE TABLE `exercise_types` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `chat_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `age` int NOT NULL,
  `gender` varchar(50) NOT NULL,
  `height` int NOT NULL,
  `weight` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `workouts`
--

CREATE TABLE `workouts` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `id_type` int NOT NULL,
  `date` date NOT NULL,
  `start` time NOT NULL,
  `end` time DEFAULT NULL,
  `duration` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `workout_types`
--

CREATE TABLE `workout_types` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `is_active` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `exercises`
--
ALTER TABLE `exercises`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_type` (`id_type`),
  ADD KEY `id_workout` (`id_workout`);

--
-- Индексы таблицы `exercise_types`
--
ALTER TABLE `exercise_types`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`chat_id`);

--
-- Индексы таблицы `workouts`
--
ALTER TABLE `workouts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_type` (`id_type`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `workout_types`
--
ALTER TABLE `workout_types`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `exercises`
--
ALTER TABLE `exercises`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `exercise_types`
--
ALTER TABLE `exercise_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `workouts`
--
ALTER TABLE `workouts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `workout_types`
--
ALTER TABLE `workout_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `exercises`
--
ALTER TABLE `exercises`
  ADD CONSTRAINT `exercises_ibfk_1` FOREIGN KEY (`id_type`) REFERENCES `exercise_types` (`id`),
  ADD CONSTRAINT `exercises_ibfk_2` FOREIGN KEY (`id_workout`) REFERENCES `workouts` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `exercise_types`
--
ALTER TABLE `exercise_types`
  ADD CONSTRAINT `exercise_types_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`chat_id`);

--
-- Ограничения внешнего ключа таблицы `workouts`
--
ALTER TABLE `workouts`
  ADD CONSTRAINT `workouts_ibfk_1` FOREIGN KEY (`id_type`) REFERENCES `workout_types` (`id`),
  ADD CONSTRAINT `workouts_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`chat_id`);

--
-- Ограничения внешнего ключа таблицы `workout_types`
--
ALTER TABLE `workout_types`
  ADD CONSTRAINT `workout_types_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`chat_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
