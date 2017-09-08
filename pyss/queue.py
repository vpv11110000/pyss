# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации увеличения длины очереди
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss.pyssobject import PyssObject
from pyss.queue_object import QueueObject


class Queue(Block):
    """Блок Queue создаёт и при прохождении транзакта увеличивает длину этой очереди.

Создаёт в наборе pyss_model.PyssModel()[QUEUE_OBJECTS], по ключу queueName, объект очереди.
При прохождении транзакта увеличивает длину очереди на значение, полученное из атрибута DELTA_INCREASE.

Уменьшение длины очереди см. depart

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    queueName - имя очереди, в которой должна увеличиться длина
    deltaIncrease - значение или функция, возвращающая значение,
                    на которое увеличивается длина очереди, по умолчанию 1.
                    Сигнатура float f(o,t).

Например, блок

queue.Queue(sgm, queueName="QUEUE_1", deltaIncrease=1)

создаст (при страте моделирования) в pyss_model.PyssModel()[QUEUE_OBJECTS] объект 
очереди QueueObject с именем QUEUE_1
и при прохождении транзакта через этот блок Queue
будет увеличивать длину очереди QUEUE_1 на 1.

Пример использования см. tests/test_queue.py.

См. также queue.py (занятие очереди)

Атрибуты блока Queue (в дополнение к атрибутам block.Block):
bl = Queue(...)
bl[QUEUE_NAME] - имя объекта (queue.Queue) очереди
bl[DELTA_INCREASE] - целое значение, на которое увеличивается длина очереди.
bl[QUEUE_OBJECT] - ссылка на объект данных очереди

    """

    def __init__(self, ownerSegment=None, label=None, queueName=None, deltaIncrease=1, initLength=0):
        super(Queue, self).__init__(QUEUE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [queueName is None or queueName.strip() == "", deltaIncrease < 0])
        self[QUEUE_NAME] = queueName
        if pyssobject.isfunction(deltaIncrease):
            self[DELTA_INCREASE] = deltaIncrease
        else:
            self[DELTA_INCREASE] = lambda o, t: deltaIncrease 
        if not ownerSegment.getModel().existsQueue(queueName):
            self[QUEUE_OBJECT] = QueueObject(ownerSegment.getModel(), queueName=queueName, initLength=initLength)
        else:
            self[QUEUE_OBJECT] = ownerSegment.getModel().findQueue(queueName)

    def transactInner(self, currentTime, transact):
        q = self.getQueueObject()
        if q:
            q.increase(currentTime, transact, self[DELTA_INCREASE](self, transact))
        else:
            raise pyssobject.ErrorQueueObjectExists("queueObject not found [%s]" % self[QUEUE_NAME])
        return transact
    
    def getQueueObject(self):
        return self.getOwnerModel()[QUEUE_OBJECTS][self[QUEUE_NAME]] 

    def transactOut(self, transact):
        super(Queue, self).transactOut(transact)

if __name__ == '__main__':
    def main():
        print "?"

    main()
