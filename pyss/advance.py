# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока задержки транзакта в течение некоторого интервала модельного времени
"""

# pylint: disable=line-too-long

import random
from pyss import pyssobject
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class Advance(Block):
    """Блок задержки транзакта в течение некоторого интервала модельного времени.

Advance(meanTime=None, modificatorFunc=None,label=None)

Args:
    meanTime - задаёт среднее время обслуживания (число или функция f()).
               Если задан список или кортеж, 
               то среднее значение будет последовательно выбираться из списка.
               По окончании списка будет возвращаться 0.
    modificatorFunc - число или функция-модификатор среднего значения meanTime (f(owner,currentTime))
    label - см. block.py.

Например, блок

advance.Advance(meanTime=3*60,modificatorFunc=lambda owner, currentTime: random.uniform(-1.0*60,1.0*60))

задерживает попавший в него транзакт на время от 120 до 240 единиц
модельного времени (например секунд, если за одну секунду принято значение 1.0).

Пример использования см. demo/demo_advance.py, demo/demo_queue.py, .

Атрибуты блока Advance (в дополнение к атрибутам block.Block):
bl = Advance(...)
bl[MEAN_TIME] - среднее время задержки.
                  Если задан список или кортеж, то формируется лямбда и среднее значение будет 
                  последовательно выбираться из списка (генератор).
                  По окончании списка будет возвращаться 0.
bl[MODIFICATOR] - функция-модификатор среднего значения, если modificatorFunc число, 
                  то формируется лямбда.

    """

    def __init__(self, ownerSegment=None, label=None, meanTime=None, modificatorFunc=None):
        super(Advance, self).__init__(ADVANCE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [(type(meanTime) is list or type(meanTime) is tuple) and len(meanTime) == 0])
        
        if pyssobject.isfunction(meanTime):
            self[MEAN_TIME] = meanTime
        elif type(meanTime) is list or type(meanTime) is tuple:
            _list = meanTime
            def f():
                for x in _list:
                    yield x
            g = f()
            self[MEAN_TIME] = lambda: next(g, 0)
        elif meanTime is not None:
            # число
            self[MEAN_TIME] = lambda: meanTime
        else:
            # meanTime is None
            pyssobject.raiseIsTrue([True])
            
        if pyssobject.isfunction(modificatorFunc):
            self[MODIFICATOR] = modificatorFunc
        else:
            if modificatorFunc is not None:
                # число
                self[MODIFICATOR] = lambda o, c: random.uniform(-float(modificatorFunc),float(modificatorFunc))
            else:
                # число
                self[MODIFICATOR] = lambda o, c: 0

    def modifiedValue(self, currentTime):
        t = self[MEAN_TIME]
        m = self[MODIFICATOR]
        if m is not None:
            return t() + m(self, currentTime)
        else:
            return t

    def transactInner(self, currentTime, transact):
        # True - was handled
        m = self.modifiedValue(currentTime)
        if pyssobject.floatEquals(m, 0, allowed_error=ALLOWED_ERROR):
            return transact
        else:
            transact[SCHEDULED_TIME] = currentTime + m
            # pylint: disable=unsubscriptable-object
            opt = self.getOwnerSegment()[OPTIONS]
            if opt:
                if opt.logTransactTrace:
                    logger.info("Advance transact [%s] to FEL" % (str(transact)))
            self.getOwnerModel().getFel().put(transact)
            return None

if __name__ == '__main__':
    pass
