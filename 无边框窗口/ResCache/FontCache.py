# -*- coding: utf-8 -*-

"""
缓存自定义字体文件
"""

from __future__ import unicode_literals

from os.path import isabs, join, isfile

from PyQt5.QtGui import QFont, QFontDatabase

class FontCache(object):
    """
    Class implementing a pixmap cache for icons.
    """
    def __init__(self):
        """
        Constructor
        """
        self.fontCache = {}
        self.searchPath = ['./res/font']

    def getFont(self, key):
        """
        Public method to retrieve a pixmap.

        @param key name of the wanted pixmap (string)
        @return the requested pixmap (QPixmap)
        """
        if key:
            try:
                return self.fontCache[key]
            except KeyError:
                if not isabs(key):
                    for path in self.searchPath:
                        f = join(path, key)
                        if isfile( f ):
                            fontId = QFontDatabase.addApplicationFont( f )
                            if not fontId == -1:
                                msyh = QFontDatabase.applicationFontFamilies(fontId)[0]
                                font = QFont(msyh)
                                break
                    else:
                        font = QFont()
                        font.setFamily("黑体")
                else:
                    if isfile( key ):
                        fontId = QFontDatabase.addApplicationFont( key )
                        if not fontId == -1:
                            msyh = QFontDatabase.applicationFontFamilies(fontId)[0]
                            font = QFont(msyh)
                    else:
                        font = QFont()
                        font.setFamily("黑体")
                self.fontCache[key] = font
                return self.fontCache[key]
        return QFont()

    def addSearchPath(self, path):
        """
        Public method to add a path to the search path.

        @param path path to add (string)
        """
        if path not in self.searchPath:
            self.searchPath.append(path)

fontCache = FontCache()

def getFont(key, cache=fontCache):
    """
    Module function to retrieve a pixmap.

    @param key name of the wanted pixmap (string)
    @param cache reference to the pixmap cache object (PixmapCache)
    @return the requested pixmap (QPixmap)
    """
    return cache.getFont(key)

def addSearchPath(path, cache=fontCache):
    """
    Module function to add a path to the search path.

    @param path path to add (string)
    @param cache reference to the pixmap cache object (PixmapCache)
    """
    cache.addSearchPath(path)
