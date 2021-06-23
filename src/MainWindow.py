# -*-coding:utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QSplitter, QFileDialog, QMessageBox, QDialog, \
    QInputDialog, QProgressDialog, QDesktopWidget, QHBoxLayout, QVBoxLayout, \
    QMenuBar, QMenu, QAction
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSlot, QMetaObject, Qt, QTimer, QUrl

from src import Ui_MainWindow
from src.Menu import *
from src.AppFiles import *
from src.VPTheme import *
from src.TabsBlock import *
from src.Folders import *
from src.BottomOfPage import *

from src.Recherche import *
from src.ThemeDialog import *
from src.NewProject import *
from src.About import *

from prog_languages.languages import *

from srcBrowser.BrowserWindow import *


class MainWindow(QMainWindow, Ui_MainWindow.Ui_MainWindow):
    """
    ---------------Main window of application -----
    ------------------- Extends from QMainWindow and Ui_MainWindow
    """

    """Constructeur"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.updateUi()
        #Positionning
        size_screen = QDesktopWidget().screenGeometry()
        #self.setGeometry(size_screen)
        self.ouvertureTabs = True
        self.ouvertureFolders = True

        #For visualisation
        self.browser = BrowserWindow(self)

        self.initProjects()
        self.initTabs()
        self.initFolders()
        QMetaObject.connectSlotsByName(self)

    def updateUi(self):
        self.theme = theme
        #Title
        self.setWindowTitle("Web Editor")
        #Hide top bar
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)

        #Menu
        self.createMenuBar()

        #folder's part
        self.projectsBottom.theme = self.theme
        self.folders = Folders(self.projectsBottom, self)
        self.foldersLayout = QVBoxLayout(self.projectsBottom)
        self.foldersLayout.addWidget(self.folders)
        self.foldersLayout.setContentsMargins(1, 1, 0, 0)
        self.folders.setStyleSheet("background:transparent;")

        # tab's part
        self.editor.theme = self.theme
        self.tabs = Tabs(self.editor, self)
        self.editorLayout = QVBoxLayout(self.editor)
        self.editorLayout.addWidget(self.tabs)
        self.editorLayout.setContentsMargins(0,0,0,0)

        self.splitterContent.setSizes([450, 100])
        self.splitterCenter.setSizes([100, 450])
        #Buttons top
        self.closeBtn.clicked.connect(self.close)
        self.growBtn.clicked.connect(self.showMaximized)
        self.shrinkBtn.clicked.connect(self.showMinimized)

    def createMenuBar(self):
        self.menuLayout = QVBoxLayout(self.menu)
        self.menuLayout.setContentsMargins(0,5,0,0)
        self.menuBar = MenuBar(self.menu)

        # Menu File
        self.menuFile = Menu("&File", self.menuBar)
        self.actionNewFile = Action("&New file", self.menuFile, icon="images/icones/new-file-cadre.png", name="actionNewFile", shortcut="CTRL+N")
        self.actionOpenFile = Action("&Open file", self.menuFile, name="actionOpenFile", shortcut="CTRL+O")
        self.actionNewProject = Action("&New project", self.menuFile, name="actionNewProject")
        self.actionNewProjectFile = Action("&New project file", self.menuFile, icon="images/icones/new-file-cadre.png", name="actionNewProjectFile")
        self.actionOpenRecentProject = Action("&Open recent project", self.menuFile, name = "actionOpenRecentProject")
        self.actionSaveFile = Action("&Save", self.menuFile, icon="images/icones/save.png", name="actionSaveFile", shortcut="CTRL+S")
        self.actionSaveFileAs = Action("&Save as", self.menuFile, icon="images/icones/save.png", name="actionSaveFileAs", shortcut="CTRL+SHIFT+S")
        self.actionCloseFile = Action("&Close", self.menuFile, name="actionCloseFile", shortcut="CTRL+W")
        self.actionQuit = Action("&Quit", self.menuFile, icon="images/icones/close-btn.png", name="actionQuitter", shortcut="CTRL+Q")

        self.menuFile.addActions(self.actionNewFile, self.actionOpenFile, self.actionNewProject, self.actionNewProjectFile, self.actionOpenRecentProject)
        self.menuFile.addSeparator()
        self.menuFile.addActions(self.actionSaveFile, self.actionSaveFileAs, self.actionCloseFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        # Menu Edit
        self.menuEdit = Menu("&Edit", self.menuBar)
        self.actionResearch = Action("&Research", self.menuEdit, icon="images/icones/visualisation.png", name="actionResearch", shortcut="CTRL+F")
        self.menuEdit.addAction(self.actionResearch)

        # Menu View
        self.menuView = Menu("&View", self.menuBar)
        self.subMenuFolders = Menu("&Folders", self.menuView)
        self.actionShowFolders = Action("&Show", self.subMenuFolders, name="actionShowFolders")
        self.actionHideFolders = Action("&Hide", self.subMenuFolders, name="actionHideFolders")

        self.subMenuFolders.addActions(self.actionShowFolders, self.actionHideFolders)
        self.menuView.addMenu(self.subMenuFolders)

        # Menu Settings
        self.menuSettings = Menu("&Settings", self.menuBar)
        self.actionTheme = Action("&Appearance", self.menuSettings, name="actionTheme")

        self.menuSettings.addAction(self.actionTheme)

        # Menu Help
        self.menuHelp = Menu("&Help", self.menuBar)
        self.actionCheckForUpdate = Action("&Check for update", self.menuHelp, name="actionCheckForUpdate")
        self.actionAPropos = Action("&About Web Editor", self.menuHelp, name="actionAPropos")

        self.menuHelp.addActions(self.actionCheckForUpdate, self.actionAPropos)

        self.menuBar.addMenus(self.menuFile, self.menuEdit, self.menuView, self.menuSettings, self.menuHelp)
        self.menuBar.setStyleSheet(self.theme.styleMenu)
        self.menuLayout.addWidget(self.menuBar)

    def initProjects(self):
        """
            ---Initialising of project's part
        """
        self.currentProject:Project = None
        self.opennedProjects = []
        dictProjects = AppFile(PATH_USER_PROJECTS).lire()
        if dictProjects is not None:
            for path in dictProjects["projectsPaths"]:
                if path != dictProjects["currentProjectPath"]:
                    self.on_actionOpenRecentProject_triggered(path=path)
            if dictProjects["currentProjectPath"] is not None:
                self.on_actionOpenRecentProject_triggered(path=dictProjects["currentProjectPath"])

    def initTabs(self):
        """--------------------------
            ---------Initialising of tab's part (openned files)
            ---------------------------------"""
        files = AppFile(PATH_USER_FILES).lire()
        if self.ouvertureTabs:
            if files is None:
                if len(self.tabs.tabtexts) == 0:
                    self.tabs.addTab("New", "")
            else:
                nombre_tabs = len(files)
                count = 0
                for file in files:
                    count += 1
                    if file["path"] not in ("", " "):
                        fichier = UserFile(file["path"])
                        if fichier.exist():
                            self.tabs.addTab(file["title"], file["path"])
                            self.tabs.currentTabText().setPlainText(fichier.lire())
                    else:
                        self.tabs.addTab(file["title"], "")
                        self.tabs.currentTabText().setPlainText(file["content"])
                    if count == nombre_tabs and len(self.tabs.tabtexts) == 0:
                        self.initTabs()
            self.ouvertureTabs = False
        else:
            if len(self.tabs.tabtexts) == 0:
                self.tabs.addTab("New", "")

    def initFolders(self, after=""):
        """Vérification du nombre de dossiers ouverts"""
        """
        if len(self.folders.foldersList) <= 0:
            self.splitterCenter.widget(0).setVisible(False)
            self.actionShowFolders.setEnabled(False)
            self.actionHideFolders.setEnabled(False)
        else:
            self.splitterCenter.widget(0).setVisible(True)
            self.actionShowFolders.setEnabled(True)
            self.actionHideFolders.setEnabled(True)
        """
        pass

    def setWindowTitle(self, title: str):
        self.title.setText(title)

    def addToWindowTitle(self, chaine = ""):
        """-----------------
            -------Changement du titre de la fenêtre
            -------------------------"""
        if chaine == "":
            self.title.setText("Web Editor")
        else:
            self.title.setText("Web Editor - "+chaine)

    def setPathCurrentFile(self, path):
        self.pathCurrentFile.setText(path)

    """ MENU FICHIER """

    @pyqtSlot()
    def on_actionNewFile_triggered(self):
        """---------------
            ---Creation of a new tab
            -----------"""
        types = [self.tr("Texte")]
        types += LANGUAGES.keys()
        types.append(self.tr("Autre"))
        message = self.tr("Quel type de fichier ?")
        type, ok = QInputDialog.getItem(self, self.tr("Type de fichier"), message, types,0, False)
        if ok:
            self.tabs.addTab(self.tr("Nouveau"), "", type = type)

    @pyqtSlot()
    def on_actionNewProject_triggered(self):
        """---------------
            ---Creation of a new tab
            -----------"""
        path = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier", "C:\\", QFileDialog.ShowDirsOnly)
        if path:
            self.newProject = NewProject(self, path)
            self.newProject.show()

    @pyqtSlot()
    def on_actionOpenFile_triggered(self, chemin = ""):
        """------------
            ---Ouverture d'un fichier
            -----------------"""
        if chemin == "":
            (chemins, filtre) = QFileDialog.getOpenFileNames(self, self.tr("Ouverture fichiers(s)"), filter="All(*.*)")
            if chemins:
                for chemin in chemins:
                    fichier = UserFile(chemin)
                    self.tabs.addTab(fichier.nom(), chemin)
        else:
            fichier = UserFile(chemin)
            if fichier.exist():
                self.tabs.addTab(fichier.nom(), chemin)

    @pyqtSlot()
    def on_actionOpenRecentProject_triggered(self, project: Project = None, path = None):
        """Open a project"""
        if project is None:
            if path is None:
                path, filter = QFileDialog.getOpenFileName(self, self.tr("Sélectionnez un fichier projet"), filter="VPEditor Project File(*.vpp)")
            if path and path is not None and path != "":
                data = AppFile(path).read()
                if type(data) != Project:
                    message = "Le fichier "+path+" n'est pas un projet ou il est corrompu"
                    msg = QMessageBox.information(self, "Echec ouverture", message, QMessageBox.Ok)
                else:
                    project = data
        if project is not None:
            self.folders.addFolder(project.path, project.name)
            self.currentProject = project
            self.opennedProjects.append(self.currentProject)

    @pyqtSlot()
    def on_actionSaveFile_triggered(self):
        """------------
                ---Saving of a file
                -----------------"""
        tabText = self.tabs.currentTabText()
        if not tabText.saved:
            if tabText.chemin != "":
                fichier = UserFile(tabText.chemin)
                fichier.write(tabText.toPlainText())
                self.tabs.setTabText(self.tabs.currentIndex(), fichier.nom())
                """Refresh the page in browser if it is showed"""
                self.tabs.refreshBrowserPage()
            else:
                self.on_actionSaveFileAs_triggered()

    @pyqtSlot()
    def on_actionSaveFileAs_triggered(self):
        """------------
        ---Enregistrement d'un fichier sous un autre nom
        -----------------"""
        tabText = self.tabs.currentTabText()
        if not tabText.saved:
            (chemin, filtre) = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", filter="All(*.*)")
            if chemin:
                fichier = UserFile(chemin)
                fichier.write(tabText.toPlainText())
                self.addToWindowTitle(chemin)
                self.tabs.currentTabText().setTitre(fichier.nom())
                self.tabs.currentTabText().setChemin(chemin)
                self.tabs.setTabText(self.tabs.currentIndex(), fichier.nom())

    @pyqtSlot()
    def on_actionCloseFile_triggered(self, index = None):
        """------------
        ---Fermeture d'un fichier
        -----------------"""
        if index is None:
            index = self.tabs.currentIndex()
        tabText = self.tabs.currentTabText(index)
        if tabText.saved:
            canClose = True
        else:
            message = "Ce fichier n'a pas été enregistré. Voulez-vous vraiment le femer ?"
            reponse = QMessageBox.question(self, "Confirmation", message, QMessageBox.Yes, QMessageBox.No)
            if reponse == QMessageBox.Yes:
                canClose = True
            else:
                canClose = False
        if canClose:
            self.tabs.removeTab(index)
            self.initTabs()

    """ MENU VUE """
    @pyqtSlot()
    def on_actionShowFolders_triggered(self):
        """To show folders zone"""
        self.topOfPage.widget(0).setVisible(True)

    @pyqtSlot()
    def on_actionHideFolders_triggered(self):
        """To hide folders zone"""
        self.topOfPage.widget(0).setVisible(False)

    @pyqtSlot()

    def on_actionShowBottom_triggered(self):
        """To show bottom zone"""
        self.divisions.widget(1).setVisible(True)

    @pyqtSlot()
    def on_actionHideBottom_triggered(self):
        """To hide bottom zone"""
        self.divisions.widget(1).setVisible(False)

    @pyqtSlot()
    def on_actionVisualisation_triggered(self):
        """Afficher la page de visualisation"""
        tabText = self.tabs.currentTabText()
        if tabText.fichier.extension().lower() in ("html", "htm", "php"):
            url = None
            if self.currentProject is not None:
                isProjectFile, projectFile = self.currentProject.isProjectFile(tabText.chemin)
                if isProjectFile:
                    if projectFile.type == ProjectFile.MAIN_FILE:
                        if self.currentProject.type == Project.LOCAL_TYPE:
                            text = projectFile.url()
                            url, response = QInputDialog.getText(self, self.tr("Lien"), self.tr("Entrez le lien d'ouverture dans le navigateur"), text = text)
                            if not url:
                                return
            if url is None:
                url = tabText.chemin
            if self.browser.isHidden():
                self.progress = QProgressDialog(self.tr("Preparation de la fenetre de visualisation"), self.tr("Arreter"), 1, 100, self)
                self.stepProgression = 0
                self.timer = QTimer(self)
                self.timer.setInterval(200)
                self.timer.start(0)
                self.timer.timeout.connect(self.on_progress_gone_on)
                self.progress.canceled.connect(self.on_progress_canceled)
            self.browser.loadUrl(url)

    def on_progress_gone_on(self):
        self.progress.setValue(self.stepProgression)
        self.stepProgression += 1
        if self.stepProgression > 100:
            self.timer.stop()
            self.browser.show()
            self.move(0, 0)
            self.resize(550, 720)
            self.browser.move(555, 0)
            self.browser.resize(720, 720)

    def on_progress_canceled(self):
        self.timer.stop()

    """  MENU EDITER """

    @pyqtSlot()
    def on_actionResearch_triggered(self):
        """Recherche"""
        self.rechercher = Recherche(self, 0, self.tabs.currentTabText())
        self.rechercher.show()

    @pyqtSlot()
    def on_actionReplace_triggered(self):
        """Remplacement"""
        self.rechercher = Recherche(self, 1, self.tabs.currentTabText())
        self.rechercher.show()

    """ MENU PREFERENCES """

    @pyqtSlot()
    def on_actionTheme_triggered(self):
        """Theme"""
        self.themeDialog = ThemeDialog(self)
        self.themeDialog.show()

    """ MENU PROJECT """

    @pyqtSlot()
    def on_actionModifyProject_triggered(self):
        if self.currentProject is not None:
            self.modifyProject = NewProject(self, action = NewProject.ACTION_MODIFY, project = self.currentProject)
            self.modifyProject.show()

    """ MENU HELP """

    @pyqtSlot()
    def on_actionAPropos_triggered(self):
        """About application"""
        self.about = About(self)
        self.about.show()

    @pyqtSlot()
    def on_actionQuitter_triggered(self):
        self.close()

    def saveOnClose(self):
        userFiles_File = AppFile(PATH_USER_FILES)
        userProjects_File = AppFile(PATH_USER_PROJECTS)
        dictProjects = {"currentProjectPath":None, "projectsPaths":[]}
        if self.currentProject is not None:
            dictProjects["currentProjectPath"] = self.currentProject.pathWithName()
        files = []
        folders = []
        for tabText in self.tabs.tabtexts:
            files.append({"title":tabText.titre, "path":tabText.chemin, "content":tabText.toPlainText()})
        for project in self.opennedProjects:
            dictProjects["projectsPaths"].append(project.pathWithName())

        userFiles_File.write(files)
        userProjects_File.write(dictProjects)


    def closeEvent(self, event):
        pass
        """
        exist_tab_not_saved = False
        for tabText in self.tabs.tabtexts:
            if not tabText.saved:
                exist_tab_not_saved = True
        if exist_tab_not_saved:
            message = "Certains fichier n'ont pas été enregistrés, ces contenus seront perdus.\nVoulez-vous quand même quitter VPEditor ?"
            reponse = QMessageBox.question(self, "Confirmation", message, QMessageBox.Yes, QMessageBox.No)
            if reponse == QMessageBox.Yes:
                event.accept()
                self.browser.close()
                self.saveOnClose()
            else:
                event.ignore()
        else:
            message = "Voulez-vous vraiment quitter VPEditor ?"
            reponse = QMessageBox.question(self, "Confirmation", message, QMessageBox.Yes, QMessageBox.No)
            if reponse == QMessageBox.Yes:
                event.accept()
                self.browser.close()
                self.saveOnClose()
            else:
                event.ignore()
        """

if __name__ == '__main__':
    pass
