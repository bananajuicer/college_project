import sys
from PyQt5.QtWidgets import QApplication
from db import DB
from star import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DB()

    if not db.user_exists('admin'):
        db.add_user('admin', 'admin', 'Babkina', 'Helen', 'admin')

    login = ''
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())



