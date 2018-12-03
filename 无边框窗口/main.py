# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from MyGui import MyGui
import ResCache.FontCache as FC

def main():
    import sys
    app = QApplication(sys.argv)

    font = FC.getFont('Exo2Light.ttf')
    font.setPointSize(14)

    app.setFont(font)
    app.setStyleSheet(open('./res/style/default/style.css').read())

    window = MyGui()
    window.show();
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
