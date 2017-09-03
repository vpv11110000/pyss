# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль объекта "устройства"
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class GReturn(Block):
    """Блок позволяет завершить прерывание устройства.

Транзакт, ранее прервавший работу устройства, при обработке этим блоком GReturn снимает ранее вызванное прерывание.

Если на устройстве имеется прерванный ранее транзакт (см. список по атрибуту facility[LISTPREEMPT]), то он возвращается в обработку. Время обработки равно остатку времени, определённому в момент прерывания.

Из транзакта снявшего прерывание удаляется атрибут FACILITY.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    facilityName=None - наименование устройства (см. facility.Facility)

Например, блок

g_return.GReturn(sgm, facilityName='F_1')

моделирует снятие прерывания c устройства 'F_1'.

Пример использования см. tests/test_preempt_return.py.

Атрибуты блока GReturn (в дополнение к атрибутам block.Block):
bl = GReturn(...)
bl[FACILITY_NAME] - наименование устройства (см. facility.Facility)

См. также preempt.py

    """

    def __init__(self, ownerSegment=None, label=None, facilityName=None):
        super(GReturn, self).__init__(RELEASE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [facilityName is None or facilityName == ""])
        self[FACILITY_NAME] = facilityName

    def transactInner(self, currentTime, transact):
        #

        # pylint: disable=unused-argument
        facilityName = self[FACILITY_NAME]
        f = self.getOwnerModel().findFacility(facilityName)
        if f[TRANSACT] == transact:
            f.toReturn(currentTime, transact)
            # возможно в f[TRANSACT] ранее прерванный транзакт
            t = f[TRANSACT]
            if t:
                t.setLifeState(delayed=False, dstState=ACTIVED, timeTick=currentTime)
                self.getOwnerModel().getFel().put(t)
            # перемещаем один транзакт из списка задержки ОКУ в список текущих событий
            t = self.getOwnerModel().extractFromDelayedListFirst(facilityName)
            if t:
                t.setLifeState(delayed=False, dstState=ACTIVED, timeTick=currentTime)
                self.getOwnerModel().getCel().insertFirst(t)            
            # текущий транзакт уже не на устройстве
            transact.removeFacility(facilityName)
        else:
            logger.info("Attemp return of return [%s]" % facilityName)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
