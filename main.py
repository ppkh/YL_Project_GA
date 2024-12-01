import sys
import csv

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QFileDialog, QMenuBar, QMenu, \
    QHeaderView
from PyQt6.QtGui import QAction


class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_ui.ui', self)
        self.setWindowTitle('Учет доходов-расходов')
        self.menubar = self.findChild(QMenuBar, 'menubar')
        self.filemenu = self.findChild(QMenu, 'menuFile')
        self.editmenu = self.findChild(QMenu, 'menuEdit')
        self.main_table = self.findChild(QTableWidget, "main_table")
        self.open_button = self.findChild(QAction, "Open_file")
        self.new_button = self.findChild(QAction, "New_file")
        self.save_options = self.findChild(QMenu, "menuSave_as")
        self.save_csv_button = self.findChild(QAction, "save_as_csv")
        self.save_txt_button = self.findChild(QAction, "save_as_txt")
        self.save_button = self.findChild(QAction, "Save")
        self.add_row = self.findChild(QAction, "Add_row")
        self.remove_row = self.findChild(QAction, "Remove_row")
        try:
            with open('cache/cache.txt', "r", encoding="utf-8") as f:
                txt = f.read()
                self.loadTable(txt)
                self.setWindowTitle(f"Подсчет доходов-расходов - {txt.split('/')[-1]}")
        except Exception:
            self.loadTable('C:/Users/amirg/PycharmProjects/AGProject/files/default.csv')
            self.setWindowTitle(f"Подсчет доходов-расходов - {txt.split('/')[-1]}")
        self.init()

    def init(self):
        self.open_button.triggered.connect(self.open_file)
        self.new_button.triggered.connect(self.new_file)
        self.add_row.triggered.connect(self.add_new_row)
        self.remove_row.triggered.connect(self.remove_last_row)
        self.save_button.triggered.connect(self.save)
        self.main_table.itemChanged.connect(self.calculate)
        self.save_csv_button.triggered.connect(self.save_table_as_csv)
        self.save_txt_button.triggered.connect(self.save_table_as_txt)

    def calculate(self):
        totalincome = []
        totaloutgo = []
        total = []
        self.main_table.blockSignals(True)
        for row in range(self.main_table.rowCount()):
            income = self.main_table.item(row, 1).text()
            outgo = self.main_table.item(row, 2).text()
            try:
                if income:
                    income = float(income)
                else:
                    income = 0
                totalincome.append(income)
                if outgo:
                    outgo = float(outgo)
                else:
                    outgo = 0
                totaloutgo.append(outgo)
                result = income - outgo
                total.append(result)
                self.main_table.setItem(row, 3, QTableWidgetItem(str(result)))
            except ValueError:
                self.statusBar().showMessage("Value error")

        self.main_table.blockSignals(False)
        self.save()

    def save(self):
        self.main_table.blockSignals(True)
        with open("cache/cache.txt", "r", encoding="utf8") as f:
            txt = f.read()
            fname = txt
            self.setWindowTitle(f"Подсчет доходов-расходов - {txt.split('/')[-1]}")
        self.saveTable(fname)
        self.main_table.blockSignals(False)

    def add_new_row(self):
        self.main_table.blockSignals(True)
        self.main_table.setRowCount(self.main_table.rowCount() + 1)
        for i in range(self.main_table.columnCount()):
            self.main_table.setItem(
                self.main_table.rowCount() - 1, i, QTableWidgetItem())
        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_table.blockSignals(False)

    def remove_last_row(self):
        self.main_table.blockSignals(True)
        if self.main_table.rowCount() > 0:
            self.main_table.removeRow(self.main_table.rowCount() - 1)
        self.main_table.blockSignals(False)

    def save_table_as_csv(self):
        self.main_table.blockSignals(True)
        fname = QFileDialog.getSaveFileName(self, 'Choose file', "",
                                            'Таблица (*.csv);;Все файлы (*)')[0]
        if fname:
            self.saveTable(fname)
        self.main_table.blockSignals(False)

    def save_table_as_txt(self):
        self.main_table.blockSignals(True)
        fname = QFileDialog.getSaveFileName(self, 'Choose file', "",
                                            'Текстовый файл (*.txt);;Все файлы (*)')[0]
        if fname:
            self.saveTable(fname)
        self.main_table.blockSignals(False)

    def open_file(self):
        self.main_table.blockSignals(True)
        fname = \
            QFileDialog.getOpenFileName(self, 'Choose file', '',
                                        'Текстовый файл (*.txt);;Таблица (*.csv);;Все файлы (*)')[0]
        if fname:
            self.loadTable(fname)
            self.setWindowTitle(f"Подсчет доходов-расходов - {fname.split('/')[-1]}")
        self.main_table.blockSignals(False)

    def new_file(self):
        self.main_table.blockSignals(True)
        fname = QFileDialog.getSaveFileName(self, 'Choose file', "",
                                            'Текстовый файл (*.txt);;Таблица (*.csv);;Все файлы (*)')[0]
        with open(fname, 'w', encoding="utf-8") as file:
            with open("files/default.csv", 'r', encoding='utf8') as default:
                read = default.read()
                file.write(read)
        if fname:
            self.setWindowTitle(f"Подсчет доходов-расходов - {fname.split('/')[-1]}")
            self.loadTable(fname)
        self.main_table.blockSignals(False)

    def loadTable(self, table_name):
        self.main_table.blockSignals(True)
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader)
            self.main_table.setColumnCount(len(title))
            self.main_table.setHorizontalHeaderLabels(title)
            self.main_table.setRowCount(0)
            for i, row in enumerate(reader):
                self.main_table.setRowCount(
                    self.main_table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.main_table.setItem(
                        i, j, QTableWidgetItem(elem))
            # for o in range(self.main_table.columnCount()):
            #    self.main_table.item(i, o).setFlags(QtCore.Qt.ItemFlag.ItemIsEditable)
        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        with open("cache/cache.txt", "w", encoding="utf8") as f:
            f.write(table_name)
        self.main_table.blockSignals(False)

    def saveTable(self, filename):
        self.main_table.blockSignals(True)
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [self.main_table.horizontalHeaderItem(i).text()
                 for i in range(self.main_table.columnCount())])
            for i in range(self.main_table.rowCount()):
                row = []
                for j in range(self.main_table.columnCount()):
                    item = self.main_table.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)
        self.main_table.blockSignals(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Notebook()
    ex.show()
    sys.exit(app.exec())
