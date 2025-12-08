CREATE DATABASE IF NOT EXISTS meinprojekt
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'meinuser'@'localhost' IDENTIFIED BY 'Password123!';
GRANT ALL PRIVILEGES ON meinprojekt.* TO 'meinuser'@'localhost';
FLUSH PRIVILEGES;
