import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from user_student import StudentApp
from user_admin import AdminWindow
import re # библиотека для использования регулярных выражений
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Интерфейс окна авторизации
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_username = None  # Добавляем атрибут для хранения логина

        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Центрирование элементов

        label_font = QFont("Inter", 12)

        # Логин
        self.username_label = QLabel("Логин:")
        self.username_label.setFont(label_font)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите ваш логин")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Пароль
        self.password_label = QLabel("Пароль:")
        self.password_label.setFont(label_font)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Кнопка "Войти"
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        # Применяем макет к окну
        self.setLayout(layout)

        # Стилизация элементов через стили
        self.apply_styles()

    def apply_styles(self):
        # Общий стиль окна
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f9;  /* Светлый фон */
                color: #333333;  /* Основной цвет текста */
            }
            QLabel {
                color: #555555;  /* Цвет текста лейблов */
            }
            QLineEdit {
                background-color: #ffffff;  /* Белый фон */
                border: 1px solid #cccccc;  /* Легкая рамка */
                border-radius: 8px;  /* Закругленные углы */
                padding: 8px;  /* Внутренний отступ */
                font-size: 14px;  /* Размер шрифта */
            }
            QLineEdit:focus {
                border: 1px solid #5c9dff;  /* Цвет рамки при фокусе */
                outline: none;  /* Убираем стандартный фокус */
            }
            QPushButton {
                background-color: #5c9dff;  /* Голубая кнопка */
                color: #ffffff;  /* Белый текст */
                border: none;
                border-radius: 8px;  /* Закругленные углы */
                padding: 10px 15px;  /* Внутренние отступы */
                font-size: 14px;  /* Размер шрифта */
            }
            QPushButton:hover {
                background-color: #4a8ce0;  /* Темнее при наведении */
            }
            QPushButton:pressed {
                background-color: #3a7ac2;  /* Еще темнее при клике */
            }
        """)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Проверка на пустые поля
        if not username or not password:
            QMessageBox.warning(self, "Ошибка ввода", "Логин и пароль не могут быть пустыми!")
            return
        # Проверка на недопустимые символы
        username_pattern = r"^[a-zA-Z0-9_.-]+$"  # Логин: латиница, цифры, _, ., -
        password_pattern = r"^[a-zA-Z0-9@#$%^&+=]+$"  # Пароль: латиница, цифры, спецсимволы @#$%^&+=
        if not re.match(username_pattern, username):
            QMessageBox.warning(self, "Ошибка ввода",
                                "Логин может содержать только латинские буквы, цифры, точки, дефисы и символы подчёркивания!")
            return
        if not re.match(password_pattern, password):
            QMessageBox.warning(self, "Ошибка ввода",
                                "Пароль может содержать только латинские буквы, цифры и символы @#$%^&+=!")
            return
        try:
            conn = sqlite3.connect('education_system.db')
            cursor = conn.cursor()
            cursor.execute('SELECT status FROM user WHERE login=? AND password=?', (username, password))
            user = cursor.fetchone()
            if user:
                status = user[0]  # Получаем статус
                self.current_username = username  # Сохраняем логин в атрибуте
                if status == 'admin':
                    QMessageBox.information(self, "Успех", "Вы вошли как администратор!")
                    self.window_admin = AdminWindow()
                    self.window_admin.show()
                    self.close()
                elif status == 'student':
                    QMessageBox.information(self, "Успех", "Вы вошли как студент!")
                    self.window_user = StudentApp(self.current_username)
                    self.window_user.show()
                    self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Ошибка при доступе к базе данных: {e}")

