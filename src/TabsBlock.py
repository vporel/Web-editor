#-*-coding:utf-8 -*-
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QLabel,\
    QTabWidget, QScrollBar, QShortcut, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot, QMetaObject, QRect, Qt, QCoreApplication, QUrl, QSize
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QFontMetrics, QTextCursor,QKeyEvent, QKeySequence, \
    QIcon, QPixmap
from src.AppFiles import *
from src.Coloration import ColorSyntax
from prog_languages.keywords import *
from prog_languages.completer import *
from prog_languages.disposition import *
from prog_languages.DocScan import *

#Création des numeros de ligne
class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.editor = editor
    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)
    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

#Classe pour les tabs
class TabText(QPlainTextEdit):
    def __init__(self, parent = None, previsualisation = False):
        super().__init__(parent = None)
        _translate = QCoreApplication.translate
        self.parent = parent
        self.saved = True
        self.title = ""
        self.path = ""
        self.theme = parent.theme
        self.fichier = UserFile(self.path)
        self.coloration()
        self.disposition = Disposition(self, self.fichier.extension())
        self.docScan = DocScan.languageClass(self.fichier.extension(), self.toPlainText())

        #Style
        self.setStyleSheet(self.theme.styleEditorText)
        self.setVerticalScrollBar(QScrollBar(Qt.Vertical, self))
        self.setHorizontalScrollBar(QScrollBar(Qt.Horizontal, self))

        #Numéros de lignes
        if not previsualisation:
            self.lineNumberArea = LineNumberArea(self)
            self.lineNumberArea.setStyleSheet(self.theme.styleLineNumberArea)
            self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Tabulation
        self.spaceWidth = self.fontMetrics().width(" ")
        self.setTabStopWidth(self.spaceWidth * 12)

        #Actions
        self.dupliquerLigne = QShortcut(QKeySequence("Ctrl+D"), self)
        self.dupliquerLigne.activated.connect(self.on_dupliquerLigne_activated)

        #Evènements
        if not previsualisation:
            self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
            self.updateRequest.connect(self.updateLineNumberArea)
            self.cursorPositionChanged.connect(self.highlightCurrentLine)
            self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.on_cursorPositionChanged)

        #Completer
        self.completer = Completer(self.fichier.extension(), self)
    # |--------------------------End of __init__------------------------------------|

    def on_cursorPositionChanged(self):
        """Lorsque la position du curseur change"""
        self.completer.cursorPosition = self.textCursor().position()
    # |____________
    #------Refresh Content
    def refreshContent(self):
        if self.fichier.exist():
            self.setPlainText(self.fichier.lire())

    # |----------------
    # |----Coloration syntaxique
    def coloration(self):
        """Coloration syntaxique"""
        self.fichier = UserFile(self.path)
        self.colorSyntax = ColorSyntax(self.document(), self.fichier.extension(), self.theme)

    # |-------Fin de la coloration
    # |----------------
    def visualise(self):
        """Rend le bouton de visualisation cliquable ou non"""
        if self.fichier.extension().lower() in ("html", "htm", "php"):
            #self.parent.fenetre.actionVisualisation.setEnabled(True)
            return True
        else:
            #self.parent.fenetre.actionVisualisation.setEnabled(False)
            return False
    # | Changement de l'attribut path
    def setPath(self, path:str):
        self.path = path
        self.fichier = UserFile(self.path)
        """Affichage ou non  de la page visualisation"""
        self.visualise()
        self.coloration()
        self.completer = Completer(self.fichier.extension(), self)
        self.disposition = Disposition(self, self.fichier.extension())
        self.docScan = DocScan.languageClass(self.fichier.extension(), self.toPlainText())
        self.parent.updateIcons() #Mise à jour des icones de tabs
    def setTitle(self, title:str):
        self.title = title

    # |----Fin du changement
    # |----------------------

    """Actions"""
    def on_dupliquerLigne_activated(self):
        oldCp = self.textCursor().position()
        if self.textCursor().selectedText() == "":
            finLigne = self.toPlainText().find("\n", oldCp, len(self.toPlainText()))
            if finLigne < 0:
                finLigne = len(self.toPlainText())
            self.moveCursor(finLigne)
            self.insertPlainText("\n"+self.docScan.lineText(oldCp))
            self.moveCursor(oldCp + len(self.docScan.lineText(oldCp)) + 1)
        else:
            selectedText = self.textCursor().selectedText()
            newCp = self.toPlainText().find(selectedText, oldCp - len(selectedText) - 1, len(self.toPlainText())) + len(selectedText)
            self.moveCursor(newCp)
            self.insertPlainText(selectedText)

    """Pour l'indentation, nombre de tabulations
        ----Retourne le nombre de tabulation au debut de la ligne précédente
    """

    def nbTabulations(self, text):
        nbTabulations = 0
        nbEspaces = 0
        debut = text.rfind("\n", 0, self.completer.cursorPosition-1) + 1
        if text.rfind("\n", 0, self.completer.cursorPosition-1) <= 0:
            debut = 0
        txt = text[debut:self.completer.cursorPosition]
        i = 0
        carac = "-"
        try:
            carac = txt[i]
        except:
            pass
        while (i < len(txt) and ord(carac) in (9, 32)):
            carac = txt[i]
            if ord(carac) == 9:
                nbTabulations += 1
            else:
                nbEspaces += 1
                if nbEspaces == 7:
                    nbTabulations += 1
                    nbEspaces = 0
            i += 1
        return nbTabulations

    """Change position curseur texte"""
    def moveCursor(self, pos):
        textCursor = self.textCursor()
        textCursor.setPosition(pos)
        self.setTextCursor(textCursor)

    """Supprimer du texte"""
    def removeText(self, start:int, end:int):
        text = self.toPlainText()
        textBefore = text[:start]
        textAfter = text[end:]
        self.setPlainText(textBefore+textAfter)
        self.moveCursor(len(textBefore))

    #----------
    # |---- Appui sur une touche du clavier
    def keyPressEvent(self, event:QKeyEvent):
        #Actions définies
        textBeforeEvent = self.toPlainText()
        cpBeforeEvent = self.textCursor().position() #cp = cursor position

        """Quelques conditions"""
        if event.key() in (Qt.Key_Return, Qt.Key_Down,Qt.Key_Up):
            if self.completer.isVisible():
                if event.key() == Qt.Key_Return:  # Code touche entree
                    motSelectionne = self.completer.currentItem().text()
                    self.completer.complete(textBeforeEvent, motSelectionne, cpBeforeEvent)
                elif event.key() == Qt.Key_Down:
                    self.completer.nextItem()
                elif event.key() == Qt.Key_Up:
                    self.completer.prevItem()
                return

        """ Evènement """
        super().keyPressEvent(event)

        textAfterEvent = self.toPlainText()
        cp = self.textCursor().position()

        """------------------------------------
        ---Autocompletion-----
        ---------------------------------"""
        blocksBefore = self.docScan.blocksBefore(cp)
        # Recherche des mots
        mot = textAfterEvent[self.docScan.posSpaceBefore(cp)+1:cp]
        mots_trouves = self.docScan.trouverMot(mot, cp)
        textBeforeCursor = textAfterEvent[self.docScan.posEnterBefore(cp)+1:cp]
        x_completer = 0
        for carac in textBeforeCursor:
            if carac == "\t":
                x_completer += int(self.tabStopWidth())
            else:
                x_completer += self.fontMetrics().width(carac)
        x_completer += 20
        y_completer = (blocksBefore * 20) + 24
        if mots_trouves is not None and len(mots_trouves) > 0:
            self.completer.setGeometry(x_completer, y_completer, 200, 300)
            self.completer.setItems(mots_trouves)
            self.completer.setVisible(True)
        else:
            self.completer.setVisible(False)

        """----CONDITIONS SUR LES TOUCHES"""
        if event.key() == Qt.Key_Return: #Code touche entree
            #Recherche du nombre de tabulation au debut de la ligne précédente
            nbTabulations = self.nbTabulations(textBeforeEvent)
            """Augmentation de la tabulation"""
            i = 1
            while i <= nbTabulations:
                self.insertPlainText("\t")
                i+= 1
            self.disposition.disposeAfterSimpleEnterKey(textBeforeEvent, cpBeforeEvent)

    # |----Fin de l'évènement keypress
    #|------------
    # |-----Evènement mouse down

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.completer.setVisible(False)

    """
        Fonctions pour la lineNumberArea
    """
    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(30, 0, 0, 0)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 34, cr.height()))
    def lineNumberAreaPaintEvent(self, event):
        myPainter = QPainter(self.lineNumberArea)
        myPainter.fillRect(event.rect(), self.theme.backgroundLineNumberArea)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                myPainter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.theme.backgroundCurrentLine)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

#---End of Widget class ----
# |------------
#Classe tabs
class Tabs(QTabWidget):
    """Classe Tabs héritant de QTabWidget"""
    def __init__(self, parent, fenetre):
        QTabWidget.__init__(self, parent)
        self.fenetre = fenetre
        self.setObjectName("tabs")
        self.theme = parent.theme
        self.setStyleSheet(self.theme.styleTabs)
        self.tabtexts = []
        #Evènement
        self.currentChanged.connect(self.on_tab_changed)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tabCloseRequested)

    """-------------
    ----Ajout d'une tab
    --------------------------"""
    def addTab(self, title, path, type = "Autre"):
        error = False
        if title.lower() == self.tr("nouveau"):
            title = self.tr("Nouveau ")+str(len(self.tabtexts)+1)
        tabText = TabText(self, False)
        tabText.setTitle(title)
        tabText.setPath(path)
        if path != "" and path != " ":
            try:
                fichier = UserFile(path)
                tabText.setPlainText(fichier.lire())
            except:
                message = "Le fichier à  l'adresse : "+path+" n'a pas pu être lu"
                reponse = QMessageBox.information(self.fenetre, "Erreur lors de l'ouverture", message, QMessageBox.Ok)
                error = True
        elif type.lower() != "autre":
            languageStructure = LanguageStructure(type)
            tabText.setPlainText(languageStructure.base())
        (exist, index) = self.TabExist(path)
        if not exist and not error:
            fichier = UserFile(path)
            icon = QIcon(fichier.pixMap())
            self.tabtexts.append(tabText)
            QTabWidget.addTab(self, tabText, title)
            self.setTabIcon(len(self.tabtexts)-1, icon)
            self.setCurrentIndex(len(self.tabtexts)-1)
            self.fenetre.addToWindowTitle(title)
            self.fenetre.setPathCurrentFile(path)
            self.initTabsText()
            #self.fenetre.bottomOfPage.refreshLinks(path)
        else:
            if not error:
                self.setCurrentIndex(index)
                #self.fenetre.bottomOfPage.refreshLinks(path)

    def currentTabText(self, index = None):
        """Revoie de la table courante"""
        if index is None:
            return self.tabtexts[self.currentIndex()]
        return self.tabtexts[index]
    def initTabsText(self):
        i = 0
        while i < len(self.tabtexts):
            self.tabtexts[i].textChanged.connect(self.on_tabText_textChanged)
            i += 1

    def TabExist(self, path):
        """Vérification de l'existence d'un dossier"""
        exist = False
        i = 0
        index = -1
        for tabText in self.tabtexts:
            if path not in ("", " ") and tabText.path == path:
                exist = True
                index = i
            i += 1
        return exist, index

    def removeTab(self, index:int):
        super().removeTab(index)
        del self.tabtexts[index]
    def on_tabText_textChanged(self):
        tabText = self.currentTabText()
        tabText.saved = False
        self.setTabText(self.currentIndex(), self.tabtexts[self.currentIndex()].title+"*")
        tabText.docScan.text = tabText.toPlainText()
        self.on_tab_changed(0)

    def refreshBrowserPage(self):
        """Refresh the age of brower when file is saved"""
        tabText = self.currentTabText()
        # si la fenetre de visualisation et ouverte
        if not self.fenetre.browser.isHidden():
            project: Project = self.fenetre.currentProject
            if project is not None:
                isProjectFile, projectFile = project.isProjectFile(tabText.path)
                if isProjectFile and projectFile is not None:
                    currentBrowserUrl = self.fenetre.browser.currentUrl()
                    if project.type == Project.SIMPLE_TYPE:
                        currentBrowserPath = currentBrowserUrl
                    else:
                        currentBrowserPath = project.path + ProjectFile.endPathFromUrl(project, currentBrowserUrl)
                    coupure = currentBrowserPath.split("?")  # On enlève les infos dans l'url (GET)
                    currentBrowserPath = coupure[0]
                    if projectFile.type == ProjectFile.MAIN_FILE:
                        if tabText.path == currentBrowserPath:
                            self.fenetre.browser.navigator.reload()
                        else:
                            self.fenetre.browser.loadUrl(tabText.path)
                    else:
                        if projectFile.isLinked(ProjectFile.MAIN_FILE, currentBrowserPath):
                            self.fenetre.browser.navigator.reload()

            else:
                if tabText.fichier.extension().lower() in ("html", "htm", "php"):
                    self.fenetre.actionSaveFile.trigger()
                    self.fenetre.browser.loadUrl(tabText.path)

    def updateIcons(self):
        """Mise à  jour des icons dans l'en-tête"""
        index = 0
        while index < len(self.tabtexts):
            tabText = self.tabtexts[index]
            if tabText.path not in ("", " "):
                icon = QIcon(tabText.fichier.pixMap())
            else:
                icon = QIcon(QPixmap("./images/icones/incomming.png"))
            self.setTabIcon(index, icon)
            index += 1
    def on_tab_changed(self, index):
        try:
            tabText = self.currentTabText()
            if tabText.saved:
                self.fenetre.actionSaveFile.setEnabled(False)
                self.fenetre.actionSaveFileAs.setEnabled(False)
            else:
                self.fenetre.actionSaveFile.setEnabled(True)
                self.fenetre.actionSaveFileAs.setEnabled(True)
            self.fenetre.addToWindowTitle(tabText.title)
            #self.fenetre.bottomOfPage.refreshLinks(tabText.path)
            tabText.visualise()
        except:
            print("TabsBlock : on_tab_changed : index not in range:", index)
    def on_tabCloseRequested(self, index):
        self.fenetre.on_actionCloseFile_triggered(index)