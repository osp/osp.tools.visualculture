import bobo

import sys
import os

sys.dont_write_bytecode = True
rootpath = os.path.dirname(__file__)
dirs = ['', 'visualculture']

for d in dirs:
    path = rootpath + d
    if path not in sys.path:
        sys.path.append(path)
        

application = bobo.Application(bobo_resources="visualculture.routes")