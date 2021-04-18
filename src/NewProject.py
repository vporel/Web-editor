# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QDialog, QFileDialog,QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot
import os
from src.Ui_NewProject import *
from src.AppFiles import Project, ProjectFile, UserFile, AppFile

class NewProject(QDialog, Ui_Dialog):
    ACTION_NEW = "nouveau"
    ACTION_MODIFY = "modifier"

    def __init__(self, parent, path = None, action = ACTION_NEW, project = None):
        self.parent = parent
        self.action = action
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.verticalLayout_2.setContentsMargins(0,0,0,0)
        self.path = path
        self.project = Project(None, path)
        if project is not None:
            self.project = project
        self.init()

    def init(self):
        if self.action == NewProject.ACTION_NEW:
            self.title.setText(self.tr("Nouveau projet"))
            coupure = self.path.split('/')
            if len(coupure) <= 1:
                coupure = self.path.split('\\')
            self.lineEditName.setText(coupure[len(coupure) - 1])
            self.lineEditPath.setText(self.path)
            self.comboBoxType.currentTextChanged.connect(self.on_comboBoxType_currentTextChanged)

        #On vide les listes
        self.listWidgetMainFiles.clear()
        self.listWidgetStyles.clear()
        self.listWidgetScripts.clear()
        #On masque les boutons d'ajout de styles et de scripts
        self.pushButtonAddStyle.setEnabled(False)
        self.pushButtonAddScript.setEnabled(False)
        #slots

        if self.action == NewProject.ACTION_MODIFY:
            self.title.setText(self.tr("Modifier projet"))
            self.lineEditName.setText(self.project.name)
            self.lineEditName.setReadOnly(True)
            self.lineEditPath.setText(self.project.path)
            self.lineEditPath.setReadOnly(True)
            self.lineEditUrl.setText(self.project.urlforbrowser)
            self.lineEditUrl.setReadOnly(True)
            self.pushButtonChanger.setEnabled(False)
            self.comboBoxType.setCurrentText(self.project.type)
            """Ajout des fichiers"""
            for file in self.project.getAllFiles():
                path = file.path
                coupure = path.split('/')
                if len(coupure) <= 1:
                    coupure = path.split('\\')
                item = QListWidgetItem(file.name + "(../" + coupure[-3] + "/" + coupure[-2] + ")")
                item.projectFile = file
                if file.type == ProjectFile.MAIN_FILE:
                    self.listWidgetMainFiles.addItem(item)
                elif file.type == ProjectFile.STYLE_FILE:
                    self.listWidgetStyles.addItem(item)
                elif file.type == ProjectFile.SCRIPT_FILE:
                    self.listWidgetScripts.addItem(item)
            self.listWidgetMainFiles.itemClicked.connect(self.on_listWidgetMainFiles_itemChanged)
            self.listWidgetStyles.itemClicked.connect(self.on_listWidgetStyles_itemChanged)
            self.listWidgetScripts.itemClicked.connect(self.on_listWidgetScripts_itemChanged)

    @pyqtSlot()
    def on_pushButtonChanger_clicked(self):
        """To change the path of project"""
        path = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier", "C:\\", QFileDialog.ShowDirsOnly)
        if path:
            self.path = path
            self.lineEditPath.setText(path)
            coupure = self.path.split('/')
            if len(coupure) <= 1:
                coupure = self.path.split('\\')
            self.lineEditName.setText(coupure[len(coupure) - 1])


    def on_comboBoxType_currentTextChanged(self, t):
        """When the type is changed"""
        if t.lower() == Project.SIMPLE_TYPE:
            self.lineEditUrl.setReadOnly(True)
        else:
            self.lineEditUrl.setReadOnly(False)

    def addFiles(self, widget:QListWidget, extensions:list, type = None):
        """Add project files"""
        filter = ""
        for ext in extensions:
            filter += ext.upper()+" "
        filter += "("
        for ext in extensions:
            filter += "*."+ext+" "
        filter += ")"
        paths, filters = QFileDialog.getOpenFileNames(self, self.tr("Selectionnez les fichiers"), self.path, filter)
        if paths:
            for path in paths:
                if path.find(self.path) == 0:
                    file = UserFile(path)
                    if file.extension().lower() not in extensions:
                        message = "Le fichier " + path + " n'a pas l'extension requise ("+", ".join(extensions)+")"
                        msg = QMessageBox.information(self, "Echec ajout", message, QMessageBox.Ok)
                    else:
                        coupure = path.split('/')
                        if len(coupure) <= 1:
                            coupure = path.split('\\')
                        projectFile = ProjectFile(file.name(), path, type)
                        item = QListWidgetItem(file.name()+"(../"+coupure[-3]+"/"+coupure[-2]+")")
                        item.projectFile = projectFile
                        itemExist = False
                        index = 0
                        while index < widget.count():
                            if widget.item(index).text() == item.text():
                                itemExist = True
                            index += 1
                        if not itemExist:
                            widget.addItem(item)
                            if type != ProjectFile.MAIN_FILE:
                                for pf in self.project.files[ProjectFile.MAIN_FILE]:
                                    if pf.path == widget.mainFile.path:
                                        pf.addLink(projectFile)
                            self.project.addFile(projectFile)
                else:
                    message = "Le fichier "+path+" n'est pas dans le dossier du projet."
                    msg = QMessageBox.information(self, "Echec ajout", message, QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButtonAddMainFile_clicked(self):
        """To add a main file"""
        self.addFiles(self.listWidgetMainFiles, ["html", "htm", "php"], ProjectFile.MAIN_FILE)
        self.listWidgetMainFiles.itemClicked.connect(self.on_listWidgetMainFiles_itemChanged)

    def on_listWidgetMainFiles_itemChanged(self, item):
        """When one main file is selected"""
        self.pushButtonAddStyle.setEnabled(True)
        self.pushButtonAddScript.setEnabled(True)
        self.listWidgetStyles.mainFile = item.projectFile
        self.listWidgetScripts.mainFile = item.projectFile
        #Research of file project which is associated
        projectFile = None
        for pf in self.project.files[ProjectFile.MAIN_FILE]:
            if pf.path == item.projectFile.path:
                projectFile = pf
        if projectFile is not None:
            self.listWidgetStyles.clear()
            self.listWidgetScripts.clear()
            for styleFile in projectFile.links[ProjectFile.STYLE_FILE]:
                path = styleFile.path
                coupure = path.split('/')
                if len(coupure) <= 1:
                    coupure = path.split('\\')
                item = QListWidgetItem(styleFile.name + "(../" + coupure[-3] + "/" + coupure[-2] + ")")
                item.projectFile = styleFile
                self.listWidgetStyles.addItem(item)
            for scriptFile in projectFile.links[ProjectFile.SCRIPT_FILE]:
                path = scriptFile.path
                coupure = path.split('/')
                if len(coupure) <= 1:
                    coupure = path.split('\\')
                item = QListWidgetItem(scriptFile.name + "(../" + coupure[-3] + "/" + coupure[-2] + ")")
                item.projectFile = scriptFile
                self.listWidgetScripts.addItem(item)

    def on_listWidgetStyles_itemChanged(self, item):
        """When one style file is selected"""
        pass

    def on_listWidgetScripts_itemChanged(self, item):
        """When one style file is selected"""
        pass

    @pyqtSlot()
    def on_pushButtonAddStyle_clicked(self):
        """To add a style file"""
        if self.listWidgetMainFiles.count() > 0:
            self.addFiles(self.listWidgetStyles, ["css", "scss"], ProjectFile.STYLE_FILE)
        else:
            message = self.tr("Sélectionnez un fichier principal auquel ceux-ci seront ajoutés")
            msg = QMessageBox.information(self, self.tr("Aucun fichier sélectionné"), message, QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButtonAddScript_clicked(self):
        """To add a script file"""
        if self.listWidgetMainFiles.count() > 0:
            self.addFiles(self.listWidgetScripts, ["js", "php"], ProjectFile.SCRIPT_FILE)
        else:
            message = self.tr("Sélectionnez un fichier principal auquel ceux-ci seront ajoutés")
            msg = QMessageBox.information(self, self.tr("Aucun fichier sélectionné"), message, QMessageBox.Ok)

    def removeFile(self, listWidget:QListWidget):
        selection = listWidget.selectedItems()
        if len(selection) <=0:
            message = "Selectionnez un fichier à retirer"
            msg, response = QMessageBox.warning(self, "Warning", message)
        else:
            item = selection[0]
            if item.projectFile.type == ProjectFile.MAIN_FILE:
                self.listWidgetStyles.clear()
                self.listWidgetScripts.clear()
            listWidget.removeItemWidget(item)

    @pyqtSlot()
    def on_pushButtonRemoveMain_clicked(self):
        """Remove a main file"""
        self.removeFile(self.listWidgetMainFiles)

    @pyqtSlot()
    def on_pushButtonRemoveStyle_clicked(self):
        """Remove a main file"""
        self.removeFile(self.listWidgetStyles)

    @pyqtSlot()
    def on_pushButtonRemoveScript_clicked(self):
        """Remove a main file"""
        self.removeFile(self.listWidgetScripts)

    @pyqtSlot()
    def on_pushButtonOk_clicked(self):
        """When clicking on ok button"""
        if self.action == NewProject.ACTION_NEW:
            #Definition of project attributes
            name = self.lineEditName.text()
            path = self.path
            type = self.comboBoxType.currentText()
            urlforbrowser = None
            if type.lower() == Project.LOCAL_TYPE:
                urlforbrowser = self.lineEditUrl.text()
            self.project.name = name
            self.project.path = path
            self.project.type = type
            self.project.urlforbrowser = urlforbrowser
            pathFile = path+"/"+name+".vpp"
        else:
            pathFile = self.project.path+"/"+self.project.name+".vpp"
        fileToSave = AppFile(pathFile)
        fileToSave.write(self.project)
        if self.action == NewProject.ACTION_NEW:
            self.parent.on_actionOpenRecentProject_triggered(self.project)

        self.on_pushButtonCancel_clicked()

    @pyqtSlot()
    def on_pushButtonCancel_clicked(self):
        """When clicking on cancel button"""
        self.hide()
        self.close()