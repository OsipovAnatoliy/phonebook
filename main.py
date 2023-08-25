from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableView, QMessageBox
import re
import requests
import sys
from add_edit import addedit_form
import sqlite3 as sl


#Подключение к бд
con = sl.connect("phonebook.db")
cur = con.cursor()


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         fam TEXT,
         name TEXT,
         otch TEXT,
         phone TEXT
         )""")
    con.commit()



#Основная форма
class App(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi('main.ui', self)
        create_table()
        self.seldb()
        self.idusers = 0
        self.aeu = addedit_form(self)
        self.add_button.clicked.connect(self.add_users)
        self.edit_button.clicked.connect(self.edit_users)
        self.delete_button.clicked.connect(self.delete_user)
        self.table.clicked.connect(self.onLeftClick)
        self.find_edit.textChanged.connect(self.seldb)
        self.reset_find.clicked.connect(self.resetfind)

#Сброс поиска
    def resetfind(self):
        self.find_edit.setText('')

#Удалить заявку
    def delete_user(self):
        qm = QtWidgets.QMessageBox
        if int(self.idusers) > 0:
           delcur = con.cursor()
           sql = f"select * from users where id='{self.idusers}'"
           delcur.execute(sql)
           record = delcur.fetchone()
           req = qm.question(self,'', f"Удалить пользователя: {record[1]} {record[2]} {record[3]}?", qm.Yes | qm.No)
           if req == qm.Yes:
             sql_q = f"delete from users where id='{self.idusers}'"
             delcur.execute(sql_q)
             con.commit()
             delcur.close()
           self.seldb()
        else:
           req = qm.question(self,'', f"Выберите, пожалуйста пользователя?", qm.Ok)

#Левая кнопка мыши по таблице
    def onLeftClick(self):
         self.table.setSortingEnabled(True)
         rows = sorted(set(index.row() for index in
                       self.table.selectedIndexes()))
         item = self.table.item(rows[0], 0)
         self.idusers = item.text()

#Новый user
    def add_users(self):
        self.aeu.idusers = 0
        self.aeu.fam_edit.setText('')
        self.aeu.name_edit.setText('')
        self.aeu.otch_edit.setText('')
        self.aeu.phone_edit.setText('')
        self.aeu.show()

#Редактирование user
    def edit_users(self):
        qm = QtWidgets.QMessageBox
        if int(self.idusers) > 0:
          editcur = con.cursor()
          sql = "select * from users where id=\'"+str(self.idusers)+"\'"
          editcur.execute(sql)
          record = editcur.fetchone()
          self.aeu.idusers = record[0]
          self.aeu.fam_edit.setText(record[1])
          self.aeu.name_edit.setText(record[2])
          self.aeu.otch_edit.setText(record[3])
          self.aeu.phone_edit.setText(record[4])
          self.aeu.show()
          editcur.close()
        else:
          req = qm.question(self,'', f"Выберите, пожалуйста пользователя?", qm.Ok)


#Выбор данных из бд
    def seldb(self):
        self.cur = con.cursor()
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setGeometry(10, 100, 570, 500)
        self.table.setStyleSheet("background-color: white;"
                                 "border: 1px solid black;"
                                 "gridline-color: black;"
                                 "font-size: 12px;")
                                 # "selection-background-color: qlineargradient(x1: 0,"
                                 # " y1: 0, x2: 0.5, y2: 0.5, stop: 0 grey, stop: 1 white)")


        self.table.setColumnCount(5)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setHorizontalHeaderLabels(['id','Фамилия','Фамилия', 'Имя', 'Отчество', 'Телефон']) # заголовки столцов
        sel = "select * from users"
        if len(str(self.find_edit.text())) > 0:
            find = self.find_edit.text()
            sqlsel = f"{sel} where fam LIKE '%{find}%' or name LIKE '%{find}%' or otch LIKE '%{find}%' or phone LIKE '%{find}%'"
        else:
            sqlsel = sel
        self.cur.execute(sqlsel)
        rows = self.cur.fetchall()
        i = 0
        for elem in rows:
            self.table.setRowCount(self.table.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.table.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.table.resizeColumnsToContents()
        self.table.setColumnHidden(0, True);
        self.cur.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
