# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для линий жизни транзактов
"""

# pylint: disable=line-too-long

import matplotlib.pyplot as plt

from pyss.pyss_const import *
from pyss import statisticalseries 
from pyss import pyssobject
from pyss.pyssownerobject import PyssOwnerObject

class PlotTransactLifeLine(PyssOwnerObject):
    """Формирование графической диаграммы для линий жизни транзактов
    
Args:
    terminateBlock=None - блок или список блоков Terminate, транзакты которого учитываются при формировании диаграммы
    transactFilter - True или функция-фильтр транзактов. Обработке подвергается транзакт, 
                     если функция фильтр вернула True.
                     Если transactFilter равен None, то построение диаграммы не производится.
    title - заголовок диаграммы
    funcAnnotate - функция аннторирования линии жизни транзакта. 
                   По умолчанию: lambda transact:str(transact[NUM])
     
Пример см. test_assemble.py

    """
    
    def __init__(self, ownerModel=None, terminateBlock=None, transactFilter=None, title=None, funcAnnotate=None):
        super(PlotTransactLifeLine, self).__init__(PLOT_MODULE, label=None, owner=ownerModel)
        self.transactFilter = transactFilter
        self.listTransact = []
        self.attr = {}
        self.attr[TERMINATE_BLOCK] = terminateBlock        
        self.attr[TITLE] = title
        if funcAnnotate is None:
            self.attr[FUNC_ANNOTATE] = lambda transact:str(transact[NUM])   
        else:     
            self.attr[FUNC_ANNOTATE] = funcAnnotate
        ownerModel.addPlot(self)
        
    def setTransactFilter(self, transactFilter=None):
        self.transactFilter = transactFilter
        return self

    def append(self, transact):
        if self.transactFilter is None:
            return
        if self.transactFilter is True or self.transactFilter(transact):
            self.listTransact.append(transact)

    def plot(self):
        for transact in self.listTransact:
            c = 0
            t = [transact[TIME_CREATED], transact[TERMINATED_TIME]]
            a = [transact[NUM], transact[NUM]]
            plt.plot(t, a, color="r")  # plotting t,a separately   
        if self.attr[TITLE]:
            plt.title(self.attr[TITLE])
        plt.show()
        
    def convertToLifeLine(self, transact):
        # список пар "start","state"
        r = []
        if transact[LIFE_TIME_LIST]:
            m = ACTIVED
            if len(transact[LIFE_TIME_LIST])>1:
                for i in xrange(len(transact[LIFE_TIME_LIST]) - 1):
                    current_item = transact[LIFE_TIME_LIST][i][START]
                    next_item = transact[LIFE_TIME_LIST][i + 1][START]
                    r.append([current_item, next_item, transact[LIFE_TIME_LIST][i][STATE]])
            else:
                current_item = transact[LIFE_TIME_LIST][0][START]
                r.append([current_item, None, transact[LIFE_TIME_LIST][0][STATE]])
            if transact[LIFE_TIME_LIST][-1][STATE] != TRANSACT_DELETED:
                transact[LIFE_TIME_LIST][-1][END]=self.getOwner().getCurTime()
                r.append([self.getOwner().getCurTime(),self.getOwner().getCurTime(),TRANSACT_DELETED])
        else:
            r.append([transact[TIME_CREATED], transact[TERMINATED_TIME], ACTIVED])
        return r
            

    def plotOnFigure(self, figure, funcAnnotate=None):
        subplot = figure.add_subplot(1, 1, 1)
        index = 1
        for transact in self.listTransact:
            c = 0
            subplot.axvline(x=transact[TIME_CREATED], dashes=[1, 1], color='#ddeedd')
            subplot.axvline(x=transact[TERMINATED_TIME], dashes=[1, 1], color='#eedddd')
                #plt.text(xx,index,str(xx),rotation=90)
            subplot.annotate(self.attr[FUNC_ANNOTATE](transact),
                             xy=(transact[TIME_CREATED], index),
                             xycoords='data',
                             xytext=(0, 2),
                             textcoords='offset points',)
            tt = self.convertToLifeLine(transact)
            for t in tt:
                # t = [transact[TIME_CREATED], transact[TERMINATED_TIME]]
                x = [t[0], t[1]]
                a = [index, index]
                if t[2] == ACTIVED:
                    subplot.plot(x, a, marker='.', color="g", linewidth=3)  # plotting t,a separately
                elif t[2] == PREEMPTED:
                    subplot.plot(x, a, marker='.', color="r", linewidth=1, dashes=[1, 1])  # plotting t,a separately
                elif t[2] == DELAYED:
                    subplot.plot(x, a, marker='.', color="#444444", linewidth=1, dashes=[1, 1])  # plotting t,a separately
                else:
                    subplot.plot(x, a, marker='.', color="#553333", linewidth=1)  # plotting t,a separately
            index += 1   
        if self.attr[TITLE]:
            subplot.title.set_text(self.attr[TITLE])            

if __name__ == '__main__':
    def main():
        print "?"

    main()
