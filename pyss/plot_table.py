# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для сомпонентов Table, QTable
"""

# pylint: disable=line-too-long

import matplotlib.pyplot as plt

from pyss.pyss_const import *
from pyss import statisticalseries
from pyss.pyssownerobject import PyssOwnerObject

# Вывод графической диаграммы для сомпонента Table

class PlotTable(PyssOwnerObject):
    """Формирование графической диаграммы по данным из таблиц Table, QTable
    
Args:
    ownerModel=None - объект модели-владельца 
    table=None - таблица
    title - заголовок диаграммы
                       
Пример см. test_enter_leave.py, test_preempt_return.py, test_queue.py, test_seize.py

    """
    
    def __init__(self, ownerModel=None, table=None, title=None):
        super(PlotTable, self).__init__(SEGMENT, label=None, owner=ownerModel)

        # pylint: disable=too-many-arguments
                  
        self.tables = []
        if table:
            self.tables.append(tuple([table, title]))
        ownerModel.addPlot(self)

    def append(self, table, title=None):
        num = len(self.tables) + 1
        if title:
            self.tables.append(tuple([table, "Table %d. " % num + title]))
        elif TITLE in table:
            self.tables.append(tuple([table, "Table %d. " % num + table[TITLE]]))
        else:
            self.tables.append(tuple([table, "Table %d" % num]))

    def extend(self, tables):
        for t in tables:
            self.append(t, None)

    def plotOn(self, subplot, table):
        ss = statisticalseries.StatisticalSeries()

        x = []
        y = []
        for z in table[LIST]:
            x.append(z)
            zz = table[INTERVALS][z]
            y.append(zz)
            ss.append(zz, 1)
        # subplot.plot((x[0], x[-1]), (ss.mean(), ss.mean()), 'k--')
        m = ss.mean()
        subplot.axhline(y=ss.mean(), dashes=[3, 1], color='#880000')
        subplot.annotate("Mean: %.3f" % (m),
                         xy=(x[0], m),
                         xycoords='data',
                         xytext=(0, 2),
                         textcoords='offset points',)
        for xx, yy in zip(x, y):
            subplot.axhline(y=yy, dashes=[1, 1], color='#dddddd')
            if yy > 0.001:
                subplot.annotate("%.3f\n%.3f" % (xx, yy),
                                 xy=(xx, yy),
                                 xycoords='data',
                                 xytext=(-2, 2),
                                 textcoords='offset points',)
        for xx, yy in zip(x, y):
            subplot.bar(xx, yy,
                        width=0.8 * table[WIDTHINT],
                        align='center', color='#005500',
                        zorder=30)

#         subplot.bar(x, y, 
#                     width=0.8*table[WIDTHINT], 
#                     align='center', color='#22bb22')
        

    def plot(self):
        f = 1
        fig = plt.figure()
        l = len(self.tables)
        for (t, title) in self.tables:
            subplot = fig.add_subplot(l, 1, f)
            if title:
                subplot.title.set_text(title)
            self.plotOn(subplot, t)
            f += 1
        plt.show()
        
    def plotOnFigure(self, figure, _ignore=None):
        f = 1
        l = len(self.tables)
        for (t, title) in self.tables:
            subplot = figure.add_subplot(l, 1, f)
            if title:
                subplot.title.set_text(title)
            self.plotOn(subplot, t)
            f += 1

if __name__ == '__main__':
    pass
