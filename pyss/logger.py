# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль журналирования

Флаг SHOW_ON_DISPLAY управляет отображением на экране

"""

# pylint: disable=line-too-long

import os
import sys
from xml.etree.ElementInclude import include

# флаг: True - отображать на экране
SHOW_ON_DISPLAY = True

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

DIRNAME = get_script_path()
FILENAME = DIRNAME + "pyss.log"

def reset():
    with open(FILENAME, "wb"):
        pass

def printLine(msg=""):
    with open(FILENAME, "a") as f:
        f.write(msg + "\n")
    if SHOW_ON_DISPLAY:
        display(msg)

def display(msg=""):
    sys.stdout.write(str(msg) + '\n')

def info(msg):
    with open(FILENAME, "a") as f:
        f.write(msg + "\n")
    if SHOW_ON_DISPLAY:
        display(msg)

def warn(msg):
    with open(FILENAME, "a") as f:
        f.write("WARN " + msg + "\n")
    if SHOW_ON_DISPLAY:
        display(msg)

def dump(obj, objName="obj", incl=None, excl=None):
    r = ""
    l = sorted(dir(obj))
    for attr in l:
        if (not attr.startswith("_")) and (incl is None or attr in incl) and ((excl is None or attr not in excl)):
            if r:
                r += "\n"
            r += "%s.%s = %s" % (objName, attr, getattr(obj, attr))
    return r

if __name__ == '__main__':
    def main():
        print "?"

    main()
