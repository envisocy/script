# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:47'

import os

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

# 解析模块设置
### 默认桌面路径(或指定html.txt所在路径)
DESKTOP_DIR = ""
FILENAME = "html.txt"


# ------------------------------
if not DESKTOP_DIR:
	DESKTOP_DIR = GetDesktopPath()