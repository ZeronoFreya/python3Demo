# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QPushButton, QMenu, 
        QPushButton, QSystemTrayIcon)

class Example(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.createActions()
        self.createTrayIcon()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('ToolTips')

        # self.button = QPushButton(self)
        # self.button.setText(self.tr('显示弹窗'))
        # self.button.clicked.connect(self.showPoput)

    def createActions(self):
        self.quitAction = QAction("&Quit", self,
                triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

        icon = QIcon('loading.gif')
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
    
    def closeEvent(self, event):
        self.trayIcon.setVisible(False)

        

    def do(self):
        print('子窗口调用')

    # def showPoput(self):
    #     dlg = PoputDialog(self)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    # QApplication.setQuitOnLastWindowClosed(False)

    ex = Example()
    ex.show()
    sys.exit(app.exec_())