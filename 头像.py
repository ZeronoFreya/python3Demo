# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

class Avatar(QLabel):
    def __init__(self, *args):
        super(Avatar, self).__init__(*args)

        self.w = 60
        self.h = 60
        self.setFixedSize(self.w, self.h)
        self.radius = 30

        self._avatar = QPixmap(self.size())
        # 填充背景为透明
        self._avatar.fill(Qt.transparent)

        p = QPixmap("avatar.png").scaled(
            self.w, self.h, Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation)
        self.setAvatar(p)

    def setAvatar(self, pixmap):
        painter = QPainter(self._avatar)
        # 抗锯齿
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 绘制边框
        painter.setPen(
            QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)
        # 切割为圆形
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.drawPath(path)



        self.setPixmap(self._avatar)

class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(Avatar(self))
        self.setStyleSheet("background: gold;")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
