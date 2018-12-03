import sys
from PyQt5.QtCore import Qt, pyqtSlot,pyqtSignal, QPropertyAnimation, QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QPushButton

class PoputDialog(QWidget):

    def __init__(self, mainWindow=None):
        super(PoputDialog, self).__init__(None, Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.SHADOW_WIDTH = 0
        self.__mw = mainWindow
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('ToolTips')
        self.setStyleSheet('background:gold;')
        # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)

        self.btn = QPushButton(self)
        self.btn.setText('调用父窗口方法')
        self.btn.clicked.connect(self.__test)

        self.desktop=QDesktopWidget().availableGeometry()
        self.move(
            (self.desktop.width()),
            self.desktop.height()-self.height()) #初始化位置到右下角
        self.showAnimation()

        self.show()

    def enterEvent(self, e):
        print(0)
        #清除Timer和信号槽
        self.remainTimer.stop()
        self.remainTimer.deleteLater()
        self.remainTimer=None

    def leaveEvent(self, e):
        print(1)
        self.__delay()

    def __test(self):
        self.__mw.do()

    #弹出动画
    def showAnimation(self):
        #显示弹出框动画
        self.animation=QPropertyAnimation(self, b'pos')
        self.animation.setDuration(1000)
        self.animation.setStartValue(QPoint(self.x(),self.y()))
        self.animation.setEndValue(
            QPoint( (self.desktop.width()-self.width()-self.SHADOW_WIDTH),
                (self.desktop.height()-self.height())))
        self.animation.start()


        self.animation.finished.connect(self.__delay)



    def __delay(self):
        self.remainTimer = QTimer(self) #初始化一个定时器
        self.remainTimer.timeout.connect(self.closeAnimation) #计时结束调用operate()方法
        self.remainTimer.start(3000) #设置计时间隔并启动

    def closeAnimation(self):
        #清除Timer和信号槽
        self.remainTimer.stop()
        # self.disconnect(self.remainTimer,pyqtSignal("timeout()"),self,pyqtSlot("closeAnimation()"))
        self.remainTimer.deleteLater()
        self.remainTimer=None
        #弹出框渐隐
        self.animation =QPropertyAnimation(self,b'windowOpacity')
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        #动画完成后清理
        self.animation.finished.connect(self.clearAll)
        self.animation.start()


    #清理及退出
    def clearAll(self):
        # self.disconnect(self.animation,pyqtSignal("finished()"),self,pyqtSlot("clearAll()"))
        sys.exit()    #退出

    # def closeEvent(self, event):   #1
    #     reply = QMessageBox.question(self, 'Message',
    #                                  'Are you sure to quit?', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.SHADOW_WIDTH = 0
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('ToolTips')

        self.button = QPushButton(self)
        self.button.setText(self.tr('显示弹窗'))
        self.button.clicked.connect(self.showPoput)

        self.show()

    def do(self):
        print('子窗口调用')

    def showPoput(self):
        dlg = PoputDialog(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
