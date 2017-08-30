# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для линий жизни ОКУ
"""

import matplotlib.pyplot as plt

# pylint: disable=line-too-long

from pyss.pyss_const import *
from pyss import pyssobject
from pyss.func_discrete import FuncDiscrete
from pyss.func_exponential import Exponential
from pyss.func_normal import Normal
from pyss.statisticalseries import StatisticalSeries, approx_equal
from pyss.pyssownerobject import PyssOwnerObject

class PlotFunc(PyssOwnerObject):
    """Формирование диаграммы плотности вероятностей и функции распределения для функций func_discrete, func_exponential, func_normal
    
Args:
    funcObj=None - объект функции (м.б. func_discrete, func_exponential, func_normal)
    maxPoints=1000 - количество формируемых значений вызова функции
    countIntervals=20 - количество интервалов аргумента в промежутке [0,1]
    title - заголовок диаграммы
     
Пример см. demo_plot_func.py

    """
    
    def __init__(self, ownerModel=None, pyplotValue=None, funcObj=None, maxPoints=10000, countIntervals=20, title="Probability density. Distribution function"):
        super(PlotFunc, self).__init__(PLOT_MODULE, label=None, owner=ownerModel)
        map(pyssobject.raiseIsFalse, [isinstance(funcObj, FuncDiscrete) or
                                      isinstance(funcObj, Exponential) or
                                      isinstance(funcObj, Normal)])
        self.pyplot=pyplotValue
        self.attr = {}
        self.attr[FUNC_OBJ] = funcObj        
        self.attr[TITLE] = title
        self.attr[MAX_POINT] = maxPoints
        self.index = 0
        self.attr[INTERVALS] = countIntervals
        self.statSer = None
        ownerModel.addPlot(self)

    def calc(self):
        r = []
        x = 0
        while x < self.attr[MAX_POINT]:
            r.append(self.attr[FUNC_OBJ].get())
            x += 1
        return r
        
    def plotDiscreteProbDenOn(self, subplot, stSer):
        cnt = stSer.count()
        l = [(x1, float(stSer[DATA][x1]) / cnt) for x1 in stSer[DATA].keys()]
        if isinstance(self.attr[FUNC_OBJ], Exponential):
            l.append((0, self.attr[FUNC_OBJ][LAMBDA_VAL]))
        else:
            l.append((0, 0))
        l = sorted(l, key=lambda t:t[0])

        for xx, yy in l:
            subplot.axhline(y=yy, dashes=[1, 1], color='#dddddd')
            subplot.annotate("%.3f:%.3f" % (xx, yy),
                             xy=(xx, yy),
                             xycoords='data',
                             xytext=(0, 2),
                             textcoords='offset points',)        

        for z in l:
            subplot.plot([z[0], z[0]], [0, z[1]], color='blue', lw=2, marker='_')
        
    def plotDiscreteDistribOn(self, subplot, stSer):
        count = stSer.count()
        l = [(x1, float(stSer[DATA][x1]) / count) for x1 in stSer[DATA].keys()]
        l = sorted(l, key=lambda t:t[0])
        sm = 0
        ld = [(0.0, 0.0)]
        for xx, yy in l:
            sm += yy
            ld.append((xx, sm))
        l = ld
        ld = None

        for xx, yy in l:
            subplot.axvline(x=xx, dashes=[1, 1], color='#dddddd')
            subplot.axhline(y=yy, dashes=[1, 1], color='#dddddd')
            subplot.annotate("%.3f:%.3f" % (xx, yy),
                             xy=(xx, yy),
                             xycoords='data',
                             xytext=(0, 2),
                             textcoords='offset points',)          

        oldX, oldY = l[0]
        for i in xrange(1, len(l)):
            x, y = l[i]
            subplot.plot([oldX, x], [oldY, oldY], color='blue', lw=2)
            subplot.plot([x, x], [oldY, y], color='blue', dashes=[1, 1], lw=2)
            subplot.plot([oldX, oldX], [oldY, oldY], color='blue', lw=1)
            subplot.plot([x, x], [oldY, oldY], color='blue', lw=2, marker='>')
            oldX = x
            oldY = y
        subplot.plot([0, 0], [0, 0], color='blue', lw=1, marker='o')
        subplot.plot([l[-1][0], l[-1][0]], [l[-1][1], l[-1][1]], color='blue', lw=1, marker='o')
        
    def plot(self):
        fig = plt.figure()
        self.plotOnFigure(fig)
        
    def show(self):
        plt.show()
        
    def plotOnFigure(self, figure, _ignore=None):
        v = self.calc()

        self.statSer = StatisticalSeries()
        if isinstance(self.attr[FUNC_OBJ], FuncDiscrete):
            for t in v:
                self.statSer.append(t, count=1)
            
        elif isinstance(self.attr[FUNC_OBJ], Exponential) or isinstance(self.attr[FUNC_OBJ], Normal):
            m = max(v)
            delta = float(m) / self.attr[INTERVALS]
            lft = 0.0
            rght = delta
            cnt = len(v)
            while lft < m:
                f = [t for t in v if (lft <= t) and (t < rght)]
                z = len(f)
                self.statSer.append(rght, count=z)
                lft = rght
                rght += delta
        # -------------

        subplot = figure.add_subplot(2, 1, 1)
        # Probably density
        if self.attr[TITLE]:
            subplot.title.set_text(self.attr[TITLE])
        self.plotDiscreteProbDenOn(subplot, self.statSer)
        # Distribution
        subplot = figure.add_subplot(2, 1, 2)
        self.plotDiscreteDistribOn(subplot, self.statSer)
            
if __name__ == '__main__':
    pass
