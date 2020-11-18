import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests

import json
import webbrowser as w

import time

import msvcrt as m
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=2560x1600")
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OSSUI(QWidget):

    def __init__(self):
        super().__init__()
        self.resultUI = None
        self.bgLabel = QLabel(self)
        self.idLabel = QLabel("ID : ", self)
        self.pwLabel = QLabel("PW : ", self)
        self.editID = QLineEdit(self)
        self.editPW = QtWidgets.QLineEdit(self)
        self.btnCheck = QPushButton("수강 확인", self)
        self.btnHelp = QPushButton("도움말", self)
        self.initUI()

    def initUI(self):
        self.editPW.setEchoMode(QLineEdit.Password)
        pixmap = QPixmap("loginbg.jpg")
        self.bgLabel.setPixmap(pixmap)
        self.idLabel.setStyleSheet("Color : red;")
        self.pwLabel.setStyleSheet("color: #FF0000;")
        self.bgLabel.resize(300, 300)
        self.idLabel.resize(40, 20)
        self.pwLabel.resize(40, 20)
        self.editID.resize(240, 20)
        self.editPW.resize(240, 20)

        self.bgLabel.move(0, 0)
        self.idLabel.move(20, 30)
        self.pwLabel.move(20, 70)
        self.editID.move(60, 30)
        self.editPW.move(60, 70)

        self.btnCheck.resize(100, 50)
        self.btnHelp.resize(100, 50)
        self.btnCheck.move(80, 250)
        self.btnHelp.move(200, 250)
        self.btnCheck.clicked.connect(self.popNewWindow)
        self.btnHelp.clicked.connect(self.help)
        self.setWindowTitle("KLAS")
        self.setWindowIcon(QIcon("KWU.png"))
        self.resize(300, 300)
        self.center()
        self.show()

    def help(self):
        QMessageBox.about(self, "HELP",
                          "본 프로그램을 실행하기 전에 chromedriver.exe를 같은 폴더로 옮겨주세요\n\n학번과 비밀번호를 입력 후\n수강 확인을 누르면 동작합니다.\n상세 방법은 github를 확인하세요.")

    def popNewWindow(self):  # 여기가 새로운 윈도우를 띄우는곳
        if self.editID.text() == "" or self.editPW.text() == "":
            QMessageBox.about(self, "Notice", "아이디와 비밀번호를 입력해주세요.")
            self.editID.setFocus()
        else:
            if int(self.editID.text()[:4]) < 2016:
                QMessageBox.about(self, "Sorry", "현재까지 개발된 시스템은\n16학번부터 이용가능합니다.\n불편을 드려 죄송합니다.")
            else:
                if int(self.editID.text()[4:7]) not in [726, 203]:
                    QMessageBox.about(self, "Notice", "소프트웨어학부로 입학하지 않은 경우\n조회된 결과의 정확도는 보장되지 않습니다.")
                else:
                    QMessageBox.about(self, "Notice",
                                      "로그인을 시도합니다.\n**결과는 단순 참고용입니다**\n\n영역간 중복되는 과목은\n총계에서는 한번만 계산됩니다.\n\n배포 초기에는 정확하지 않을 수 있습니다.")
                self.user = Student(self.editID.text(), self.editPW.text())
                if self.user.cookies != 1:
                    self.close()
                    QMessageBox.about(self, "Success", "데이터가 정상적으로 입력되었습니다.")
                    # if self.resultUI is None:
                    #    self.w = ResultUI()
                    # self.w.show()

                else:
                    QMessageBox.about(self, "Notice", "로그인에 실패하였습니다.\n아이디와 비밀번호를 확인해주세요.")

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            if self.editPW.hasFocus() or self.editID.hasFocus():
                if self.editPW.text() != "" and self.editID.text() != "":
                    self.popNewWindow()
                else:
                    QMessageBox.about(self, "Notice", "아이디와 비밀번호를 입력해주세요.")
                    self.editID.setFocus()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ResultUI(QWidget):

    def __init__(self, require, current, remain, balance, is_pass, balance_pass):
        super().__init__()
        self.require_counts = require
        self.current_counts = current
        self.remain_value = remain
        self.balance_counts = balance
        self.is_pass = is_pass
        #print(self.balance_counts)
        self.balance_pass = balance_pass
        self.resultUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resultUI(self):

        vbox = QVBoxLayout()
        horizontalList = ["취득(예정) 학점", "졸업기준 학점", "남은 학점", "비고", "필독"]
        verticalList = ["필수교양(A)", "균형교양(B)", "기초교양(C)", "교양선택,일반선택(D)",
                        "전공(E)", "총계(A~E+공학기초)", "공학인증학점"]
        self.setWindowTitle("RESULT")
        self.center()
        self.resize(1020, 600)
        self.setWindowIcon(QIcon("KWU.png"))
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(7)
        for i in range(5):
            headerItem = QTableWidgetItem(horizontalList[i])
            headerItem.setBackground(QColor("#203764"))
            if i == 4:
                headerItem.setForeground(QColor("#FF0000"))
            self.tableWidget.setHorizontalHeaderItem(i, headerItem)
        for i in range(7):
            headerItem = QTableWidgetItem(verticalList[i])
            headerItem.setBackground(QColor("#203764"))
            self.tableWidget.setVerticalHeaderItem(i, headerItem)

        self.tableWidgetDetail = QTableWidget(self)
        self.tableWidgetDetail.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetDetail.setColumnCount(6)
        self.tableWidgetDetail.setRowCount(2)
        horizontalListDetail = (["언어와표현(1)", "과학과 기술(2)", "인간과 철학(3)", "사회와 경제(4)",
                                 "글로벌문화와 제2외국어(5)", "예술과체육(6)"])
        verticalListDetail = (["인정 학점", "이수 학점"])
        for i in range(6):
            headerItem = QTableWidgetItem(horizontalListDetail[i])
            headerItem.setBackground(QColor("#203764"))
            self.tableWidgetDetail.setHorizontalHeaderItem(i, headerItem)

        for i in range(2):
            headerItem = QTableWidgetItem(verticalListDetail[i])
            headerItem.setBackground(QColor("#203764"))
            self.tableWidgetDetail.setVerticalHeaderItem(i, headerItem)

        self.tableWidget.setSpan(0, 4, 6, 4)
        item = QTableWidgetItem("각 영역별\n기준과목과\n기준학점등은\n\nGithub\nGraduate-helper\n ㄴdata 폴더\n확인하세요.")
        item.setForeground(QColor("#FF0000"))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, item)

        vbox.addWidget(self.tableWidget, 3)
        vbox.addWidget(self.tableWidgetDetail, 1)
        self.setLayout(vbox)

        for i in range(7):

            for j in range(4):
                ###
                # string에 데이터를 넣어서 보내면 됨, i는 행, j는 열, 원한다면 변형가능 하지만 item에 데이터를 넣어줘야하는건 수정금지
                ###
                if j == 0:  # 취득
                    string = self.current_counts[i]
                    if i == 3:
                        string = self.current_counts[7]
                    elif i == 4:
                        string = self.current_counts[3]
                    elif i == 5:
                        string = self.current_counts[6]
                    elif i == 6:
                        string = self.current_counts[4]
                elif j == 1:  # 기준
                    string = self.require_counts[i]
                    if i == 3:
                        string = "-"
                    elif i == 4:
                        string = self.require_counts[3]
                    elif i == 5:
                        string = self.require_counts[6]
                    elif i == 6:
                        string = self.require_counts[4]
                elif j == 2:  # 잔여
                    string = self.remain_value[i]

                    if i == 3:
                        string = self.remain_value[7]
                    elif i == 4:
                        string = self.remain_value[3]
                    elif i == 5:
                        string = self.remain_value[6]
                    elif i == 6:
                        string = self.remain_value[4]
                else:  # 비고
                    if self.tableWidget.item(i, j - 1).text() == "0":
                        string = "만족"
                        if i == 3:
                            string = "-"
                    elif i == 6:
                        if self.current_counts[5] >= 12 and self.remain_value[5] == 0:
                            string = "만족"
                        else:
                            string = "캡스톤 미이수"
                    else:
                        string = "-"
                item = QTableWidgetItem(str(string))
                ###
                # 수정 금지
                ###
                item.setTextAlignment(Qt.AlignCenter)
                if j % 2 == 0:
                    item.setBackground(QColor("#DDEBF7"))
                if i == 5:
                    item.setBackground(QColor("#FFFF00"))
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.setItem(6, 4, QTableWidgetItem("설계학점 " + str(self.current_counts[5]) + "/12"))

        for i in range(6):
            if (self.balance_counts[i] >= 3):
                string = 3
            else:
                string = 0
            item = QTableWidgetItem(str(string))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#DDEBF7"))
            self.tableWidgetDetail.setItem(0, i, item)
            item2 = QTableWidgetItem(str(self.balance_counts[i]))
            item2.setTextAlignment(Qt.AlignCenter)
            self.tableWidgetDetail.setItem(1,i,item2)
    def closeEvent(self, event):
        event.accept()
        sys.exit(0)


class Student:
    def __init__(self, user_id, user_pw):
        self.hakbun = user_id[:4]  # 학번에 따른 졸업기준 판단을 위한 슬라이싱
        self.ispass = False  # 대학영어 면제 여부 (19학번부터는 반드시 대학영어를 수강해야 하므로 기본값 False로 지정)
        self.domain = "https://klas.kw.ac.kr/"  # 기본 도메인
        self.cookies = self.login_klas(user_id, user_pw)  # 로그인 성공 시의 쿠키 저장공간(요청을 위한 세션 구성에 필요)
        self.sungjuk_data = ''  # 수강 data 저장공간
        if self.cookies != 1:
            self.data_request()  # 수강 data, 대학영어 면제 여부 추출
            self.DB = Database(self.hakbun, self.ispass)  # 학번에 따른 졸업기준 DB 생성
            self.Data = Data(self.sungjuk_data, self.DB)  # 본인의 수강내역과 DB를 비교하여 추출된 영역별 계산 공간
            self.Graduate = Graduate(self.hakbun, self.ispass, self.Data.count_hakjum,
                                     self.Data.count_names)  # 졸업이수기준과 이수내역을 비교하여 최종결과 도출
        else:
            print("로그인에 실패하였습니다.")

    # ==================== STEP 1 KLAS 로그인 ====================
    def login_klas(self, id, pw):

        # Selenium으로 로그인
        browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        browser.get(self.domain)

        # KLAS 로그인 페이지에 입력 정보 전달
        elem = browser.find_element_by_id("loginId")
        elem.send_keys(id)
        elem = browser.find_element_by_id("loginPwd")
        elem.send_keys(pw)
        elem = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/form/div[2]/button")
        elem.click()
        try:  # 로그인 시도
            elem = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='appModule']/div/div[1]/div[1]/select")))
            return browser.get_cookies()
        except Exception:  # 실패 예외처리
            browser.quit()
            return 1

    # ==================== STEP 2 수강/성적 , 대학영어 면제여부 data 추출====================
    def data_request(self):
        if self.cookies != 1:  # 로그인에 성공한 경우
            sugang_header = {'POST': '/std/cps/inqire/AtnlcScreSungjukInfo.do HTTP/1.1',
                             'Host': 'klas.kw.ac.kr',
                             'Connection': 'Keep-Alive',
                             'Content-Length': '0',
                             'Accept': 'application/json, text/plain, */*',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                             'Content-Type': 'application/json; charset=UTF-8',
                             'Origin': 'https://klas.kw.ac.kr',
                             'Sec-Fetch-Site': 'same-origin',
                             'Sec-Fetch-Mode': 'cors',
                             'Sec-Fetch-Dest': 'empty',
                             'Referer': 'https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreStdPage.do',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
                             }
            s = requests.Session()
            s.headers.update(sugang_header)
            # 요청을 위한 header, cookie 등록
            for cookie in self.cookies:
                c = {cookie['name']: cookie['value']}
                s.cookies.update(c)
            # 수강 성적 데이터 서버에 data 요청
            sungjuk_res = s.post('https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreSungjukInfo.do')
            self.sungjuk_data = sungjuk_res.json()
            level_header = {'POST': '/std/cps/inqire/ToeicLevelInfo.do HTTP/1.1',
                            'Host': 'klas.kw.ac.kr',
                            'Connection': 'Keep-Alive',
                            'Content-Length': '0',
                            'Accept': 'application/json, text/plain, */*',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                            'Content-Type': 'application/json; charset=UTF-8',
                            'Origin': 'https://klas.kw.ac.kr',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://klas.kw.ac.kr/std/cps/inqire/ToeicStdPage.do',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
                            }
            # 요청을 위한 header 변경
            s.headers.update(level_header)
            # 신입생 영어 레벨 테스트 서버에 data 요청
            level_res = s.post('https://klas.kw.ac.kr/std/cps/inqire/ToeicLevelInfo.do')
            level_data = level_res.text

            # 요청에 대한 반환은 None,30,70 중 하나로 19학번 이후는 None(테스트 미실시) , 16~18학번에 한하여 30인 경우 대학영어 면제, 70인 경우 대학영어 필수 수강
            if (level_data == '"30"'):
                self.ispass = True
        else:
            return


# ==================== STEP 3  학번, 대학영어 면제여부에 따른 수강과목 기준 Database 생성====================
class Database:
    __culture_require = []  # 교양필수목록
    __culture_select = {}  # 균형교양목록
    __basic_math = []  # 기초교양 수학목록
    __basic_science = []  # 기초교양 과학목록
    __basic_engineer = []  # 공학기초(교양)목록
    __major_engineer = []  # 공학주제(전공)목록
    __major_require = []  # 전공필수목록
    __major_select = []  # 전공선택목록
    __design_engineer = {}  # 설계학점 과목 목록
    __admission_year = 0  # 입학년도
    __leveltest = False  # 대학영어 면제여부

    def __init__(self, year, ispass):
        self.__admission_year = year
        self.__leveltest = ispass
        self.__culture_require = self.set_cr()
        self.__culture_select = self.set_cs()
        self.__basic_math = self.set_bm()
        self.__basic_science = self.set_bs()
        self.__basic_engineer = self.set_be()
        self.__major_require = self.set_mr()
        self.__major_select = self.set_ms()
        self.__major_engineer = self.set_me()
        self.__design_engineer = self.set_de()
    def get_year(self):  # 학번에 따른 졸업요건
        return self.__admission_year

    def get_level(self):  # 대학영어 면제여부
        return self.__leveltest

    def get_cr(self):  # 교양필수
        return self.__culture_require

    def get_cs(self):  # 균형교양
        return self.__culture_select

    def get_bm(self):  # 기초교양 수학
        return self.__basic_math

    def get_bs(self):  # 기초교양 과학
        return self.__basic_science

    def get_be(self):  # 공학기초
        return self.__basic_engineer

    def get_mr(self):  # 전공필수
        return self.__major_require

    def get_ms(self):  # 전공선택
        return self.__major_select

    def get_me(self):  # 공학주제
        return self.__major_engineer

    def get_de(self):  # 설계과목
        return self.__design_engineer

    # ==================== 이 영역은 학번에 따른 영역별 Database를 구성하는 곳입니다.====================
    # 2016학번부터 2020학번까지 변화하는 졸업이수체계에 따라 구성됩니다.
    # 이 영역에 해당하지 않는 과목에는 균형교양으로 인정되지 않는 교양선택, 교직, 타과전공과목(일선),다전공이수과목(복필,복선,부필,부선,연필,연선), ROTC(무관) 등이 포함됩니다.
    # 본 프로그램은 필수교양,균형교양,전공,공학인증에 대한 졸업요건을 만족하기 위한 가이드라인을 제공하는 것을 목표로 제작되었습니다.
    # 다전공등에 대한 구현 역시 정보 수집의 한계로 여러분의 Contribute를 기다리고 있습니다.

    def set_cr(self):  # 필수교양 과목 구성
        result = []
        result.append('8128')  # 광운인되기 (2016학번부터 전체 필수)
        if self.get_year() == '2016':  # ==================== 2016 학번====================
            if not self.get_level():  # 레벨테스트 미통과자
                result.append('3362')  # 대학영어 추가
        elif self.get_year() == '2017' or self.get_year() == '2018':  # ==================== 2017,2018 학번====================
            result.append('0019')  # C프로그래밍 필수지정
            result.append('8297')  # 컴퓨팅사고 필수지정
            if not self.get_level():
                result.append('3362')
        elif self.get_year() == '2019':  # ==================== 2019 학번====================
            result.append('3362')  # 대학영어,C프로그래밍,컴퓨팅사고 필수 지정
            result.append('0019')
            result.append('8297')
        elif self.get_year() == '2020':  # ==================== 2020 학번====================
            result.append('3362')  # 대학영어,C프로그래밍,컴퓨팅사고,융합적사고와글쓰기 필수 지정
            result.append('0019')
            result.append('8297')
            result.append('3095')
        else:  # ==================== ~2015 학번====================
            # print("교양이수체계 개편에 따른 정보 수집의 한계로 여러분의 Contribute가 필요한 영역입니다.")
            return
        return result

    def set_cs(self):  # 균형교양 구성
        # 본 Database는 2016학년도 1학기부터 2020학년도 2학기까지 개설된 균형교양 과목을 반영하고 있습니다.
        # 앞으로 학기를 거듭함에 따라 추가로 개설되는 과목만 리스트에 추가하면 지속적으로 사용할 수 있습니다.
        # key값은 과목명과 1:1 대응하는 학정번호의 3번째 구간을 사용하며, value 값은 균형교양영역을 구분하도록 설정합니다.
        # Ex. 0000-1-5909-01 중 5909를 key로, 2를 value로 사용합니다. 과목명: 공학과디자인 , 영역 : 과학과기술
        # 1:언어와표현 2:과학과기술 3:인간과철학 4:사회와경제 5:글로벌문화와제2외국어 6:예술과체육
        # 단 3학점 중 균형교양으로 인정되는 과목만 포함하고 있습니다.
        # 본 프로그램은 균형교양 이수요건을 만족했는지를 판단하기 위하여
        # 사용자의 수강내역과 Database의 비교시 영역에 포함되지 않는 경우(교양선택)는 단순 교양학점으로 계산하기위해 0으로 value를 설정합니다.
        result = {}
        data1 = ['3095', '2948', '6523', '5914', '7465', '6518', '7132', '2337', '2977', '6021', '5904']
        data2 = ['5909', '4283', '4711', '5675', '7461', '5674', '9735', '5704', '1659', '3293', '8118', '6519', '6019',
                 '7459', '6957', '3298', '4263', '7724', '8581', '9251', '9252', '3029', '2991', '2993', '6020',
                 '8119', '5676', '2994', '7725', '7728', '3085', '5765', '2997', '7462', '8120']
        data3 = ['5899', '0221', '3925', '8085', '5224', '4390', '3919', '5659', '2337', '5660', '2959', '5661', '7460',
                 '1794', '5655', '7723', '8123', '5662', '3937', '4050', '5368', '7727', '6133', '4052', '3933', '6018',
                 '5900', '3189', '5663', '7726', '2038', '3932', '3944', '5658', '6517', '8122', '6516', '3924', '5665',
                 '1879', '7459', '3931', '5666']
        data4 = ['8876', '8583', '5901', '0670', '4282', '3948', '0806', '4638', '3928', '9736', '9743', '3363', '4280',
                 '9253', '9450', '2982', '5667', '5908', '8832', '4723', '1797', '8586', '2981', '2987', '9472', '3930',
                 '9744', '5668', '6137', '2988', '8834', '3645', '8124', '8125', '5903', '3008', '8585', '8588', '3950',
                 '8587', '6136', '4717', '5671', '9448', '3946', '4735', '5672', '5703', '5669']
        data5 = ['3589', '3693', '3812', '6135', '5688', '6524', '6525', '3593', '3696', '3090', '2950', '3039', '2419',
                 '2977', '3349', '4921', '4932', '5689', '6022', '6023', '6526', '8653', '5690', '4917', '2665', '4933',
                 '8593', '5690', '4917', '2665', '4933', '8593', '5637', '8594', '6134', '3590', '6376', '3697', '4052',
                 '5219', '5687']
        data6 = ['5678', '6948', '3814', '3196', '4051', '2968', '4925', '7595', '3200', '5682', '7463', '5679', '4081',
                 '2437', '5226', '2942', '5681', '5680', '3934', '3936', '8590', '8591', '3935', '6381', '2970']
        for data in data1:
            result.setdefault(data, 1)
        for data in data2:
            result.setdefault(data, 2)
        for data in data3:
            result.setdefault(data, 3)
        for data in data4:
            result.setdefault(data, 4)
        for data in data5:
            result.setdefault(data, 5)
        for data in data6:
            result.setdefault(data, 6)

        return result

        # ==================== 이 영역은 소프트웨어학부를 기준으로 기초교양 수학,과학,공학기초로 인정되는 과목의 목록입니다. 수강신청 자료집을 참고하시기 바랍니다.====================

    def set_bm(self):  # 기초교양 수학 구성
        result = ['4625', '4626', '4969', '4970', '0819', '4627', '1942', '0875', '4628', '2103']
        return result

    def set_bs(self):  # 기초교양 과학 구성
        result = ['3414', '3415', '3416', '3417']
        return result

    def set_be(self):  # 공학기초 구성
        result = ['5714', '2957']  # 공학설계입문은 선택과목이나 산학협력캡스톤설계를 수강하기위한 선수과목이므로 필수로 지정하였습니다 / 고급 C프로그래밍 및 설계 필수
        '''if (self.get_year() == '2016'):  # 2016학번 대상
            result.append('0019')  # C프로그래밍 필수 (2017부터는 필수교양)
            result.append('1640')  # 컴퓨터개론 선택 (2017부터는 컴퓨팅사고(필수교양))
        '''
        result.append('0019')  # C프로그래밍 필수 (2017부터는 필수교양이면서 공학인증학점) - 졸업이수학점 계산시 중복계산 방지필요
        result.append('8297')  # 컴퓨팅사고 (2017부터는 필수교양이면서 공학인증학점) - 졸업이수학점 계산기 중복계산 방지필요
        result.append('1640')  # 컴퓨터개론 (2016학번ver 컴퓨팅사고, 공학인증학점)
        return result

        # ==================== 이 영역은 소프트웨어학부를 기준으로 전공과목의 목록입니다. 수강신청 자료집을 참고하시기 바랍니다.====================

    def set_mr(self):  # 전공 필수과목
        result = ['8484', '3660', '1243', '3405', '8486', '3690', '0969', '8485', '3661']
        return result

    def set_ms(self):  # 전공 선택과목 ( 세부전공필수 및 공학인증 필수 포함)
        result = ['3395', '1647', '1110', '8487', '3663', '0846', '8995', '4164', '8996', '4165', '8998', '0448',
                  '1183', '3403', '5409', '2910', '4534', '6899', '1637', '4535', '4839', '3709', '9151', '7777',
                  '1762', '1196', '1655', '1765', '3951', '5266', '5694', '6387', '5009', '7412', '8999', '3458',
                  '3113', '4858', '3114', '4262', '9156', '3875', '4862', '4955', '5193', '3874', '3830']
        return result

        # ==================== 이 영역은 소프트웨어학부를 기준으로 공학인증 대상 전공 과목입니다. 수강신청 자료집을 참고하시기 바랍니다.====================

    def set_me(self):
        result = self.set_mr() + self.set_ms()  # 전공필수 및 선택과목을 병합
        result.remove('5694')  # 경력개발과취업전략 제외(전공,공학인증X)
        result.remove('1183')  # 이산구조 제외 (전공,수학O,공학인증X) - 졸업이수 학점 계산시 중복계산 방지필요
        return result

        # ==================== 이 영역은 소프트웨어학부를 기준으로 설계학점 과목입니다. 수강신청 자료집을 참고하시기 바랍니다.====================

    def set_de(self):
        data1 = ['8484', '3660', '3405', '8486', '3690', '0969', '8485', '3661', '1110', '0846', '3403', '1637',
                 '5193']  # 설계학점 1학점 과목
        data2 = ['5714', '5266']  # 설계학점 2학점 과목
        data3 = ['2957', '8995', '4164', '8996', '4165']  # 설계학점 3학점 과목
        result = {}
        for data in data1:
            result.setdefault(data, 1)
        for data in data2:
            result.setdefault(data, 2)
        for data in data3:
            result.setdefault(data, 3)
        return result
    # ==================== STEP 4  사용자의 수강내역과 Database를 비교하여 영역별 계산 ====================


class Data:
    def __init__(self, sungjuk_data, DB):
        self.sungjuk_data = sungjuk_data  # 사용자의 수강 내역
        self.culture_RDB = DB.get_cr()  # 비교기준 DB
        self.culture_SDB = DB.get_cs()
        self.basic_MDB = DB.get_bm()
        self.basic_SDB = DB.get_bs()
        self.basic_EDB = DB.get_be()
        self.major_RDB = DB.get_mr()
        self.major_SDB = DB.get_ms()
        self.major_EDB = DB.get_me()
        self.design_DB = DB.get_de()
        self.Grade = ['C+(삭제)', 'C0(삭제)', 'D+(삭제)', 'D0(삭제)', 'NP',
                      'F ']  # 취득학점으로 인정되지 않는 성적 , 현재 재학중인 학기까지의 결과를 포함합니다.
        self.count_hakjum = [0, [0, 0, 0, 0, 0, 0], 0, 0, 0, 0, 0, 0, 0, 0,
                             0]  # 취득학점 계산 : 필수교양, 균형교양(1~6), 교양선택, 수학, 과학, 전공필수, 전공선택, 공학기초, 공학주제, 일반선택(복필,복선,부필,부선,연필,연선,교직,무관,일선), 설계
        self.count_names = [[], [[], [], [], [], [], []], [], [], [], [], [], [], [], [],
                            []]  # 취득과목명 저장 : 필수교양,균형교양, 교양선택, 수학, 과학, 전필, 전선, 공학기초, 공학주제, 일반선택 , 설계
        self.calculation(self.sungjuk_data)

    def calculation(self, sungjuk_data):
        for sungjuk_hakgi in sungjuk_data:
            for gwamok in sungjuk_hakgi['sungjukList']:
                if (gwamok['retakeGetGrade'] == None):  # 삭제예정(재수강) 과목은 카운트 하지 않음 -> 성적 마감 이후에도, 다시 이수한 과목만 카운트 되는 점을 반영
                    if (gwamok['hakjungNo'] == "교류"):  # 참빛설계학기 혹은 타대학 교류학점
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            if (gwamok['codeName1'] == "전선"):
                                self.count_hakjum[6] += gwamok['hakjumNum']
                                self.count_names[6].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == "일선"):
                                self.count_hakjum[9] += gwamok['hakjumNum']
                                self.count_names[9].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == "교선"):
                                self.count_names[2].append(gwamok['gwamokKname'])
                                self.count_hakjum[2] += gwamok['hakjumNum']
                    # 필수교양,균형교양,기초수학,기초과학,전공필수,전공선택 계산
                    elif (gwamok['hakjungNo'][7:11] in self.culture_RDB):  # 필수교양 계산
                        if (gwamok['getGrade'] in self.Grade):  # 수강과목의 마감 성적이 재수강,NP,F인 경우는 카운트 제외
                            continue
                        else:
                            self.count_hakjum[0] += gwamok['hakjumNum']  # 필수교양 학점 합계
                            self.count_names[0].append(gwamok['gwamokKname'])  # 필수교양 과목 list

                    elif (gwamok['hakjungNo'][7:11] in self.culture_SDB):  # 균형교양 계산
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_names[1][self.culture_SDB.get(gwamok['hakjungNo'][7:11]) - 1].append(
                                gwamok['gwamokKname'])  # 수강과목의 이름과 학정번호로 영역을 구분(1~6)하여 저장
                            self.count_hakjum[1][self.culture_SDB.get(gwamok['hakjungNo'][7:11]) - 1] += gwamok[
                                'hakjumNum']  # 구분된 값에 따라, 영역별 학점 합계
                    elif (gwamok['hakjungNo'][7:11] in self.basic_MDB):  # 수학 학점 계산
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[3] += gwamok['hakjumNum']
                            self.count_names[3].append(gwamok['gwamokKname'])

                    elif (gwamok['hakjungNo'][7:11] in self.basic_SDB):  # 과학 학점 계산
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[4] += gwamok['hakjumNum']
                            self.count_names[4].append(gwamok['gwamokKname'])

                    elif (gwamok['hakjungNo'][7:11] in self.major_RDB):  # 전공필수 계산
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[5] += gwamok['hakjumNum']
                            self.count_names[5].append(gwamok['gwamokKname'])

                    elif (gwamok['hakjungNo'][7:11] in self.major_SDB):  # 전공선택 계산
                        if (gwamok['hakjungNo'][7:11] == '1183'):  # 이산구조과목은 전공선택이면서 동시에 수학과목으로도 들어감.
                            if (gwamok['getGrade'] in self.Grade):
                                continue
                            else:
                                self.count_hakjum[3] += gwamok['hakjumNum']
                                self.count_names[3].append(gwamok['gwamokKname'])
                                self.count_hakjum[6] += gwamok['hakjumNum']
                                self.count_names[6].append(gwamok['gwamokKname'])
                        else:  # 이산구조를 제외한 전선과목
                            if (gwamok['getGrade'] in self.Grade):
                                continue
                            else:
                                self.count_hakjum[6] += gwamok['hakjumNum']
                                self.count_names[6].append(gwamok['gwamokKname'])
                    else:  # 위의 분류기준에 해당하지 않는 균형 교양(2학점이하), 기타 교양(E-learning,K-Mooc), 교직, 무관, 다전공, 타과전공 등
                        if gwamok['hakgwa'] in ['소프트웨어학부', '컴퓨터소프트웨어학과']:
                            if gwamok['hakjungNo'][7:11] in self.basic_EDB:  # 공학기초는 아랫단에서 별도로 계산함
                                pass
                            else:  # 그외 학과에 개설된 과목(교양선택)
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[2] += gwamok['hakjumNum']
                                    self.count_names[2].append(gwamok['gwamokKname'])
                        else:  # 타학과 개설과목 혹은 전체공통
                            if (gwamok['hakjungNo'][7:11] == '3240'):
                                if sungjuk_hakgi['thisYear'] == '2017' and sungjuk_hakgi[
                                    'hakgi'] == '2':  # 취업전략과목이 2017-2 한하여 3학점(균형교양)
                                    if (gwamok['getGrade'] in self.Grade):
                                        continue
                                    else:
                                        self.count_names[1][3].append(gwamok['gwamokKname'])
                                        self.count_hakjum[1][3] += gwamok['hakjumNum']
                                else:  # 그 외에는 교양선택
                                    if (gwamok['getGrade'] in self.Grade):
                                        continue
                                    else:
                                        self.count_names[2].append(gwamok['gwamokKname'])
                                        self.count_hakjum[2] += gwamok['hakjumNum']
                            elif (gwamok['hakjungNo'][7:11] == '5657'):  # 예술작품속의동양사상이 2019년 1학기부터 예술과체육에서 인간과철학으로 변경
                                if int(sungjuk_hakgi['thisYear']) < 2019:  # 예술과체육
                                    if (gwamok['getGrade'] in self.Grade):
                                        continue
                                    else:
                                        self.count_names[1][5].append(gwamok['gwamokKname'])
                                        self.count_hakjum[1][5] += gwamok['hakjumNum']
                                else:  # 2019년부터는 인간과철학
                                    if (gwamok['getGrade'] in self.Grade):
                                        continue
                                    else:
                                        self.count_names[1][2].append(gwamok['gwamokKname'])
                                        self.count_hakjum[1][2] += gwamok['hakjumNum']
                            elif (gwamok['codeName1'] == '교선' or gwamok['codeName1'] == '교필' or gwamok[
                                'codeName1'] == '기필' or gwamok['codeName1'] == '기선'):  # 교양선택과목
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[2] += gwamok['hakjumNum']
                                    self.count_names[2].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == '교직' or gwamok['codeName1'] == '무관' or gwamok[
                                'codeName1'] == '복필' or gwamok['codeName1'] == '복선' or gwamok['codeName1'] == '부필' or
                                  gwamok['codeName1'] == '부선' or gwamok['codeName1'] == '연필' or gwamok[
                                      'codeName1'] == '연선'):
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[9] += gwamok['hakjumNum']
                                    self.count_names[9].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == '일선'):
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[9] += gwamok['hakjumNum']
                                    self.count_names[9].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == '전선'):  # 수강/성적 내역에 전선,전필로 표기되면 본인의 전공과목으로 인정됨
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[6] += gwamok['hakjumNum']
                                    self.count_names[6].append(gwamok['gwamokKname'])
                            elif (gwamok['codeName1'] == '전필'):
                                if (gwamok['getGrade'] in self.Grade):
                                    continue
                                else:
                                    self.count_hakjum[5] += gwamok['hakjumNum']
                                    self.count_names[5].append(gwamok['gwamokKname'])
                    # 공학인증 계산
                    if (gwamok['hakjungNo'][7:11] in self.basic_EDB):
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[7] += gwamok['hakjumNum']
                            self.count_names[7].append(gwamok['gwamokKname'])

                    elif (gwamok['hakjungNo'][7:11] in self.major_EDB):
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[8] += gwamok['hakjumNum']
                            self.count_names[8].append(gwamok['gwamokKname'])
                    # 설계학점 계산
                    if (gwamok['hakjungNo'][7:11] in self.design_DB):
                        if (gwamok['getGrade'] in self.Grade):
                            continue
                        else:
                            self.count_hakjum[10] += self.design_DB.get(gwamok['hakjungNo'][7:11])
                            self.count_names[10].append(gwamok['gwamokKname'])

        print("현재까지 수강한 내역을 영역별로 알려드립니다.")
        print()
        print("<필수교양>:", self.count_hakjum[0], self.count_names[0])
        print()
        print("<균형교양>")
        print("-언어와표현:", self.count_hakjum[1][0], self.count_names[1][0])
        print("-과학과기술:", self.count_hakjum[1][1], self.count_names[1][1])
        print("-인간과철학:", self.count_hakjum[1][2], self.count_names[1][2])
        print("-사회와경제:", self.count_hakjum[1][3], self.count_names[1][3])
        print("-글로벌문화와제2외국어:", self.count_hakjum[1][4], self.count_names[1][4])
        print("-예술과체육:", self.count_hakjum[1][5], self.count_names[1][5])
        print()
        print("<교양선택>:", self.count_hakjum[2], self.count_names[2])
        print()
        print("<기초교양>")
        print("수학:", self.count_hakjum[3], self.count_names[3])
        print("과학:", self.count_hakjum[4], self.count_names[4])
        print()
        print("<전공>")
        print("전필:", self.count_hakjum[5], self.count_names[5])
        print("전선:", self.count_hakjum[6], self.count_names[6])
        print()
        print("<일반선택>:", self.count_hakjum[9], self.count_names[9])
        print()
        print("<공학인증>")
        print("공학기초:", self.count_hakjum[7], self.count_names[7])
        print("공학주제:", self.count_hakjum[8], self.count_names[8])
        print()
        print("<설계과목>")
        print("설계:", self.count_hakjum[10], self.count_names[10])


# ==================== STEP 5  학번별 졸업이수기준과 사용자의 이수내역을 비교하여 최종 결과를 도출====================
class Graduate:
    def __init__(self, hakbun, ispass, count, names):
        self.resultUI = None
        self.hakbun = hakbun
        self.ispass = ispass
        self.count = count
        self.names = names
        self.set_requirements(self.hakbun, self.ispass)
        self.can_graduate()
        if self.resultUI is None:
            self.w = ResultUI(self.require_counts, self.evaluate_value, self.remain_value, self.count[1],
                              self.evaluate_graduate, self.balance_count)
            self.w.show()

    def set_requirements(self, hakbun, ispass):  # 학번 별 졸업 이수요건 설정

        self.require_counts = [0, 12, 18, 60, 60, 12,
                               133]  # 필수교양, 균형교양(6영역 중 4영역x3학점 최소이수), 기초교양(수학+과학 18학점이상), 전공(전필포함 60이상), 공학인증(60), 설계, 총계

        if self.hakbun == "2016":  # 2016학번은 영어레벨테스트에 따라 필수 교양 학점 변동
            if self.ispass == True:
                self.require_counts[0] = 1
            else:
                self.require_counts[0] = 4
            self.require_counts[6] = 140  # 2016학번은 140, 2017학번부터는 졸업이수학점 133으로 하향
        elif self.hakbun == "2017" or self.hakbun == "2018":  # 2017,2018학번은 영어레벨테스트에 따라 필수 교양 학점 변동
            if self.ispass == True:
                self.require_counts[0] = 7
            else:
                self.require_counts[0] = 10
        elif self.hakbun == "2019":  # 2019학번부터는 영어레벨테스트가 폐지됨에 따라 동일
            self.require_counts[0] = 10
        elif self.hakbun == "2020":
            self.require_counts[0] = 13  # 융합적사고와글쓰기 추가
            self.require_counts[1] = 9  # 균형교양 : [융합적사고와글쓰기- 언어와 표현]을 제외한 영역 중 3영역x3학점 최소이수

    def can_graduate(self):
        self.evaluate_graduate = [False, False, False, False, False, False,
                                  False]  # 필수교양, 균형교양, 기초교양, 전공, 공학주제, 설계, 졸업이수학점 만족여부 판단
        self.evaluate_value = [0, 0, 0, 0, 0, 0, 0, 0]  # 필수교양, 균형교양, 기초교양, 전공, 공학주제, 설계, 총 이수 학점, 기타
        self.remain_value = [0, 0, 0, 0, 0, 0, 0, 0]  # 영역별 남은 이수학점 기록
        self.culture_balance = [False, False, False, False, False, False]  # 균형교양 영역별 3학점 이상 이수 판단

        if self.count[0] >= self.require_counts[0]:  # 이수내역이 기준을 만족하는 경우
            self.evaluate_graduate[0] = True

        self.evaluate_value[0] = self.count[0]  # 기준 만족과는 무관하게 이수학점을 영역별로 합산
        self.remain_value[0] = self.require_counts[0] - self.evaluate_value[0]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        if self.count[1][0] >= 3:  # 균형교양의 경우 각영역에 3학점 이상 이수해야 해당 영역을 이수한 것으로 판단함
            self.culture_balance[0] = True
        if self.count[1][1] >= 3:
            self.culture_balance[1] = True
        if self.count[1][2] >= 3:
            self.culture_balance[2] = True
        if self.count[1][3] >= 3:
            self.culture_balance[3] = True
        if self.count[1][4] >= 3:
            self.culture_balance[4] = True
        if self.count[1][5] >= 3:
            self.culture_balance[5] = True

        self.evaluate_value[1] += self.count[1][0]  # 기준 만족과는 무관하게 이수학점을 영역별로 합산
        self.evaluate_value[1] += self.count[1][1]
        self.evaluate_value[1] += self.count[1][2]
        self.evaluate_value[1] += self.count[1][3]
        self.evaluate_value[1] += self.count[1][4]
        self.evaluate_value[1] += self.count[1][5]

        self.balance_count = 0
        for isOK in self.culture_balance:  # 3학점 이상 이수한 영역을 계산하고, 계산 결과가 학번에 따라 영역의 수로 판단
            if isOK == True:
                self.balance_count += 1
        if self.balance_count * 3 >= self.require_counts[1]:
            self.evaluate_graduate[1] = True
        self.remain_value[1] = self.require_counts[1] - self.balance_count * 3  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        if self.count[3] >= 6 and self.count[4] >= 3 and self.count[3] + self.count[4] >= self.require_counts[
            2]:  # 기초교양은 수학 6학점이상,과학 3학점이상, 수학+과학 18학점 이상 이수시 만족
            self.evaluate_graduate[2] = True

        self.evaluate_value[2] += (self.count[3] + self.count[4])
        self.remain_value[2] = self.require_counts[2] - self.evaluate_value[2]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        if self.count[5] + self.count[6] >= self.require_counts[3]:  # 전공은 전공필수포함 60학점 이상 이수시 만족
            self.evaluate_graduate[3] = True

        self.evaluate_value[3] = self.count[5] + self.count[6]
        self.remain_value[3] = self.require_counts[3] - self.evaluate_value[3]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        if self.count[7] + self.count[8] >= self.require_counts[
            4]:  # 공학주제는 공학기초와 공학일반,심화를 포함하여 60이상 이수시 만족(단 설계학점 12학점 이상)
            self.evaluate_graduate[4] = True

        self.evaluate_value[4] = self.count[7] + self.count[8]
        self.remain_value[4] = self.require_counts[4] - self.evaluate_value[4]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        self.total = 0
        self.total += self.count[0]
        self.total += self.count[1][0]
        self.total += self.count[1][1]
        self.total += self.count[1][2]
        self.total += self.count[1][3]
        self.total += self.count[1][4]
        self.total += self.count[1][5]
        self.total += self.count[2]
        self.total += self.count[3]
        self.total += self.count[4]
        self.total += self.count[5]
        self.total += self.count[6]
        self.total += self.count[9]

        if '이산구조' in self.names[3]:  # 이산구조는 수학,전공에 중복계산되므로 이수한 경우 졸업이수학점은 한번만 계산
            self.total -= 3

        self.total += self.count[7]  # 공학기초 합산

        # 단 17학번부터는 C프로그래밍과 컴퓨팅사고가 필수교양으로 지정됨
        # 또한 공학인증으로 계산되므로, 이수한 경우 졸업이수학점으로는 한번만 계산
        if 'C프로그래밍' in self.names[0]:
            self.total -= 3
        if '컴퓨팅사고' in self.names[0]:
            self.total -= 3

        # 설계학점은 12학점이상 및 산학협력 캡스톤설계 이수시 만족
        self.evaluate_value[5] = self.count[10]
        if self.count[10] >= self.require_counts[5]:
            if '캡스톤설계1' in self.names[10] or '산학협력캡스톤설계1' in self.names[10] or '캡스톤설계2' in self.names[
                10] or '산학협력캡스톤설계2' in self.names[10]:
                self.evaluate_graduate[5] = True
                self.remain_value[5] = 0
            else:  # 설계학점은 12학점 이상이나, 공학필수과목을 이수하지 않은 경우
                self.remain_value[5] = 3
        else:  # 설계학점이 12학점 미만인 경우
            self.remain_value[5] = self.require_counts[5] - self.evaluate_value[5]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        # 총 이수학점은 16학번(140), 17~20(133) 이수시 만족
        if self.total >= self.require_counts[6]:
            self.evaluate_graduate[6] = True
        self.evaluate_value[6] = self.total
        self.remain_value[6] = self.require_counts[6] - self.evaluate_value[6]  # 기준학점 - 이수학점 = 남아있는 이수해야하는 학점

        self.evaluate_value[7] = self.count[2] + self.count[9]
        # 잔여 이수학점이 음수인 경우는 이미 만족한 경우이므로 0으로 설정
        for i in range(5):
            if self.remain_value[i] < 0:
                self.remain_value[i] = 0
        temp = 0
        for i in range(4):
            temp += self.remain_value[i]
        self.remain_value[7] = self.remain_value[6] - temp

        if(self.remain_value[7]<0):
            self.remain_value[7]=0
        # print()
        # print("필수교양,균형교양,기초교양(수학+과학),전공,공학인증,설계,졸업이수학점,기타")
        # print("기준:", self.require_counts)
        # print("이수:", self.evaluate_value)
        # print("잔여:", self.remain_value)
        # print("영역별 만족여부:", self.evaluate_graduate)
        # print("균형교양 영역별 만족여부:", self.culture_balance)
        # print("균형교양 3학점이상 영역 수:", self.balance_count)


if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = OSSUI()
    sys.exit(app.exec_())