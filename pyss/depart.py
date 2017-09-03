# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации уменьшения длины очереди
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss.queue_object import QueueObject

class Depart(Block):
    """Блок Depart служит для уменьшения длины очереди.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    queueName - имя объекта (queue.Queue) очереди или функция без параметров,
            определяющая имя объекта очереди, в которой должна уменьшиться длина
    deltaDecrease - значение или функция, возвращающая целое значение,
                    на которое уменьшается длина очереди, по умолчанию 1.
                    Это значение не должно превышать текущую длину очереди.
                    Параметр deltaDecrease, как правило, должен быть равен deltaIncrease
                    блока queue.Queue.
                    Сигнатура float f(o,t).                    

Например, блок

depart.Depart(sgm, queueName="QUEUE_1", deltaDecrease=1)

или

depart.Depart(queueName=lambda:"QUEUE_1", deltaDecrease=1)

при прохождении транзакта будет уменьшать длину очереди QUEUE_1 на 1.

См. также queue.py (занятие очереди).

Атрибуты блока Depart (в дополнение к атрибутам block.Block и pyssobject.PyssObject):
bl = Depart(...)
bl[QUEUE_NAME] - имя объекта (queue.Queue) очереди или функция без параметров,
            определяющая имя объекта очереди.
bl[DELTA_DECREASE] - целое значение, на которое уменьшается длина очереди.

    """
    def __init__(self, ownerSegment=None, label=None, queueName=None, deltaDecrease=1):
        super(Depart, self).__init__(DEPART, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [queueName is None, deltaDecrease < 0])
        self[QUEUE_NAME] = queueName
        if pyssobject.isfunction(deltaDecrease):
            self[DELTA_DECREASE] = deltaDecrease
        else:
            self[DELTA_DECREASE] = lambda o, t: deltaDecrease         
        
    def getQueueObject(self):
        return self.getOwnerModel()[QUEUE_OBJECTS][self[QUEUE_NAME]] 
    
    def transactInner(self, currentTime, transact):
        q = self.getQueueObject()
        if q:
            currentTimeActial = currentTime
            currentTimeOld = q[LISTTRANSACT][transact[NUM]]
            d = currentTimeActial - currentTimeOld
            deltaDec = self[DELTA_DECREASE](self, transact)
            # точность по умолчани ALLOWED_ERROR = 1e-07
            if pyssobject.floatEquals(d, 0.0, allowed_error=ALLOWED_ERROR):
                q[ENTRY_ZERO] += deltaDec
            elif d > 0.0:
                pass
            else:
                raise Exception("Illegal value currentTimeActial<currentTimeOld")
            q.decrease(currentTime, transact, deltaDec)
            q[STATISTICAL_SERIES].append(value=d, count=deltaDec)
            q[TIME_MEAN] = q[STATISTICAL_SERIES].mean()
            ss = q[STATISTICAL_SERIES].cloneWithFilter(funcFilter=lambda k, v: k != 0.0)
            q[TIME_MEAN_WITHOUT_ZERO] = ss.mean()
            z = self[QUEUE_NAME]
            m = self.getOwnerModel()
            if z in m.qtableList:
                m.qtableList[z].handle(timeBusyOfQueue=d)

            q[LISTTRANSACT].pop(transact[NUM])
            q[CURRENT_COUNT] -= 1
        else:
            raise pyssobject.ErrorQueueObjectExists("Reference to Queue is null [%s]" % z)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
