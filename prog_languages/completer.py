# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QTextCursor

class Completer(QListWidget):
    def __init__(self, language:str=None, parent=None):
        self.language = language
        self.tabText = parent
        QListWidget.__init__(self, parent)
        self.setMinimumSize(200,300)
        self.nbItems = 0
        self.cursorPosition = -1
        self.itemClicked.connect(self.on_itemClicked)
        self.itemDoubleClicked.connect(self.on_itemDoucleClicked)

        self.setVisible(False)

    def setItems(self, mots):
        self.clear()
        self.nbItems = 0
        for mot in mots:
            self.addItem(mot)
            self.nbItems += 1
    def setVisible(self, visible: bool):
        super().setVisible(visible)
        self.setCurrentRow(0)
    def nextItem(self):
        index = self.currentRow() + 1
        if index >= self.nbItems:
            index = 0
        self.setCurrentRow(index)
    def prevItem(self):
        index = self.currentRow() - 1
        if index <= 0:
            index = self.nbItems-1
        self.setCurrentRow(index)

    def complete(self, textBeforeEvent, newWord, cp):
        oldWord = textBeforeEvent[self.tabText.docScan.posSpaceBefore(cp) + 1 : cp]
        self.tabText.setFocus()
        tc = self.tabText.textCursor() #tc = text cursor
        posDebutMot = self.tabText.docScan.posSpaceBefore(cp) + 1 #position du debut du mot à enlever dans le texte
        tc.setPosition(posDebutMot) #On place le curseur au debut de ce mot
        tc.setPosition(cp, QTextCursor.KeepAnchor) #On change la position du curseur, on le met à la fin du mot avec une sélection
        self.tabText.setTextCursor(tc)
        # insertion du nouveau mot
        #Le mot est inséré par un fonction de la classe disposition,
        # en fonction du langage, les parametres d'insertion changent
        self.tabText.disposition.showWordFromCompleter(newWord, posDebutMot+len(newWord))
        # Verification du langage pour d'autres ajouts
        if self.tabText.fichier.extension() != None:
            #On met à jour la disposition en fonction du langage
            self.tabText.disposition.disposeAfterCompleterByEnterKey(textBeforeEvent, newWord)
        #ON affiche le completer
        self.setVisible(False)

    def on_itemClicked(self, item):
        """Lorsqu'on clique sur un item"""
        self.tabText.setFocus()
        tc = self.tabText.textCursor()
        tc.setPosition(self.cursorPosition)
        self.tabText.setTextCursor(tc)

    def on_itemDoucleClicked(self, item):
        """Lorsqu'on double-clique sur un item"""
        textBeforeEvent = self.tabText.toPlainText()
        mot = item.text()
        self.complete(textBeforeEvent, mot, self.cursorPosition)