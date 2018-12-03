from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys


class Test(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.file_list = QListWidget()
        self.btn = QPushButton('Start')
        layout = QGridLayout(self)
        layout.addWidget(self.file_list,0,0,1,2)
        layout.addWidget(self.btn,1,1)
        
        self.thread = Worker()
        self.thread.file_changed_signal.connect(self.update_file_list)
        self.btn.clicked.connect(self.thread_start)
        
    def update_file_list(self, file_inf):
        self.file_list.addItem(file_inf)
        
    def thread_start(self):
        self.btn.setEnabled(False)
        self.thread.start()
        
        
        
class Worker(QThread):
    
    file_changed_signal = pyqtSignal(str) # 信号类型：str
    
    def __init__(self, sec=0, parent=None):
        super().__init__(parent)
        self.working = True
        self.sec = sec
        
    def __del__(self):
        self.working = False
        self.wait()
        
    def run(self):
        while self.working == True:
            self.file_changed_signal.emit('当前秒数：{}'.format(self.sec))
            self.sleep(1)
            self.sec += 1
            
app = QApplication(sys.argv)
dlg = Test()
dlg.show()
sys.exit(app.exec_())