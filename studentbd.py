import sqlite3


class Database:
    def __init__(self, db_name: str = "student.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_database()

    def create_database(self):
        with sqlite3.connect('student.db') as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                id_user INTEGER,
                id_group INTEGER,
                time INTEGER,
                day_week TEXT
            )
            ''')
            db.commit()

    def add_student(self, id_user: int, id_group: int, time: int, day_week: str):
        with self.conn:
            self.conn.execute('''
                INSERT INTO users (id_user, id_group, time, day_week)
                VALUES (?, ?, ?, ?)
            ''', (id_user, id_group, time, day_week))
        print(f"Студент {id_user} добавлен.")

    def get_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()

    def print_students(self):
        students = self.get_students()
        if not students:
            print("Нет данных о студентах.")
        else:
            for student in students:
                print(student)
