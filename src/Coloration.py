# -*-coding:utf-8 -*-
import os, sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont, QTextBlockUserData
from prog_languages.languages import *
from src.VPTheme import VPTheme

class TextFormat(QTextCharFormat):
    def __init__(self,motCle, styles):
        QTextCharFormat.__init__(self)
        self.motCle = motCle
        self.styles = styles
        if self.motCle != "":
            self.setForeground(QColor(self.styles[self.motCle]["couleur"]))
            self.setFontItalic(self.styles[self.motCle]["italique"])
            if self.styles[self.motCle]["gras"]:
                self.setFontWeight(QFont.Bold)
            else:
                self.setFontWeight(QFont.Normal)

class Regle:
    """Règles et format dans un langage"""
    def __init__(self, langage, coloration):
        if langage != "":
            self.keywords = LANGUAGES[langage]["keywords"]
        try:
            self.styles = coloration[langage]
        except:
            defaultTheme = VPTheme()
            self.styles = defaultTheme.coloration[langage]

class RegleHTML(Regle):
    """Règles et format dans le langage html"""
    def __init__(self, coloration):
        Regle.__init__(self, "HTML", coloration)
        self.regles_tags = []
        self.regles_attributes = []

        # Regex
        """Balises"""
        self.tagsFormat = TextFormat("Balises", self.styles)
        self.unknownTagsFormat = TextFormat("Balises inconnues", self.styles)
        unknownTag_regex = QRegExp("</?[^<>]+>", Qt.CaseInsensitive)
        self.regles_tags.append([unknownTag_regex, self.unknownTagsFormat])
        for tag in self.keywords["tags"]:
            tag_regex = QRegExp("(</?"+tag+" [^<>]*>)|(</?"+tag+">)", Qt.CaseInsensitive)
            self.regles_tags.append([tag_regex, self.tagsFormat])

        """Attributs"""
        self.attributesFormat = TextFormat("Attributs", self.styles)
        self.unknownAttributesFormat = TextFormat("Attributs inconnus", self.styles)
        unknownAttribute_regex = QRegExp("[a-z0-9\\-]+", Qt.CaseInsensitive)
        self.regles_attributes.append([unknownAttribute_regex, self.unknownAttributesFormat])
        for attribute in self.keywords["attributes"]:
            attribute_regex = QRegExp(attribute, Qt.CaseInsensitive)
            self.regles_attributes.append([attribute_regex, self.attributesFormat])

        """Texte des attributs"""
        self.attributesTextFormat = TextFormat("Textes attributs", self.styles)
        self.attributesText_regex = QRegExp('("[^<>"]*")|(\'[^<>\']*\')', Qt.CaseInsensitive)

        """Commentaires"""
        self.commentsFormat = TextFormat("Commentaires", self.styles)
        self.comments_debut = QRegExp("<!--")
        self.comments_fin = QRegExp("-->")

class RegleCSS(Regle):
    """Règles et formats dans le langage CSS"""
    def __init__(self, coloration):
        Regle.__init__(self, "CSS", coloration)
        self.regles_props = []
        self.regles_tags = []
        self.regles_valeurs = []
        self.regleHTML = RegleHTML(coloration)

        #Regex
        """Propriétés"""
        self.propsFormat = TextFormat("Propriétés", self.styles)
        for prop in self.keywords["properties"]:
            prop_regex = QRegExp(prop+" *:", Qt.CaseInsensitive)
            self.regles_props.append([prop_regex, self.propsFormat])

        """Valeurs"""
        self.valsFormat = TextFormat("Valeurs", self.styles)
        for val in self.keywords["values"]:
            val_regex = QRegExp(val, Qt.CaseInsensitive)
            self.regles_valeurs.append([val_regex, self.valsFormat])

        """Balises"""
        self.tagsFormat = TextFormat("Balises", self.styles)
        for tag in self.regleHTML.keywords["tags"]:
            tag_regex = QRegExp(tag+"[^a-z0-9-()]+", Qt.CaseInsensitive)
            self.regles_tags.append([tag_regex, self.tagsFormat])

        """Classes"""
        self.classesFormat = TextFormat("Classes", self.styles)
        self.classes_regex = QRegExp("\\.[a-z][a-z0-9-]*", Qt.CaseInsensitive)

        """Ids"""
        self.idsFormat = TextFormat("Ids", self.styles)
        self.ids_regex = QRegExp("#[a-z][a-z0-9-]*", Qt.CaseInsensitive)

        """Accolades"""
        self.accoladesFormat = TextFormat("Accolades", self.styles)
        self.accolades_regex = QRegExp("[{}]")

        """Unites"""
        self.unitesFormat = TextFormat("Unités", self.styles)
        self.unites_regex = QRegExp("(([0-9]+\.?[0-9]?)|( \.[0-9]+))((px)|(em)|(cm)|(rem)|(pc)|(s)|(ms)|(%))")

        """Commentaires"""
        self.commentsFormat = TextFormat("Commentaires", self.styles)
        self.comments_debut = QRegExp("/\*")
        self.comments_fin = QRegExp("\*/")

        self.lists_regles = [self.regles_tags, self.regles_valeurs, self.regles_props]

        self.simples_regles = [
            {"regex": self.classes_regex, "format": self.classesFormat},
            {"regex": self.ids_regex, "format": self.idsFormat},
            {"regex": self.accolades_regex, "format": self.accoladesFormat},
            {"regex": self.unites_regex, "format": self.unitesFormat}
        ]

class ReglePHP(Regle):
    """Règles et formats dans le langage PYTHON"""
    def __init__(self, coloration):
        Regle.__init__(self, "PHP", coloration)
        self.regles_special_classes_functions = []
        self.regles_words = []
        self.debutPHP, self.finPHP = QRegExp("<\\?php", Qt.CaseInsensitive), QRegExp("\\?>")

        #Regex
        """words"""
        self.motsCles1 = TextFormat("Mots clés 1", self.styles)
        for word in self.keywords["words"]:
            word_regex = QRegExp("[ \t]"+word+"[ \t()]")
            word_start_regex = QRegExp("^"+word+"[ \t()]")
            word_end_regex = QRegExp("[ \t()]"+word+"$")
            self.regles_words.append([word_regex, self.motsCles1])
            self.regles_words.append([word_start_regex, self.motsCles1])
            self.regles_words.append([word_end_regex, self.motsCles1])

        """types"""
        self.typesFormat = TextFormat("Types", self.styles)
        for type in self.keywords["types"]:
            type_regex = QRegExp("[ \t()]"+type+"[ \t()]")
            type_start_regex = QRegExp("^"+type+"[ \t()]")
            type_end_regex = QRegExp("[ \t()]"+type+"$")
            self.regles_words.append([type_regex, self.typesFormat])
            self.regles_words.append([type_start_regex, self.typesFormat])
            self.regles_words.append([type_end_regex, self.typesFormat])

        """functions"""
        self.functionsFormat = TextFormat("Fonctions", self.styles)
        for function in self.keywords["functions"]:
            function_regex = QRegExp("[ \t()]" + function + "[ \t()]")
            function_start_regex = QRegExp("^" + function + "[ \t()]")
            function_end_regex = QRegExp("[ \t()]" + function + "$")
            self.regles_words.append([function_regex, self.functionsFormat])
            self.regles_words.append([function_start_regex, self.functionsFormat])
            self.regles_words.append([function_end_regex, self.functionsFormat])

        """String"""
        self.stringFormat = TextFormat("Chaines", self.styles)
        self.string_regex = QRegExp('("[^"]*")|(\'[^\']*\')', Qt.CaseInsensitive)
        """Variables"""
        self.variableFormat = TextFormat("Variables", self.styles)
        self.variable_regex = QRegExp("[^a-b0-9]\$[a-z_]+[^a-b0-9]", Qt.CaseInsensitive)

        """Numbers"""
        self.numberFormat = TextFormat("Nombres", self.styles)
        self.number_regex = QRegExp("[ \t():]([0-9]*\\.?[0-9])|([0-9]+)+[ \t():]")

        """Commentaires"""
        self.commentsFormat = TextFormat("Commentaires", self.styles)
        self.lineComment = QRegExp("//")
        self.comments_debut = QRegExp("/\\*")
        self.comments_fin = QRegExp("\\*/")

        self.lists_regles = [self.regles_words]

        self.simples_regles = [
            {"regex": self.number_regex, "format": self.numberFormat},
            {"regex": self.variable_regex, "format": self.variableFormat},
            {"regex": self.string_regex, "format": self.stringFormat}
        ]

class ColorSyntax(QSyntaxHighlighter):
    """Classe pour la coloration syntaxique du texte dans l'éditeur"""
    def __init__(self, parent = None, language:str = None, theme:VPTheme = None):
        super(ColorSyntax, self).__init__(parent)
        self.language = language
        self.theme = theme
        self.simpleTextFormat = QTextCharFormat()
        if theme.isRgb(theme.themeGeneral.foregrounds[0]):
            couleur = theme.decomposerCode(theme.themeGeneral.foregrounds[0])#couleur du texte simple
            self.simpleTextFormat.setForeground(QColor(couleur[0], couleur[1], couleur[2]))
        else:
            self.simpleTextFormat.setForeground(QColor(theme.themeGeneral.foregrounds[0]))
        self.coloration = self.theme.coloration
        """Attributs pour des langages particuliers"""
        self.styleFound = False #Pour dire si la balise <style> a été trouvée
        self.phpFound = False #Pour dire si un cde php a été trouvé

    """-------------------------------
    --------Fonction de coloration des commentaires
    ----------------"""
    def colorationCommentaires(self, text, regex_debut, regex_fin, format, previousCarac = 0):
        """Le parametre previousCarac change de valeur lorsque le texte initial et tronqué"""
        startIndex = -1
        if self.previousBlockState() != 1:
            # Debut du commentaire
            startIndex = regex_debut.indexIn(text)
        while startIndex >= 0:
            # On vérifie si la fin du commentaire est sur la ligne courante
            endIndex = regex_fin.indexIn(text, startIndex)
            if endIndex == -1:
                # Si ce n'est pas le cas
                self.setCurrentBlockState(1)
                comments_length = len(text) - startIndex
            else:
                # Si oui
                comments_length = endIndex - startIndex + regex_fin.matchedLength()
            self.setFormat(previousCarac+startIndex, comments_length, format)
            startIndex = regex_debut.indexIn(text, startIndex + comments_length)

    """----------------
    -----------Fonction de coloration totale-----
    ---------------------------------"""
    def highlightBlock(self, text):
        """Analyse chaque ligne et applique les lignes"""
        """Analyse des lignes avec les règles"""
        #Style avec
        if not hasattr(self.currentUserData(), "isPHP"):
            userData = QTextBlockUserData()
            userData.isStyle = False
            userData.isPHP = False
            self.setCurrentUserData(userData)
        if not hasattr(self.nextUserData(), "isPHP"):
            userData = QTextBlockUserData()
            userData.isStyle = False
            userData.isPHP = False
            self.setNextUserData(userData)

        if self.language.lower() in ("html", "htm","php"):
            """-------Langage HTML---------------"""

            regle = RegleHTML(self.coloration)
            """Balises"""
            for expression, tformat in regle.regles_tags:
                #Si l'expression ne doit pas avoir de parent
                index = expression.indexIn(text)
                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, tformat)
                    """Attributs"""
                    # Recherche des attributs dans la balise
                    contenuTag = text[index:(length + index)]
                    #Debut de la partie apres le nom de la balise
                    debutAttr = contenuTag.find(" ")
                    #Recuperation de la chaine correspondant à cette partie
                    after_space = contenuTag[debutAttr::]
                    for exp_attr, format_attr in regle.regles_attributes:
                        index_attr = exp_attr.indexIn(after_space)
                        while index_attr >=0:
                            length_attr = exp_attr.matchedLength()
                            self.setFormat(index + debutAttr + index_attr, length_attr, format_attr)
                            index_attr = exp_attr.indexIn(after_space, index_attr+length_attr)
                        index_text_attr = regle.attributesText_regex.indexIn(after_space)
                        """Texte attributs"""
                        while index_text_attr >= 0:
                            length_text_attr = regle.attributesText_regex.matchedLength()
                            self.setFormat(index + debutAttr + index_text_attr, length_text_attr, regle.attributesTextFormat)
                            index_text_attr = regle.attributesText_regex.indexIn(after_space, index_text_attr+length_text_attr)
                    index = expression.indexIn(text, index + length)
            self.setCurrentBlockState(0)
            """Utilisation de la fonction colorationCommentaires pour le style"""
            debutStyle = QRegExp("(<style [^<>]*>)|(<style>)", Qt.CaseInsensitive)
            finStyle = QRegExp("</style>", Qt.CaseInsensitive)
            startIndexStyle = debutStyle.indexIn(text)
            if hasattr(self.previousUserData(), "isStyle") and self.previousUserData().isStyle:
                startIndexStyle = 0
            while startIndexStyle >= 0:
                if not self.previousUserData().isStyle:
                    startText = startIndexStyle+debutStyle.matchedLength()
                else:
                    startText = startIndexStyle
                self.currentUserData().isStyle = True
                textStyle = ""
                # On vérifie si la fin du style est sur la ligne courante
                endIndexStyle = finStyle.indexIn(text, startIndexStyle)
                if endIndexStyle == -1:
                    # Si ce n'est pas le cas
                    style_length = len(text) - startIndexStyle
                    textStyle = text[startText:]
                else:
                    # Si oui
                    self.currentUserData().isStyle = False
                    textStyle = text[startText:endIndexStyle]
                    style_length = len(textStyle)
                regleCSS = RegleCSS(self.coloration)
                for list_regles in regleCSS.lists_regles:
                    for regex, format in list_regles:
                        index = regex.indexIn(textStyle)
                        while index >= 0:
                            self.setFormat(startText + index, regex.matchedLength(), format)
                            index = regex.indexIn(textStyle, index + regex.matchedLength())
                """Les autres règles"""
                for simple_regle in regleCSS.simples_regles:
                    index = simple_regle["regex"].indexIn(textStyle)
                    while index >= 0:
                        self.setFormat(startText + index, simple_regle["regex"].matchedLength(), simple_regle["format"])
                        index = simple_regle["regex"].indexIn(textStyle, index + simple_regle["regex"].matchedLength())
                startIndexStyle = debutStyle.indexIn(text, startIndexStyle + style_length)
            self.setCurrentBlockState(0)
            """Commentaires"""
            self.colorationCommentaires(text, regle.comments_debut, regle.comments_fin, regle.commentsFormat)

            """------Coloration du PHP------------"""
            regle = ReglePHP(self.coloration)
            startPHP = regle.debutPHP.indexIn(text)
            if hasattr(self.previousUserData(), "isPHP") and self.previousUserData().isPHP:
                startPHP = 0
            if startPHP >= 0:
                self.currentUserData().isPHP = True
                endPHP = regle.finPHP.indexIn(text, startPHP)
                if endPHP == -1:
                    lengthPHP = len(text) - startPHP
                else:
                    self.currentUserData().isPHP = False
                    lengthPHP = endPHP - startPHP + regle.finPHP.matchedLength()
                textPHP = text[startPHP:(endPHP+regle.finPHP.matchedLength())]
                self.setFormat(startPHP, lengthPHP, self.simpleTextFormat)
                for list_regles in regle.lists_regles:
                    for regex, format in list_regles:
                        index = regex.indexIn(textPHP)
                        while index >= 0:
                            self.setFormat(startPHP + index, regex.matchedLength(), format)
                            index = regex.indexIn(textPHP, index + regex.matchedLength())

                """Les autres règles"""
                for simple_regle in regle.simples_regles:
                    index = simple_regle["regex"].indexIn(textPHP)
                    while index >= 0:
                        self.setFormat(startPHP + index, simple_regle["regex"].matchedLength(), simple_regle["format"])
                        index = simple_regle["regex"].indexIn(textPHP, index + simple_regle["regex"].matchedLength())
                """Commentaire sur une ligne"""
                index = regle.lineComment.indexIn(textPHP)
                if index >= 0:
                    self.setFormat(startPHP + index, len(textPHP), regle.commentsFormat)
                self.setCurrentBlockState(0)
                self.colorationCommentaires(textPHP, regle.comments_debut, regle.comments_fin, regle.commentsFormat,
                                            startPHP)

                startPHP = regle.debutPHP.indexIn(text, startPHP + lengthPHP)

        elif self.language.lower() in ("css", "scss"):
            """------Langage CSS--------------"""

            regle = RegleCSS(self.coloration)
            """Regles sur les mots clés"""
            for list_regles in regle.lists_regles:
                for regex, format in list_regles:
                    index = regex.indexIn(text)
                    while index >= 0:
                        self.setFormat(index, regex.matchedLength(), format)
                        index = regex.indexIn(text, index + regex.matchedLength())

            """Les autres règles"""
            for simple_regle in regle.simples_regles:
                index = simple_regle["regex"].indexIn(text)
                while index >= 0:
                    self.setFormat(index, simple_regle["regex"].matchedLength(), simple_regle["format"])
                    index = simple_regle["regex"].indexIn(text, index + simple_regle["regex"].matchedLength())

            self.setCurrentBlockState(0)

            """Commentaires"""
            self.colorationCommentaires(text, regle.comments_debut, regle.comments_fin, regle.commentsFormat)
    def currentUserData(self):
        return self.currentBlock().userData()
    def previousUserData(self):
        return self.currentBlock().previous().userData()
    def nextUserData(self):
        return self.currentBlock().next().userData()
    def setCurrentUserData(self, e:QTextBlockUserData):
        self.currentBlock().setUserData(e)
    def setPreviousUserData(self, e:QTextBlockUserData):
        self.currentBlock().previous().setUserData(e)
    def setNextUserData(self, e:QTextBlockUserData):
        self.currentBlock().next().setUserData(e)