import pyvisa
import time
import csv
import numpy
import schedule
import sys
from FSWP26 import FSWP26
from Meas_VNA import M9373A
from Plan import UI_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QMainWindow, QHBoxLayout,  QGridLayout, QLineEdit, QPushButton, QSpacerItem, QStackedLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5 import QtWidgets
from PyQt5 import QtCore


def test():
    app = QApplication(sys.argv)
    ex = UI_MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    
    
    pn = FSWP26()
    #vna = M9373A()
    #test()

    pn.InitFSWP26Spec()
    pn_data_list = []

    pn_data_list.extend(pn.GetSpecData())
    pn.InitFSWP26PN()
    pn_data_list.extend(pn.GetPNData())
#    pn.UnLink()
#    data_list.extend(vna.VNAInit())

    vna_data_list = []
#    vna_data_list.extend(vna.VNAInit())

    time_list = []
    time_list = time.localtime()
    time_str_list = []
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_list)
    time_str_list = [time_str]

#    data_list.extend(time_str_list)

    with open('file.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(pn_data_list)
        
    with open('file.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        rows[len(rows)-1].extend(vna_data_list)
        print(rows)
    
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        
    with open('file.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        rows[len(rows)-1].extend(time_str_list)
        print(rows)
    
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
