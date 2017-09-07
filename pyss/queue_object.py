# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль объекта очереди
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss import statisticalseries
from pyss.pyssobject import PyssObject
from pyss.pyssstateobject import PyssStateObject

class QueueObject(PyssStateObject):
    """Объект очереди
    
Хранит данные очереди.
Можно назначать обработчики изменения состояния (см. PyssStateObject).
Под значением старого состояния понимается старое значение текущей длины очереди.

Владельцем QueueObject является модель.

При изменении состояния, вызывается обработчик измененния состояния (см. pyssstateobject.PyssStateObject).

Args:
    ownerModel=None - объект модели-владельца
    queueName - имя очереди
    initLength=0 - начальная длина очереди

Атрибуты объекта QueueObject (в дополнение к атрибутам pyssownerobject.PyssOwnerObject):
bl = Queue(...)
bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
bl[QUEUE_OBJECT][TIME_MEAN] - Среднее время пребывания транзактов в очереди (включая нулевые входы).
bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - Среднее время пребывания сообщения в очереди (без нулевых входов).
bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
bl[QUEUE_OBJECT][LISTTRANSACT] - словарь: key - <номера транзактов> : value - <время входа в очередь> 
bl[QUEUE_OBJECT][LIFE_TIME_LIST] - писок меток времени и длины очереди [{START:<time>, STATE:<len>}]
bl[QUEUE_OBJECT][STATISTICAL_SERIES] - статистическая последовательность времён нахождения транзактов в очереди
    
    """
    def __init__(self, ownerModel=None, queueName=None, initLength=0):
        super(QueueObject, self).__init__(QUEUE_OBJECT, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [queueName is None or queueName.strip() == ""])
        self[QUEUE_NAME] = queueName
        # текущая длина очереди
        self[QUEUE_LENGTH] = initLength
        self[QUEUE_LENGTH_MAX] = initLength
        self[ENTRY_ZERO] = 0
        self[TIME_MEAN] = None
        self[TIME_MEAN_WITHOUT_ZERO] = None
        self[QUEUE_MEAN_LENGTH_BY_TIME] = None
        self[ENTRY_COUNT] = 0
        self[CURRENT_COUNT] = 0
        self[RETRY] = 0
        # список номеров транзактов и времени постановки в очередь
        self[LISTTRANSACT] = {}
        self[LIFE_TIME_LIST] = [{START:ownerModel.getCurTime(), STATE:initLength}]
        self[STATISTICAL_SERIES] = statisticalseries.StatisticalSeries()
        ownerModel.addQueueObject(self)
        
    def increase(self, currentTime, transact, delta):
        oldState = self[QUEUE_LENGTH]
        self[QUEUE_LENGTH] += delta
        if self[QUEUE_LENGTH_MAX] < self[QUEUE_LENGTH]:
            self[QUEUE_LENGTH_MAX] = self[QUEUE_LENGTH]
        self[LISTTRANSACT][transact[NUM]] = currentTime
        self[ENTRY_COUNT] += 1
        self[CURRENT_COUNT] += 1
        self[LIFE_TIME_LIST].append({START:currentTime, STATE:self[QUEUE_LENGTH]})
        # под значением старого состояния понимается старое значение текущей длины очереди
        self.fireHandlerOnStateChange(oldState=oldState)
        
    def decrease(self, currentTime, transact, delta):
        """Здесь делается не всё, что нужно"""

        oldState = self[QUEUE_LENGTH]
        self[QUEUE_LENGTH] -= delta
        self[LIFE_TIME_LIST].append({START:currentTime, STATE:self[QUEUE_LENGTH]})        
        self.fireHandlerOnStateChange(oldState=oldState)

if __name__ == '__main__':
    def main():
        print "?"

    main()
