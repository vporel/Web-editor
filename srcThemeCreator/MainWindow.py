# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QFileDialog, QColorDialog, QScrollBar, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot, QObject
from PyQt5.QtGui import QIcon, QPixmap, QColor

from VPEdThemeCreatorSRC.Ui_MainWindow import *
from VPEditorSRC.VPTheme import *
from prog_languages.languages import *
from VPEditorSRC.AppFiles import UserFile
from VPEditorSRC.Coloration import *
from VPEditorSRC.VpPyQt5 import *

from threading import Thread
import socket

ICON_APP = "./images/logo-bleu.png"

class MainWindow(QMainWindow, Ui_MainWindow):
     def __init__(self):
         QMainWindow.__init__(self)
         self.setupUi(self)
         try:
             icon = QIcon()
             icon.addPixmap(QPixmap(ICON_APP), QIcon.Normal, QIcon.Off)
             self.setWindowIcon(icon)
         except:
             print("Erreur de chargement de l'icone")
         self.fichier = None
         self.fichierPrevisualisation = None
         self.theme = None
         self.langage = None
         self.mot = None
         self.colorDialog = QColorDialog(self)
         self.colorDialog.currentColorChanged.connect(self.on_colorChanged)
         self.nom.textChanged.connect(self.on_nom_textChanged)
         self.auteur.textChanged.connect(self.on_auteur_textChanged)
         self.show()
         self.initCreation()
     def initCreation(self):
         """
            Initialisation de la création du thème
         """
         if self.fichier is None:
             actions = ["Créer un thème", "Charger un thème"]
             message = "Que voulez-vous faire ?"
             item, ok = QInputDialog.getItem(self, "VPEdThemeCreator", message, actions, 0, False)
             if ok and item == actions[1]:
                 self.on_actionOuvrir_triggered(init = True)
             else:
                 self.on_actionNouveau_triggered()

         # Tabulation
         self.previsualisation.spaceWidth = self.previsualisation.fontMetrics().width(" ")
         self.previsualisation.setTabStopWidth(self.previsualisation.spaceWidth * 7)
         self.previsualisation.setStyleSheet("""
                font:14px comic sans ms, verdana;background:rgb(""" + self.theme.themeGeneral.backgrounds[4] + """);
                color:rgb(""" + self.theme.themeGeneral.foregrounds[0] + """);
         """)
         self.previsualisation.setHorizontalScrollBar(QScrollBar(Qt.Horizontal, self.previsualisation))

         # Evènements
         self.langages.itemClicked.connect(self.on_langages_itemChanged)
         self.mots.itemClicked.connect(self.on_mots_itemChanged)

         for lang in LANGUAGES.keys():
             self.langages.addItem(lang)

         #Changement de couleur (évènement)
         self.changerCouleur.clicked.connect(self.on_changerCouleur)
         self.italique.clicked.connect(self.on_checkBoxFont_clicked)
         self.gras.clicked.connect(self.on_checkBoxFont_clicked)
         self.general.currentTextChanged.connect(self.on_comboBoxGeneral_textChanged)

     @pyqtSlot()
     def on_nom_textChanged(self):
         self.theme.nom = self.nom.text()

     @pyqtSlot()
     def on_auteur_textChanged(self):
         self.theme.auteur = self.auteur.text()

     @pyqtSlot()
     def on_actionNouveau_triggered(self):
         """
            Création d'un nouveau
         :return:
         """
         self.fichier = VPThemeFile(THEME_DEFAUT)
         self.theme = self.fichier.lire()
         self.setWindowTitle("VPEditor Theme Creator - New...")
         self.chargerTheme(self.theme)

     @pyqtSlot()
     def on_actionOuvrir_triggered(self, init=False):
         """
            Ouverture d'un thème
         :return:
         """
         chemin, filtre = QFileDialog.getOpenFileName(self, "Chargement thème", filter="VPEditor Thème(*.vpt)")
         if chemin:
             self.fichier = VPThemeFile(chemin)
             if self.fichier.isThemeFile():
                 self.theme = self.fichier.lire()
                 self.setWindowTitle("VPEditor Theme Creator - " + chemin)
                 self.chargerTheme(self.theme)
             else:
                 message = "Ce fichier n'est pas un thème VPEditor"
                 reponse = QMessageBox.information(self, "Erreur", message, QMessageBox.Ok)
                 if init is True:
                     self.on_actionNouveau_triggered()
         else:
             if init is True:
                 self.on_actionNouveau_triggered()

     def chargerTheme(self, theme:VPTheme):
         """
            Chargment du thème
         :param theme:
         :return:
         """
         #Nom du thème
         self.nom.setText(theme.nom)
         self.auteur.setText(theme.auteur)
         self.previsualisation.theme = theme
         self.previsualisation.setPlainText("")
         self.couleur.setStyleSheet("background:none")
         self.mots.clear()

     @pyqtSlot()
     def on_actionEnregistrer_triggered(self):
         """Enregistrement du theme"""
         if type(self.fichier) == VPThemeFile and self.fichier.chemin != THEME_DEFAUT:
             self.fichier.ecrire(self.theme)
         else:
             self.on_actionEnregitrer_sous_triggered()

     @pyqtSlot()
     def on_actionEnregitrer_sous_triggered(self):
         """Enregistrement du theme"""
         """Parfois confusion dans ui_main entre enregitrer et enregistrer"""
         #Vérification
         if self.nom.text() not in ("", " "):
             if self.auteur.text() not in ("", " "):
                 chemin, filtre = QFileDialog.getSaveFileName(self, "Enregistrement du thème", filter="VPEditor Thème(*.vpt)")
                 if chemin:
                     fichier = VPThemeFile(chemin)
                     fichier.ecrire(self.theme)
                     self.fichier = fichier
                     self.setWindowTitle("VPEditor Theme Creator - " + chemin)
             else:
                 alerte = alert(self, "Veuillez entrer votre nom en tant qu'auteur");
         else:
             alerte = alert(self, "Veuillez entrer le nom du thème");


     def on_langages_itemChanged(self, item):
         langageSelectionne = item.text()
         self.langage = langageSelectionne
         self.rafraichirMots(langageSelectionne)
         try:
             cheminPrevisualisation = "VPEdThemeCreatorSRC/previsualisation/"+langageSelectionne+"."+LANGUAGES[langageSelectionne]["exts"][0]
             self.fichierPrevisualisation = UserFile(cheminPrevisualisation)
             self.previsualisation.theme = self.theme
             self.previsualisation.colorSyntax = ColorSyntax(self.previsualisation.document(), self.fichierPrevisualisation.extension(), self.theme)
             self.previsualisation.setPlainText(self.fichierPrevisualisation.lire())
         except:
             pass

     def rafraichirMots(self, langage):
         """Actualiser la partie des mots"""
         # On efface la liste des mots
         self.mots.clear()
         for mot in LANGUAGES[langage]["coloration"]:
             self.mots.addItem(mot)

     def on_mots_itemChanged(self, item):
         """Lorsqu'on change de mot"""
         self.rafraichirCouleurs(item.text())


     def rafraichirCouleurs(self, mot):
         """Mettre à jour la zone couleurs"""
         self.mot = mot
         if mot is not None:
             if self.langage is not None:
                 self.codeCouleur = self.theme.coloration[self.langage][mot]["couleur"]
                 self.couleur.setStyleSheet("background:" + self.codeCouleur + ";")
                 self.italique.setChecked(self.theme.coloration[self.langage][mot]["italique"])
                 self.gras.setChecked(self.theme.coloration[self.langage][mot]["gras"])
                 self.colorDialog.setCurrentColor(QColor(self.codeCouleur))

     def on_changerCouleur(self):
         """Lorsqu'on clique sur le bouton changer couleur"""
         self.colorDialog.show()

     def on_colorChanged(self, color):
         """Lorsqu'on change la couleur dans QColorDialog"""
         self.couleur.setStyleSheet("background:" + color.name() + ";")
         self.theme.coloration[self.langage][self.mot]["couleur"] = color.name()
         self.rafraichirTabs()

     def on_checkBoxFont_clicked(self):
         """Quand on clique sur un checkbox dans la zone font"""
         self.theme.coloration[self.langage][self.mot]["italique"] = self.italique.checkState()
         self.theme.coloration[self.langage][self.mot]["gras"] = self.gras.checkState()
         self.rafraichirTabs()

     def rafraichirTabs(self):
         """Mise à jour des TabText"""
         self.previsualisation.theme = self.theme
         self.previsualisation.colorSyntax = ColorSyntax(self.previsualisation.document(), self.fichierPrevisualisation.extension(), self.theme)

     def on_comboBoxGeneral_textChanged(self, text):
         """Lorsqu'on change le thème général"""
         if text.lower().find("sombre") >= 0 or text.lower().find("noir") >= 0:
             self.theme.setStylesWidgets("sombre")
         else:
             self.theme.setStylesWidgets("clair")
         self.previsualisation.setStyleSheet("""
             font:14px comic sans ms, verdana;background:rgb(""" + self.theme.themeGeneral.backgrounds[4] + """);
             color:rgb(""" + self.theme.themeGeneral.foregrounds[0] + """);
         """)