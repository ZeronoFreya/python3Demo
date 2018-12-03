from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time
import sys

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def work(self): # A slot takes no params
        for i in range(1, 100):
            time.sleep(1)
            self.intReady.emit(i)

        self.finished.emit()
        

class Form(QWidget):
    def __init__(self):
       super().__init__()
       self.label = QLabel("0")

       # 1 - create Worker and Thread inside the Form
       self.worker = Worker()  # no parent!
       self.thread = QThread()  # no parent!

       self.worker.intReady.connect(self.updateLabel)
       self.worker.moveToThread(self.thread)
       self.worker.finished.connect(self.thread.quit)
       self.thread.started.connect(self.worker.work)
       #self.thread.finished.connect(app.exit)

       self.thread.start()

       self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.label,0,0)

        self.move(300, 150)
        self.setWindowTitle('thread test')

    def updateLabel(self, i):
        self.label.setText("{}".format(i))
        #print(i)

        
app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())