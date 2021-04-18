# -*-coding:utf-8 -*-

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QIcon, QPixmap

from prog_languages.languages import LANGUAGES
from src.VPTheme import ICON_APP

class About(QDialog):
    """
        Class which define the dialog box for informations about program
    """
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle("About VPEditor")
        self.setWindowIcon(QIcon(QPixmap(ICON_APP)))
        self.resize(300, 150)
        self.move((parent.width()-300)/2, ((parent.height()-200)/2))
        self.setStyleSheet("background:white;color:darkgray;font:15px comic sans ms;")
        self.windowLayout = QHBoxLayout(self)

        self.widgetLabels = QWidget(self)
        self.widgetLabels.setStyleSheet("max-width:80px")
        self.widgetLabelsLayout = QVBoxLayout(self.widgetLabels)
        self.labelNom = QLabel("Nom : ", self.widgetLabels)
        self.labelVersion = QLabel("Version : ", self.widgetLabels)
        self.labelAuteur = QLabel("Auteur : ", self.widgetLabels)
        self.widgetLabelsLayout.addWidget(self.labelNom)
        self.widgetLabelsLayout.addWidget(self.labelVersion)
        self.widgetLabelsLayout.addWidget(self.labelAuteur)

        self.widgetContenus = QWidget(self)
        self.widgetContenusLayout = QVBoxLayout(self.widgetContenus)
        self.nomApp = QLabel("VPEditor", self.widgetContenus)
        self.versionApp = QLabel("1.2", self.widgetContenus)
        self.auteurApp = QLabel("NKOUANANG Porel", self.widgetContenus)
        self.widgetContenusLayout.addWidget(self.nomApp)
        self.widgetContenusLayout.addWidget(self.versionApp)
        self.widgetContenusLayout.addWidget(self.auteurApp)

        self.windowLayout.addWidget(self.widgetLabels)
        self.windowLayout.addWidget(self.widgetContenus)

