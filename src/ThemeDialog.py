# -*-coding : utf-8 -*-
from PyQt5.QtWidgets import QDialog, QWidget, QColorDialog, QMessageBox
from PyQt5.QtGui import QColor, QIcon, QPixmap

from src.Ui_ThemeDialog import *
from prog_languages.languages import *
from src.AppFiles import *
from src.VPTheme import fichier_theme, VPThemeFile, VPTheme, ICON_APP, THEME_PREDEFINIS

class ThemeDialog(QDialog, Ui_dialogTheme):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.fenetre = parent
        self.setupUi(self)
        self.verticalLayout_5.setContentsMargins(0,0,0,0)
        icon = QIcon()
        icon.addPixmap(QPixmap(ICON_APP), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.theme = parent.theme
        self.langage = ""
        self.mot = ""
        self.codeCouleur = ""
        self.colorDialog = QColorDialog(self)
        self.colorDialog.setWindowTitle("Selectionnez une couleur")
        self.colorDialog.setWindowIcon(icon)

        #Initialisation de certains éléments
        #Chargement des themes prédéefinis
        fichier_themes_predefinis = AppFile(THEME_PREDEFINIS)
        self.themes = fichier_themes_predefinis.lire()
        if self.themes is not None:
            for nom, fichier in self.themes:
                self.comboBoxThemes.addItem(nom)
        
        self.couleur.setEnabled(False)
        if self.theme.themeGeneral.environnement in ("sombre", "noir"):
            self.comboBoxGeneral.setCurrentIndex(0)
        else:
            self.comboBoxGeneral.setCurrentIndex(1)
        #Ajout des langages
        for lang in LANGUAGES.keys():
            self.listLangages.addItem(lang.upper())
        self.rafraichirMots()
        #Slots
        self.comboBoxThemes.currentTextChanged.connect(self.on_comboBoxThemes_textChanged)
        self.listLangages.itemClicked.connect(self.on_langageClicked)
        self.listMots.itemClicked.connect(self.on_motClicked)
        self.pushButtonChangerCouleur.clicked.connect(self.on_changerCouleur)
        self.colorDialog.currentColorChanged.connect(self.on_colorChanged)
        self.checkBoxItalique.clicked.connect(self.on_checkBoxFont_clicked)
        self.checkBoxGras.clicked.connect(self.on_checkBoxFont_clicked)
        self.comboBoxGeneral.currentTextChanged.connect(self.on_comboBoxGeneral_textChanged)
        self.show()
    def on_comboBoxThemes_textChanged(self, text):
        #Recherche du fichier theme
        nomFichierNouveau = ""
        for nom, fichier in self.themes:
            if nom == text:
                nomFichierNouveau = fichier
        fichierNouveau = VPThemeFile(appFolder+"/themes/"+nomFichierNouveau)
        theme = fichierNouveau.lire()
        if theme is not None and type(theme) == VPTheme:
            self.theme = theme
            self.rafraichirTabs()
    def on_comboBoxGeneral_textChanged(self, text):
        """Lorsqu'on change le thème général"""
        if text.lower().find("sombre") >= 0 or text.lower().find("noir") >= 0:
            self.theme.setStylesWidgets("sombre")
        else:
            self.theme.setStylesWidgets("clair")
        message = "Ce nouveau thème sera pris en compte au prochain démarrage de l'application"
        messageBox = QMessageBox.information(self, "Message", message, QMessageBox.Ok)

    def rafraichirMots(self):
        """Actualiser la partie des mots"""
        langagesSelectionnes = self.listLangages.selectedItems()
        if len(langagesSelectionnes) > 0:
            langage = langagesSelectionnes[0].text().upper()
        else:
            langage = self.listLangages.item(0).text().upper()
            self.listLangages.setCurrentRow(0)
        #On efface la liste des mots
        self.listMots.clear()
        for mot in LANGUAGES[langage]["coloration"]:
            self.listMots.addItem(mot)
        self.langage = langage
        self.listMots.setCurrentRow(0)
        self.rafraichirCouleurs()

    def on_langageClicked(self, item):
        """Lorsqu'on change de langage"""
        self.rafraichirMots()

    def rafraichirCouleurs(self):
        """Mettre à jour la zone couleurs"""
        motsSelectionnes = self.listMots.selectedItems()
        if len(motsSelectionnes) > 0:
            mot = motsSelectionnes[0].text()
        else:
            mot = None
        self.mot = mot
        if mot is not None:
            if self.langage != "":
                self.codeCouleur = self.theme.coloration[self.langage][mot]["couleur"]
                self.couleur.setStyleSheet("min-height:45px;background:" + self.codeCouleur + ";")
                self.checkBoxItalique.setChecked(self.theme.coloration[self.langage][mot]["italique"])
                self.checkBoxGras.setChecked(self.theme.coloration[self.langage][mot]["gras"])
                self.colorDialog.setCurrentColor(QColor(self.codeCouleur))

    def on_motClicked(self):
        """Lorsqu'on change de mot"""
        self.rafraichirCouleurs()

    def on_changerCouleur(self):
        """Lorsqu'on clique sur le bouton changer couleur"""
        self.colorDialog.show()

    def on_colorChanged(self, color):
        """Lorsqu'on change la couleur dans QColorDialog"""
        self.couleur.setStyleSheet("min-height:45px;background:" + color.name() +";")
        self.theme.coloration[self.langage][self.mot]["couleur"] = color.name()
        self.rafraichirTabs()

    def on_checkBoxFont_clicked(self):
        """Quand on clique sur un checkbox dans la zone font"""
        self.theme.coloration[self.langage][self.mot]["italique"] = self.checkBoxItalique.checkState()
        self.theme.coloration[self.langage][self.mot]["gras"] = self.checkBoxGras.checkState()
        self.rafraichirTabs()

    def rafraichirTabs(self):
        """Mise à jour des TabText"""
        tabs = self.fenetre.tabs
        for tabText in tabs.tabtexts:
            tabText.theme = self.theme
            tabText.coloration()

    def closeEvent(self, event):
        """Quand on ferme la boîte"""
        fichier_theme.ecrire(self.theme)
        event.accept()