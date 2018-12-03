# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy
class loadingGif(QWidget):
    def __init__(self, parent=None):
        super(loadingGif, self).__init__(parent)
        # self.setStyleSheet('background:gold;')
        self.label = QLabel('No movie loaded', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(100,100)
        self.label.setStyleSheet('background:gold;')
        self.label.setScaledContents(True)
        # self.setFixedSize(200, 200)
        # self.setWindowFlags(Qt.Dialog|Qt.CustomizeWindowHint)
        self.movie = QMovie("loading.gif")

        self.label.setMovie(self.movie)

        self.movie.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = loadingGif()
    mw.show()
    sys.exit(app.exec_())
