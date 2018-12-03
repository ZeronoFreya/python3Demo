from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QDesktopWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QStyleOption, QStyle
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QFont, QPalette, QBrush

import ResCache.FontCache as FC
import ResCache.PixmapCache as PC

fontCode = {
    'close': '\ue904',
    'max': '\ue902',
    'min': '\ue903',
    'restore': '\ue900',
    'resize': '\ue905',
}

class MyWidget(QWidget):
    '''
    自定义QWidget, 重载paintEvent事件, 否则无法使用样式表定义样式
    '''
    def __init__(self, parent=None):
        super(MyWidget,self).__init__(parent)
        self.setMinimumSize(10,10)


    def setBackground(self, pixmap):
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setBrush(self.backgroundRole(),
            QBrush( pixmap ) )
        self.setPalette(p)

    def paintEvent(self, evt):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        # 反锯齿
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

class WindowStatusButton(QPushButton):
    """
    窗口状态按钮
    """
    def __init__(self, parent=None, *args):
        super(WindowStatusButton, self).__init__(parent, *args)
        self.setObjectName('window_status_button')
        # self.setFont(QFont("Webdings"))
        font = FC.getFont('caption-icon.ttf')
        # font.setPointSize(8)
        self.setFont( font )
        self.setFixedWidth(40)

class WindowStatusBar(MyWidget):
    def __init__(self, parent=None, *args):
        super(WindowStatusBar, self).__init__(parent, *args)
        self.setObjectName('window_status_bar')
        # self.setStyleSheet('background: transparent;')
        self.setFixedSize(0,0)
        self.lay = QHBoxLayout()
        self.lay.setContentsMargins(0,0,0,0)
        self.lay.setSpacing(0)
        # 右上对齐 & 从右向左排列
        self.lay.setDirection(QBoxLayout.RightToLeft)
        self.lay.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.setLayout(self.lay)

    def addWidget(self, w):
        self.lay.addWidget(w)
        # print(self.sizeHint())
        self.setFixedSize(self.minimumSizeHint())

class ResizeHandle(QLabel):
    """
    更改窗口尺寸的手柄(右下角)
    """
    def __init__(self, parent, sw):
        super(ResizeHandle, self).__init__(parent)
        self.setObjectName('resize_handle_right_bottom')
        self.SHADOW_SIZE = sw
        self._Window = parent
        self._resize_drag = False

        font = FC.getFont('caption-icon.ttf')
        font.setPointSize(8)
        self.setFont( font )
        self.setText(fontCode['resize'])
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setFixedSize(18, 18)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        self.setCursor(Qt.SizeFDiagCursor)

    def leaveEvent(self, e):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        self._resize_drag = True
        # 获取窗口的RECT
        rect = self._Window.geometry()
        # 计算窗口右下角坐标与鼠标点击时坐标的差值(相对于屏幕)
        pt = QPoint(rect.x()+rect.width(), rect.y()+rect.height()) - e.globalPos()
        # 此处偏移窗口坐标, 方便计算(相当于重叠鼠标点击坐标与窗口右下角坐标)
        self.resize_DragPosition = QPoint(rect.x(), rect.y()) - pt
        e.accept()

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self._resize_drag:
            point = e.globalPos() - self.resize_DragPosition
            self._Window.resize( point.x(), point.y() )
            e.accept()

    def mouseReleaseEvent(self, e):
        self._resize_drag = False

class UnFrameWindow(QWidget):
    """
    无边框窗口类
    wintype:
        1 - 显示关闭按钮
        2 - 显示最大化按钮
        4 - 显示最小化按钮
        8 - 添加窗口移动功能
        16 - 添加窗口缩放功能
    """
    def __init__(self, wintype=31):
        # 设置为顶级窗口，无边框
        super(UnFrameWindow, self).__init__(None, Qt.FramelessWindowHint)
        self.SHADOW_SIZE = 8
        self._ss = self.SHADOW_SIZE
        # self.setWindowFlags(Qt.FramelessWindowHint) #无边框
        self.setAttribute(Qt.WA_TranslucentBackground,True) #背景透明

        # 添加一个布局
        self.__MainLayout = QVBoxLayout()
        self.__MainLayout.setContentsMargins(
            self._ss, self._ss,
            self._ss, self._ss )
        self.__MainLayout.setSpacing(0)
        self.setLayout(self.__MainLayout)

        # 添加主窗口, 除非需要否则窗口元素都应添加到self.__main
        self.__main = MyWidget()
        self.__MainLayout.addWidget(self.__main)

        self.resizeHandle = False
        self.WindowStatusBar = WindowStatusBar(self)


        self.__closeButton = None
        self.__minButton = None
        self.__maxButton = None

        self.winTypeDict()

        _list = self.analysisWintype( wintype )

        if _list:
            for k in _list:
                self.__winType[str(k)]()

        self.resizeWindow()
        self.setMinimumSize(136, 84)

    def winTypeDict(self):
        self.__winType = {
            '1' : self.setCloseButton,
            '2' : self.setMaxButton,
            '4' : self.setMinButton,
            '8' : self.setMoveHandle,
            '16' : self.setResizeHandle
        }
        self.keyList = []
        for k in self.__winType:
            self.keyList.append(int(k))
        self.keyList.sort(reverse=True)

    def analysisWintype(self, winType:int):
        if winType > self.keyList[0]*2:
            return None
        _sum = 0
        _list = []
        for v in self.keyList:
            if v > winType:
                continue
            _sum += v
            if _sum == winType:
                _list.append(v)
                _list.sort()
                return _list
            elif _sum > winType:
                _sum -= v
            else:
                _list.append(v)
        return None

    def initLayout(self, lay):
        '''
        设置主窗口布局
        '''
        self.__main.__MainLayout = lay
        self.__main.__MainLayout.setContentsMargins(0,0,0,0)
        self.__main.__MainLayout.setSpacing(0)
        self.__main.setLayout(self.__main.__MainLayout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setBackground(self, pixmap):
        self.__main.setBackground( pixmap )

    def setMargin(self,l=0,t=0,r=0,b=0):
        self.__main.__MainLayout.setContentsMargins(l,t,r,b)

    def setSpacing(self,s=0):
        self.__main.__MainLayout.setSpacing(s)

    def setHorizontalSpacing(self,h=0):
        self.__main.__MainLayout.setHorizontalSpacing(h)

    def setVerticalSpacing(self, v=0):
        self.__main.__MainLayout.setVerticalSpacing(v)

    def addWidget(self, w):
        '''
        添加元素到布局
        '''
        self.__main.__MainLayout.addWidget( w )

    def addLayout(self, l, *args):
        '''
        添加布局到布局
        '''
        self.__main.__MainLayout.addLayout(l, *args)

    def addChildren(self, w):
        '''
        不经过布局添加子元素(设置w的父元素为__main)
        '''
        w.setParent(self.__main)

    def drawShadow(self,painter, s):
        x1 = s
        y1 = s
        x2 = self.width()-s
        y2 = self.height()-s

        #左上角
        painter.drawPixmap(0, 0, s, s, QPixmap('./res/shadow/left_top.png'))
        #右上角
        painter.drawPixmap(x2, 0, s, s, QPixmap('./res/shadow/right_top.png'))
        #左下角
        painter.drawPixmap(0, y2, s, s, QPixmap('./res/shadow/left_bottom.png'))
        #右下角
        painter.drawPixmap(x2, y2, s, s, QPixmap('./res/shadow/right_bottom.png'))
        #左
        painter.drawPixmap(0, x1, s, y2-y1, QPixmap('./res/shadow/left_mid.png').scaled(s, y2-y1))
        #右
        painter.drawPixmap(x2, y1, s, y2-y1, QPixmap('./res/shadow/right_mid.png').scaled(s, y2-y1))
        #上
        painter.drawPixmap(x1, 0, x2-x1, s, QPixmap('./res/shadow/top_mid.png').scaled(x2-x1, s))
        #下
        painter.drawPixmap(x1, y2, x2-x1, s, QPixmap('./res/shadow/bottom_mid.png').scaled(x2-x1, s))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        if self._ss > 0:
            self.drawShadow(painter, self._ss)
        painter.drawRect(QRect(self._ss, self._ss, self.width()-2*self._ss, self.height()-2*self._ss))

    def resizeEvent(self, e):
        w = self.width()
        h = self.height()
        self.WindowStatusBar.move(
            w-self.WindowStatusBar.width()-self._ss, self._ss )
        if self.resizeHandle:
            self.rightBottom.move( w-self.rb['w'], h-self.rb['h'] )

    def resizeWindow(self, w=816, h=504):
        self.resize(w,h)
        # 窗口居中
        self.center()


    def setMoveHandle(self, h=None):
        self.MOVEHAND = h or self
        self.MOVEHAND.mousePressEvent = self._mousePress
        self.MOVEHAND.mouseMoveEvent = self._mouseMove
        self.MOVEHAND.mouseReleaseEvent = self._mouseRelease

    def setResizeHandle(self):
        self.resizeHandle = True
        self.rightBottom = ResizeHandle(self, self._ss)
        self.rb = {
            'w': self.rightBottom.width(),
            'h': self.rightBottom.height()
        }

    def setCloseButton(self):
        self.__closeButton = WindowStatusButton()
        # self.__closeButton.setText(b'\xef\x81\xb2'.decode("utf-8"))
        self.__closeButton.setText(fontCode['close'])
        self.__closeButton.setObjectName("CloseButton")
        # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
        self.__closeButton.setMouseTracking(True)
        # 按钮信号连接到关闭窗口的槽函数
        # self.__closeButton.clicked.connect(self.shutdown)
        self.__closeButton.clicked.connect(self.close)
        self.WindowStatusBar.addWidget(self.__closeButton)

    def setMaxButton(self):
        # 最大化|还原
        self.__switchBtn = WindowStatusButton()
        # self.__switchBtn.setText(b'\xef\x80\xb1'.decode("utf-8"))
        self.__switchBtn.setText(fontCode['max'])
        self.__switchBtn.setObjectName("SwitchBtn")
        self.__switchBtn.setMouseTracking(True)
        self.__switchBtn.clicked.connect(self._showMaximized)
        self.WindowStatusBar.addWidget(self.__switchBtn)
        # 还原
        # self._RestoreBn = WindowStatusButton('\ue904')
        # self._RestoreBn.setObjectName("RestoreBn")
        # self._RestoreBn.setMouseTracking(True)
        # self._RestoreBn.setVisible(False)
        # self.WindowStatusBar.addWidget(self._RestoreBn)

    def setMinButton(self):
        # 最小化
        self.__minButton = WindowStatusButton()
        # self.__minButton.setText(b'\xef\x80\xb0'.decode("utf-8"))
        self.__minButton.setText(fontCode['min'])
        self.__minButton.setObjectName("MinButton")
        self.__minButton.setMouseTracking(True)
        self.__minButton.clicked.connect(self.showMinimized)
        self.WindowStatusBar.addWidget(self.__minButton)

    def _showMaximized(self):
        '''
        最大化窗口
        '''
        try:
            self._ss = 0
            self.rightBottom.setVisible(False)
            self.__MainLayout.setContentsMargins(0,0,0,0)

            self.showMaximized() # 先实现窗口最大化
            # self.__switchBtn.setText(b'\xef\x80\xb2'.decode("utf-8"))
            self.__switchBtn.setText(fontCode['restore']) # 更改按钮文本
            # self.__switchBtn.setToolTip("恢复") # 更改按钮提示
            self.__switchBtn.disconnect() # 断开原本的信号槽连接
            self.__switchBtn.clicked.connect(self._showNormal) # 重新连接信号和槽
        except:
            pass


    def _showNormal(self):
        '''
        还原窗口
        '''
        try:
            self._ss = self.SHADOW_SIZE
            self.rightBottom.setVisible(True)
            self.__MainLayout.setContentsMargins(self._ss,self._ss,
                self._ss,self._ss)

            self.showNormal()
            # self.__switchBtn.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self.__switchBtn.setText(fontCode['max'])
            # self.__switchBtn.setToolTip("最大化")
            self.__switchBtn.disconnect()
            self.__switchBtn.clicked.connect(self._showMaximized)
        except:
            pass

    # ------------------ 窗体拖动 ------------------

    def _mousePress(self,e):
        try:
            if self._ss and e.buttons() == Qt.LeftButton:
                # self.setCursor(Qt.ArrowCursor)
                self._move_drag = True
                self.move_DragPosition = e.globalPos() - self.pos()
                e.accept()
        except Exception as e:
            pass

    def _mouseMove(self,e):
        try:
            if self._ss and e.buttons() == Qt.LeftButton and self._move_drag:
                self.move(e.globalPos() - self.move_DragPosition)
                e.accept()
        except Exception as e:
            pass

    def _mouseRelease(self,e):
        try:
            self._move_drag = False
            self.move_DragPosition = None
            e.accept()
        except Exception as e:
            pass
