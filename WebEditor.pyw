# -*-coding:utf-8 -*-
import sys, os, time
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtGui import QPixmap
from VPEditorSRC.MainWindow import *
from VPEditorSRC.AppFiles import appFolder

"""
    Recupération des fichiers qui ont été passé en aramêtre pour l'ouverture automatique
"""
arguments = sys.argv
app = QApplication(arguments)
translator = QTranslator()
if len(arguments) == 1:
    locale = QLocale(QLocale.French, QLocale.France)
    translator.load(locale, "vplang_", ".", suffix = "qm")
else:
    translator.load("vplang_."+sys.argv[1], directory="languages", suffix = "qm")
app.installTranslator(translator)

#SplashScreen
splash = QSplashScreen(QPixmap(appFolder+"/images/splashscreen.jpg"))
splash.show()
app.processEvents()
time.sleep(3)

mainWindow = MainWindow()
mainWindow.show()
#Fin du splash
splash.finish(mainWindow)
fichiers = []
i = 1
while i<len(arguments):
    arg = arguments[i]
    if os.path.isfile(arg):
        mainWindow.on_actionOuvrir_triggered(arg)
    i += 1

app.exec_()