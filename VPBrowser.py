#-*-coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from VPBrowserSRC.BrowserWindow import BrowserWindow


app = QApplication(sys.argv)

window = BrowserWindow()
window.show()

app.exec_()