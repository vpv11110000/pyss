# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации объекта таблицы статистики для очереди
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssownerobject import PyssOwnerObject
from pyss.pyss_const import *

class Qtable(PyssOwnerObject):
    """Объект Qtable предназначен для получения распределения времени пребывания транзакта в очереди.

При использовании Qtable информация в таблицу заносится автоматически при обработке транзакта в блоках Depart.

Транзакт проходя блок Queue отмечает в атрибуте Queue[LISTTRANSACT][transact[NUM]] время вхождения в Queue.

Далее транзакт проходя блок Depart инициирует вычисление времени нахождения в очереди Queue (атрибут Queue[LISTTRANSACT][transact[NUM]]) и учёт этого времени в Qtable. После этого атрибут Queue[LISTTRANSACT][transact[NUM]]) удалается.

По окончании моделирования собранная в таблице информация выводится в стандартном отчете GPSS.

Объект Qtable добавляется в модель с помощью метода PyssModel.addQtable.

Объекту Qtable присваивается атрибут label: QTABLE+"_"+queueName.

Args:
    ownerModel=None - объект модели-владельца
    queueName - имя очереди
    limitUpFirst=None - верхний предел первого частотного интервала
    widthInt=None - ширина частотного интервала
    countInt=None - число частотных интервалов (положительное целое число)

Владельцем QTable является модель.

Например, объект

qtable.Qtable(queueName="QUEUE_1", limitUpFirst=1, widthInt=1, countInt=20)

создаст объект ведения статистики времени пребывания транзакта в очереди.

Множество объектов qtable.Qtable хранится в pyss_model.PyssModel().qtableList.

Пример использования см. tests/test_queue.py.

См. также queue.py и depart.py (занятие и освобождение очереди)

Атрибуты объекта Qtable (в дополнение к атрибутам block.Block):
bl = Qtable(...)
bl[QUEUE_NAME] - имя объекта (queue.Queue) очереди
bl[TITLE] - дубль: имя объекта (queue.Queue) очереди
bl[DISPLAYING] - true - отображать результат обработки данных таблицы
bl[LIMITUPFIRST] - верхний предел первого частотного интервала
bl[WIDTHINT] - ширина частотного интервала
bl[COUNTINT] - число частотных интервалов (положительное целое число)
bl[TOTAL] - общее число транзактов, прошедшее через очередь
bl[INTERVALS] - интервалы статистики
bl[MIN_BOUND] - левая граница первого интервала
bl[MAX_BOUND] - правая граница последнего интервала

    """
    def __init__(self, ownerModel=None, queueName=None, limitUpFirst=None, widthInt=None, countInt=None):
        # # таблица
        #
        # limitUpFirst is None - вся область определения, счётчик в self[TOTAL]
        #
        # limitUpFirst is not None and countInt == 0 - область значений разделена
        #   на две подобласти: до limitUpFirst (счётчик в self[INTERVALS][NEGATIVE_INFINITY])
        #   и после limitUpFirst, включая границу (счётчик в self[INTERVALS][POSITIVE_INFINITY])
        #
        # limitUpFirst is not None and countInt > 0 - область значений разделена:
        #    [NEGATIVE_INFINITY,self[MIN_BOUND]) - счётчик в self[INTERVALS][NEGATIVE_INFINITY]
        #    [self[MIN_BOUND],limitUpFirst) - счётчик в self[LIST][0]
        #    ...
        #    [MIN_BOUND+widthInt*(countInt-1),MIN_BOUND+widthInt*countInt) - счётчик в self[LIST][countInt-1]
        #    [MIN_BOUND+widthInt*countInt,POSITIVE_INFINITY) - счётчик в self[INTERVALS][POSITIVE_INFINITY]
        #

        # pylint: disable=too-many-arguments

        super(Qtable, self).__init__(QTABLE, label=QTABLE + "_" + queueName, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [not queueName])
        map(pyssobject.raiseIsTrue, [limitUpFirst is None and (widthInt is not None or countInt is not None)])
        map(pyssobject.raiseIsTrue, [limitUpFirst is not None and (countInt is None or (countInt == 0 and widthInt is not None) or (countInt > 0 and (widthInt is None or widthInt == 0)))])
        #
        self[QUEUE_NAME] = queueName
        self[TITLE] = queueName
        self[LIMITUPFIRST] = limitUpFirst
        self[WIDTHINT] = widthInt
        self[COUNTINT] = countInt
        self[TOTAL] = 0
        self[INTERVALS] = {}
        self[MIN_BOUND] = None
        self[MAX_BOUND] = None
        self[LIST] = []
        if limitUpFirst is None:
            self[ACTION_FUNC] = self.writeToIntervalsFunctionDomainFull
            self[ACTION_VIEW] = self.table2strFunctionDomainFull
        elif limitUpFirst is not None and countInt == 0:
            self[ACTION_FUNC] = self.writeToIntervalsFunctionDomainHalf
            self[ACTION_VIEW] = self.table2strFunctionDomainHalf
        else:
            self[MIN_BOUND] = limitUpFirst - widthInt
            self[MAX_BOUND] = self[MIN_BOUND] + countInt * widthInt
            self[ACTION_FUNC] = self.writeToIntervals
            self[ACTION_VIEW] = self.table2strInterv
            while countInt > 0:
                # интервалы
                self[LIST].append(limitUpFirst)
                self[INTERVALS][limitUpFirst] = 0
                limitUpFirst += widthInt
                countInt -= 1

        self[INTERVALS][POSITIVE_INFINITY] = 0
        self[INTERVALS][NEGATIVE_INFINITY] = 0
        self[DISPLAYING] = True
        
        ownerModel.addQtable(self)
    

    def setDisplaying(self, displaying=False):
        self[DISPLAYING] = displaying
        return self

    def writeToIntervalsFunctionDomainFull(self, x, y):
        pass

    def writeToIntervalsFunctionDomainHalf(self, x, y):
        if x < self[LIMITUPFIRST]:
            self[INTERVALS][NEGATIVE_INFINITY] += y
        else:
            self[INTERVALS][POSITIVE_INFINITY] += y

    def writeToIntervals(self, x, y):
        # #
        # x - значение из области определения, ассоциируется с интервалом значений
        #     нижняя граница принадлежит, верхняя не принадлежит
        # y - значение из области значений, добавляется к счётчику
        #
        if x < self[MIN_BOUND]:
            self[INTERVALS][NEGATIVE_INFINITY] += y
        elif x >= self[MAX_BOUND]:
            self[INTERVALS][POSITIVE_INFINITY] += y
        else:
            l = self[LIST]
            for z in l:
                if x < z:
                    self[INTERVALS][z] += y
                    break

    def handle(self, timeBusyOfQueue=None):
        if timeBusyOfQueue is None:
            return
        self[TOTAL] += 1
        self[ACTION_FUNC](timeBusyOfQueue, 1)

    def table2strFunctionDomainFull(self):
        rv = "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def formatL(self, x, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % ("<%0.3f" % x, str(y))

    def formatG(self, x, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % (">=%0.3f" % x, str(y))

    def formatF(self, x0, x1, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % ("%0.3f-%0.3f" % (x0, x1), str(y))

    def table2strFunctionDomainHalf(self):
        rv = "!   Value  !  Count   !" + "\n"
        rv += "=======================" + "\n"
        key = self[LIMITUPFIRST]
        v = self[INTERVALS][NEGATIVE_INFINITY]
        rv += self.formatL(key, v) + "\n"
        v = self[INTERVALS][POSITIVE_INFINITY]
        rv += self.formatG(key, v) + "\n"
        rv += "=======================" + "\n"
        rv += "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def table2strInterv(self):
        rv = "!   Value  !  Count   !" + "\n"
        rv += "=======================" + "\n"
        key = None
        oldKey = self[MIN_BOUND]
        l = self[LIST]
        v = self[INTERVALS][NEGATIVE_INFINITY]
        rv += self.formatL(self[MIN_BOUND], v) + "\n"
        for key in l:
            v = self[INTERVALS][key]
            rv += self.formatF(oldKey, key, v) + "\n"
            oldKey = key
        # rv+="! %8s ! %8s !"%(s,str(self[INTERVALS][POSITIVE_INFINITY]))+"\n"
        v = self[INTERVALS][POSITIVE_INFINITY]
        rv += self.formatG(self[MAX_BOUND], v) + "\n"
        rv += "=======================" + "\n"
        rv += "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def table2str(self):
        rv = "=======================" + "\n"
        rv += "Table: %s" % self[QUEUE_NAME] + "\n"
        rv += "=======================" + "\n"
        rv += self[ACTION_VIEW]()
        return rv

if __name__ == '__main__':
    def main():
        print "?"

    main()
