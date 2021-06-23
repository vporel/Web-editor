from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

class MenuBar(QMenuBar):
    def __init__(self, parent):
        QMenuBar.__init__(self,parent)
    def addMenus(self, *menus):
        menus = list(menus)
        for menu in menus:
            self.addMenu(menu)

class Menu(QMenu):
    def __init__(self, title, parent):
        QMenu.__init__(self,title, parent)
    def addMenus(self, *menus):
        menus = list(menus)
        for menu in menus:
            self.addMenu(menu)
    def addActions(self, *actions):
        actions = list(actions)
        for action in actions:
            self.addAction(action)
class Action(QAction):
    def __init__(self, text, parent, icon = None, name = None, shortcut = None):
        QAction.__init__(self, text, parent)
        if icon is not None:
            self.setIcon(QIcon(icon))
        if name is not None:
            self.setObjectName(name)
        if shortcut is not None:
            self.setShortcut(shortcut)

