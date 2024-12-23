import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,  QGridLayout
from PyQt5.QtGui import QPalette, QColor

#创建颜色实例
class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout1.setContentsMargins(0,0,0,0)    # 设置外边距
        layout1.setSpacing(20)  # 设置控件之间的间距

        layout2.addWidget(Color('white'))
        layout2.addWidget(Color('purple'))
        layout2.addWidget(Color('green'))

        layout1.addLayout(layout2)

        layout1.addWidget(Color('yellow'))

        layout3.addWidget(Color('blue'))
        layout3.addWidget(Color('red'))

        layout1.addLayout(layout3)

        layout4 = QGridLayout()
        
        layout4.addWidget(Color('black'), 0, 0)
        layout4.addWidget(Color('white'), 0, 1)
        layout4.addWidget(Color('blue'), 4, 0)

        widget = QWidget()  
        widget.setLayout(layout1)
        self.setCentralWidget(widget)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()