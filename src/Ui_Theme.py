# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Theme_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialogTheme(object):
    def setupUi(self, dialogTheme):
        dialogTheme.setObjectName("dialogTheme")
        dialogTheme.resize(700, 439)
        dialogTheme.setMinimumSize(QtCore.QSize(700, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/VPOREL-PC/.designer/backup/images/logo-bleu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialogTheme.setWindowIcon(icon)
        dialogTheme.setStyleSheet("color:lightgray;background:rgb(50,50,50)")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(dialogTheme)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.titre = QtWidgets.QLabel(dialogTheme)
        self.titre.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titre.setStyleSheet("font:25px calibri;padding-left:5px;")
        self.titre.setObjectName("titre")
        self.verticalLayout_5.addWidget(self.titre)
        self.zoneTheme = QtWidgets.QWidget(dialogTheme)
        self.zoneTheme.setStyleSheet("QWidget#zoneTheme{border-top:2px solid lightgray;}")
        self.zoneTheme.setObjectName("zoneTheme")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.zoneTheme)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.zoneTheme)
        self.label.setStyleSheet("font:15px calibri;margin: 0 10px")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxThemes = QtWidgets.QComboBox(self.zoneTheme)
        self.comboBoxThemes.setStyleSheet("border:1px solid lightgray;width:100px;")
        self.comboBoxThemes.setObjectName("comboBoxThemes")
        self.horizontalLayout.addWidget(self.comboBoxThemes)
        self.label_6 = QtWidgets.QLabel(self.zoneTheme)
        self.label_6.setStyleSheet("font:15px calibri;margin: 0 10px")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.comboBoxGeneral = QtWidgets.QComboBox(self.zoneTheme)
        self.comboBoxGeneral.setStyleSheet("border:1px solid lightgray;width:100px;")
        self.comboBoxGeneral.setObjectName("comboBoxGeneral")
        self.comboBoxGeneral.addItem("")
        self.comboBoxGeneral.addItem("")
        self.horizontalLayout.addWidget(self.comboBoxGeneral)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(self.zoneTheme)
        self.splitter.setMinimumSize(QtCore.QSize(0, 300))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setMaximumSize(QtCore.QSize(150, 16777215))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("font:15px calibri;")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listLangages = QtWidgets.QListWidget(self.widget)
        self.listLangages.setStyleSheet("border:1px solid lightgray;")
        self.listLangages.setObjectName("listLangages")
        self.verticalLayout.addWidget(self.listLangages)
        self.widget_3 = QtWidgets.QWidget(self.splitter)
        self.widget_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setStyleSheet("font:15px calibri;")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listMots = QtWidgets.QListWidget(self.widget_3)
        self.listMots.setStyleSheet("border:1px solid lightgray;")
        self.listMots.setObjectName("listMots")
        self.verticalLayout_2.addWidget(self.listMots)
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setMinimumSize(QtCore.QSize(280, 0))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupCouleurs = QtWidgets.QGroupBox(self.widget_2)
        self.groupCouleurs.setStyleSheet("QGroupBox{font:15px calibri;}")
        self.groupCouleurs.setObjectName("groupCouleurs")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupCouleurs)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.couleur = QtWidgets.QPushButton(self.groupCouleurs)
        self.couleur.setStyleSheet("min-height:45px;")
        self.couleur.setText("")
        self.couleur.setObjectName("couleur")
        self.verticalLayout_6.addWidget(self.couleur)
        self.pushButtonChangerCouleur = QtWidgets.QPushButton(self.groupCouleurs)
        self.pushButtonChangerCouleur.setStyleSheet("min-height:45px;border-radius:5px;border:2px solid lightgray;width:100px;font-size:15px;")
        self.pushButtonChangerCouleur.setObjectName("pushButtonChangerCouleur")
        self.verticalLayout_6.addWidget(self.pushButtonChangerCouleur)
        self.verticalLayout_3.addWidget(self.groupCouleurs)
        self.groupMots = QtWidgets.QGroupBox(self.widget_2)
        self.groupMots.setStyleSheet("QGroupBox{font:15px calibri;}")
        self.groupMots.setObjectName("groupMots")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupMots)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBoxItalique = QtWidgets.QCheckBox(self.groupMots)
        self.checkBoxItalique.setStyleSheet("font:italic 20px sans-serif;min-height:30px;padding-left:25px;")
        self.checkBoxItalique.setObjectName("checkBoxItalique")
        self.verticalLayout_7.addWidget(self.checkBoxItalique)
        self.checkBoxGras = QtWidgets.QCheckBox(self.groupMots)
        self.checkBoxGras.setStyleSheet("font:bold 20px sans-serif;min-height:30px;padding-left:25px;")
        self.checkBoxGras.setObjectName("checkBoxGras")
        self.verticalLayout_7.addWidget(self.checkBoxGras)
        self.verticalLayout_3.addWidget(self.groupMots)
        self.verticalLayout_4.addWidget(self.splitter)
        self.verticalLayout_5.addWidget(self.zoneTheme)

        self.retranslateUi(dialogTheme)
        QtCore.QMetaObject.connectSlotsByName(dialogTheme)

    def retranslateUi(self, dialogTheme):
        _translate = QtCore.QCoreApplication.translate
        dialogTheme.setWindowTitle(_translate("dialogTheme", "Th??me"))
        self.titre.setText(_translate("dialogTheme", "Th??me VPEditor"))
        self.label.setText(_translate("dialogTheme", "Th??mes pr??d??finis :"))
        self.label_6.setText(_translate("dialogTheme", "G??n??ral : "))
        self.comboBoxGeneral.setItemText(0, _translate("dialogTheme", "Th??me sombre"))
        self.comboBoxGeneral.setItemText(1, _translate("dialogTheme", "Th??me clair"))
        self.label_2.setText(_translate("dialogTheme", "Langages :"))
        self.label_3.setText(_translate("dialogTheme", "Mots : "))
        self.groupCouleurs.setTitle(_translate("dialogTheme", "Couleurs"))
        self.pushButtonChangerCouleur.setText(_translate("dialogTheme", "Changer couleur"))
        self.groupMots.setTitle(_translate("dialogTheme", "Font"))
        self.checkBoxItalique.setText(_translate("dialogTheme", "Italique"))
        self.checkBoxGras.setText(_translate("dialogTheme", "Gras"))
