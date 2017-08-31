##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль настроек модели
"""

# pylint: disable=bad-whitespace, missing-docstring

class Options(object):
    """Настройки модели
    
    self.printSegmentLabel = True - печать меток сегментов в трасе времени (если метка определена)
    
    """
    
    def __init__(self):
        self.logTransactGenerate=True
        self.logTransactMoveFromFelToCel=True
        self.logTransactTrace=True
        self.logCel=True
        self.logFel=True
        self.logTransactTrack=False
        #self.logDelaiedList=True
        self.reportTransactFamilies=True
        self.reportCel=True
        self.printEventList = False
        self.printStat = True
        self.printSegmentLabel = True
        self.printResult=True
        #self.printOptions=True
        
    def setAll(self,value):
        self.logTransactGenerate=value
        self.logTransactMoveFromFelToCel=value
        self.logTransactTrace=value
        self.logCel=value
        self.logFel=value
        self.logTransactTrack=value
        self.reportTransactFamilies=value
        self.reportCel=value
        self.printEventList = value
        self.printStat = value
        self.printSegmentLabel = value
        self.printResult=value
        #self.printOptions=value
        
    def setAllFalse(self):
        self.setAll(False)

    def setAllTrue(self):
        self.setAll(True)

if __name__ == '__main__':
    def main():
        print "?"

    main()
