"""
    FENETRE PRINCIPALE POUR LE NAVIGATEUR INTEGRE A VPEDITOR
"""

# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from srcBrowser import Ui_BrowserWindow
from src.VPTheme import ICON_APP, theme
from src.AppFiles import WELCOME_FILE


class Page(QWebEngineView):
    """
        class which define pages of navigator
    """
    def __init__(self, parent, url = ""):
        QWebEngineView.__init__(self, parent)
        self.navigator = parent
        self.webProfile = QWebEngineProfile(self)
        self.origineUrl = url
        self.currentUrl = url
        self.load(url)
        self.urlChanged.connect(self.on_urlChanged)

    def load(self, url:str):
        """Load an url in this page"""
        url = self.reformUrl(url)
        self.webProfile.clearHttpCache()
        self.setUrl(QUrl(url))
        self.currentUrl = url
        QWebEngineView.load(self, QUrl(url))

    def on_urlChanged(self, url):
        """When the page is changed by a link or other action"""
        self.currentUrl = url.toString()
        self.navigator.window.setWindowTitle("VPBrowser - "+self.currentUrl)

    @staticmethod
    def reformUrl(url:str):
        if url.lower().find("localhost") == 0: #If the project is local
             url  = "http://"+url
        return url



class Navigator(QTabWidget):
    """
        Class which define the main widget of VPEditor Browser
    """
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.window = parent
        self.setTabsClosable(True)
        #Slots
        self.currentChanged.connect(self.on_pageChanged) #When the current page is changed
        self.tabCloseRequested.connect(self.on_tabClosed)
        self.showWelcomePage()

        """Style"""
        self.setStyleSheet(theme.styleTabs)

    def showWelcomePage(self):
        #Adding a welcome page
        self.addTab(WELCOME_FILE)

    def loadUrl(self, url:str):
        """Check if the url exist in pages. If it is the case, page is reloaded. Otherwise, a new page is created"""
        exist, index = False, -1
        for i in range(self.count()):
            if self.widget(i).currentUrl == Page.reformUrl(url):
                exist = True
                index = i
        if exist:
            self.widget(i).reload()
        else:
            self.addTab(url)
        return exist
    def reload(self):
        """Reload the current page"""
        self.currentWidget().reload()

    def addTab(self, url:str):
        page = Page(self, url)
        cutUrl = url.split("/")
        title = cutUrl[-2]+"/"+cutUrl[-1]
        QTabWidget.addTab(self, page, title)

    def currentUrl(self):
        """Get the url of the current browser page"""
        return self.currentWidget().currentUrl

    def on_pageChanged(self, index):
        """When the current page is changed"""
        try:
            #Un try parce que s'il n'y a pas de page une exception sera levée
            #Changement du titre de la fenetre
            self.window.setWindowTitle("VPBrowser - "+self.currentUrl())
        except:
            pass

    def on_tabClosed(self, index):
        self.removeTab(index)
        if self.count() <=0:
            self.showWelcomePage()


class BrowserWindow(QMainWindow, Ui_BrowserWindow.Ui_MainWindow):
     def __init__(self, principale = None):
         QMainWindow.__init__(self)
         self.principale = principale
         self.setupUi(self)
         self.verticalLayout.setContentsMargins(0,0,0,0)
         try:
             icon = QIcon()
             icon.addPixmap(QPixmap(ICON_APP), QIcon.Normal, QIcon.Off)
             self.setWindowIcon(icon)
         except:
             print("Erreur de chargement de l'icone")

         self.navigator = Navigator(self)
         self.verticalLayout.addWidget(self.navigator, 1)

     def loadUrl(self, url:str):
         self.navigator.loadUrl(url)

     def currentUrl(self):
         """Get the url of the current browser page"""
         return self.navigator.currentUrl()
