from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import sqlite3 as sl




#Подключение к бд
con = sl.connect("phonebook.db")


class addedit_form(QMainWindow):
    def __init__(self, parent=None):
        super(addedit_form, self).__init__(parent)
        self.parent = parent
        uic.loadUi('add_edit.ui', self)
        self.cancel_button.clicked.connect(self.mainshow)
        self.save_button.clicked.connect(self.Save)
        self.idusers = 0

    def Save(self):
        savecur = con.cursor()
        if int(self.idusers) > 0:
           sql = f"update users set fam='{self.fam_edit.text()}',name='{self.name_edit.text()}', otch='{self.otch_edit.text()}', phone='{self.phone_edit.text()}' where id='{int(self.idusers)}'"
        else:
           sql = f"insert into users (fam, name, otch, phone) values('{self.fam_edit.text()}', '{self.name_edit.text()}', '{self.otch_edit.text()}', '{self.phone_edit.text()}')"
        savecur.execute(sql)
        con.commit()
        savecur.close()
        self.mainshow()

    def mainshow(self):
        self.parent.seldb()
        self.idz = 0
        self.close()
