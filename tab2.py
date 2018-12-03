import sys
from qtpy.QtWidgets import QTabWidget, QWidget, QToolButton, QTabBar, QApplication

class Trace_Tabs(QTabWidget):

    def __init__(self):
        QTabWidget.__init__(self)
        self.setTabsClosable(True)
        self._build_tabs()

    def _build_tabs(self):

        self.insertTab(0, QWidget(), "Trace 0" )

        # create the "new tab" tab with button
        self.insertTab(1, QWidget(),'')
        nb = self.new_btn = QToolButton()
        nb.setText('+') # you could set an icon instead of text
        nb.setAutoRaise(True)
        nb.clicked.connect(self.new_tab)
        self.tabBar().setTabButton(1, QTabBar.RightSide, nb)

    def new_tab(self):
        index = self.count() - 1
        self.insertTab(index, QWidget(), "Trace %d" % index)
        self.setCurrentIndex(index)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    tabs = Trace_Tabs()
    tabs.show()

    app.exec_()
