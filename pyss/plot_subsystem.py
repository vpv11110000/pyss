# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль подсистемы формирования и отображения графических диаграмм
"""

# pylint: disable=line-too-long

import matplotlib.pyplot as plt

from pyss.pyss_const import *
from pyss import plot_table
from pyss import plot_transact_lifeline
from pyss.pyssobject import ErrorPlotExists


class PlotSubsystem(object):
    """Подсистема формирования и отображения графических диаграмм
    
Methods:    
    append - добавление объекта формирования диаграммы 
             (см. plot_table, plot_transact_lifeline)
    
    """
    
    def __init__(self):
        self.diaModules = []
        
    def getPlt(self):
        return plt

    def append(self, diaModule):
        """Добавление модуля формирования конкретной диаграммы
        
        Args:
              diaModule - объект формирования диаграммы 
             (см. plot_table, plot_transact_lifeline)
        """
#         if diaModule in self.diaModules:
#             raise ErrorPlotExists("diaModule in self.diaModules") 
        self.diaModules.append(diaModule)
        
    def plotByModules(self):
        figCount = 0
        for d in self.diaModules:
            figCount += 1
            figure = plt.figure(figCount)            
            d.plotOnFigure(figure)
            
    def appendPlotTable(self, table=None, title=None):
        p = plot_table.PlotTable(table, title)
        self.append(p)
        return p

    def appendPlotTransactLifeLine(self, terminateBlock=None, transactFilter=None, title=None):
        """Добавляет диаграмму для отображения линий жизни транзактов для блока terminateBlock.
        
        Возвращает объект PlotTransactLifeLine 
        
        Args:
            terminateBlock=None - объект блока Terminate 
            transactFilter=None - фильтр транзактов
            title=None - название диаграммы
        
        """
        p = plot_transact_lifeline.PlotTransactLifeLine(terminateBlock=terminateBlock, transactFilter=transactFilter, title=title)
        terminateBlock[ON_DELETED]=p.append
        self.append(p)        
        return p
    
    def show(self):
        plt.show()
        
    def plotByModulesAndSave(self, filename):
        self.plotByModules()
        
        # [<matplotlib.figure.Figure object at 0xb788ac6c>, <matplotlib.figure.Figure object at 0xa143d0c>]
        

        for i in plt.get_fignums():
            fig = plt.figure(i)
            #21x19
            fig.set_size_inches(8.26, 7.48)
            plt.savefig("%s_%3d"%(filename, i))
            plt.close(i)    # close the figure

if __name__ == '__main__':
    def main():
        print "?"

    main()
