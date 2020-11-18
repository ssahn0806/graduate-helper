import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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

if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = OSSUI()
    sys.exit(app.exec_())