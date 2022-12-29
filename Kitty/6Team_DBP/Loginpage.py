#기태가 만드는 로그인 페이지
import sqlite3
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

form_class = uic.loadUiType('./login.ui')[0]


class Login(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.Signal_login = False
        self.INFO_login = []
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        # 커서 획득
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS MEMBERINFO (NAME TEXT, ID TEXT, PASSWORD TEXT,PHONE TEXT, ADDRESS TEXT\
                    QUESTION TEXT, ANSWER TEXT)")
        c.close()
        self.checkStatus = False        # 회원가입페이지-중복확인 시 필요
        self.setupUi(self)
        self.id_lineEdit.setText("") # 아무것도입력안할시 오류나서 미리 설정해둠.
        self.login_SW.setCurrentIndex(0)        # 스택위젯
        self.login_Button.clicked.connect(self.Login_Check)        # 로그인페이지-로그인버튼
        self.signup_Button.clicked.connect(self.MoveSignupPage)     # 로그인페이지-회원가입버튼
        self.Home1_Button.clicked.connect(self.MoveMainPage)        # 로그인페이지-홈버튼
        self.Home2_Button.clicked.connect(self.MoveMainPage)        # 회원가입페이지-홈버튼
        self.Home3_Button.clicked.connect(self.MoveMainPage)        # 회원가입페이지-홈버튼
        self.Home4_Button.clicked.connect(self.MoveMainPage)        # 회원가입페이지-홈버튼
        self.join_Button.clicked.connect(self.Sign_Up)              # 회원가입페이지-가입하기버튼
        self.duplication_Button.clicked.connect(self.Double_Check)  # 회원가입페이지-중복확인버튼
        self.idFind_Button.clicked.connect(self.MovefindIDPage)
        self.pwFind_Button.clicked.connect(self.MovefindPWPage)
        self.IDfind_Execute.clicked.connect(self.findID)
        self.PWfind_Execute.clicked.connect(self.findPW)
        # 숫자만 입력 받게하기 위해 추가
        self.onlyInt = QIntValidator()
        self.phone_lineEdit.setValidator(self.onlyInt)      # self. 다음에 적용할 lineEdit 객체명으로 변경
        self.id_lineEdit.textChanged.connect(self.Double_change) #중복체크하고 아이디 바꿀시 다시 중복체크하도록 바꿈.


    def MoveMainPage(self):     # 메인페이지로 이동하는 함수
        self.login_SW.setCurrentIndex(0)
    def MovefindIDPage(self):     # 메인페이지로 이동하는 함수
        self.login_SW.setCurrentIndex(2)
    def MovefindPWPage(self):     # 메인페이지로 이동하는 함수
        self.login_SW.setCurrentIndex(3)
    def MoveSignupPage(self):       # 회원가입 페이지로 이동하는 함수
        self.login_SW.setCurrentIndex(1)
        self.id_lineEdit.clear()
        self.pw_lineEdit.clear()
        self.pw2_lineEdit.clear()
        self.name_lineEdit.clear()
        self.phone_lineEdit.clear()
        self.address_lineEdit.clear()
        self.answer_lineEdit.clear()


    # 아이디 찾기
    def findID(self):
        Name = self.lE_findName.text()
        Phonenumber = self.lE_findPhone.text()
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        # 커서 획득
        c = conn.cursor()
        c.execute(f"SELECT * FROM MEMBERINFO WHERE NAME = '{Name}' AND  PHONE = '{Phonenumber}'")
        memberinfo = c.fetchall()
        c.close()
        if memberinfo == []:
            self.DisplayID.setText(f"일치하는 회원 정보가 없습니다")
        else:
            self.DisplayID.setText(f"아이디는 {memberinfo[0][1]}입니다")
        self.lE_findName.clear()
        self.lE_findPhone.clear()

    #비밀번호 찾기
    def findPW(self):
        ID = self.lE_findID.text()
        Question = self.CB_findQuestion.currentText()
        Answer = self.lE_findAnswer.text()
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        # 커서 획득
        c = conn.cursor()
        c.execute(f"SELECT * FROM MEMBERINFO WHERE ID = '{ID}' AND  QUESTION = '{Question}' \
                    AND  ANSWER = '{Answer}'")
        CheckPW = c.fetchall()
        print(CheckPW)
        c.close()
        if CheckPW == []:
            self.DisplayPW.setText(f"일치하는 회원 정보가 없습니다")
        else:
            self.DisplayPW.setText(f"비밀번호는 {CheckPW[0][2]}입니다")
        self.lE_findID.clear()
        self.lE_findAnswer.clear()
    # 회원가입 함수
    def Double_Check(self):         # 회원가입 페이지-중복 확인하는 함수
        user = self.id_lineEdit.text()  # id_lineEdit에 입력되는 텍스트
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT * FROM MEMBERINFO WHERE ID = "{user}"')
        memberlist = c.fetchall()
        c.close()
        if memberlist == [] :
            QMessageBox.information(self, "알림", "사용 가능한 아이디")
            self.checkStatus = True
        else :
            QMessageBox.critical(self, "알림", "아이디 중복")
    def Double_change(self):
        self.checkStatus = False

    def Sign_Up(self):
        id = self.id_lineEdit.text()        # lineEdit에 입력받은 데이터
        pw1 = self.pw_lineEdit.text()
        pw2 = self.pw2_lineEdit.text()
        name = self.name_lineEdit.text()
        phone = self.phone_lineEdit.text()
        address = self.address_lineEdit.text()
        question = self.Question.currentText()
        answer = self.answer_lineEdit.text()
        user = (name, id, pw1, phone, address,question,answer)      # 정보 저장 순서
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        c = conn.cursor()
        # 회원가입 시 필요한 조건
        if pw1 != pw2:
            QMessageBox.critical(self, "알림", "비밀번호가 일치하지 않습니다. 다시 확인해주세요")
        elif self.checkStatus == False:
            QMessageBox.critical(self, "알림", "아이디 중복 확인이 안 되어있습니다")
        elif id == '' or pw1 == '' or name == '' or phone == '' or address == '':
            QMessageBox.critical(self, "알림", "정보를 입력하세요")
        else:
            c.execute(f'INSERT INTO MEMBERINFO(NAME,ID,PASSWORD,PHONE,ADDRESS,QUESTION,ANSWER) \
                        VALUES (?,?,?,?,?,?,?)', user)
            c.close()
            QMessageBox.information(self, "알림", "회원가입 됐습니다")
            self.login_SW.setCurrentIndex(1)
            #Line_edit에 입력 받은 값 지워주기
            self.id_lineEdit.clear()
            self.pw_lineEdit.clear()
            self.pw2_lineEdit.clear()
            self.name_lineEdit.clear()
            self.phone_lineEdit.clear()
            self.address_lineEdit.clear()
            self.answer_lineEdit.clear()

    # 로그인
    def Login_Check (self):

        if self.login_id_lineEdit.text() == "":
            QMessageBox.critical(self, "로그인 오류", "정보를 입력하세요")
            return
        self.id = self.login_id_lineEdit.text() # 원래는 id엿지만 메인페이지에서 id의 정보를 불러오기 위해 self.을 붙여줬다 (기태)
        pw = self.login_pw_lineEdit.text()
        logined = 0
        print("self.id")
        conn = sqlite3.connect("MemberInfo.db", isolation_level=None)
        c = conn.cursor()
        print("pw")
        c.execute(f"SELECT * FROM MEMBERINFO WHERE ID = '{self.id}' AND PASSWORD = '{pw}'")
        self. INFO_login = c.fetchall()



        if self.id not in self. INFO_login[0]:
            logined = 1
        elif pw not in self. INFO_login[0]:
            logined = 2
        else:
            logined = 3

        if logined == 1:
            QMessageBox.critical(self, "로그인 오류", "ID 정보가 없습니다. 회원가입 해주세요")
        elif logined == 2:
            QMessageBox.critical(self, "로그인 오류", "비밀번호를 다시 입력하세요")
        elif pw == '':
            QMessageBox.critical(self, "로그인 오류", "비밀번호를 입력하세요")
        else:
            self.Signal_login = True
            self.close()
            return True    # 로그인 성공





if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    mainWindow = Login()

    widget.addWidget(mainWindow)

    widget.setFixedHeight(600)
    widget.setFixedWidth(600)
    widget.show()
    app.exec_()