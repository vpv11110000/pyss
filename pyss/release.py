# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока освобождения одноканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class Release(Block):
    """Блок моделирования освобождения одноканального устройства.
    
Занятие одноканального устройства в блоке seize.Seize.     

При входе транзакта в блок Release одноканальное устройство переводится в состояние STATE_FREE. Из списка задержки ОКУ в список текущих событий перемещается один транзакт. У перемещённое транзакта сбрасывается флаг задержки.
У текущий транзакта сбрасывается присвоенное в блоке Seize наименование устройства (FACILITY_NAME).

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    facilityName=None - наименование устройства (см. facility.Facility)

Например, блок

release.Release(sgm, facilityName='F_1')

моделирует освобождение устройства 'F_1'.

Пример использования см. tests/test_seize.py.

Атрибуты блока Release (в дополнение к атрибутам block.Block):
bl = Release(...)
bl[FACILITY_NAME] - наименование устройства (см. facility.Facility)

См. также seize.py

    """

    def __init__(self, ownerSegment=None, label=None, facilityName=None):
        super(Release, self).__init__(RELEASE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [facilityName is None or facilityName == ""])
        self[FACILITY_NAME] = facilityName

    def transactInner(self, currentTime, transact):
        #

        # pylint: disable=unused-argument
        facilityName = self[FACILITY_NAME]
        m=self.getOwnerModel()
        f = m.findFacility(facilityName)
        if f.isBusy():
            f.toFree(currentTime, transact)
            # перемещаем один транзакт из списка задержки ОКУ в список текущих событий
            t = m.extractFromDelayedListFirst(facilityName)
            if t:
                if self.getOwnerModel().getOptions().logTransactTrack:
                    logger.info("Release: Transact[%d] TRACK:%s " % (transact[NUM], transact.strTrack()))                
                t.setLifeState(delayed=False, dstState=ACTIVED, timeTick=m.getCurTime())
                m.getCel().insertFirst(t)
            # текущий транзакт уже не на устройстве
            transact.removeFacility(facilityName)
        else:
            logger.info("Attemp free of free [%s]" % facilityName)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
