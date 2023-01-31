import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QTextEdit, QPushButton, QTextBrowser
from methods import local_test, full_test
from excel_view import to_db

class AppInterface(QWidget):

    ids_list = []
    totals = []

    def __init__(self):
        super().__init__()
        self.input_ids = QTextEdit()
        self.output = QTextBrowser()
        self.initUI()

    def initUI(self):

        task = QLabel("Введите id пользователей для анализа")

        local = QPushButton("Анализ стены")
        full = QPushButton("Анализ ленты")
        to_ex = QPushButton("Вывести в Excel")

        grid = QVBoxLayout()

        grid.addWidget(task)
        grid.addWidget(self.input_ids)
        grid.addWidget(local)
        grid.addWidget(full)
        grid.addWidget(to_ex)
        grid.addWidget(self.output)

        self.setLayout(grid)

        self.setGeometry(200, 200, 400, 600)
        self.setWindowTitle("PsychoAnalyser v0.5")

        local.clicked.connect(self.run_local_test)
        full.clicked.connect(self.run_full_test)
        to_ex.clicked.connect(self.to_excel)

        self.show()

    def run_local_test(self):
        self.ids_list = self.input_ids.toPlainText().split('\n')
        self.output.clear()
        self.output.append("Запущен тест стены пользователей\n")
        res = local_test(self.ids_list)
        self.totals.append(res[0])
        self.output.append(res[1])

    def run_full_test(self):
        self.ids_list = self.input_ids.toPlainText().split('\n')
        self.output.clear()
        self.output.append("Запущен полный тест ленты пользователей(анализ друзей и групп пользователя\n")
        res = full_test(self.ids_list)
        self.totals.append(res[0])
        self.output.append(res[1])

    def to_excel(self):
        to_db(self.totals)
        self.output.append("Резудльтаты перенесены в файл PsychoReader.xlsx")


def main():

    app = QApplication(sys.argv)
    gui = AppInterface()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
