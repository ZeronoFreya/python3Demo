# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class Ui_Simple(object):
    def setupUi(self):
        self.setObjectName("Simple")
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')


class Simple(QWidget, Ui_Simple):
    def __init__(self, parent=None):
        super(Simple, self).__init__(parent)
        self.setupUi()
        self.installEventFilter(self)

    def __clicked(self):
        pass

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            print(123)
        return QWidget.eventFilter(self, object, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Simple()
    w.show()
    sys.exit(app.exec_())
