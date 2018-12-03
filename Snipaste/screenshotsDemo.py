# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from screenshots import ScreenShotsWin
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenshot = ScreenShotsWin()
    screenshot.showFullScreen()
    sys.exit(app.exec_())
