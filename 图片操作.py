# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
from PyQt5.QtCore import Qt
from os.path import join, dirname
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QTransform, QPainter, QColor


class Ui_Simple(object):
    def setupUi(self):
        self.setObjectName("Simple")
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')

        self.rotate = QPushButton('旋转', self)

        self.imageLabel = QLabel()
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)


class Simple(QWidget, Ui_Simple):
    def __init__(self, parent=None):
        super(Simple, self).__init__(parent)
        self.setupUi()

        self.cnt = 0
        self.transform = QTransform()

        hLay = QHBoxLayout()
        hLay.addWidget(self.rotate)
        self.rotate.clicked.connect(self.__rotate)

        lay = QVBoxLayout(self)
        lay.addLayout(hLay)
        lay.addWidget(self.imageLabel)

        self.image = QImage()
        if self.image.load(
                join(dirname(__file__), 'img1.png')):
            # self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
            self.resize(self.image.width(), self.image.height())

    def __rotate(self):
        if self.image.isNull():
            return

        # self.image = self.image.transformed(transform)
        # self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        # self.resize(self.image.width(), self.image.height())
        if self.cnt >= 360:
            self.cnt = 10
        else:
            self.cnt += 10
        # self.transform.rotate(10, Qt.ZAxis)
        self.update()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)  # 抗锯齿
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)  # 像素光滑
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self.cnt)
        painter.translate(-self.width()/2, -self.height()/2)
        # painter.setTransform(self.transform)
        # painter.drawPixmap(0, 0, self.width(), self.height(),
        #                    QPixmap.fromImage(self.image).copy(100,100,100,100))
        painter.drawPixmap(0, 0, QPixmap.fromImage(
            self.image), 100, 100, 100, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Simple()
    w.show()
    sys.exit(app.exec_())
