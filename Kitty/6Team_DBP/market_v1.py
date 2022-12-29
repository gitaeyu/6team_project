import sqlite3
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys

from Login import Login

class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("maintest.ui", self)
        self.ui.show()

        content = sqlite3.connect("SHOP_DB.db", isolation_level=None)
        self.point = content.cursor()
        self.codeData = pd.read_csv('분류코드표.csv', encoding='cp949')
        self.codeData = pd.DataFrame(self.codeData)

        self.Page_login = Login()
        self.bt_loginout.clicked.connect(self.login_select)
        self.Page_login.login_Button.clicked.connect(self.update)
        self.bt_d_select.stateChanged.connect(self.move_detail_search)

        self.cb_select_d_code1.currentTextChanged.connect(self.search_comboadd)

    def move_detail_search(self):
        if self.bt_d_select.isChecked() == True:
            self.st_search_select.setCurrentIndex(1)
        else:
            self.st_search_select.setCurrentIndex(0)

    def search_comboadd(self):
        self.cb_select_d_code2.clear()
        self.cb_select_d_code2.addItem('중분류')
        addlist=self.codeData[['중분류코드','중분류명']].drop_duplicates()           #중복제거
        temp = addlist[addlist['중분류코드'].str.contains(str(self.cb_select_d_code1.currentText()[0]))]
        print(len(temp['중분류코드']))
        for i,j in zip(temp['중분류코드'],temp['중분류명']):
            self.cb_select_d_code2.addItem(i + '-' + j)

    def login_select(self):
        if self.Page_login.Signal_login == False:
            self.Page_login.show()
        elif self.Page_login.Signal_login == True:
            self.Page_login.Signal_login = False
            self.bt_loginout.setText('로그인')
            self.lb_UserName.clear()

    def update(self):
        if self.Page_login.Signal_login:
            self.bt_loginout.setText('로그아웃')
            self.lb_UserName.setText(str(self.Page_login.INFO_login[0][0])+'님 환영합니다.')


app = QtWidgets.QApplication(sys.argv)
me = MyApp()
sys.exit(app.exec())

