CREATE DATABASE IF NOT EXISTS course_recommendation DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE course_recommendation;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS majors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credit DECIMAL(3,1) NOT NULL,
    description TEXT,
    major_id INT NOT NULL,
    teacher_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS evaluations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    course_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

INSERT INTO majors (name, description) VALUES
('公共课', '全校公共基础课程'),
('计算机', '计算机科学与技术专业课程'),
('软件', '软件工程专业课程'),
('大数据', '大数据技术专业课程'),
('人工智能', '人工智能专业课程');

INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('student', 'student123', 'student');

INSERT INTO teachers (name) VALUES
('张教授'),
('李教授'),
('王教授'),
('赵教授'),
('刘教授');

INSERT INTO courses (name, credit, description, major_id, teacher_id) VALUES
('高等数学', 4.0, '微积分、线性代数等基础数学知识', 1, 1),
('大学英语', 3.0, '英语听说读写综合训练', 1, 2),
('计算机导论', 3.0, '计算机科学基础入门', 2, 3),
('数据结构', 4.0, '常用数据结构与算法', 2, 1),
('软件工程', 3.0, '软件开发流程与方法', 3, 4),
('数据库原理', 4.0, '关系型数据库设计与应用', 3, 2),
('大数据技术基础', 3.0, 'Hadoop、Spark等大数据技术', 4, 5),
('数据分析', 3.0, '数据挖掘与统计分析', 4, 3),
('机器学习', 4.0, '机器学习算法与应用', 5, 1),
('深度学习', 4.0, '神经网络与深度学习', 5, 5);

INSERT INTO evaluations (teacher_id, course_id, rating, comment) VALUES
(1, 1, 5, '张教授讲课非常清晰，例题讲解详细'),
(1, 4, 5, '数据结构讲得很好，作业设计合理'),
(1, 9, 4, '机器学习内容丰富，但难度较大'),
(2, 2, 4, '李老师很有耐心，英语进步很大'),
(2, 6, 5, '数据库原理讲得深入浅出'),
(3, 3, 4, '王教授的课很有趣，引人入胜'),
(3, 8, 5, '数据分析实战项目很有价值'),
(4, 5, 4, '赵教授的软件工程课很实用'),
(5, 7, 5, '刘教授的大数据课很前沿'),
(5, 10, 5, '深度学习课讲解透彻，收获满满');
