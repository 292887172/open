# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil 
root = "/home/rdy/git-workspace/open"

for dirpath, dirnames, filenames in os.walk(root):
    for filepath in filenames:
        if '__' in dirpath:
            print(dirpath)