CREATE DATABASE IF NOT EXISTS course_recommendation
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'course_user'@'%' IDENTIFIED BY 'CoursePass2026!';
GRANT ALL PRIVILEGES ON course_recommendation.* TO 'course_user'@'%';
FLUSH PRIVILEGES;
