# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока прерывания работы одноканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
# from pyssobject import PyssObject
from pyss.pyss_const import *
from pyss import queue_event_priorities
from pyss.block import Block
from pyss import facility

class Preempt(Block):
    """Блок переводит устройство в прерванное состояние.

Транзакт получает в пользование устройство, указанное в параметре конструктора facilityName, если это устрой-ство не было прервано другим транзактом. Если предыдущий транзакт захватил устройство через блок Preempt, текущий транзакт блокируется.

При вызове конструктора блока,
если устройство ещё не существует в словаре pyss_model.Pyssmodel()[FACILITIES],
происходит его создание и добавление в словарь устройств pyss_model.Pyssmodel()[FACILITIES].
Ключом является наименование устройства.

Перед входом транзакта в блок Preempt, cистема проверяет возможность прерывания работы устройства. Условием прерывания является нахождение устройства в состоянии, не являющимся STATE_NOT_ACCESS.

Если устройство находится в состоянии STATE_NOT_ACCESS, то транзакт задерживается (transact[DELAYED]=True) в
предыдущем блоке. Также транзакт помещается в список задержек ОКУ components.delayedList[facilityName].

Если устройство находится в состоянии STATE_NOT_ACCESS, то транзакт ("транзакт А") входит в блок Preempt. При этом если устройство занято транзактом ("транзакт Б"), то его обработка прерывается. Транзакт Б заносится в список facility[LISTPREEMPT]. Устройство занимается транзактом А. Состояние устройства переводится в STATE_NOT_ACCESS.

Если устройство находится в состоянии STATE_FREE, то транзакт ("транзакт А") занимает его. Состояние устройства переводится в STATE_NOT_ACCESS.

В атрибут транзакта А transact[FACILITY] записывается наименование устройства (FACILITY_NAME).

Освобождение устройства происходит в блоке g_return.GReturn.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    facilityName=None - наименование устройства (см. facility.Facility)

Например, блок

preempt.Preempt(sgm, facilityName='F_1')

моделирует прерывание устройства 'F_1'.

Пример использования см. tests/test_preempt_return.py.

Атрибуты блока Preempt (в дополнение к атрибутам block.Block):
bl = Preempt(...)
bl[FACILITY_NAME] - наименование устройства (см. facility.Facility)

См. также g_return.py

    """

    def __init__(self, ownerSegment=None, label=None, facilityName=None):
        # # funcGetFacility - функция получения устройства для прерывания
        # funcGetFacility - функция получения устройства для прерывания
        super(Preempt, self).__init__(SEIZE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [facilityName is None or facilityName == ""])
        self[FACILITY_NAME] = facilityName
        if facilityName not in ownerSegment.getModel().getFacilities():
            facility.Facility(ownerModel=ownerSegment.getModel(), facilityName=facilityName)

    def canEnter(self, transact):
        f = self.getOwnerModel().findFacility(self[FACILITY_NAME])
        return f.canPreempt(transact)

    def handleCanNotEnter(self, transact):
        facilityName = self[FACILITY_NAME]
        m = self.getOwnerModel()
        f = m.findFacility(facilityName)
        if not f.canPreempt(transact):
            m.appendToDelayedList(facilityName, transact)
        else:
            raise Exception("facility must NOT canPreempt [%s]" % facilityName)

    def transactInner(self, currentTime, transact):
        # #

        # pylint: disable=unused-argument

        facilityName = self[FACILITY_NAME]
        f = self.getOwnerModel().findFacility(facilityName)
        if f.canPreempt(transact):
            # transact[DELAYED]=False
            f.toPreempt(currentTime, transact)
            transact.setFacility(facilityName)
            return transact
        else:
            raise Exception("facility must canPreempt [%s]" % facilityName)

if __name__ == '__main__':
    def main():
        print "?"

    main()
