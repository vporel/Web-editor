"""
    SCANNER LES DOCUMENTSS TEXTES
    LES DIFFERENTES PROPRIETES, POSITIONS DES ESPACES, TABULATIONS
    DISPOSITION DU CODE EN FONCTION DU LANGAGE
"""

# -*-coding:utf-8 -*-
from prog_languages.languages import *

keywords_html = LANGUAGES["HTML"]["keywords"]
keywords_css = LANGUAGES["CSS"]["keywords"]
keywords_php = LANGUAGES["PHP"]["keywords"]

class DocScan:
    """Scan des documents en fonction des différents languages"""
    def __init__(self, text):
        self.text = text
        self.keywords = []

    @staticmethod
    def languageClass(language, text):
        language = language.lower()
        if language in ("htm", "html", "php"):
            return HTMLScan(text)
        elif language in ("css", "scss"):
            return CSSScan(text)
        else:
            return DocScan(text)

    def trouverMot(self, mot, cp):
        """
            Fonction qui recherche dans la liste de mots clés le mot entré par l'utilisateur
        :param mot:
        :return:
        """
        mots_trouves_avec_index = []
        mots_trouves = []
        if mot not in (""," "):
            for word in self.keywords:
                if word.lower() != mot.lower() and word.lower().find(mot.lower()) >= 0:
                    mots_trouves_avec_index.append((word.lower().find(mot.lower()), word))
        def positionMot(elmt):
            return elmt[0]
        """On classe les éléments en fonction de leurs positions dans les chaines de caractères"""
        mots_trouves_avec_index.sort(key=positionMot)
        for el in mots_trouves_avec_index:
            mots_trouves.append(el[1])
        return mots_trouves
    def countLines(self):
        """ Retourne le nombre de lignes dans le doc """
        return self.blocksBefore(len(self.text)) + 1

    def lineText(self, pos = -1, numLine = 0):
        """
            Fonction renvoyant le texte dans une ligne précise du text
        :param numLigne:
        :return:
        """
        if numLine <= 0:
            if pos == -1:
                return ""
            start = self.posEnterBefore(pos)+1
            end = self.text.find("\n", start, len(self.text))
            if end < 0:
                end = len(self.text)
            return self.text[start: end]
        elif numLine <= self.countLines():
            count = 1
            posEnter = self.posEnterAfter(0)
            while (posEnter >= 0):
                count += 1
                if count == numLine:
                    break #On arrête la boucle
                else:
                    posEnter = self.posEnterAfter(posEnter + 1)
            nextEnter = self.posEnterAfter(posEnter + 1)
            if nextEnter < 0: #Ceci signifierait qu'on est à la fin du fichier
                nextEnter = len(self.text)
            return self.text[posEnter+1:nextEnter]
        else:
            return ""

    def blocText(self, numLineStart, numLineEnd):
        """Fonction renvoyant le texte dans un bloc d'une ligne x à une ligne y"""
        txt = ""
        for i in range(numLineStart, numLineEnd+1):
            txt += self.lineText(-1, i)

    def posCaracBefore(self, carac = "", pos:int = -1):
        """  Fonction qui retourne la position du caractère 'carac' avant la position donnée"""
        return self.text.rfind(carac, 0, pos)

    def posCaracAfter(self, carac = "", pos:int = -1):
        """  Fonction qui retourne la position du caractère 'carac' avant la position donnée"""
        return self.text.rfind(carac, pos)

    def posEnterBefore(self, pos:int):
        """Fonction qui retourne la position du dernier caractère '\n' avant la position donnée """
        return self.posCaracBefore("\n", pos)
    def posEnterAfter(self, pos:int):
        """Fonction qui retourne la position du dernier caractère '\n' avant la position donnée """
        return self.posCaracAfter("\n", pos)

    def posSpaceBefore(self, pos:int):
        """
            Fonction qui retourne la position du dernier espace avant la position donnée
        :param pos:
        :return:
        """
        p = self.text.rfind(" ", self.posEnterBefore(pos)+1, pos)
        if p < 0:
            p = self.text.rfind("\t", self.posEnterBefore(pos), pos)
        if p < 0:
            return self.posEnterBefore(pos)
        else:
            return p

    def blocksBefore(self, pos):
        """
            Nombre de blocks avant une position donnée
        """
        nbBlocks = 0
        posEnter = self.text.find("\n", 0, pos)
        while posEnter >= 0:
            nbBlocks += 1
            posEnter = self.text.find("\n", posEnter+1, pos)
        return nbBlocks

    def nbCaracBefore(self, carac = "", pos = -1):
        """
            Nombre de fois qu'on retrouve un caractère avant la position donnée
        :param carac:
        :param pos:
        :return:
        """
        nb = 0
        indexes = []
        index = self.text.find(carac, 0, pos)
        while index >= 0:
            nb += 1
            indexes.append(index)
            index = self.text.find(carac, index + len(carac), pos)
        return nb, indexes

    def caracFermes(self, pos, debutCarac, finCarac, blocks = []):
        """
            Verifier si tous les commentaires avant la position donnée ont été fermés
        :param indexes:
        :param pos:
        :return:
        """
        nbCaracAvant, indexes = self.nbCaracBefore(debutCarac, pos)
        fermes = True
        if debutCarac == finCarac:
            if nbCaracAvant % 2 == 0:
                fermes = True
            else:
                fermes = False
        else:
            for i, index in enumerate(indexes):
                startSearch = index
                if i < len(indexes)-1:
                    endSearch = indexes[i+1]
                else:
                    endSearch = pos
                search = self.text.find(finCarac, startSearch, endSearch)
                if search < 0:
                    fermes = False
        return fermes

class HTMLScan(DocScan):
    """Scan HTML"""
    def __init__(self, text):
        DocScan.__init__(self, text)
        self.keywords = keywords_html["tags"] + keywords_html["attributes"]
        self.debutComment = "<!--"
        self.finComment = "-->"

    def trouverMot(self, mot, cp = -1):
        mots_trouves_avec_index = []
        mots_trouves = []
        if mot != "" and mot != " ":
            """On vérifie que nous ne sommes pas dans un commentaire ou une chaine"""
            if self.caracFermes(cp, self.debutComment, self.finComment) and self.caracFermes(cp-1, '"', '"'):
                """On vérifie si on n'est pas dans une balise"""
                #if self.caracFermes(cp-3, "<", ">", [('"', '"'), (self.debutComment, self.finComment)]):
                continu = True
                if mot[0:2] == "</":
                    mot = mot[2:len(mot)]
                elif mot[0] == "<":
                    mot = mot[1:len(mot)]
                else:
                    continu = False
                if continu:
                    for word in self.keywords:
                        if word.lower() != mot.lower() and word.lower().find(mot.lower()) >= 0:
                            mots_trouves_avec_index.append((word.lower().find(mot.lower()), word))
        def positionMot(elmt):
            return elmt[0]
        """On classe les éléments en fonction de leurs positions dans les chaines de caractères"""
        mots_trouves_avec_index.sort(key=positionMot())
        for el in mots_trouves_avec_index:
            mots_trouves.append(el[1])
        return mots_trouves

class CSSScan(DocScan):
    """Scan CSS"""
    def __init__(self, text):
        DocScan.__init__(self, text)
        self.keywords = keywords_css["properties"]
