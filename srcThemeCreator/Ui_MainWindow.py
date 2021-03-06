# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 617)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setStyleSheet("QWidget#widget_1{border:1px solid lightgray;}")
        self.widget_1.setObjectName("widget_1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labelTitre_2 = QtWidgets.QLabel(self.widget_1)
        self.labelTitre_2.setStyleSheet("font:20px comic sans ms")
        self.labelTitre_2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitre_2.setObjectName("labelTitre_2")
        self.verticalLayout_5.addWidget(self.labelTitre_2)
        self.line_2 = QtWidgets.QFrame(self.widget_1)
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_2.setStyleSheet("background:darkgray;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_5.addWidget(self.line_2)
        self.widget_5 = QtWidgets.QWidget(self.widget_1)
        self.widget_5.setStyleSheet("QWidget#widget_5{border:1px solid lightgray;}")
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_5)
        self.label.setStyleSheet("font:14px sans-serif;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.langages = QtWidgets.QListWidget(self.widget_5)
        self.langages.setObjectName("langages")
        self.verticalLayout_2.addWidget(self.langages)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget_5)
        self.label_2.setStyleSheet("font:14px sans-serif;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.mots = QtWidgets.QListWidget(self.widget_5)
        self.mots.setObjectName("mots")
        self.verticalLayout.addWidget(self.mots)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_5.addWidget(self.widget_5)
        self.widget_3 = QtWidgets.QWidget(self.widget_1)
        self.widget_3.setStyleSheet("QWidget#widget_3{border:1px solid lightgray;}")
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setStyleSheet("font:14px sans-serif;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.couleur = QtWidgets.QPushButton(self.widget_3)
        self.couleur.setMinimumSize(QtCore.QSize(0, 15))
        self.couleur.setStyleSheet("height:45px;")
        self.couleur.setText("")
        self.couleur.setObjectName("couleur")
        self.horizontalLayout_2.addWidget(self.couleur)
        self.changerCouleur = QtWidgets.QPushButton(self.widget_3)
        self.changerCouleur.setMinimumSize(QtCore.QSize(0, 15))
        self.changerCouleur.setStyleSheet("height:45px;")
        self.changerCouleur.setObjectName("changerCouleur")
        self.horizontalLayout_2.addWidget(self.changerCouleur)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_1)
        self.widget_4.setStyleSheet("QWidget#widget_4{border:1px solid lightgray;}")
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setStyleSheet("font:14px sans-serif;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.italique = QtWidgets.QCheckBox(self.widget_4)
        self.italique.setStyleSheet("font:italic 13px sans-serif;margin-left:35px;")
        self.italique.setObjectName("italique")
        self.horizontalLayout_3.addWidget(self.italique)
        self.gras = QtWidgets.QCheckBox(self.widget_4)
        self.gras.setStyleSheet("font:bold 13px sans-serif;margin-left:35px;")
        self.gras.setObjectName("gras")
        self.horizontalLayout_3.addWidget(self.gras)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addWidget(self.widget_4)
        self.labelTitre_2.raise_()
        self.widget_3.raise_()
        self.widget_4.raise_()
        self.widget_5.raise_()
        self.line_2.raise_()
        self.horizontalLayout_4.addWidget(self.widget_1)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setStyleSheet("QWidget#widget_2{border:1px solid lightgray;}")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.labelTitre = QtWidgets.QLabel(self.widget_2)
        self.labelTitre.setStyleSheet("font:20px comic sans ms")
        self.labelTitre.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitre.setObjectName("labelTitre")
        self.verticalLayout_6.addWidget(self.labelTitre)
        self.line = QtWidgets.QFrame(self.widget_2)
        self.line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line.setStyleSheet("background:darkgray")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setMinimumSize(QtCore.QSize(110, 0))
        self.label_5.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_5.setStyleSheet("font:13px sans-serif;")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.nom = QtWidgets.QLineEdit(self.widget_2)
        self.nom.setMinimumSize(QtCore.QSize(200, 0))
        self.nom.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.nom.setObjectName("nom")
        self.horizontalLayout_5.addWidget(self.nom)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.widget_2)
        self.label_7.setMinimumSize(QtCore.QSize(110, 0))
        self.label_7.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_7.setStyleSheet("font:13px sans-serif;")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.auteur = QtWidgets.QLineEdit(self.widget_2)
        self.auteur.setMinimumSize(QtCore.QSize(200, 0))
        self.auteur.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.auteur.setObjectName("auteur")
        self.horizontalLayout_7.addWidget(self.auteur)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.widget_2)
        self.label_6.setMinimumSize(QtCore.QSize(110, 0))
        self.label_6.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_6.setStyleSheet("font:13px sans-serif;")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.general = QtWidgets.QComboBox(self.widget_2)
        self.general.setMinimumSize(QtCore.QSize(200, 0))
        self.general.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.general.setObjectName("general")
        self.general.addItem("")
        self.general.addItem("")
        self.horizontalLayout_6.addWidget(self.general)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.labelPrevisualisation = QtWidgets.QLabel(self.widget_2)
        self.labelPrevisualisation.setStyleSheet("font:17px sans-serif")
        self.labelPrevisualisation.setObjectName("labelPrevisualisation")
        self.verticalLayout_6.addWidget(self.labelPrevisualisation)
        self.previsualisation = QtWidgets.QPlainTextEdit(self.widget_2)
        self.previsualisation.setObjectName("previsualisation")
        self.verticalLayout_6.addWidget(self.previsualisation)
        self.horizontalLayout_4.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionEnregistrer = QtWidgets.QAction(MainWindow)
        self.actionEnregistrer.setObjectName("actionEnregistrer")
        self.actionEnregitrer_sous = QtWidgets.QAction(MainWindow)
        self.actionEnregitrer_sous.setObjectName("actionEnregitrer_sous")
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionNouveau = QtWidgets.QAction(MainWindow)
        self.actionNouveau.setObjectName("actionNouveau")
        self.menuFichier.addAction(self.actionNouveau)
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionEnregistrer)
        self.menuFichier.addAction(self.actionEnregitrer_sous)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFichier.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VPEditor Theme Creator"))
        self.labelTitre_2.setText(_translate("MainWindow", "Modification couleurs"))
        self.label.setText(_translate("MainWindow", "Langages"))
        self.label_2.setText(_translate("MainWindow", "Mots cl??s"))
        self.label_3.setText(_translate("MainWindow", "Couleur"))
        self.changerCouleur.setText(_translate("MainWindow", "Changer couleur"))
        self.label_4.setText(_translate("MainWindow", "Font"))
        self.italique.setText(_translate("MainWindow", "Italique"))
        self.gras.setText(_translate("MainWindow", "Gras"))
        self.labelTitre.setText(_translate("MainWindow", "Cr??ation de th??mes pour  VPEditor"))
        self.label_5.setText(_translate("MainWindow", "Nom du th??me : "))
        self.label_7.setText(_translate("MainWindow", "Auteur : "))
        self.label_6.setText(_translate("MainWindow", "G??n??ral : "))
        self.general.setItemText(0, _translate("MainWindow", "clair"))
        self.general.setItemText(1, _translate("MainWindow", "sombre"))
        self.labelPrevisualisation.setText(_translate("MainWindow", "Pr??visualisation"))
        self.menuFichier.setTitle(_translate("MainWindow", "&Fichier"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionEnregistrer.setText(_translate("MainWindow", "Enregistrer"))
        self.actionEnregitrer_sous.setText(_translate("MainWindow", "Enregitrer-sous"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionNouveau.setText(_translate("MainWindow", "Nouveau"))
