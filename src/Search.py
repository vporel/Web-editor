# -*-coding:utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QTextCursor, QIcon, QPixmap
from src.Ui_Search import *
from src.AppFiles import *
from src.VPTheme import ICON_APP

class Search(QDialog, Ui_Search):
    """QDialog pour la recherche d'un mot"""
    def __init__(self, parent, currentIndex = 0, tabText = None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(ICON_APP), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.theme = parent.theme
        self.setStyleSheet(self.theme.styleRecherche)
        self.fenetre = parent
        self.tabText = tabText
        self.tabWidgetRecherche.setCurrentIndex(currentIndex)
        self.pushButtonRechercher.clicked.connect(self.rechercher)
        self.pushButtonRemplacer.clicked.connect(self.remplacer)
        self.pushButtonClear.clicked.connect(self.clearRecherche)
        self.pushButtonClear2.clicked.connect(self.clearRemplacement)

        self.pushButtonNext.clicked.connect(self.nextSelection)
        self.pushButtonPrev.clicked.connect(self.prevSelection)

        self.currentSelection = -1
        self.show()

    def rechercher(self, stats = False, mot = ""):
        """Rechercher le mot ou l'expression en parametre"""
        if not stats:
            mot = self.motRechercher.text()
        positions = []
        text = self.tabText.toPlainText()
        index = text.find(mot)
        while index >= 0:
            positions.append(index)
            index = text.find(mot, index+1)
        nbResultats = len(positions)
        self.lineEditProgression.setText("0/" + str(nbResultats))
        numsLignes = []
        if nbResultats > 0:
            for button in (self.pushButtonToutSelectionner, self.pushButtonNext, self.pushButtonPrev):
                button.setEnabled(True)
            resultatRecherche = "Nombre de résultats : "+ str(nbResultats) + "\n"
            resultatRecherche += "Lignes : "
            for pos in positions:
                tc = self.tabText.textCursor()
                tc.setPosition(pos, QTextCursor.MoveAnchor)
                tc.setPosition(pos + len(mot), QTextCursor.KeepAnchor)
                self.tabText.setTextCursor(tc)
                if pos == 0:
                    numsLignes.append(1)
                else:
                    indexEnter = text.find("\n", 0, pos)
                    if indexEnter < 0:
                        numsLignes.append(1)
                    else:
                        i = 1
                        while indexEnter >= 0 and indexEnter < pos:
                            i+=1
                            if text.find("\n", indexEnter+1, len(text)) > pos:
                                exist = False
                                for numLigne in numsLignes:
                                    if numLigne == i:
                                        exist = True
                                if not exist:
                                    numsLignes.append(i)
                            indexEnter = text.find("\n", indexEnter+1, len(text))
            for i, numLigne in enumerate(numsLignes):
                resultatRecherche += str(numLigne)
                if i < len(numsLignes)-1:
                    resultatRecherche += ", "
        else:
            for button in (self.pushButtonToutSelectionner, self.pushButtonNext, self.pushButtonPrev):
                button.setEnabled(False)
            resultatRecherche = "Aucun résultat"
        self.resultatRecherche.setPlainText(resultatRecherche)
        if stats:
            return {"positions": positions, "numsLignes": numsLignes, "infos":resultatRecherche}

    def remplacer(self):
        """remplacer le mot ou l'expression en parametre"""
        motRemplacer = self.motRemplacer.text()
        nouveauMot = self.nouveauMot.text()
        recherche = self.rechercher(True, motRemplacer)
        positions = recherche["positions"]
        infosRemplacement = recherche["infos"]
        ajouts = 0 #Cette variable sert à vérifier si de remplacement ont déjà été faits
        for pos in positions:
            posPlus = 0 #posPlus pour les décalages de positions à cause des autres remplacements
            ajouts_ = ajouts
            while ajouts_ > 0:
                posPlus += len(nouveauMot) - len(motRemplacer)
                ajouts_ -= 1
            tc = self.tabText.textCursor()
            tc.setPosition(pos + posPlus)
            tc.setPosition(pos + posPlus + len(motRemplacer), QTextCursor.KeepAnchor)
            self.tabText.setTextCursor(tc)
            self.tabText.insertPlainText(nouveauMot)
            ajouts += 1
        self.fenetre.setFocus()
        if (len(positions) > 0):
            infosRemplacement += "\nL'expression \"" + motRemplacer+"\" a été remplacée par \"" + nouveauMot + "\""
        else:
            infosRemplacement += "\nAucun remplacement possible"
        self.infosRemplacement.setPlainText(infosRemplacement)

    def changeSelection(self, direction):
        """Changer de sélection"""
        mot = self.motRechercher.text()
        recherche = self.rechercher(True, mot)
        positions = recherche["positions"]
        sel = -1
        if direction == "next":
            sel = self.currentSelection + 1
            if sel >= len(positions):
                sel = 0
        else:
            sel = self.currentSelection - 1
            if sel < 0:
                sel = len(positions)-1
        self.currentSelection = sel
        self.lineEditProgression.setText(str(sel+1) + "/" + str(len(positions)))
        pos = positions[sel]
        tc = self.tabText.textCursor()
        tc.setPosition(pos)
        tc.setPosition(pos + len(mot), QTextCursor.KeepAnchor)
        self.tabText.setTextCursor(tc)
        self.fenetre.setFocus()

    def nextSelection(self):
        """Passer au mot suivant"""
        self.changeSelection("next")

    def prevSelection(self):
        """Passer au mot précédent"""
        self.changeSelection("prev")

    def clearRecherche(self):
        """Efface le champ pour la recherche"""
        self.motRechercher.setText("")
        self.resultatRecherche.setPlainText("")

    def clearRemplacement(self):
        """Efface le champ pour la recherche"""
        self.motRemplacer.setText("")
        self.nouveauMot.setText("")
        self.infosRemplacement.setPlainText("")