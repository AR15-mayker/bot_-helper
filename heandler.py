import mysql.connector
from mysql.connector import Error
from datetime import datetime


class ScheduleDBHandler:
    def __init__(self, host, database, user, password):
        """Инициализация соединения с базой данных"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Установка соединения с БД"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Успешное подключение к базе данных")
        except Error as e:
            print(f"Ошибка подключения к MySQL: {e}")

    def disconnect(self):
        """Закрытие соединения с БД"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Соединение с MySQL закрыто")

    # ========== CRUD для преподавателей ==========
    def add_teacher(self, first_name, last_name, department_id, **kwargs):
        """Добавление преподавателя"""
        query = """
        INSERT INTO teachers (first_name, last_name, department_id, middle_name,
                            academic_degree, academic_title, position, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            first_name, last_name, department_id,
            kwargs.get('middle_name'),
            kwargs.get('academic_degree'),
            kwargs.get('academic_title'),
            kwargs.get('position'),
            kwargs.get('phone'),
            kwargs.get('email')
        )
  
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Преподаватель {last_name} {first_name} добавлен")
            return cursor.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении преподавателя: {e}")
            return None

    # ========== CRUD для студентов ==========
    def add_student(self, first_name, last_name, group_id, **kwargs):
        """Добавление студента"""
        query = """
        INSERT INTO students (first_name, last_name, group_id, middle_name, 
                             birth_date, address, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            first_name, last_name, group_id,
            kwargs.get('middle_name'),
            kwargs.get('birth_date'),
            kwargs.get('address'),
            kwargs.get('phone'),
            kwargs.get('email')
        )
 
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Студент {last_name} {first_name} добавлен")
            return cursor.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении студента: {e}")
            return None

    # ========== CRUD для расписания ==========
    def add_schedule_entry(self, group_id, subject_id, teacher_id, classroom_id,
                          day_of_week, lesson_number, lesson_type, **kwargs):
        """Добавление записи в расписание"""
        query = """
        INSERT INTO schedule (group_id, subject_id, teacher_id, classroom_id,
                             day_of_week, week_parity, lesson_number, lesson_type,
                             start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            group_id, subject_id, teacher_id, classroom_id,
            day_of_week,
            kwargs.get('week_parity', 'каждую'),
            lesson_number,
            lesson_type,
            kwargs.get('start_date'),
            kwargs.get('end_date')
        )

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Запись в расписание добавлена")
            return cursor.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении записи в расписание: {e}")
            return None

    def get_group_schedule(self, group_id, date_from=None, date_to=None):
        """Получение расписания для группы"""
        query = """
        SELECT s.schedule_id, sub.subject_name, t.last_name as teacher_name, 
               c.building, c.room_number, sch.day_of_week, sch.lesson_number, 
               sch.lesson_type, sch.start_date, sch.end_date
        FROM schedule sch
        JOIN subjects sub ON sch.subject_id = sub.subject_id
        JOIN teachers t ON sch.teacher_id = t.teacher_id
        JOIN classrooms c ON sch.classroom_id = c.classroom_id
        JOIN student_groups s ON sch.group_id = s.group_id
        WHERE sch.group_id = %s
        """

        params = (group_id,)

        if date_from and date_to:
            query += " AND (sch.end_date >= %s OR sch.end_date IS NULL) AND sch.start_date <= %s"
            params += (date_from, date_to)

        query += " ORDER BY sch.day_of_week, sch.lesson_number"

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении расписания: {e}")
            return None

    # ========== Методы для изменений расписания ==========
    def add_schedule_change(self, original_schedule_id, **kwargs):
        """Добавление изменения в расписание"""
        query = """
        INSERT INTO schedule_changes (original_schedule_id, new_teacher_id, 
                                    new_classroom_id, new_date, new_lesson_number, 
                                    change_reason, is_cancelled)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            original_schedule_id,
            kwargs.get('new_teacher_id'),
            kwargs.get('new_classroom_id'),
            kwargs.get('new_date'),
            kwargs.get('new_lesson_number'),
            kwargs.get('change_reason'),
            kwargs.get('is_cancelled', False)
        )

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Изменение в расписание добавлено")
            return cursor.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении изменения в расписание: {e}")
            return None

    # ========== Вспомогательные методы ==========
    def get_teacher_by_name(self, last_name, first_name=None):
        """Поиск преподавателя по фамилии (и имени)"""
        query = "SELECT * FROM teachers WHERE last_name LIKE %s"
        params = (f"%{last_name}%",)

        if first_name:
            query += " AND first_name LIKE %s"
            params += (f"%{first_name}%",)

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при поиске преподавателя: {e}")
            return None

    def get_students_by_group(self, group_id):
        """Получение списка студентов группы"""
        query = """
        SELECT student_id, last_name, first_name, middle_name 
        FROM students 
        WHERE group_id = %s
        ORDER BY last_name, first_name
        """

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (group_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка студентов: {e}")
            return None
