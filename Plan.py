import time
import sympy
import math
import sys
import pyvisa
import csv
import numpy
import schedule
from FSWP26 import FSWP26
from Meas_VNA import M9373A
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QMainWindow, QHBoxLayout,  QGridLayout, QLineEdit, QPushButton, QSpacerItem, QStackedLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5 import QtWidgets
from PyQt5 import QtCore


#创建颜色实例
class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


# 创建应用程序实例
class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        #创建DIALOG
        self.win = QDialog()
        self.button_dia = QPushButton(self.win)
        self.button_dia.setText("关闭")
        self.button_dia.move(50, 50)
        self.button_dia.clicked.connect(lambda: print("Button1 clicked!"))
        self.win.setGeometry(300, 100, 200, 100)
        self.win.show()

        # 创建主窗口
#        self.resize(400, 300)      #改变窗口大小
        self.setWindowTitle("SAW_Test")
        self.setGeometry(300, 300, 500, 500)   #设置窗口的位置和大小     x坐标：窗口左上角的横坐标；y坐标：窗口左上角的纵坐标；宽度：窗口的宽度；高度：窗口的高度。

        #创建文字框
        self.label = QLabel(self)
        self.label.setText("产品编号")
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.move(10, 10)

        # 创建一个按钮并设置点击事件
        self.button = QPushButton("写入数据", self)
#        self.button.clicked.connect(self.on_click)
        self.button.clicked.connect(lambda: print("Button clicked!")) 

        # 布局管理
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

class UI_MainWindow(QMainWindow):
    def __init__(self, pn, vna):
        super().__init__()
        self.pn_data_list = []
        self.vna_data_list = []
        self.time_list = []
        self.time_str_list = []
        self.text_list = []

        self.pn = pn
        self.vna = vna

        self.setWindowTitle("My App")
        self.resize(300, 200)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        
        self.widget = QWidget(self.central_widget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 280, 180))
        self.widget.setObjectName("widget")

        self.pagelayout = QGridLayout(self.widget)
        self.pagelayout.setContentsMargins(0, 0, 0, 0)
        self.pagelayout.setObjectName("pagelayout")

        self.color_stacklayout_1 = QStackedLayout()
        self.color_stacklayout_1.addWidget(Color('white'))
        self.color_stacklayout_1.addWidget(Color('green'))

        self.color_stacklayout_2 = QStackedLayout()
        self.color_stacklayout_2.addWidget(Color('white'))
        self.color_stacklayout_2.addWidget(Color('green'))

        self.color_stacklayout_3 = QStackedLayout()
        self.color_stacklayout_3.addWidget(Color('white'))
        self.color_stacklayout_3.addWidget(Color('green'))

        self.color_stacklayout_4 = QStackedLayout()
        self.color_stacklayout_4.addWidget(Color('white'))
        self.color_stacklayout_4.addWidget(Color('green'))


        self.widget.lineEdit_1 = QLineEdit(self.widget)
        self.widget.lineEdit_1.setObjectName("lineEdit_1")
        self.pagelayout.addWidget(self.widget.lineEdit_1, 0, 0, 1, 1)

        self.widget.lineEdit_2 = QLineEdit(self.widget)
        self.widget.lineEdit_2.setObjectName("lineEdit_2")
        self.pagelayout.addWidget(self.widget.lineEdit_2, 0, 1, 1, 1)

        self.widget.pushButton_1 = QPushButton(self.widget)
        self.widget.pushButton_1.setObjectName("pushButton_1")
        self.widget.pushButton_1.setText("产品编码")
        self.pagelayout.addWidget(self.widget.pushButton_1, 1, 0, 1, 1)
        self.widget.pushButton_1.clicked.connect(self.on_pushButton_1_clicked)
        self.pagelayout.addLayout(self.color_stacklayout_1, 2, 0, 1, 1)


        self.widget.pushButton_2 = QPushButton(self.widget)
        self.widget.pushButton_2.setObjectName("pushButton_2")
        self.widget.pushButton_2.setText("产品状态")
        self.pagelayout.addWidget(self.widget.pushButton_2, 1, 1, 1, 1)
        self.widget.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pagelayout.addLayout(self.color_stacklayout_2, 2, 1, 1, 1)

        self.widget.pushButton_3 = QPushButton(self.widget)
        self.widget.pushButton_3.setObjectName("pushButton_3")
        self.widget.pushButton_3.setText("网分数据获取")
        self.pagelayout.addWidget(self.widget.pushButton_3, 1, 2, 1, 1)
        self.widget.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)
        self.pagelayout.addLayout(self.color_stacklayout_3, 2, 2, 1, 1)

        self.widget.pushButton_4 = QPushButton(self.widget)
        self.widget.pushButton_4.setObjectName("pushButton_4")
        self.widget.pushButton_4.setText("频谱数据获取")
        self.pagelayout.addWidget(self.widget.pushButton_4, 1, 3, 1, 1)
        self.widget.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)
        self.pagelayout.addLayout(self.color_stacklayout_4, 2, 3, 1, 1)

        spacerItem_x = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem_y = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.pagelayout.addItem(spacerItem_y, 3, 0, 1, 1) 
        self.pagelayout.addItem(spacerItem_x, 1, 4, 1, 1)
        self.pagelayout.addItem(spacerItem_x, 0, 2, 1, 1)
        self.pagelayout.addItem(spacerItem_x, 0, 3, 1, 1)
        '''
        self.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))   
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        '''
        #QtCore.QMetaObject.connectSlotsByName(self)


        #button_layout = QHBoxLayout()
        #title_layout = QHBoxLayout()
        #feedback_layout = QHBoxLayout()

        #self.stacklayout = QStackedLayout()

        #pagelayout.addLayout(button_layout, 1, 0)
        #pagelayout.addLayout(title_layout, 0, 0)
        #pagelayout.addLayout(feedback_layout, 2, 0)
        #pagelayout.addLayout(self.stacklayout)

        '''
        self.widget.lineEdit = QLineEdit()
        btn = QPushButton("产品编号")
#        btn.pressed.connect(lambda: print("产品编号"))
        btn.clicked.connect(self.on_button_clicked)
        self.pagelayout.addWidget(btn, 2, 0, 1, 1)
        button_layout.addWidget(btn)
        title_layout.addWidget(self.widget.lineEdit, 1, 0)
        feedback_layout.addWidget(Color('white'))


        btn = QPushButton("产品状态")
        btn.pressed.connect(lambda: print("产品状态"))
        button_layout.addWidget(btn)
        title_layout.addWidget(QLabel("产品状态"))
        feedback_layout.addWidget(Color('white'))

        btn = QPushButton("网分数据")
        btn.pressed.connect(lambda: print("网分数据"))
        button_layout.addWidget(btn)
        title_layout.addWidget(QLabel("网分数据"))
        feedback_layout.addWidget(Color('white'))

        btn = QPushButton("频谱数据")
        btn.pressed.connect(lambda: print("频谱数据"))
        button_layout.addWidget(btn)
        title_layout.addWidget(QLabel("频谱数据"))
        feedback_layout.addWidget(Color('white'))
        '''
   
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)
        #self.setFixedSize(QSize(500, 500))  #设置固定大小的window

    def on_button_clicked(self):
    # 获取 QLineEdit 控件中的文本
        text = self.widget.lineEdit.text()
        print("Text from QLineEdit:", text)

    def on_pushButton_1_clicked(self):            
    # 获取 QLineEdit_1 控件中的文本
        self.color_stacklayout_1.setCurrentIndex(0)
        self.color_stacklayout_2.setCurrentIndex(0)
        self.color_stacklayout_3.setCurrentIndex(0)
        self.color_stacklayout_4.setCurrentIndex(0)

        text = self.widget.lineEdit_1.text()
        self.text_list.clear()
        self.text_list = text.split(",")

        with open('file.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.text_list)
        
        #print("Text from QLineEdit_1:", self.text_list)
        print("Text from QLineEdit_1:", text)
        self.color_stacklayout_1.setCurrentIndex(1)

    def on_pushButton_2_clicked(self):            
    # 获取 QLineEdit_1 控件中的文本
        text = self.widget.lineEdit_2.text()
        self.text_list.clear()
        self.text_list = text.split(",")

        with open('file.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[len(rows)-1].extend(self.text_list)
            #print(rows)

        with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        print("Text from QLineEdit_2:", text)
        self.color_stacklayout_2.setCurrentIndex(1)

    def on_pushButton_3_clicked(self):            
        print("网分数据获取")
        self.vna_data_list.clear()
        self.vna_data_list.extend(self.vna.VNAInit())
        #print(self.vna_data_list)
        self.vna.set_save_file_format('DB')           #设置保存文件格式为DB单位
        text_Qline1 = self.widget.lineEdit_1.text()
        text_Qline2= self.widget.lineEdit_2.text()
        self.vna.save_snp_file(str(text_Qline1) + '_' + str(text_Qline2))     #保存SNP文件
        
        with open('file.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[len(rows)-1].extend(self.vna_data_list)
            #print(rows)

        with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
      
        self.color_stacklayout_3.setCurrentIndex(1)
        
    def on_pushButton_4_clicked(self):            
        print("频谱数据获取")
        self.pn_data_list.clear()
        self.pn.InitFSWP26Spec()
        self.pn_data_list.extend(self.pn.GetSpecData())
        self.pn.InitFSWP26PN()
        self.pn_data_list.extend(self.pn.GetPNData())
        #print(self.pn_data_list)
        self.time_list = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S",self.time_list)
        self.time_str_list = [time_str]
       
        with open('file.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[len(rows)-1].extend(self.pn_data_list)
            #print(rows)

        with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        with open('file.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[len(rows)-1].extend(self.time_str_list)
            #print(rows)

        with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self.color_stacklayout_4.setCurrentIndex(1)
        
def main():
    pn = FSWP26()
    vna = M9373A()
    app = QApplication(sys.argv)
    ex = UI_MainWindow(pn = pn, vna = vna)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
#    window() 
    main()


    



