# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока для удаления транзакта из модели
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss import options
from pyss import logger

class Terminate(Block):
    """Блок для удаления транзакта из модели
    
Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    deltaTerminate=1 - величина, на которую уменьшается значение счётчика завершений components.terminateCounter.

При входе транзакта в блок Terminate, происходит:
- уменьшение значение счётчика завершений components.terminateCounter;
- выставление флага удаления транзакта  transact[TRANSACT_DELETED]=True;
- выставление флага завершения полной обработки транзакта;
- запись времени исключения транзакта из модели transact[TERMINATED_TIME]

Пример, блока:

terminate.Terminate(sgm, deltaTerminate=1)

Пример использования см. tests/*

Атрибуты блока Terminate (в дополнение к атрибутам block.Block):
bl = Terminate(...)
bl[DELTA_TERMINATE] - величина, на которую уменьшается значение счётчика завершений components.terminateCounter.
bl[ON_DELETED] - обработчик события "после удаления транзакта" (сигнатура void handle(transact)).
                 Обработчик устанавливается вне конструктора.
    
    """
    
    def __init__(self, ownerSegment=None, label=None, deltaTerminate=1):
        super(Terminate, self).__init__(TERMINATE, label=label, ownerSegment=ownerSegment)
        self[DELTA_TERMINATE] = deltaTerminate
        self[ON_DELETED] = None

    def transactInner(self, currentTime, transact):
        if transact is None:
            return None
        m=self.getOwnerModel()
        m.terminateCounter.dec(self[DELTA_TERMINATE])
        transact[TRANSACT_DELETED] = True
        transact[HANDLED] = True
        transact[TERMINATED_TIME] = currentTime
        transact.setLifeState(delayed=False, dstState=TRANSACT_DELETED, timeTick=currentTime)
        if m.getOptions().logTransactTrack:
            logger.info("Terminate: Transact[%d] TRACK:%s " % (transact[NUM], transact.strTrack()))
        if self[ON_DELETED]:
            self[ON_DELETED](transact)
        return None
    
if __name__ == '__main__':
    def main():
        print "?"

    main()

