# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль графической диаграммы для линий жизни ОКУ
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *
from pyss import statisticalseries
from pyss import pyssobject
from pyss.pyssownerobject import PyssOwnerObject

class PlotFacilityLifeLine(PyssOwnerObject):
    """Формирование графической диаграммы для линий жизни ОКУ
    
Args:
    facilities=None - ОКУ или список блоков ОКУ
    title - заголовок диаграммы
    funcAnnotate - функция аннторирования линии жизни ОКУ. 
                   По умолчанию: lambda faclty:facility[FACILITY_NAME]
     
Пример см. test_assemble.py

    """
    
    def __init__(self, ownerModel=None, facilities=None, title=None, funcAnnotate=None):
        super(PlotFacilityLifeLine, self).__init__(PLOT_MODULE, label=None, owner=ownerModel)
        self.attr = {}
        self.attr[FACILITIES] = facilities        
        self.attr[TITLE] = title
        if funcAnnotate is None:
            self.attr[FUNC_ANNOTATE] = lambda faclty:faclty[FACILITY_NAME]   
        else:     
            self.attr[FUNC_ANNOTATE] = funcAnnotate
        #ownerModel.addPlotModule(self)
        ownerModel.addPlot(self)

    def convertToLifeLine(self, lifeTimeList):
        # список пар "start","state"
        r = []
        if len(lifeTimeList)>1:
            for i in xrange(len(lifeTimeList) - 1):
                current_item = lifeTimeList[i][START]
                next_item = lifeTimeList[i + 1][START]
                r.append([current_item, next_item, lifeTimeList[i][STATE]])
        else:
            current_item = lifeTimeList[0][START]
            r.append([current_item, self.getOwner()[END_TIME], lifeTimeList[0][STATE]])
        return r

    def plotOnFigure(self, figure, funcAnnotate=None):
        subplot = figure.add_subplot(1, 1, 1)
        index = 1
        for fac in self.attr[FACILITIES]:
            c = 0
            tt = self.convertToLifeLine(fac[LIFE_TIME_LIST])
            subplot.axvline(x=tt[-1][1], dashes=[1, 1], color='#dddddd')
            subplot.annotate(self.attr[FUNC_ANNOTATE](fac),
                             xy=(tt[0][0], index),
                             xycoords='data',
                             xytext=(0, 2),
                             textcoords='offset points',)
            for t in tt:
                subplot.axvline(x=t[0], dashes=[1, 1], color='#dddddd')
                x = [t[0], t[1]]
                a = [index, index]
                if t[2] == STATE_FREE:
                    subplot.plot(x, a, marker='.', color="#000010", linewidth=1)  # plotting t,a separately
                elif t[2] == STATE_BUSY:
                    subplot.plot(x, a, marker='.', color="g", linewidth=3)  # plotting t,a separately
                elif t[2] == STATE_NOT_ACCESS:
                    subplot.plot(x, a, marker='.', color="r", linewidth=1)  # plotting t,a separately
                else:
                    subplot.plot(x, a, marker='.', color="#553333", linewidth=1)  # plotting t,a separately
            index += 1   
        if self.attr[TITLE]:
            subplot.title.set_text(self.attr[TITLE])            

if __name__ == '__main__':
    def main():
        print "?"

    main()
