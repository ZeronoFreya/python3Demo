# -*- coding: utf-8 -*-

"""
主窗口
"""

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import  QVBoxLayout, QLabel
from .UnFrameWindow import UnFrameWindow


class MyGui(UnFrameWindow):
    def __init__(self, parent=None):
        super(MyGui, self).__init__(31)
        self.setObjectName('myGui')
        self.initLayout( QVBoxLayout() )
        self.animation = None

        self._label = QLabel('2333')
        self._label.setStyleSheet("background-color:red;")
        self.addChildren(self._label)
        self._label.setFixedSize(100, 100)
        self._label.move(0,0)

    def closeEvent(self, event):
        if self.animation is None:
            self.animation = QPropertyAnimation(self, b'windowOpacity')
            self.animation.setDuration(300)
            self.animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation.setStartValue(self.windowOpacity())
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.close)
            self.animation.start()
            event.ignore()
