# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для линий жизни МКУ
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *
from pyss import statisticalseries
from pyss.pyssownerobject import PyssOwnerObject
from pyss import pyssobject

class PlotLogicObjectLifeLine(PyssOwnerObject):
    """Формирование графической диаграммы для линий жизни логических ключей (ЛК)
    
Args:
    ownerModel=None - объект модели-владельца 
    logicObjectList=None - список объектов ЛК
    title - заголовок диаграммы
     
    """
    
    def __init__(self, ownerModel=None, logicObjectList=None, title=None):
        super(PlotLogicObjectLifeLine, self).__init__(PLOT_MODULE, label=None, owner=ownerModel)
        self.attr = {}
        self.logicObjects = []
        if logicObjectList:
            for o in logicObjectList: 
                self.logicObjects.append(tuple([o, "%s%s" % (title, o[LOGIC_OBJECT_NAME])]))
        else:
            raise pyssobject.ErrorInvalidArg("logicObjectList must be list")
        self.attr[TITLE] = title if title is not None else ""

        # ownerModel.addPlotModule(self)
        ownerModel.plotSubsystem.append(self)
        
    def append(self, logicObject, title=None):
        num = len(self.logicObjects) + 1
        self.logicObjects.append(tuple([logicObject, "%s%s" % (title, logicObject[LOGIC_OBJECT_NAME])]))

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
        l = len(self.logicObjects)
        for (o, title) in self.logicObjects:
            subplot = figure.add_subplot(l, 1, f)
            if title:
                subplot.title.set_text(title)
            tt = self.convertToLifeLine(o[LIFE_TIME_LIST])
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
            f += 1        

if __name__ == '__main__':
    pass
