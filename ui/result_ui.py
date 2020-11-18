import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ResultUI(QWidget):

    def __init__(self):
        super().__init__()
        self.resultUI()
        self.show()
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

        for i in range(6):
            string = "-"
            item = QTableWidgetItem(string)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#DDEBF7"))
            self.tableWidgetDetail.setItem(0, i, item)
            item2 = QTableWidgetItem(string)
            item2.setTextAlignment(Qt.AlignCenter)
            self.tableWidgetDetail.setItem(1,i,item2)
    def closeEvent(self, event):
        event.accept()
        sys.exit(0)

if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = ResultUI()
    sys.exit(app.exec_())