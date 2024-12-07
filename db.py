import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('education_system.db')
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            login TEXT PRIMARY KEY NOT NULL,
            password TEXT,
            last_name TEXT,
            first_name TEXT,
            status TEXT
        );
        ''')
        # Расписание
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS schedule ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        day TEXT,
        subject TEXT,
        time_start TEXT,
        time_end TEXT,
        login TEXT,
        FOREIGN KEY (login)  REFERENCES user (login) ) ''')

        # Таблица курсов
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS course (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                );
                ''')

        # Таблица тем
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS topic (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER,
                    name TEXT NOT NULL,
                    content TEXT,
                    FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE
                );
                ''')

        # Таблица для связи студентов и курсов
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS student_courses (
                        student_login TEXT,
                        course_id INTEGER,
                        FOREIGN KEY (student_login) REFERENCES user (login) ON DELETE CASCADE,
                        FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE,
                        PRIMARY KEY (student_login, course_id)
                    );
                    ''')
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS study_materials (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   course_id INTEGER,
                   file_name TEXT NOT NULL,
                   file_path TEXT NOT NULL,
                   file_type TEXT NOT NULL,
                   FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE
               );
           ''')

        self.conn.commit()

    def user_exists(self, login):
        """
        Проверяет, существует ли пользователь с заданным логином.
        """
        self.cursor.execute("SELECT 1 FROM user WHERE login = ?", (login,))
        return self.cursor.fetchone() is not None

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM user WHERE status='student'")
        return self.cursor.fetchall()

    def get_all_students_1(self):
        # Извлекаем только необходимые поля (логин, фамилия, имя)
        self.cursor.execute("SELECT login, last_name, first_name FROM user WHERE status='student'")
        return self.cursor.fetchall()

    def get_user(self,login):
        self.cursor.execute('SELECT * FROM user WHERE login=?', (login,))
        return self.cursor.fetchone()

    def add_user(self, login, password, last_name, first_name, status):
        self.cursor.execute('INSERT INTO user (login, password, last_name, first_name, status) VALUES (?, ?, ?, ?, ?)',
                            (login, password, last_name, first_name, status))

        self.conn.commit()

    def add_student_schedule(self, date, day, subject, time_start, time_end, login):
        self.cursor.execute('''INSERT INTO schedule (date, day, subject, time_start, time_end, login) 
                                   VALUES (?, ?, ?, ?, ?, ?)''',
                                (date, day, subject, time_start, time_end, login))
        self.conn.commit()

    def remove_user(self, login):
        # Check if the user exists
        user = self.get_user(login)
        if not user:
            raise Exception("Пользователь не найден")  # User not found

        # Delete associated schedules first
        self.cursor.execute('DELETE FROM schedule WHERE login = ?', (login,))
        # Now, delete the user
        self.cursor.execute('DELETE FROM user WHERE login = ?', (login,))
        self.conn.commit()

    def add_course(self, name, description):
        self.cursor.execute('INSERT INTO course (name, description) VALUES (?, ?)', (name, description))
        self.conn.commit()

    def get_all_courses(self):
        self.cursor.execute('SELECT * FROM course')
        return self.cursor.fetchall()

    def get_all_study_materials(self):
        self.cursor.execute('SELECT * FROM study_materials')
        return self.cursor.fetchall()

    # Пример методов для работы с темами
    def add_topic(self, course_id, name, content):
        self.cursor.execute('INSERT INTO topic (course_id, name, content) VALUES (?, ?, ?)', (course_id, name, content))
        self.conn.commit()

    def get_topics_by_course(self, course_id):
        self.cursor.execute('SELECT * FROM topic WHERE course_id = ?', (course_id,))
        return self.cursor.fetchall()

    def add_student_course(self, student_login, course_id):
        self.cursor.execute('INSERT INTO student_courses (student_login, course_id) VALUES (?, ?)',
                            (student_login, course_id))
        self.conn.commit()

    def get_student_courses(self, student_login):
        self.cursor.execute('''
            SELECT course.id, course.name, course.description 
            FROM course 
            INNER JOIN student_courses ON course.id = student_courses.course_id 
            WHERE student_courses.student_login = ?''',
                            (student_login,))
        return self.cursor.fetchall()

    def add_study_material(self, course_id, file_name, file_path, file_type):
        self.cursor.execute('''
            INSERT INTO study_materials (course_id, file_name, file_path, file_type)
            VALUES (?, ?, ?, ?)
        ''', (course_id, file_name, file_path, file_type))
        self.conn.commit()

    def get_course_popularity(self):
        query = """
            SELECT course.name, COUNT(student_courses.student_login) as student_count
            FROM course
            LEFT JOIN student_courses ON course.id = student_courses.course_id
            GROUP BY course.id
            ORDER BY student_count DESC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_study_materials_for_course(self, course_id):
        try:
            # Удаляем все материалы для курса
            self.cursor.execute('DELETE FROM study_materials WHERE course_id = ?', (course_id,))
            self.conn.commit()  # Применяем изменения в базе данных

            if self.cursor.rowcount > 0:
                print(f"Учебные материалы для курса с ID {course_id} успешно удалены.")
            else:
                print(f"Нет учебных материалов для курса с ID {course_id}.")
        except Exception as e:
            print(f"Произошла ошибка при удалении материалов для курса с ID {course_id}: {e}")
            self.conn.rollback()  # Откатываем изменения в случае ошибки

    def get_course_by_id(self, course_id):
        try:
            self.cursor.execute('SELECT * FROM course WHERE id = ?', (course_id,))
            course = self.cursor.fetchone()  # Получаем одну запись
            return course  # Возвращаем данные о курсе (id, name, description)
        except Exception as e:
            print(f"Произошла ошибка при получении данных о курсе с ID {course_id}: {e}")
            return None

    def delete_course(self, course_id):
        """Удалить курс по ID."""
        try:
            # Проверяем, существует ли курс с указанным ID
            self.cursor.execute('SELECT * FROM course WHERE id = ?', (course_id,))
            course = self.cursor.fetchone()

            if not course:
                raise ValueError(f"Курс с ID {course_id} не найден!")

            # Удаляем курс
            self.cursor.execute('DELETE FROM course WHERE id = ?', (course_id,))
            self.conn.commit()
            print(f"Курс с ID {course_id} успешно удалён.")

        except ValueError as ve:
            print(f"Ошибка: {ve}")
            raise
        except Exception as e:
            print(f"Ошибка при удалении курса: {e}")
            raise

    def is_course_in_progress_by_login(self, user_login, course_id):
        """
        Проверяет, изучает ли пользователь курс.
        """
        self.cursor.execute(
            'SELECT 1 FROM student_courses WHERE student_login = ? AND course_id = ?',
            (user_login, course_id)
        )
        return self.cursor.fetchone() is not None

    def enroll_user_in_course_by_login(self, user_login, course_id):
        """
        Добавляет курс для пользователя.
        """
        try:
            self.cursor.execute(
                'INSERT INTO student_courses (student_login, course_id) VALUES (?, ?)',
                (user_login, course_id)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise

    def close(self):
        self.conn.close()
