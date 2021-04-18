#-*-coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from VPEdThemeCreatorSRC.MainWindow import MainWindow


app = QApplication(sys.argv)

window = MainWindow()

app.exec_()