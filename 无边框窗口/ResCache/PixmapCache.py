# -*- coding: utf-8 -*-

"""
缓存图片文件
"""

from __future__ import unicode_literals

from os.path import isabs, join, isfile

from PyQt5.QtGui import QPixmap, QIcon


class PixmapCache(object):
    """
    Class implementing a pixmap cache for icons.
    """
    def __init__(self):
        """
        Constructor
        """
        self.pixmapCache = {}
        self.searchPath = ['./res/shadow']

    def getPixmap(self, key):
        """
        Public method to retrieve a pixmap.

        @param key name of the wanted pixmap (string)
        @return the requested pixmap (QPixmap)
        """
        if key:
            try:
                return self.pixmapCache[key]
            except KeyError:
                if not isabs(key):
                    for path in self.searchPath:
                        f = join(path, key)
                        if isfile( f ):
                            pm = QPixmap( f )
                            if not pm.isNull():
                                break
                    else:
                        pm = QPixmap()
                else:
                    if isfile( key ):
                        pm = QPixmap(key)
                    else:
                        pm = QPixmap()
                self.pixmapCache[key] = pm
                return self.pixmapCache[key]
        return QPixmap()

    def addSearchPath(self, path):
        """
        Public method to add a path to the search path.

        @param path path to add (string)
        """
        if path not in self.searchPath:
            self.searchPath.append(path)

pixCache = PixmapCache()


def getPixmap(key, cache=pixCache):
    """
    Module function to retrieve a pixmap.

    @param key name of the wanted pixmap (string)
    @param cache reference to the pixmap cache object (PixmapCache)
    @return the requested pixmap (QPixmap)
    """
    return cache.getPixmap(key)


def getIcon(key, cache=pixCache):
    """
    Module function to retrieve an icon.

    @param key name of the wanted icon (string)
    @param cache reference to the pixmap cache object (PixmapCache)
    @return the requested icon (QIcon)
    """
    return QIcon(cache.getPixmap(key))

def addSearchPath(path, cache=pixCache):
    """
    Module function to add a path to the search path.

    @param path path to add (string)
    @param cache reference to the pixmap cache object (PixmapCache)
    """
    cache.addSearchPath(path)
