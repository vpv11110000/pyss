# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока занятия одноканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss import facility
from pyss import queue_event_priorities
from pyss.block import Block

class Seize(Block):
    """Занятие транзактом одноканального устройства.
    
Освобождение устройства происходит в блоке release.Release.

При вызове конструктора блока,
если устройство ещё не существует в словарь pyss_model.PyssModel()[FACILITIES],
происходит его создание и добавление в словарь устройств pyss_model.PyssModel()[FACILITIES].
Ключом является наименование устройства.

Перед входом транзакта в блок Seize, cистема проверяет доступность устройства (STATE_FREE).

Если устройство не доступно, то транзакт задерживается (transact[DELAYED]=True) в
предыдущем блоке. Также транзакт помещается в список задержек ОКУ components.delayedList[facilityName].

Если устройство доступно, то транзакт входит в блок Seize. При этом устройство занимается текущим транзактом. Устройство переводится в состояние STATE_BUSY. В атрибут транзакта transact[FACILITY] записывается наименование устройства (FACILITY_NAME).

Освобождение устройства происходит в блоке release.Release.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    facilityName=None - наименование устройства (см. facility.Facility)

Например, блок

seize.Seize(sgm, facilityName='F_1')

моделирует занятие устройства 'F_1'.

Пример использования см. tests/test_seize.py.

Атрибуты блока Seize (в дополнение к атрибутам block.Block):
bl = Seize(...)
bl[FACILITY_NAME] - наименование устройства (см. facility.Facility)

См. также release.py

    """

    def __init__(self, ownerSegment=None, label=None, facilityName=None):
        super(Seize, self).__init__(SEIZE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [facilityName is None or facilityName == ""])
        self[FACILITY_NAME] = facilityName
        if facilityName not in ownerSegment.getModel().getFacilities():
            facility.Facility(ownerModel=ownerSegment.getModel(), facilityName=facilityName)        

    def canEnter(self, transact):
        facilityName = self[FACILITY_NAME]
        f = self.getOwnerModel().findFacility(facilityName)
        return f.isFree()

    def handleCanNotEnter(self, transact):
        facilityName = self[FACILITY_NAME]
        m = self.getOwnerModel()
        f = m.findFacility(facilityName)
        if not f.isFree():
            m.appendToDelayedList(facilityName, transact)
        else:
            raise Exception("facility must NOT free [%s]" % facilityName)

    def transactInner(self, currentTime, transact):
        # #

        # pylint: disable=unused-argument

        facilityName = self[FACILITY_NAME]
        f = self.getOwnerModel().findFacility(facilityName)
        if f.isFree():
            f.toBusy(currentTime, transact)
            transact.setFacility(facilityName)
            return transact
        else:
            raise Exception("facility must free [%s]" % facilityName)

if __name__ == '__main__':
    pass
