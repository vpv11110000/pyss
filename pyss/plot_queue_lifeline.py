# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для линий жизни МКУ
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *
from pyss import statisticalseries
from pyss.pyssownerobject import PyssOwnerObject
from pyss import pyssobject

class PlotQueueLifeLine(PyssOwnerObject):
    """Формирование графической диаграммы для линий жизни объекта Очереди
    
Args:
    ownerModel - модель-владелец
    queueObject=None - объект очереди
    title - заголовок диаграммы
    funcAnnotate - функция анноторирования линии жизни. 
                   По умолчанию: lambda stor:queue_object[QUEUE_NAME]
     
    """
    
    def __init__(self, ownerModel=None, queueObject=None, title=None, funcAnnotate=None):
        super(PlotQueueLifeLine, self).__init__(PLOT_MODULE, label=None, owner=ownerModel)
        self.attr = {}
        self.queues = []
        if queueObject:
            self.queues.append(tuple([queueObject, title]))
        self.attr[TITLE] = title
        if funcAnnotate is None:
            self.attr[FUNC_ANNOTATE] = lambda stor:queueObject[QUEUE_NAME]   
        else:     
            self.attr[FUNC_ANNOTATE] = funcAnnotate
        #ownerModel.addPlotModule(self)
        ownerModel.plotSubsystem.append(self)
        
    def append(self, stor, title=None):
        num = len(self.queues) + 1
        if title:
            self.queues.append(tuple([stor, "Queue %d. " % num + title]))
        elif TITLE in stor:
            self.queues.append(tuple([stor, "Queue %d. " % num + stor[TITLE]]))
        else:
            self.queues.append(tuple([stor, "Queue %d" % num]))

    def convertToLifeLine(self, lifeTimeList):
        # список пар "start","state"
        r = []
        if len(lifeTimeList) > 1:
            for i in xrange(len(lifeTimeList) - 1):
                current_item = lifeTimeList[i][START]
                next_item = lifeTimeList[i + 1][START]
                r.append([current_item, next_item, lifeTimeList[i][STATE]])
            r.append([lifeTimeList[-1][START], self.getOwner()[END_TIME], lifeTimeList[-1][STATE]])
        else:
            current_item = lifeTimeList[0][START]
            r.append([current_item, self.getOwner()[END_TIME], lifeTimeList[0][STATE]])
        return r

    def plotOnFigure(self, figure, funcAnnotate=None):
        
        f = 1
        l = len(self.queues)
        for (stor, title) in self.queues:
            subplot = figure.add_subplot(l, 1, f)
            if title:
                subplot.title.set_text(title)
            tt = self.convertToLifeLine(stor[LIFE_TIME_LIST])
            x = []
            y = []
            for ttt in tt:
                x.append(ttt[0])
                y.append(ttt[2])
            # subplot.step(x, y, marker='.', color="g", linewidth=1, zorder=10)  # plotting t,a separately
            oldX, _, oldY = tt[0]
            for ttt in tt:
                x = ttt[0]
                y = ttt[2]
                subplot.plot([oldX, x], [oldY, oldY], color='g', lw=1)
                subplot.plot([x, x], [oldY, y], color='g', dashes=[1, 1], lw=1)
                subplot.plot([oldX, oldX], [oldY, oldY], color='g', lw=1)
                subplot.plot([x, x], [oldY, oldY], color='g', lw=1, marker='.')
                oldX = x
                oldY = y
#             for xx in list(set(x)):
#                 subplot.axvline(x=xx, dashes=[1, 1], color='#dddddd')
#             for yy in list(set(y)):
#                 subplot.axhline(y=yy, dashes=[1, 1], color='#dddddd')
#                 subplot.annotate("%.3f" % (yy),
#                                  xy=(x[0], yy),
#                                  xycoords='data',
#                                  xytext=(0, 2),
#                                  textcoords='offset points',)
            f += 1        
        

if __name__ == '__main__':
    def main():
        print "?"

    main()
