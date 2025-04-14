# SQL for creating database tables

drop database if EXISTS bob_ross_episodes;
CREATE DATABASE IF NOT EXISTS bob_ross_episodes;

USE bob_ross_episodes;


CREATE TABLE `subject` (
  `subject_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `subject_name`  VARCHAR(255) UNIQUE
);

CREATE TABLE `episode` (
  `episode_id` INTEGER PRIMARY KEY,
  `title`  VARCHAR(255),
  `season` INTEGER,
  `episode` INTEGER,
  `og_date`  VARCHAR(255),
  `month`  VARCHAR(255),
  `colors`  VARCHAR(255),
  `subjects`  VARCHAR(255)
);

CREATE TABLE `color` (
  `color_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `color_name`  VARCHAR(255) UNIQUE
);

CREATE TABLE `episode_subject` (
  `episode_id` INTEGER,
  `subject_id` INTEGER,
  PRIMARY KEY (episode_id, subject_id),
  FOREIGN KEY (episode_id) REFERENCES episode (episode_id),
  FOREIGN KEY (subject_id) REFERENCES subject (subject_id)
);

CREATE TABLE `episode_color` (
  `episode_id` INTEGER,
  `color_id` INTEGER,
  PRIMARY KEY (episode_id, color_id),
  FOREIGN KEY (episode_id) REFERENCES episode (episode_id),
  FOREIGN KEY (color_id) REFERENCES color (color_id)
);