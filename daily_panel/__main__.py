#!usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import daily_panel.view as view

try:
    argv = sys.argv[1]
except:
    argv = 0

panel = view.dashboard(argv)
panel.run()
