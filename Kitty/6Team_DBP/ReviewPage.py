import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# 리뷰 페이지 클래스
class ReviewPage(QWidget):

    def __init__(self):
        super().__init__()
        # 외부에서 받아올 유저, 레스토랑 정보[유저 id, 레스토랑 상가업소번호]
        # 리뷰 평점
        self.review_score = 0
        # 메인에서 받아올 유저와 식당 정보
        self.user_restaurant_info = []
        # 리뷰에 필요한 정보 저장용 리스트
        self.save_review = []
        # 임의의 값 입력 -------------------------------------------------------추후 삭제할 것
        self.user_restaurant_info = ['selfishracer', '25195570']

        # ui 세팅
        self.set_ui()
        self.review_ui()

        # 프로그램 세팅
        self.setWindowTitle('리뷰')
        self.setGeometry(0, 0, 800, 600)
        self.show()

    # 공통 ui 설정
    def set_ui(self):
        self.set_button()

    # 버튼 세팅
    def set_button(self):
        self.return_button = QPushButton('돌아가기', self)
        self.return_button.setGeometry(700, 560, 80, 20)
        self.return_button.clicked.connect(self.close_app)

    # 닫기
    def close_app(self):
        self.close()

    # 리뷰 ui 세팅
    def review_ui(self):
        # 리뷰 데이터 로드하기
        conn = sqlite3.connect("shop2.db", isolation_level=None)
        c = conn.cursor()
        # 리뷰 테이블이 없을 경우 테이블 작성
        c.execute('create table if not exists 리뷰 \
                  (상가업소번호 text not null, ID text not null, 상호명 text not null, 지점명 text,'
                  ' 평점 int not null, 리뷰 text);')
        c.execute(f'select * from 리뷰 where 상가업소번호={self.user_restaurant_info[1]}')
        # save review 변수에 받아온 식당 상가업소번호에 해당하는 모든 리뷰 정보를 저장
        self.save_review = c.fetchall()
        # 반복 횟수 설정
        ui_length = len(self.save_review)

        # 리뷰 작성 안내 라벨
        self.review_announce_label = QLabel('100자 이내로 작성해주세요.', self)
        self.review_announce_label.setGeometry(25, 25, 200, 20)

        # 식당 점수를 review_score 함수에 입력
        self.review_score = self.score_calc(ui_length)
        
        # 별점 라벨(김연수 아이디어 추가)
        self.review_score_label = QLabel('★★★★★', self)
        # 별을 평점에 맞게 잘라서 출력함
        self.review_score_label.setGeometry(25, 130, int(self.review_score * 12), 20)

        # self.i값에 받아 반복에 사용
        for self.i in range(ui_length):
            # 리뷰 뷰어 실행
            self.review_viewer_ui()
        # 리뷰 작성 ui 출력
        self.review_write_ui()

        # 지점명이 있을 경우 지점명 더함
        if not self.save_review:
            # 평가가 없을 경우 평가 없음 문구 출력
            self.nocoment_label = QLabel('평가가 없습니다.', self)
            self.nocoment_label.setGeometry(350, 300, 100, 20)
        else:
            # 평가가 있을 경우 유저 리뷰 출력, 지점명이 있을 경우 지점명을 더함
            if self.save_review[0][3]:
                # 출력문('식당명 지점명 별점 유저리뷰')
                self.restaurant_name_label = QLabel(f'{self.save_review[0][2]}{self.save_review[0][3]}'
                                                    f'({self.review_score:.1f} / 5) 유저리뷰', self)
            else:
                self.restaurant_name_label = QLabel(f'{self.save_review[0][2]}({self.review_score:.1f}'
                                                    f' / 5) 유저리뷰', self)
            # 라벨 지오메트리
            self.restaurant_name_label.setGeometry(100, 130, 300, 20)

    # 평점 계산기
    def score_calc(self, length):
        # 0개일 경우 0 반환
        if length == 0:
            return 0
        else:
            review_score = 0
            # 평점을 모두 더해서
            for i in range(length):
                review_score += self.save_review[i][4]
            # 평가수로 나누어 평균을 구함
            return review_score / length

    # 리뷰 뷰어?
    def review_viewer_ui(self):
        # 라벨을 통한 유저 아이디 출력
        self.user_label = QLabel(f'{self.save_review[self.i][1]} 님', self)
        self.user_label.setGeometry(700, (self.i + 1) * 70 + 90, 100, 20)

        # 라벨을 통한 평점 출력
        self.score_label = QLabel(f'{self.save_review[self.i][4]} / 5', self)
        self.score_label.setGeometry(650, (self.i + 1) * 70 + 90, 50, 20)

        # 텍스트 에딧 창에 리뷰 내용 출력
        self.review_content = QTextEdit(self.save_review[self.i][5], self)
        self.review_content.setReadOnly(True)
        self.review_content.setGeometry(25, (self.i + 1) * 70 + 90, 620, 40)

    # 리뷰 입력 ui
    def review_write_ui(self):
        # 등록 버튼
        self.post_review_button = QPushButton('등록', self)
        self.post_review_button.setGeometry(680, 60, 100, 20)
        self.post_review_button.clicked.connect(self.upload_review)

        # 콤보박스
        self.score_combobox = QComboBox(self)
        self.score_combobox.addItem('별점 선택', 5)
        self.score_combobox.addItem('★★★★★', 5)
        self.score_combobox.addItem('★★★★', 4)
        self.score_combobox.addItem('★★★', 3)
        self.score_combobox.addItem('★★', 2)
        self.score_combobox.addItem('★', 1)
        self.score_combobox.setGeometry(680, 90, 100, 20)

        # 평가용 textedit
        self.review_write_text = QTextEdit('', self)
        self.review_write_text.setGeometry(25, 60, 640, 50)
        # self.review_write_text = 100

    # 리뷰 업로드
    def upload_review(self):
        # 별점이 선택되지 않으면 리뷰가 등록되지 않음
        if self.score_combobox.currentText() == '별점 선택':
            QMessageBox.warning(self, '별점 선택', '별점이 선택되지 않았습니다.')
        else:
            # 리뷰 등록 여부 확인
            upload = QMessageBox.question(self, '게시물 등록', '리뷰를 등록하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
            if upload == QMessageBox.Yes:
                # 오토커밋 db오픈
                conn = sqlite3.connect("shop2.db", isolation_level=None)
                c = conn.cursor()
                # 상호명과 지점명을 상가업소번호를 통해 받아옴
                c.execute(f'select 상호명 from Gwangju where 상가업소번호={self.user_restaurant_info[1]}')
                restaurant_name = c.fetchone()[0]
                c.execute(f'select 지점명 from Gwangju where 상가업소번호={self.user_restaurant_info[1]}')
                restaurant_branch = c.fetchone()[0]
                # 지점명 유무에 따른 등록 db 차이
                if not restaurant_branch:
                    c.execute(f'insert into 리뷰 (상가업소번호, ID, 상호명, 평점, 리뷰) values ("{self.user_restaurant_info[1]}", "{self.user_restaurant_info[0]}", "{restaurant_name}", {self.score_combobox.currentData()}, "{self.review_write_text.toPlainText()}")')
                else:
                    c.execute(f'insert into 리뷰 ("{self.user_restaurant_info[1]}", "{self.user_restaurant_info[0]}", "{restaurant_name}", "{restaurant_branch}", {self.score_combobox.currentData()}, "{self.review_write_text.toPlainText()}")')
                # 리뷰 등록 완료
                QMessageBox.information(self, '리뷰 등록', '리뷰가 등록되었습니다.')
                self.close()
            else:
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReviewPage()
    sys.exit(app.exec_())
