import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QTextEdit, QPushButton, QTextBrowser
from methods import local_test, full_test

class AppInterface(QWidget):

    ids_list = []

    def __init__(self):
        super().__init__()
        self.input_ids = QTextEdit()
        self.output = QTextBrowser()
        self.initUI()

    def initUI(self):

        task = QLabel("Введите id пользователей для анализа")

        local = QPushButton("Анализ стены")
        full = QPushButton("Анализ ленты")

        grid = QVBoxLayout()

        grid.addWidget(task)
        grid.addWidget(self.input_ids)
        grid.addWidget(local)
        grid.addWidget(full)
        grid.addWidget(self.output)

        self.setLayout(grid)

        self.setGeometry(200, 200, 400, 600)
        self.setWindowTitle("PsychoAnalyser v0.5")

        local.clicked.connect(self.run_local_test)
        full.clicked.connect(self.run_full_test)

        self.show()

    def run_local_test(self):
        self.ids_list = self.input_ids.toPlainText().split('\n')
        self.output.clear()
        self.output.append("Запущен тест стены пользователей\n")
        self.output.append(local_test(self.ids_list))

    def run_full_test(self):
        self.ids_list = self.input_ids.toPlainText().split('\n')
        self.output.clear()
        self.output.append("Запущен полный тест ленты пользователей(анализ друзей и групп пользователя\n")
        self.output.append(full_test(self.ids_list))


def main():

    app = QApplication(sys.argv)
    gui = AppInterface()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
