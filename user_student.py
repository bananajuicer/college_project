from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QLabel, QCalendarWidget,
                             QMessageBox, QListWidget, QTableWidget, QLineEdit, QTableWidgetItem, QFileDialog)
from db import DB
#import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StudentApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.db = DB()
        self.login = username

        self.setWindowTitle('Личный кабинет студента')
        self.setGeometry(100, 100, 400, 500)  # Немного увеличим окно

        # Основной Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)  # Пространство между элементами

        # Стиль для фона
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fa;
                font-family: 'Arial', sans-serif;
            }
        """)

        # Кнопка личного кабинета
        self.profile_button = QPushButton('Личный кабинет')
        self.profile_button.setFont(QFont("Arial", 14))
        self.profile_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a8e;
            }
            QPushButton:pressed {
                background-color: #00477a;
            }
        """)
        self.profile_button.clicked.connect(self.show_profile)
        self.layout.addWidget(self.profile_button)

        # Календарь
        self.calendar = QCalendarWidget(self)
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #0078d7;
                selection-color: white;
            }
            QCalendarWidget QTableView {
                font-size: 14px;
            }
        """)
        self.calendar.clicked.connect(self.show_schedule)
        self.layout.addWidget(self.calendar)

        # Метка для расписания
        self.schedule_label = QLabel('Расписание на выбранный день будет здесь.')
        self.schedule_label.setFont(QFont("Arial", 12))
        self.schedule_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 14px;
                padding: 15px;
                background-color: #e6f7ff;
                border-radius: 8px;
                margin-top: 20px;
            }
        """)
        self.layout.addWidget(self.schedule_label)

        # Кнопка для курса изучения
        self.choose_course_button = QPushButton("Выбор курса для изучения")
        self.choose_course_button.setFont(QFont("Arial", 14))
        self.choose_course_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.choose_course_button.clicked.connect(self.choose_course)
        self.layout.addWidget(self.choose_course_button)

        # Кнопка для просмотра начатых курсов
        self.look_course_button = QPushButton("Посмотреть начатые курсы")
        self.look_course_button.setFont(QFont("Arial", 14))
        self.look_course_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
            QPushButton:pressed {
                background-color: #c69500;
            }
        """)
        self.look_course_button.clicked.connect(self.show_started_courses)
        self.layout.addWidget(self.look_course_button)

        # Кнопка для учебных материалов
        self.study_materials_button = QPushButton("Учебные материалы")
        self.study_materials_button.setFont(QFont("Arial", 14))
        self.study_materials_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a8e;
            }
            QPushButton:pressed {
                background-color: #00477a;
            }
        """)
        self.study_materials_button.clicked.connect(self.show_study_materials)
        self.layout.addWidget(self.study_materials_button)

        # Кнопка выхода
        self.exit_button = QPushButton('Выход')
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def show_schedule(self):
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString('yyyy-MM-dd')

        try:
            # Проверяем, что логин установлен
            if not self.login:
                self.schedule_label.setText("Текущий пользователь не найден.")
                return

            # Получаем расписание для выбранной даты и текущего пользователя
            schedules = self.db.cursor.execute(
                'SELECT subject, time_start, time_end FROM schedule WHERE date = ? AND login = ?',
                (date_str, self.login)
            ).fetchall()

            if schedules:
                schedule_info = "\n".join(
                    [f"{subject} ({time_start} - {time_end})" for subject, time_start, time_end in schedules]
                )
                self.schedule_label.setText(f"Расписание на {date_str}:\n{schedule_info}")
            else:
                self.schedule_label.setText(f"Расписание на {date_str} отсутствует.")

        except Exception as e:
            self.schedule_label.setText(f"Ошибка: {str(e)}")

    def show_profile(self):
        try:
            # Получаем данные пользователя по его логину
            user_data = self.db.get_user(self.login)
            if user_data:
                # user_data: (login, password, last_name, first_name, status)
                last_name, first_name = user_data[2], user_data[3]

                # Отображаем фамилию и имя в окне
                QMessageBox.information(self, "Личный кабинет", f"Фамилия: {last_name}\nИмя: {first_name}")
            else:
                QMessageBox.warning(self, "Ошибка", "Данные пользователя не найдены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def choose_course(self):
        # Окно для выбора курса
        self.choose_course_window = QWidget()
        self.choose_course_window.setWindowTitle('Выбор курса')
        self.choose_course_window.setGeometry(150, 150, 500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Заголовок окна
        header_label = QLabel("Выберите курс для изучения")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(header_label)

        # Таблица для отображения курсов
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(3)
        self.courses_table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание'])

        # Отключаем возможность редактировать данные в таблице
        self.courses_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Устанавливаем стиль таблицы
        self.courses_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 10px;
            }
            QTableWidget::item {
                padding: 12px;
                font-size: 14px;
                color: #333;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 12px;
                text-align: center;
            }
            QTableWidget::item:selected {
                background-color: #e8f5e9;
            }
        """)

        try:
            courses = self.db.get_all_courses()  # Получаем список всех курсов
            if not courses:
                QMessageBox.information(self.choose_course_window, 'Информация', 'Нет доступных курсов.')
            else:
                self.courses_table.setRowCount(len(courses))
                for row, course in enumerate(courses):
                    # course - это кортеж (id, name, description)
                    self.courses_table.setItem(row, 0, QTableWidgetItem(str(course[0])))  # ID
                    self.courses_table.setItem(row, 1, QTableWidgetItem(course[1]))  # Название
                    self.courses_table.setItem(row, 2, QTableWidgetItem(course[2]))  # Описание
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

        layout.addWidget(self.courses_table)

        # Поле для ввода ID выбранного курса
        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText('Введите ID выбранного курса')
        self.course_id_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        layout.addWidget(self.course_id_input)

        # Кнопка для подтверждения выбора
        self.submit_course_button = QPushButton('Выбрать курс')
        self.submit_course_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.submit_course_button.clicked.connect(self.submit_course_choice)
        layout.addWidget(self.submit_course_button)

        self.choose_course_window.setLayout(layout)
        self.choose_course_window.show()

    def submit_course_choice(self):
        try:
            # Получаем введённый ID курса
            course_id = self.course_id_input.text().strip()
            if not course_id.isdigit():
                QMessageBox.warning(self.choose_course_window, 'Ошибка', 'Введите корректный ID курса.')
                return

            course_id = int(course_id)

            # Проверяем, изучает ли пользователь уже этот курс
            if self.db.is_course_in_progress_by_login(self.login, course_id):
                QMessageBox.information(self.choose_course_window, 'Информация', 'Этот курс уже изучается.')
            else:
                # Добавляем курс в список изучаемых
                self.db.enroll_user_in_course_by_login(self.login, course_id)
                QMessageBox.information(self.choose_course_window, 'Успех', 'Курс успешно добавлен в ваш список.')
                self.choose_course_window.close()

        except Exception as e:
            QMessageBox.warning(self.choose_course_window, 'Ошибка', str(e))

    def show_started_courses(self):
        try:
            # Получаем список курсов, которые студент выбрал
            courses = self.db.get_student_courses(self.login)

            if not courses:
                QMessageBox.information(self, 'Информация', 'Вы не начали ни одного курса.')
                return

            # Создание окна для отображения курсов
            self.courses_window = QWidget()
            self.courses_window.setWindowTitle('Начатые курсы')
            self.courses_window.setGeometry(150, 150, 500, 400)

            layout = QVBoxLayout()
            layout.setSpacing(20)  # Пространство между элементами

            # Заголовок окна
            header_label = QLabel("Список начатых курсов")
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setFont(QFont("Arial", 18, QFont.Bold))
            layout.addWidget(header_label)

            # Список для отображения курсов
            self.courses_list = QListWidget()
            self.courses_list.setStyleSheet("""
                QListWidget {
                    background-color: #ffffff;
                    border-radius: 10px;
                    border: 1px solid #e0e0e0;
                    padding: 15px;
                }
                QListWidget::item {
                    padding: 12px;
                    font-size: 14px;
                    color: #333333;
                    border-bottom: 1px solid #e0e0e0;
                }
                QListWidget::item:selected {
                    background-color: #e0f7fa;
                }
            """)

            for course in courses:
                # courses - это список кортежей вида (id, name, description)
                course_info = f"ID: {course[0]} - {course[1]}\nОписание: {course[2]}"
                self.courses_list.addItem(course_info)

            # Обработчик выбора курса
            self.courses_list.itemClicked.connect(self.on_course_selected)

            layout.addWidget(self.courses_list)

            # Кнопка для закрытия окна
            self.close_button = QPushButton("Закрыть")
            self.close_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                    font-size: 16px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #388e3c;
                }
            """)
            self.close_button.clicked.connect(self.courses_window.close)
            layout.addWidget(self.close_button)

            self.courses_window.setLayout(layout)
            self.courses_window.show()

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

    def on_course_selected(self, item):
        try:
            # Получаем выбранный курс
            course_info = item.text().split("\n")
            # Извлекаем только цифры из строки 'ID: 1-Python'
            course_id_str = course_info[0].split(":")[1].strip()  # Получаем '1-Python'
            self.current_course_id = int(course_id_str.split('-')[0])  # Берем только числовую часть перед дефисом

            # Получаем темы, связанные с этим курсом
            topics = self.db.get_topics_by_course(self.current_course_id)

            if not topics:
                QMessageBox.information(self, 'Информация', 'У этого курса нет доступных тем.')
                return

            # Создание окна для отображения тем
            self.topics_window = QWidget()
            self.topics_window.setWindowTitle('Темы курса')
            self.topics_window.setGeometry(150, 150, 500, 400)

            layout = QVBoxLayout()

            # Список для отображения тем
            self.topics_list = QListWidget()

            for topic in topics:
                # topics - это список кортежей вида (id, course_id, name, content)
                self.topics_list.addItem(topic[2])  # Добавляем только название темы

            # Обработчик выбора темы
            self.topics_list.itemClicked.connect(self.on_topic_selected)

            layout.addWidget(self.topics_list)

            # Кнопка для закрытия окна
            self.close_button = QPushButton("Закрыть")
            self.close_button.clicked.connect(self.topics_window.close)
            layout.addWidget(self.close_button)

            self.topics_window.setLayout(layout)
            self.topics_window.show()

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

    def on_topic_selected(self, item):
        try:
            # Получаем выбранную тему
            topic_name = item.text()

            # Получаем подробную информацию о теме
            topics = self.db.get_topics_by_course(self.current_course_id)
            topic = next((t for t in topics if t[2] == topic_name), None)  # Ищем тему по названию

            if not topic:
                QMessageBox.warning(self, 'Ошибка', 'Выбранная тема не найдена.')
                return

            content = topic[3]  # Содержимое темы

            # Отображаем содержимое темы в окне сообщения
            QMessageBox.information(self, 'Содержание темы', content)

        except Exception as e:
            QMessageBox

    def show_study_materials(self):
        try:
            materials = self.db.get_all_study_materials()  # Получаем все материалы

            if not materials:
                QMessageBox.warning(self, 'Ошибка', 'Нет доступных учебных материалов.')
                return

            self.materials_window = QWidget()  # Сохраняем ссылку на окно
            self.materials_window.setWindowTitle('Учебные материалы')
            self.materials_window.setGeometry(100, 100, 600, 400)

            layout = QVBoxLayout()
            layout.setSpacing(20)  # Пространство между элементами

            # Заголовок окна
            header_label = QLabel("Доступные учебные материалы")
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setFont(QFont("Arial", 18, QFont.Bold))
            layout.addWidget(header_label)

            # Инициализация таблицы, показываем только название
            self.materials_table = QTableWidget()
            self.materials_table.setColumnCount(1)  # Показываем только один столбец
            self.materials_table.setHorizontalHeaderLabels(['Название'])  # Заголовок только для названия

            # Устанавливаем стиль таблицы
            self.materials_table.setStyleSheet("""
                QTableWidget {
                    background-color: #ffffff;
                    border-radius: 8px;
                    border: 1px solid #e0e0e0;
                    padding: 10px;
                }
                QTableWidget::item {
                    padding: 10px;
                    font-size: 14px;
                    color: #333333;
                }
                QTableWidget::item:hover {
                    background-color: #f5f5f5;
                }
                QTableWidget::item:selected {
                    background-color: #b2ebf2;
                }
                QHeaderView::section {
                    background-color: #0078d7;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                }
            """)

            # Устанавливаем количество строк в таблице
            self.materials_table.setRowCount(len(materials))

            # Заполняем таблицу только названиями файлов
            for row, material in enumerate(materials):
                self.materials_table.setItem(row, 0, QTableWidgetItem(material[2]))  # Отображаем только file_name

            layout.addWidget(self.materials_table)

            # Подключаем обработчик клика на строку
            self.materials_table.cellClicked.connect(self.download_material)

            self.materials_window.setLayout(layout)
            self.materials_window.show()  # Показываем окно

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f"Произошла ошибка при загрузке материалов: {e}")

    def download_material(self, row, column):
        try:
            # Получаем данные о материале по строке
            material = self.db.get_all_study_materials()[row]  # Получаем данные из базы
            file_name = material[2]  # Название файла
            file_path = material[3]  # Путь к файлу на сервере или локальной системе

            # Открываем диалог для сохранения файла на компьютер
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", file_name)

            if save_path:
                # Копируем файл в выбранное место
                import shutil
                shutil.copy(file_path, save_path)  # Копируем файл по новому пути
                QMessageBox.information(self, 'Успех', f'Файл "{file_name}" успешно сохранен!')

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f"Произошла ошибка при скачивании материала: {e}")

