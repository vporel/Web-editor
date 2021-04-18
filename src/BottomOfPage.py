# -*-coding:utf-8 -*-
"""
    define the window's bottom section

"""

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, \
    QHBoxLayout, QLabel, QGroupBox, QListWidget, QListWidgetItem, QSpacerItem
from src.AppFiles import ProjectFile, Project, UserFile
import os

class BottomTab(QWidget):
    """This define the tab of bottom page"""
    def __init__(self, parent):
        QWidget.__init__(self, parent)

class Links(BottomTab):
    """This part will show the files which have a link with the current file"""
    def __init__(self, parent, path = None, window = None):
        BottomTab.__init__(self, parent)
        self.path = path
        self.window = window
        self.layout = QVBoxLayout(self)
        """Building of interface"""
        #Top
        self.top = QWidget(self)
        self.topLayout = QHBoxLayout(self.top)
        self.labelProjectName = QLabel("Projet : ",self.top)
        self.labelProjectName.setObjectName("label1_links")
        self.projectName = QLabel("Aucun", self.top)
        self.projectName.setObjectName("content1_links")
        self.labelName = QLabel("Nom : ",self.top)
        self.labelName.setObjectName("label2_links")
        self.name = QLabel("Inconnu", self.top)
        self.name.setObjectName("content2_links")
        self.labelType = QLabel("Type : ",self.top)
        self.labelType.setObjectName("label3_links")
        self.type = QLabel("Inconnu", self.top)
        self.type.setObjectName("content3_links")
        self.topLayout.addWidget(self.labelProjectName)
        self.topLayout.addWidget(self.projectName)
        self.topLayout.addWidget(self.labelName)
        self.topLayout.addWidget(self.name)
        self.topLayout.addWidget(self.labelType)
        self.topLayout.addWidget(self.type)
        spacer = QSpacerItem(250,20)
        self.topLayout.addItem(spacer)
        self.layout.addWidget(self.top, 1)
        #Bottom
        self.bottom = QWidget(self)
        self.bottomLayout = QHBoxLayout(self.bottom)
        self.mainFiles = QGroupBox(self.tr("Fichiers principaux liés"), self.bottom)
        self.mainFiles.setObjectName("list1_links")
        self.mainFilesList = QListWidget(self.mainFiles)
        mfLayout = QVBoxLayout(self.mainFiles)
        mfLayout.addWidget(self.mainFilesList)

        self.styleFiles = QGroupBox(self.tr("Styles liés"), self.bottom)
        self.styleFiles.setObjectName("list2_links")
        self.styleFilesList = QListWidget(self.styleFiles)
        stfLayout = QVBoxLayout(self.styleFiles)
        stfLayout.addWidget(self.styleFilesList)

        self.scriptFiles = QGroupBox(self.tr("Scripts liés"), self.bottom)
        self.scriptFiles.setObjectName("list3_links")
        self.scriptFilesList = QListWidget(self.scriptFiles)
        scfLayout = QVBoxLayout(self.scriptFiles)
        scfLayout.addWidget(self.scriptFilesList)

        self.details = QGroupBox(self.tr("Détails"), self.bottom)
        self.chemin_det = QLabel(self.details)
        dLayout = QVBoxLayout(self.details)
        dLayout.addWidget(self.chemin_det)
        self.bottomLayout.addWidget(self.mainFiles)
        self.bottomLayout.addWidget(self.styleFiles)
        self.bottomLayout.addWidget(self.scriptFiles)
        self.bottomLayout.addWidget(self.details)
        self.layout.addWidget(self.bottom, 3)
        self.setStyleSheet("""
            *{font-family:calibri;}
            QLabel{max-height:35px;font-size:15px;}
            QLabel#label1_links, QLabel#label2_links, QLabel#label3_links{max-width:70px;}
            QLabel#content1_links, QLabel#content2_links, QLabel#content3_links{font-weight:bold;}
            #list1_links,#list2_links,#list3_links{max-width:250px;}
        """)

        self.refresh(path)

    def refresh(self, path = None):
        if path is not None:
            self.path = path
        #Nettoyage de listes et des champs
        self.projectName.setText("Aucun")
        self.name.setText("Inconnu")
        self.type.setText("Inconnu")
        self.mainFilesList.clear()
        self.styleFilesList.clear()
        self.scriptFilesList.clear()
        self.chemin_det.setText("")
        if self.path is not None:
            if os.path.isfile(self.path):
                file = UserFile(self.path)
                self.name.setText(file.name())
                isProjectFile, projectFile = False, None
                projects = self.window.opennedProjects
                project = None
                for p in projects:
                    isProjectFile, projectFile = p.isProjectFile(self.path)
                    if isProjectFile:
                        project = p
                if isProjectFile:
                    self.projectName.setText(project.name)
                    self.type.setText(projectFile.type)
                    for pf in projectFile.links[ProjectFile.MAIN_FILE]:
                        item = QListWidgetItem(pf.name)
                        item.projectFile = pf
                        self.mainFilesList.addItem(item)
                    for pf in projectFile.links[ProjectFile.STYLE_FILE]:
                        item = QListWidgetItem(pf.name)
                        item.projectFile = pf
                        self.styleFilesList.addItem(item)
                    for pf in projectFile.links[ProjectFile.SCRIPT_FILE]:
                        item = QListWidgetItem(pf.name)
                        item.projectFile = pf
                        self.scriptFilesList.addItem(item)
                    self.mainFilesList.itemClicked.connect(self.on_widgetList_itemClicked)
                    self.styleFilesList.itemClicked.connect(self.on_widgetList_itemClicked)
                    self.scriptFilesList.itemClicked.connect(self.on_widgetList_itemClicked)
    def on_widgetList_itemClicked(self, item):
        projectFile = item.projectFile
        self.chemin_det.setText(self.tr("Chemin : ")+projectFile.path)


class BottomOfPage(QTabWidget):
    """Class"""
    def __init__(self, parent, window):
        QTabWidget.__init__(self, parent)
        self.window = window
        self.theme = parent.theme
        self.setStyleSheet(self.theme.styleFolders)
        self.init()
        
    def init(self):
        self.tabLinks = Links(self, window = self.window)
        self.addTab(self.tabLinks, "Links")

    def refreshLinks(self, path:str):
        """Update link's zone with the links of the new file"""
        self.tabLinks.refresh(path)
