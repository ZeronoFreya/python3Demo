# -*- coding: utf-8 -*-

from os.path import realpath, dirname
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QFileInfo, pyqtSignal

from PyQt5.QtGui import QPalette, QPixmap, QBrush, QColor, QPen, QImage
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QRect, QPoint
# from Globals import Cfg


class ScreenshotStatus:
    init = 0
    dragging = 1
    ok = 2
    move = 3
    resize = 4
    resize_tl = 5
    resize_tr = 6
    resize_bl = 7
    resize_br = 8
    


class ToolBox(QWidget):

    sg_close = pyqtSignal()

    def __init__(self, mainWindow, parent=None):
        super(ToolBox, self).__init__(parent)

        self.mainWindow = mainWindow

        self.setGeometry(0, 0, 200, 60)
        self.setVisible(False)
        

        self.btn_save = QPushButton('Save', self)
        self.btn_cancel = QPushButton('Cancel', self)

        self.btn_cancel.clicked.connect(self.sg_close.emit)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        # lay.addStretch()
        lay.addWidget(self.btn_save)
        lay.addWidget(self.btn_cancel)

        self.sg_close.connect(mainWindow.closeApp)


class Snipaste(QWidget):

    sg_close = pyqtSignal()

    def __init__(self, parent=None):
        super(Snipaste, self).__init__(parent)
        self.start = (0, 0)  # 开始坐标点
        self.end = (0, 0)  # 结束坐标点

        self.mouse = (0, 0)

        self.mainWindow = parent

        self.status = ScreenshotStatus.init
        self.resize = None

        self.setCursor(Qt.CrossCursor)

        self.originalPixmap = self.mainWindow.originalPixmap
        self.setGeometry(0, 0, self.originalPixmap.width(),
                         self.originalPixmap.height())

        self.toolbox = ToolBox(self.mainWindow, self)

        self.sg_close.connect(self.mainWindow.closeApp)

    def paintEvent(self, event):
        if (self.status == ScreenshotStatus.dragging or
            self.status == ScreenshotStatus.ok or
            self.status == ScreenshotStatus.move or
            self.status == ScreenshotStatus.resize):
            qp = QPainter()
            qp.begin(self)
            self.drawCutRect(qp)
            # qp.drawRect(x, y, w, h)
            qp.end()

    def drawCutRect(self, qp):
        x = min(self.start[0], self.end[0])
        y = min(self.start[1], self.end[1])
        w = abs(self.end[0] - self.start[0])
        h = abs(self.end[1] - self.start[1])
        # pen = QPen(Qt.red, 1, Qt.DashLine)
        if w == 0 or h == 0:
            return
        pen = QPen(QColor(32, 128, 240), 3, Qt.SolidLine)
        qp.setPen(pen)
        # r = QRect(QPoint(self.start[0], self.start[1]),
        #           QPoint(self.end[0], self.end[1]))
        qp.drawPixmap(x, y, self.originalPixmap, x, y, w, h)
        qp.drawRect(x, y, w, h)
        pen = QPen(Qt.white, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QColor(32, 128, 240))
        # 左上
        qp.drawEllipse(self.start[0]-4, self.start[1]-4, 7, 7)
        # 右上
        qp.drawEllipse(self.end[0]-3, self.start[1]-4, 7, 7)
        # 右下
        qp.drawEllipse(self.end[0]-3, self.end[1]-3, 7, 7)
        # 左下
        qp.drawEllipse(self.start[0]-4, self.end[1]-3, 7, 7)

    def mousePressEvent(self, event):

        # 点击左键开始选取截图区域
        if event.button() == Qt.LeftButton:
            self.toolbox.setVisible(False)
            if self.status == ScreenshotStatus.init:
                self.start = (event.pos().x(), event.pos().y())
                self.status = ScreenshotStatus.dragging
            elif self.status == ScreenshotStatus.ok:
                offset = 10
                x0 = min(self.start[0], self.end[0]) + offset
                y0 = min(self.start[1], self.end[1]) + offset
                x1 = max(self.start[0], self.end[0]) - offset
                y1 = max(self.start[1], self.end[1]) - offset
                posx = event.pos().x()
                posy = event.pos().y()
                if posx < x0 and posy < y0:
                    self.status = ScreenshotStatus.resize
                    self.resize = ScreenshotStatus.resize_tl
                    self.start = (posx, posy)
                    self.update()
                elif posx > x1 and posy < y0:
                    self.status = ScreenshotStatus.resize
                    self.resize = ScreenshotStatus.resize_tr
                    self.start = (self.start[0], posy)
                    self.end = (posx, self.end[1])
                    self.update()
                elif posx > x1 and posy > y1:
                    self.status = ScreenshotStatus.resize
                    self.resize = ScreenshotStatus.resize_br
                    self.end = (posx, posy)
                    self.update()
                elif posx < x0 and posy > y1:
                    self.status = ScreenshotStatus.resize
                    self.resize = ScreenshotStatus.resize_bl
                    self.start = (posx, self.start[1])
                    self.end = (self.end[0], posy )
                    self.update()
                elif (posx > x0 and posx < x1 and
                        posy > y0 and posy < y1):
                    self.status = ScreenshotStatus.move
                    self.mouse = (event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            x = max(self.start[0], self.end[0])
            y = max(self.start[1], self.end[1])
            self.toolbox.move(x-self.toolbox.width(), y)
            self.toolbox.setVisible(True)
            if self.status == ScreenshotStatus.dragging:
                self.status = ScreenshotStatus.ok
                self.end = (event.pos().x(), event.pos().y())
            elif self.status == ScreenshotStatus.move:
                self.status = ScreenshotStatus.ok
            self.status = ScreenshotStatus.ok
            # 进行重新绘制
            self.update()
        elif event.button() == Qt.RightButton:
            if self.status == ScreenshotStatus.ok:
                self.status = ScreenshotStatus.init
                self.start = (0, 0)
                self.end = (0, 0)
                self.toolbox.setVisible(False)
                self.update()
            elif self.status == ScreenshotStatus.init:
                # self.mainWindow.close()
                self.sg_close.emit()

    def mouseMoveEvent(self, event):
        offset = 10
        x0 = min(self.start[0], self.end[0]) + offset
        y0 = min(self.start[1], self.end[1]) + offset
        x1 = max(self.start[0], self.end[0]) - offset
        y1 = max(self.start[1], self.end[1]) - offset
        posx = event.pos().x()
        posy = event.pos().y()
        if self.status == ScreenshotStatus.dragging:
            self.end = (event.pos().x(), event.pos().y())
            # 进行重新绘制
            self.update()
        elif self.status == ScreenshotStatus.move:
            offsetX = event.pos().x() - self.mouse[0]
            offsetY = event.pos().y() - self.mouse[1]
            self.mouse = (event.pos().x(), event.pos().y())
            w = self.width()
            h = self.height()
            x0 = self.start[0]+offsetX
            y0 = self.start[1]+offsetY
            x1 = self.end[0]+offsetX
            y1 = self.end[1]+offsetY
            # x0 = x0 if x0 >= 0 else 0
            if x0 < 0:
                x1 = x1 - x0
                x0 = 0
            elif x1 > w:
                x0 = x0 - x1 + w
                x1 = w
            if y0 < 0:
                y1 = y1 - y0
                y0 = 0
            elif y1 > h:
                y0 = y0 - y1 + h
                y1 = h
            self.start = (x0, y0)
            self.end = (x1, y1)
            self.update()
        elif self.status == ScreenshotStatus.resize:
            if self.resize == ScreenshotStatus.resize_tl:
                self.start = (event.pos().x(), event.pos().y())
            elif self.resize == ScreenshotStatus.resize_tr:
                self.start = (self.start[0], event.pos().y())
                self.end = (event.pos().x(), self.end[1])
            elif self.resize == ScreenshotStatus.resize_br:
                self.end = (event.pos().x(), event.pos().y())
            elif self.resize == ScreenshotStatus.resize_bl:
                self.start = (event.pos().x(), self.start[1])
                self.end = (self.end[0], event.pos().y())
            self.update()


class ScreenShotsWin(QMainWindow):

    def __init__(self):
        super(ScreenShotsWin, self).__init__()
        self.originalPixmap = None
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen()
        if screen is not None:
            self.originalPixmap = screen.grabWindow(0)
        else:
            self.originalPixmap = QPixmap()

        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QBrush(self.originalPixmap))
        self.setPalette(window_pale)

        mask = QWidget(self)
        black = QColor(0, 0, 0)
        black.setAlphaF(0.4)
        mask_pale = QPalette()
        mask_pale.setBrush(mask.backgroundRole(), black)
        mask.setPalette(mask_pale)
        mask.setAutoFillBackground(True)
        mask.setGeometry(0, 0, self.originalPixmap.width(),
                         self.originalPixmap.height())

        self.snipaste = Snipaste(self)

        # self.toolbox = QWidget(self)
        # self.toolbox.setVisible(False)
        # self.toolbox.setGeometry(0,0,200,60)
        # self.toolbox.setContentsMargins(0,0,0,0)
        # toolboxLay = QHBoxLayout(self.toolbox)

        # # self.showFullScreen()
        # # self.setWindowOpacity(0.4)
        # self.btn_ok = QPushButton('上传', self)
        # self.btn_ok.clicked.connect(
        #     lambda: self.screenshots(self.start, self.end))
        # # self.oksignal.connect(lambda: self.screenshots(self.start, self.end))
        # self.btn_cancer = QPushButton('取消', self)
        # self.btn_cancer.clicked.connect(self.close)
        # toolboxLay.addWidget(self.btn_ok)
        # toolboxLay.addWidget(self.btn_cancer)

    def screenshots(self, start, end):
        '''
        截图功能
        :param start:截图开始点
        :param end:截图结束点
        :return:
        '''

        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])

        pix = self.originalPixmap.copy(
            QRect(x, y, width, height))

        fileName = QFileDialog.getSaveFileName(self, '保存图片', '.', ".png;;.jpg")

        if fileName:
            pix.save(fileName)
        self.close()

    def closeApp(self):
        self.close()
