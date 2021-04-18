# -*-coding:utf-8 -*-
import os
from pickle import Pickler, Unpickler
from PyQt5.QtGui import QColor, QFont, QPixmap

filePath = os.path.realpath(__file__)
filePath = filePath.split("\\")
del filePath[len(filePath)-1]
del filePath[len(filePath)-1] #Delete the both last element in the file path
appFolder = "/".join(filePath)

CHEMIN_THEME = appFolder + "/data/theme.vpd"
PATH_USER_FOLDERS = appFolder + "/data/user_folders.vpd"
PATH_USER_FILES = appFolder + "/data/user_files.vpd"
PATH_USER_PROJECTS = appFolder + "/data/user_projects.vpd"
WELCOME_FILE = appFolder + "/data/welcome.html"

"""
    HOW ARE THE USER'S DATA KEPT,???
    -- Files (list of dicts)
        
        ({title: str, path: str, content: long_str})
    -- Folders ( list of dicts)
        ({url: str})
    -- Projects : dict
        {currentProjectPath : str, projectsPaths: list()}
    
    EXTENSIONS OF APPFILES
    -- app-data(as files, folders, info-theme) : .vpd
    -- Themes : .vpt
    -- projects : .vpp
        
"""
def inList(el, list:list):
    "Check if el is in list"
    isInside, index = False, -1
    for i, e in enumerate(list):
        if e == el:
            isInside = True
            index = i
    return isInside,index

class ProjectFile:
    """Structure of a project file"""
    MAIN_FILE = "main"
    STYLE_FILE = "style"
    SCRIPT_FILE = "script"
    def __init__(self, name, path, type, project = None):
        self.name = name
        self.path = path
        self.type = type #Three types: main, style, script
        self.links = {ProjectFile.MAIN_FILE:[], ProjectFile.STYLE_FILE:[], ProjectFile.SCRIPT_FILE: []} #Links
        """When a link is established, if one file is change, all the others files will change"""
        self.project = project
    def addLink(self, file):
        """Only the file which is from the types below can be a source a link"""
        if not self.isLinked(file.type.lower(),file.path):
            self.links[file.type.lower()].append(file)
            file.addLink(self)
    def isLinked(self, type, path):
        """Check if a file is linked to the current file"""
        result = False
        for f in self.links[type.lower()]:
            if f.path == path:
                result = True
        return result
    def endPathFromProject(self):
        """The next of path after the name of project's folder"""
        if self.project is not None:
            coupure = self.path.split(self.project.path)
            return coupure[-1]

    @staticmethod
    def endPathFromUrl(project, url):
        """The next of path after url"""
        if project is not None and project.type == Project.LOCAL_TYPE:
            coupure = url.split(project.urlforbrowser)
            return coupure[-1]

    def url(self):
        """To visualise in navigator"""
        if self.project is not None:
            if self.project.type == Project.SIMPLE_TYPE:
                return self.path
            else:
                return self.project.urlforbrowser+self.endPathFromProject()



class Project:
    """
        This class define a project structure
        A project file have the extension ".vpp"
    """
    SIMPLE_TYPE = "simple"
    LOCAL_TYPE = "local"
    def __init__(self, name, path, type = SIMPLE_TYPE, urlforbrowser = None):
        self.name = name
        self.path = path
        self.type = type #We have two types : simple and local
        self.urlforbrowser = urlforbrowser #Url to visualise the project in the browser
        self.files = {ProjectFile.MAIN_FILE:[], ProjectFile.STYLE_FILE:[], ProjectFile.SCRIPT_FILE:[]} #List of project files

    def pathWithName(self):
        """Get the path of projet with his name"""
        return self.path+"/"+self.name+".vpp"

    def addFile(self, file:ProjectFile):
        """Add a file to the project"""
        file.project = self
        self.files[file.type.lower()].append(file)

    def getAllFiles(self):
        """Return all the project files"""
        files = list(self.files[ProjectFile.MAIN_FILE])
        files.extend(self.files[ProjectFile.STYLE_FILE])
        files.extend(self.files[ProjectFile.SCRIPT_FILE])
        return files

    def isProjectFile(self, path:str):
        """Check if a file which the name "name" is a project file"""
        files = self.getAllFiles()
        isProjectFile, projectFile = False, None
        for f in files:
            if f.path == path:
                isProjectFile = True
                projectFile = f
                break
        return (isProjectFile, projectFile)

    def getProjectFile(self, path:str):
        """Return the project file which have the name "name" """
        isProjectFile, projectFile = self.isProjectFile()
        return projectFile

#Classe qui gère les fichiers
class File:
    def __init__(self, chemin, modeLecture = "r", modeEcriture = "w"):
        self.chemin = chemin
        self.modeLecture = modeLecture
        self.modeEcriture = modeEcriture

    def exist(self):
        """Fonction qui vérifie l'existence du fichier"""
        if os.path.isfile(self.chemin):
            return True
        else:
            return False

    def lire(self):
        """Lecture du fichier"""
        with open(self.chemin, self.modeLecture) as f:
            return f.read()
    def read(self):
        """Lecture du fichier"""
        with open(self.chemin, self.modeLecture) as f:
            return f.read()

    def ecrire(self, donnee):
        """Ecriture dans le fichier"""
        with open(self.chemin, self.modeEcriture) as f:
            f.write(donnee)
    def write(self, data):
        """Ecriture dans le fichier"""
        with open(self.chemin, self.modeEcriture) as f:
            f.write(data)

    def nom(self):
        """Determination du nom du fichier"""
        coupure = self.chemin.split('/')
        if len(coupure) <= 1:
            coupure = self.chemin.split('\\')
        nom = coupure[-1]
        return nom

    def name(self):
        """Determination du nom du fichier"""
        coupure = self.chemin.split('/')
        if len(coupure) <= 1:
            coupure = self.chemin.split('\\')
        name = coupure[-1]
        return name

    def extension(self):
        """Determination de l'extension du fichier"""
        coupure = self.nom().split('.')
        ext = coupure[len(coupure) - 1]
        return ext

# Classe qui gère les fichiers des utilisateurs
class UserFile(File):
    def __init__(self, chemin):
        File.__init__(self, chemin)

    def pixMap(self):
        ext = self.extension()
        if ext == "txt":
            return QPixmap(appFolder+"/images/icones/txt.png")
        elif ext in ("html", "html"):
            return QPixmap(appFolder+"/images/icones/html.png")
        elif ext == "css":
            return QPixmap(appFolder+"/images/icones/css.png")
        elif ext == "scss":
            return QPixmap(appFolder+"/images/icones/scss.png")
        elif ext == "js":
            return QPixmap(appFolder+"/images/icones/js.png")
        elif ext == "php":
            return QPixmap(appFolder+"/images/icones/php.png")
        else:
            return QPixmap(appFolder+"/images/icones/incomming.png")

# Classe qui gère les fichiers de l'app
class AppFile(File):
    def __init__(self, chemin):
        File.__init__(self, chemin)

    def lire(self):
        if self.exist():
            if os.path.getsize(self.chemin) > 0:
                with open(self.chemin, 'rb') as f:
                    unpickler = Unpickler(f)
                    return unpickler.load()
            else:
                return None
        else:
            f = open(self.chemin, 'w')
            f.close()
            self.lire()
    def read(self):
        if self.exist():
            if os.path.getsize(self.chemin) > 0:
                with open(self.chemin, 'rb') as f:
                    return Unpickler(f).load()
            else:
                return None
        else:
            f = open(self.chemin, 'w')
            f.close()
            self.read()
    def ecrire(self, donnee):
        with open(self.chemin, 'wb') as f:
            Pickler(f).dump(donnee)
    def write(self, data):
        with open(self.chemin, 'wb') as f:
            Pickler(f).dump(data)


if __name__ == '__main__':
    class er:
        def __init__(self):
            self.c = "Paaaaaaa"
            self.d = "opoloplo"
    ap = AppFile("data/tabs.vp")
    t = er()
    ap.ecrire(t)

