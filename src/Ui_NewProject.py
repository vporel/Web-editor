# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewProject_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(588, 423)
        Dialog.setStyleSheet("*{color:lightgray;background-color:rgb(50,50,50);}\n"
"QDialog{background-color:rgb(50,50,50);}\n"
"QLineEdit{border:1px solid lightgray;height:25px;}\n"
"QPushButton{border:1px solid rgb(130,130,130);border-radius:5px;padding:5px 5px;color:rgb(130,130,130);}QPushButton:hover{background:rgb(110,110,110);}QPushButton::enabled{color:lightgray;border-color:lightgray;}")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title.setStyleSheet("font:25px calibri;padding-left:5px;")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.zoneProjet = QtWidgets.QWidget(Dialog)
        self.zoneProjet.setStyleSheet("QWidget#zoneProjet{border-top:2px solid lightgray;}")
        self.zoneProjet.setObjectName("zoneProjet")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.zoneProjet)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.zoneProjet)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setStyleSheet("font:15px calibri;margin: 0 5px")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditName = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.widget_2)
        self.label_7.setStyleSheet("font:15px calibri;margin: 0 5px")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 3, 1, 1)
        self.comboBoxType = QtWidgets.QComboBox(self.widget_2)
        self.comboBoxType.setStyleSheet("border:1px solid lightgray;width:100px;")
        self.comboBoxType.setObjectName("comboBoxType")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.gridLayout.addWidget(self.comboBoxType, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_2)
        self.label_6.setStyleSheet("font:15px calibri;margin: 0 5px")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineEditPath = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditPath.setReadOnly(True)
        self.lineEditPath.setPlaceholderText("")
        self.lineEditPath.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEditPath.setObjectName("lineEditPath")
        self.gridLayout.addWidget(self.lineEditPath, 1, 1, 1, 1)
        self.pushButtonChanger = QtWidgets.QPushButton(self.widget_2)
        self.pushButtonChanger.setObjectName("pushButtonChanger")
        self.gridLayout.addWidget(self.pushButtonChanger, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_2)
        self.label_8.setStyleSheet("font:15px calibri;margin: 0 5px")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 3, 1, 1)
        self.lineEditUrl = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditUrl.setReadOnly(True)
        self.lineEditUrl.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEditUrl.setObjectName("lineEditUrl")
        self.gridLayout.addWidget(self.lineEditUrl, 1, 4, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.groupBox = QtWidgets.QGroupBox(self.zoneProjet)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonAddStyle = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonAddStyle.setObjectName("pushButtonAddStyle")
        self.gridLayout_2.addWidget(self.pushButtonAddStyle, 1, 1, 1, 1)
        self.pushButtonAddScript = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonAddScript.setObjectName("pushButtonAddScript")
        self.gridLayout_2.addWidget(self.pushButtonAddScript, 1, 2, 1, 1)
        self.pushButtonAddMainFile = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonAddMainFile.setObjectName("pushButtonAddMainFile")
        self.gridLayout_2.addWidget(self.pushButtonAddMainFile, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setStyleSheet("font-style:italic;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 2)
        self.listWidgetScripts = QtWidgets.QListWidget(self.groupBox)
        self.listWidgetScripts.setObjectName("listWidgetScripts")
        self.gridLayout_2.addWidget(self.listWidgetScripts, 2, 2, 1, 1)
        self.listWidgetStyles = QtWidgets.QListWidget(self.groupBox)
        self.listWidgetStyles.setObjectName("listWidgetStyles")
        self.gridLayout_2.addWidget(self.listWidgetStyles, 2, 1, 1, 1)
        self.listWidgetMainFiles = QtWidgets.QListWidget(self.groupBox)
        self.listWidgetMainFiles.setObjectName("listWidgetMainFiles")
        self.gridLayout_2.addWidget(self.listWidgetMainFiles, 1, 0, 2, 1)
        self.pushButtonRemoveStyle = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRemoveStyle.setObjectName("pushButtonRemoveStyle")
        self.gridLayout_2.addWidget(self.pushButtonRemoveStyle, 3, 1, 1, 1)
        self.pushButtonRemoveScript = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRemoveScript.setObjectName("pushButtonRemoveScript")
        self.gridLayout_2.addWidget(self.pushButtonRemoveScript, 3, 2, 1, 1)
        self.pushButtonRemoveMain = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRemoveMain.setObjectName("pushButtonRemoveMain")
        self.gridLayout_2.addWidget(self.pushButtonRemoveMain, 3, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.widget = QtWidgets.QWidget(self.zoneProjet)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(444, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonOk = QtWidgets.QPushButton(self.widget)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtWidgets.QPushButton(self.widget)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout_2.addWidget(self.zoneProjet)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Nouveau  projet"))
        self.title.setText(_translate("Dialog", "Nouveau projet"))
        self.label.setText(_translate("Dialog", "Nom du projet : "))
        self.label_7.setText(_translate("Dialog", "Type :"))
        self.comboBoxType.setItemText(0, _translate("Dialog", "simple"))
        self.comboBoxType.setItemText(1, _translate("Dialog", "local"))
        self.label_6.setText(_translate("Dialog", "Emplacement : "))
        self.pushButtonChanger.setText(_translate("Dialog", "Changer"))
        self.label_8.setText(_translate("Dialog", "Url :"))
        self.lineEditUrl.setPlaceholderText(_translate("Dialog", "Si le type est \"local\""))
        self.groupBox.setTitle(_translate("Dialog", "Liens entre fichiers"))
        self.pushButtonAddStyle.setText(_translate("Dialog", "Ajouter un style"))
        self.pushButtonAddScript.setText(_translate("Dialog", "Ajouter un script (JS ou PHP)"))
        self.pushButtonAddMainFile.setText(_translate("Dialog", "Ajouter un fichier principal"))
        self.label_2.setText(_translate("Dialog", "Si un fichier est modifi??, tout fichier principal auquel il est li??\n"
" sera automatiquement actualis?? en cas de visualisation"))
        self.pushButtonRemoveStyle.setText(_translate("Dialog", "Retirer"))
        self.pushButtonRemoveScript.setText(_translate("Dialog", "Retirer"))
        self.pushButtonRemoveMain.setText(_translate("Dialog", "Retirer"))
        self.pushButtonOk.setText(_translate("Dialog", "OK"))
        self.pushButtonCancel.setText(_translate("Dialog", "Annuler"))
