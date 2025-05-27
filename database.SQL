CREATE TABLE IF NOT EXISTS faculties (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_name VARCHAR(100) NOT NULL,
    dean_name VARCHAR(100),
    office_location VARCHAR(50),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_id INT NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    head_name VARCHAR(100),
    office_location VARCHAR(50),
    phone VARCHAR(20),
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    department_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    academic_degree VARCHAR(50),
    academic_title VARCHAR(50),
    position VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS student_groups (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_id INT NOT NULL,
    group_name VARCHAR(20) NOT NULL,
    course_number INT NOT NULL,
    study_form ENUM('очная', 'заочная', 'вечерняя') NOT NULL,
    creation_year INT NOT NULL,
    curator_id INT,
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (curator_id) REFERENCES teachers(teacher_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE,
    address VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (group_id) REFERENCES student_groups(group_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    department_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    hours_total INT NOT NULL,
    hours_lecture INT,
    hours_practice INT,
    hours_lab INT,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS classrooms (
    classroom_id INT PRIMARY KEY AUTO_INCREMENT,
    building VARCHAR(10) NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    capacity INT,
    room_type ENUM('приёмная', 'дизайнерская') NOT NULL,
    UNIQUE (building, room_number)
);

CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    subject_id INT NOT NULL,
    teacher_id INT NOT NULL,
    classroom_id INT NOT NULL,
    day_of_week ENUM('понедельник', 'вторник', 'среда', 'четверг', 'пятница') NOT NULL,
    week_parity ENUM('четная', 'нечетная', 'каждую') NOT NULL DEFAULT 'каждую',
    lesson_number INT NOT NULL,
    lesson_type ENUM('пара') NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (group_id) REFERENCES student_groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS schedule_changes (
    change_id INT PRIMARY KEY AUTO_INCREMENT,
    original_schedule_id INT NOT NULL,
    new_teacher_id INT,
    new_classroom_id INT,
    new_date DATE,
    new_lesson_number INT,
    change_reason VARCHAR(200),
    is_cancelled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (original_schedule_id) REFERENCES schedule(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (new_teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    FOREIGN KEY (new_classroom_id) REFERENCES classrooms(classroom_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_schedule_group ON schedule(group_id);
CREATE INDEX IF NOT EXISTS idx_schedule_teacher ON schedule(teacher_id);
CREATE INDEX IF NOT EXISTS idx_schedule_day_week ON schedule(day_of_week, week_parity);
CREATE INDEX IF NOT EXISTS idx_student_group ON students(group_id);
CREATE INDEX IF NOT EXISTS idx_student_name ON students(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_teacher_name ON teachers(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_teacher_department ON teachers(department_id);