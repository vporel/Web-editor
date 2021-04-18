#-*-coding:utf-8 -*-
from PyQt5.QtWidgets import QWidget, QTreeView, QFileSystemModel, QScrollBar, QSplitter, QTabWidget, QVBoxLayout
from PyQt5.QtCore import QDir, Qt, QModelIndex
from PyQt5.QtGui import QColor, QPixmap
from src.AppFiles import *

class SystemModel(QFileSystemModel):
    def __init__(self, parent, url):
        QFileSystemModel.__init__(self, parent)
        self.setRootPath(url)

    def data(self, index:QModelIndex, role:int):
        """Modification des datas"""
        if role == Qt.DecorationRole:
            info = self.fileInfo(index)
            if info.isFile():
                fichier = UserFile(info.filePath())
                return fichier.pixMap()
        return QFileSystemModel.data(self, index, role)
class Folder(QTreeView):
    """Dossier ouvert par l'utilisateur"""
    def __init__(self, parent, url, nom):
        QTreeView.__init__(self, parent)
        self.parent = parent
        self.url = url
        self.nom = nom
        self.model = SystemModel(self, url)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(url))
        self.show
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)

        self.theme = parent.theme
        self.setStyleSheet(self.theme.styleFolder)

        self.doubleClicked.connect(self.on_doucleClicked)

    def on_doucleClicked(self, index):
        """Lorsqu'on doucle-clique sur un élément"""
        url = self.model.filePath(index)
        if not self.model.isDir(index):
            self.parent.window.on_actionOpenFile_triggered(url)

class Folders(QWidget):
    """Class contenant les dossiers ouverts par l'utilisateur"""
    def __init__(self, parent, window):
        QWidget.__init__(self,parent)
        self.window = window
        self.theme = parent.theme
        self.setStyleSheet(self.theme.styleFolders)
        self.foldersList = []
        self.foldersLayout = QVBoxLayout(self)
        self.foldersLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.foldersLayout)

    def addFolder(self, url:str, name:str = None):
        """Ajout d'un nouveau dossier"""
        if name is None:
            #Recherche du nom
            splitUrl = url.split("/")
            name = splitUrl[len(splitUrl)-1]
        (exist, index) = self.folderExist(url)
        if not exist:
            folder = Folder(self, url, name)
            self.foldersList.append(folder)
            self.foldersLayout.addWidget(folder)
            self.window.initFolders("add")


    def currentFolder(self, index = None):
        """Retourne de dossier ouvert"""
        if index is None:
            return self.foldersList[self.currentIndex()]
        return self.foldersList[index]

    def folderExist(self, url):
        """Vérification de l'existence d'un dossier"""
        exist = False
        index = -1
        for i, folder in enumerate(self.foldersList):
            if url == folder.url:
                exist = True
                index = i
        return exist, index

    def removeFolder(self, index:int):
        """Fermeture d'un dossier"""
        del self.foldersList[index]
        self.window.initFolders("remove")
