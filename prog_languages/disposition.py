#-*-coding:utf-8 -*-

from prog_languages.languages import *
from PyQt5.QtCore import QRegExp

keywords_html = LANGUAGES["HTML"]["keywords"]
keywords_css = LANGUAGES["CSS"]["keywords"]
keywords_php = LANGUAGES["PHP"]["keywords"]

class LanguageStructure:
    def __init__(self, language = "", tabulations = ""):
        self.language = language.lower()
        self.tabulations = tabulations
    def base(self):
        if self.language == "html":
            return '<!Doctype HTML>\n<html lang="fr">\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<title></title> \
                \n\t</head>\n\t<body>\n\t\t\n\t</body>\n</html>'
        else:
            return ""
    def structure(self, keyword):
        tabulations = self.tabulations
        keyword = keyword.lower()
        if self.language == "html":
            if keyword == "table":
                return '<table border="2px">\n'+tabulations+'\t<caption></caption>\n'+tabulations+'\t<tr>\n'+tabulations+'\t\t<th></th>\n'+tabulations+'\t</tr>\n'+tabulations+'\t<tr>\n'+tabulations+'\t\t<td></td>\n'+tabulations+'\t</tr>\n'+tabulations+'</table>'
            elif keyword == "fieldset":
                return '<fieldset>\n'+tabulations+'\t<legend></legend>\n\n'+tabulations+'</fieldset>'
            elif keyword == "img":
                return '<img src="" alt=""/>'
        else:
            return ""

class Disposition:
    """
         Classe qui s'occupe de la disposition
    """
    def __init__(self, tab = None, language = ""):
        self.tab = tab
        self.language = language.lower()
        self.languageStructure = LanguageStructure(self.language)

    def acceptShowWordFromCompleter(self, motSelectionne):
        """
            Fonction qui dit si le mot issu du completer doit être afficher
        :return: boolean
        """
        canShowWord = True
        if self.language == "html":
            if motSelectionne.lower() in ("html", "table", "fieldset", "img"):
                canShowWord = False
        return canShowWord

    def showWordFromCompleter(self, motSelectionne, finalCursorPosition):
        """
            Affichage du mot sélectionné dans le completer
        :param motSelectionne:
        :return:
        """
        motSelectionne = motSelectionne.lower()
        if self.acceptShowWordFromCompleter(motSelectionne):
            if self.language in ("htm", "html"):
                if motSelectionne in list(mot.lower() for mot in keywords_html["tags"]):
                    self.tab.insertPlainText("<"+motSelectionne+"></"+motSelectionne+">")
                    self.tab.moveCursor(finalCursorPosition)
                elif motSelectionne == "!doctype html":
                    self.tab.insertPlainText("<!DOCTYPE HTML>")
            else:
                self.tab.insertPlainText(motSelectionne)

    def disposeAfterCompleterByEnterKey(self, textBeforeEvent, motSelectionne):
        """
            Fonction qui dispose le code en fonction du langage
            :return: void()
        """
        tabulations = ""
        j = 1
        while j <= self.tab.nbTabulations(textBeforeEvent):
            tabulations += "\t"
            j += 1
        self.languageStructure.tabulations = tabulations
        if self.language == "html":
            # Si la balise est <html>
            if motSelectionne.lower() == "html":
                # On insére la structure de base d'un document html
                self.tab.insertPlainText(self.languageStructure.base())
            elif motSelectionne.lower() == "table":
                # On insére la structure d'un tableau
                self.tab.insertPlainText(self.languageStructure.structure("table"))
            elif motSelectionne.lower() == "fieldset":
                # On insére la structure d'un fieldset
                self.tab.insertPlainText(self.languageStructure.structure("fieldset"))
            elif motSelectionne.lower() == "img":
                # On insére la structure d'une image
                self.tab.insertPlainText(self.languageStructure.structure("img"))

    def disposeAfterSimpleEnterKey(self, textBeforeEvent, cursorPositionBeforeEvent):
        """
            Fonction qui redispose le code lorsqu'on appui sur la touche entrée sans autocompletion
        :param textBeforeEvent:
        :param cursorPositionBeforeEvent:
        :return: void()
        """
        tabulations = ""
        j = 1
        while j <= self.tab.nbTabulations(textBeforeEvent):
            tabulations += "\t"
            j += 1
        if self.language == "html":
            #Recherche d'une éventuelle balise située directement avant le curseur de la souris
            posDernierChevronFermant = textBeforeEvent.rfind(">", 0, cursorPositionBeforeEvent)
            if posDernierChevronFermant >= 0 and posDernierChevronFermant in (cursorPositionBeforeEvent-1,cursorPositionBeforeEvent-2):
                posDernierChevronOuvrant = textBeforeEvent.rfind("<", 0, posDernierChevronFermant)
                if posDernierChevronOuvrant >= 0 and posDernierChevronOuvrant != posDernierChevronFermant:
                    textInside = textBeforeEvent[posDernierChevronOuvrant+1:posDernierChevronFermant]
                    if textInside[0] == "/":
                        textInside = textInside[1:len(textInside)]
                    regex_tag = QRegExp("^[a-z][0-9a-z-]*$")
                    if regex_tag.indexIn(textInside) >= 0:
                        self.tab.moveCursor(cursorPositionBeforeEvent)
                        self.tab.insertPlainText("\n"+tabulations+"\t")
        elif self.language == "css":
            ##Recherche d'une éventuelle accolade située directement avant le curseur de la souris
            posDerniereAccoladeOuvrante = textBeforeEvent.rfind("{", 0, cursorPositionBeforeEvent)
            if posDerniereAccoladeOuvrante >= 0 and posDerniereAccoladeOuvrante in (
            cursorPositionBeforeEvent - 1, cursorPositionBeforeEvent - 2):
                self.tab.moveCursor(cursorPositionBeforeEvent)
                self.tab.insertPlainText("\n" + tabulations + "\t")