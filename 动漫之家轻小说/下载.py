#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request, os
from chinese_digits import chineseToDigits
dicts = [
    {
        "url": "http://xs.dmzj.com/1728/6346/6346_GBK.txt",
        "title": "异世界狂想曲",
        "subtitle": "第一卷"
    }
]
saveTo = 'r:/'
for f in dicts:
    # data = urllib.request.urlopen(f['url']).read()
    subtitle = f['subtitle'].split(' ',1)
    name = '{title}( {number} )[{subtitle}].txt'.format(
        title = f['title'],
        number = chineseToDigits(subtitle[0], 2, 0),
        subtitle = subtitle[1]
    )
    print(subtitle[0], name)
    # with open(os.path.join(saveTo, name), "wb") as txt:
    #     txt.write(data)
