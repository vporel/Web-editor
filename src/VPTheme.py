# -*-coding:utf-8 -*-

from pickle import Pickler, Unpickler
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from src.AppFiles import *

THEME_DEFAUT = appFolder+"/themes/VPTDefault.vpt"
THEME_PREDEFINIS = appFolder+"/themes/themes_predefinis.vpd"
ICON_APP = appFolder+"/images/logo-bleu.png"

colors = {
    "windowBackground" : "50,60,70",
    "editorBackground" : "30,30,30",
    "btnColor" : "30,150,220"
}

class VPThemeFile(AppFile):
    def __init__(self, chemin):
        AppFile.__init__(self,chemin)

    def isThemeFile(self):
        """
            Vérifie si le fichier est bien un thème
        :return:
        """
        content = self.lire()
        return (type(content) == VPTheme)

class ThemeGeneral:
    def __init__(self, environnement:str = "noir"):
        #Initialisation des variables pour un thème foncé
        self.environnement = environnement
        self.getBackgrounds(80)
        self.foregrounds = ("200,200,200", "255, 255, 255", "50,50,50")
        self.backgroundMenu = "0,110,255"
        if self.environnement in ("blanc", "clair"):
            self.getBackgrounds(215)
            self.foregrounds = ("0,0,0", "30,30,30", "50,50,50")

    def getBackgrounds(self, debut:int):
        bgs = []
        i, ajout = 1, 0
        while i <= 5:
            bgs.append(str(debut+ajout)+", "+str(debut+ajout)+", "+str(debut+ajout))
            if self.environnement in ("noir", "sombre"):
                ajout -= 10
            else:
                ajout += 10
            i += 1
        self.backgrounds = bgs

class VPTheme:
    """
        Classe de définition d'un thème
    """
    def __init__(self, nom = "", auteur = ""):
        self.nom = nom
        self.auteur = auteur
        self.coloration = dict()
        self.initTheme("clair")
        self.default()
        self.setStylesWidgets("sombre")
    def initTheme(self, environnement):
        self.themeGeneral = ThemeGeneral(environnement)

    def decomposerCode(self, code: str):
        """Give a rgb Color as a list"""
        valeurs = code.split(",")
        valeurs = [int(val.strip()) for val in valeurs]
        return valeurs

    def isRgb(self, couleur: str):
        """Check a code is on rgb format"""
        valeurs = self.decomposerCode(couleur)
        if len(valeurs) >= 3:
            return True
        else:
            return False
    def default(self):
        self.coloration = {
            #-------------HTML-------------
            "HTML" : {
                "Balises" : {"couleur":"#079090", "italique":False, "gras":True},
                "Balises inconnues" : {"couleur":"#b502a2", "italique":False, "gras":False},
                "Attributs" : {"couleur":"#7b7a03", "italique":False, "gras":False},
                "Attributs inconnus" : {"couleur":"#16ab03", "italique":False, "gras":False},
                "Textes attributs" : {"couleur":"#c99006", "italique":False, "gras":False},
                "Commentaires" : {"couleur":"#7f7f7f", "italique":True, "gras":False}
            },

            #------------CSS--------
            "CSS" : {
                "Propriétés": {"couleur":"#969696", "italique":False, "gras":False},
                "Valeurs": {"couleur":"#965656", "italique":False, "gras":False},
                "Balises": {"couleur":"#0164de", "italique":False, "gras":False},
                "Classes": {"couleur":"#7b7a03", "italique":False, "gras":False},
                "Ids": {"couleur":"#29789f", "italique":False, "gras":False},
                "Accolades": {"couleur":"#c99006", "italique":False, "gras":False},
                "Unités": {"couleur":"#d00000", "italique":False, "gras":False},
                "Commentaires": {"couleur":"#138301", "italique":True, "gras":False}
            },

            #------------PHP------
            "PHP" : {
                "Variables": {"couleur":"#555555", "italique":False, "gras":False},
                "Chaines": {"couleur":"#139001", "italique":False, "gras":True},
                "Nombres": {"couleur":"#5984b0", "italique":False, "gras":False},
                "Mots clés 1": {"couleur":"#ecb130", "italique":False, "gras":False},
                "Types": {"couleur":"#c00006", "italique":False, "gras":False},
                "Fonctions": {"couleur":"#fda110", "italique":True, "gras":False},
                "Commentaires": {"couleur":"#7f7f7g", "italique":True, "gras":True}
            }
        }

    def setStylesWidgets(self, environnement):
        self.themeGeneral = ThemeGeneral(environnement)
        styleScrollbar = """
            QScrollBar{background:rgb("""+colors["editorBackground"]+""");border:0px;}
            QScrollBar:vertical{width:7px;}
            QScrollBar:horizontal{height:7px;}
            QScrollBar::handle{background:rgba(150,150,150,100);border-radius:5px;}
            QScrollBar::add-line, QScrollBar::sub-line{border: 0px;background: transparent;}
            QScrollBar::add-page, QScrollBar::sub-page {background: none;}
        """
        self.styleMenu = """
            QMenuBar{}
            QMenuBar::item{color:rgb(200,200,200);height:100%;width:50px;}
            QMenuBar::item:selected{color:black;background:rgb("""+colors["btnColor"]+""");}
            QMenu{padding:0;border-top:1px solid gray;}
            QMenu::item:selected{background:rgba(255,255,255,30);}
        """
        # Editor
        # ------------
        self.styleTabs = """
            Tabs, Navigator{border:0px;}
            Tabs::pane, Navigator::pane{border:0px;}
            Tabs:tab-bar, Navigator:tab-bar{
                border:2px solid black;left:34px;
            }
            QTabBar::tab{
                background:transparent;border:0;padding:5px 8px;color:rgb(230,230,230);
                font:11px sans-serif;
            }
            QTabBar::tab:selected{background:rgba("""+colors["editorBackground"]+""", 150);}
            QTabBar::tab:hover{background:rgba("""+colors["editorBackground"]+""", 100);}
        """
        self.styleGroupEdit = """
            QListWidget{
                background:rgb(""" + self.themeGeneral.backgrounds[4] + """);border:1px solid lightgray;
                color:rgb(""" + self.themeGeneral.foregrounds[1] + """);
            }
            QListWidget::item{font:17px comic sans ms, verdana, sans-serif;height:25px;text-indent:5px;}
            QListWidget::item:selected{background:rgb(""" + self.themeGeneral.backgroundMenu + """)}
        """ + styleScrollbar
        self.styleEditorText = """
            TabText{
                font:14px  Lucida Sans Unicode;background:rgb("""+colors["editorBackground"]+""");
                color:rgb(230,230,230);border:0px
            }
        """ + styleScrollbar
        self.styleLineNumberArea = """
            color:rgb(220,220,220);font:12px sans-serif;
        """
        c = self.decomposerCode(colors["windowBackground"])
        self.backgroundLineNumberArea = QColor(c[0], c[1], c[2],100)
        self.backgroundCurrentLine = QColor(c[0], c[1], c[2],50)

        # Dossiers
        self.styleFolders = """
            Folders{
                background:transparent;    
            }
        """
        self.styleFolder = """
            Folder{
                font:13px sans-serif;border:0px;
            }
        """ + styleScrollbar

        # QDialog
        self.styleRecherche = """
           QDialog{background:rgb(110,110,110);}
           QTabWidget{border:0px;}
           QTabBar::tab{
                background:transparent;border:0;padding:5px 10px;color:rgb(200,200,200);font:12px sans-serif;
                min-width:100px;
           }
           QTabBar::tab:selected{background:rgb(70,70,70);color:white;}
           QTabBar::tab:hover{background:rgb(80,80,80)}
        """ + styleScrollbar

fichier_theme = AppFile(CHEMIN_THEME)
#theme = fichier_theme.lire()
theme = None
if theme is None:
    theme = VPTheme()
    fichier_theme.ecrire(theme)