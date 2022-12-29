import sys
import csv
import sqlite3

from PyQt5 import QtCore
from PyQt5.QtCore import QDate, QCoreApplication
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic

# from ReviewPage import ReviewPage

form_kwangju=uic.loadUiType("searching_restaurant.ui")[0]

class Kwangju_Restaurant(QWidget,form_kwangju):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        con = sqlite3.connect("Shop2.db.")
        c = con.cursor()
        c.execute("SELECT*FROM Gwangju")
        kwangju = c.execute("SELECT*FROM Gwangju")
        self.kwangju_list=c.fetchall()
        self.set_data=[]
        del self.kwangju_list[0]
        for i in self.kwangju_list:
            self.set_data.append(i[4])
        self.set_data=set(self.set_data)
        con.commit()
        con.close()
        self.big_comboBox.currentTextChanged.connect(self.secondbox)
        self.searching_btn.clicked.connect(self.searching_data)
        self.searching_lineEdit.returnPressed.connect(self.searching_data)#엔터누르면 검색어 검색기능 실행
        self.cancel_btn.clicked.connect(self.cancel)
        self.store_table.setEditTriggers(QAbstractItemView.NoEditTriggers) ## 태이블 위젯 셀 내용 수정 불가
        self.searching_lineEdit.setPlaceholderText("검색어를 입력하세요") # PlaceholerText "검색어를 입력하세요" 라인에딧에 플레이스홀더 입력
    #     self.store_table.doubleClicked.connect(self.go_reviewsite)
    #
    # def go_reviewsite(self):
    #     if self.Signal_login == False:
    #         QMessageBox.critical(self, "", "로그인 후 이용해주세요")
    #         return
    #     self.review = ReviewPage()
    #     self.selectrow = self.store_table.currentIndex().row()
    #     print(self.data_list[self.selectrow])
    #     self.review.user_restaurant_info = [self.INFO_user, self.data_list[0][0]]
    #     print([self.INFO_user, self.data_list[0][0]])
    #     # self.review.show()

    def cancel(self): ## 현재창 닫기
        self.close()

    def secondbox(self):
    # 상권업종중분류명 comboBox에 addItems
        if self.big_comboBox.currentText()=='상권업종대분류명':
            self.middle_comboBox.clear()
        elif self.big_comboBox.currentText()=='부동산':
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['부동산중개','분양','평가/개발/관리'])
        elif self.big_comboBox.currentText()=='소매':
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['음/식료품소매','선물/팬시/기념품','종합소매점','취미/오락관련소매','의복의류','가방/신발/액세서리',
                                           '가정/주방/인테리어','사무/문구/컴퓨터','애견/애완/동물','건강/미용식품','유아용품',
                                           '가전제품소매','책/서적/도서','운동/경기용품소매','가구소매','화장품소매','예술품/골동품/수석/분재',
                                           '사진/광학/정밀기기소매','종교용품판매','의약/의료품소매','철물/난방/건설자재소매',
                                           '페인트/유리제품소매','자동차/자동차용품','중고품소매/교환','기타판매업','시계/귀금속소매'])
        elif self.big_comboBox.currentText()=="생활서비스":
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['세탁/가사서비스', '자동차/이륜차', '대행업', '장례/묘지', '법무세무회계', '기타서비스업',
                                           '대중목욕탕/휴게', '주택수리', '물품기기대여', '개인서비스', '주유소/충전소', '이/미용/건강',
                                           '개인/가정용품수리', '행사/이벤트', '운송/배달/택배', '예식/의례/관혼상제', '사진', '광고/인쇄', '인력/고용/용역알선'])
        elif self.big_comboBox.currentText()=="숙박":
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['호텔/콘도', '모텔/여관/여인숙', '캠프/별장/펜션', '유스호스텔', '민박/하숙'])
        elif self.big_comboBox.currentText()=="음식":
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['양식', '한식', '제과제빵떡케익', '음식배달서비스', '패스트푸드', '기타음식업', '커피점/카페',
                                           '유흥주점', '분식', '별식/퓨전요리', '중식', '부페', '닭/오리요리', '일식/수산물'])
        elif self.big_comboBox.currentText() == "학문/교육":
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['학원-어학', '학원-자격/국가고시', '학원-창업취업취미', '학문교육기타', '학원-보습교습입시',
                                           '학원-음악미술무용', '학원-예능취미체육', '학원기타', '학원-컴퓨터', '유아교육', '도서관/독서실'])
        elif self.big_comboBox.currentText() == "스포츠":
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['실외운동시설', '운영관리시설', '실내운동시설'])
        else:
            self.middle_comboBox.clear()
            self.middle_comboBox.addItems(['연극/영화/극장', '놀이/여가/취미', 'PC/오락/당구/볼링등', '경마/경륜/성인오락',
                                           '요가/단전/마사지', '스포츠/운동', '무도/유흥/가무'])


    def searching_data(self): # 검색 눌렀을때 테이블 위젯에 데이터 입력
        word1=self.gu_comboBox.currentText()  # 콤보박스 현재 텍스트
        word2=self.big_comboBox.currentText()
        word3=self.middle_comboBox.currentText()
        word4=self.searching_lineEdit.text() # 라인에디트 현재 텍스트


        data_list=[] # word1,word2,word3에 해당하는 data값 append하기 위해 빈 리스트 생성
        for i in self.kwangju_list:
            if word1 in i[7]:
                if word2 in i[3]:
                    if word3 in i[4]:
                        if word4 in i[1]:
                            data_list.append(i)
                        else:
                            pass
        ## 테이블위젯에 데이터 입력
        self.store_table.setRowCount(len(data_list))
        self.store_table.setColumnCount(12)
        for j in range(len(data_list)):
            for k in range(0, 12):
                self.store_table.setItem(j, k, QTableWidgetItem(str(data_list[j][k])))








if __name__=="__main__":
    app=QApplication(sys.argv)
    popup=Kwangju_Restaurant()
    popup.show()
    app.exec_()
