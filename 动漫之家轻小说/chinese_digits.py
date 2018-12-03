#!/usr/bin/env python
# -*- coding: utf-8 -*-

def chineseToDigits(chinese_str, fill_in, placeholder=0):
    t = chinese_str
    if t is None or t.strip() == "":
        raise Exception("input error for %s" % chinese_str)
    t = t.strip()
    t = t.replace("百十", "百一十")
    common_used_numerals = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
    t2 = ''
    keys = common_used_numerals.keys()
    for i in range(len(t) - 1):
        if t[i] in keys:
            t2 = ''.join((t2, t[i]))
    t = t2
    total = 0
    r = 1
    for i in range(len(t) - 1, -1, -1):
        val = common_used_numerals.get(t[i])
        if val >= 10 and i == 0:
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    # fill_in = '%{0}{1}d'.format(placeholder, fill_in) % total
    return '%{0}{1}d'.format(placeholder, fill_in) % total
