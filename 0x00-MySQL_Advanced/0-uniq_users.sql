-- A SQL script that creates a table named users
CREATE DATABASE IF NOT EXISTS holberton;
USE holberton;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255)
);

