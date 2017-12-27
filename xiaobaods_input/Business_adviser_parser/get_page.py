#!usr/bin/env python
# -*- coding: utf-8 -*-


from xiaobaods_input.Business_adviser_parser.config import *
import re


def from_desktop_text(filename='html.txt'):
    '''
    :param html # type(str)
    :return: html # type(list)
    '''
    import sys
    try:
        with open(DESKTOP + '/' + filename, 'r', encoding="gb18030") as f:
            html = f.read()
    except:
        with open(DESKTOP + '/' + filename, 'r', encoding="utf8") as f:
            html = f.read()
    pattern = re.compile('(<html.*?</html>)', re.S)
    htmls = re.findall(pattern, html)
    return htmls
