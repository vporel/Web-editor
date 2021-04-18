# -*-coding:utf-8 -*-

from PyQt5.QtWidgets import QMessageBox

def alert(parent, message, titre = "Alert"):
    return QMessageBox.information(parent, titre, message, QMessageBox.Ok)