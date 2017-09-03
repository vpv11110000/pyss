# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации занятия памяти или многоканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss import queue_event_priorities
from pyss.block import Block

class Enter(Block):
    """Блок Enter помещает транзакт в память. 
    
Память должна существовать.
    
Также может служить для имитации занятия многоканального устройства.

При создании блока в списке components.delayedList по ключу [storageName]
создаётся очередь с приоритетом для хранения хадержанных транзактов.

При проверке возможности входа транзакта в блок проверяется наличие свободного объема памяти, имя которой определено параметром storageName. Если имеется свободная память, то транзакт входит в блок Enter. При этом занятый объем памяти увеличивается на значение расчитанное функцией, указанной в параметре funcBusySize.

Если транзакт не может войти в блок Enter:
- он задерживается в предыдущем блоке;
- значение по атрибуту transact[DELAYED] устанавливается в True
- транзакт запоминается в списке задержки components.delayedList[storageName].

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    storageName=None - строка с наименованием памяти
    funcBusySize=1 - число занимаемых единиц памяти или функция, возвращающая указанное число. Сигнатура функции f(owner,transact).

Например, блок

enter.Enter(sgm, storageName="mcd",funcBusySize=1)

или

enter.Enter(sgm, storageName="mcd", funcBusySize=lambda x: 1)

при прохождении транзакта будет занимать память на одну единицу.

См. также leave.py, storage.py

Атрибуты блока Enter (в дополнение к атрибутам block.Block):
bl = Enter(...)
bl[STORAGE_NAME] - имя памяти или функция без параметров, возвращающая имя памяти.
bl[FUNC_BUSY_SIZE] - число занимаемых единиц памяти или функция, возвращающая указанное число
bl[TEMP_VALUE] - внутреннее использование

    """

    def __init__(self, ownerSegment=None, label=None, storageName=None, funcBusySize=1):
        # # funcBusySize(transact) - функция, возвращающая необходимый объем МКУ
        super(Enter, self).__init__(ENTER, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [storageName is None or storageName == "", funcBusySize is None])
        self[STORAGE_NAME] = storageName
        self[FUNC_BUSY_SIZE] = funcBusySize
        # self[firstBlock_4365643]=None
        self[TEMP_VALUE] = None

    def _findStorage(self):
        """return tuple (storageLabel, storage)"""
        s = self[STORAGE_NAME]
        return s, self.getOwnerModel().getStorages()[s]

    def canEnter(self, transact):
        _, storage = self._findStorage()
        if pyssobject.isfunction(self[FUNC_BUSY_SIZE]):
            self[TEMP_VALUE] = self[FUNC_BUSY_SIZE](self, transact)
        else:
            self[TEMP_VALUE] = self[FUNC_BUSY_SIZE]
        return storage[R] >= self[TEMP_VALUE]

    def handleCanNotEnter(self, transact):
        if self[TEMP_VALUE] is None:
            raise Exception(Must_before_call_FUNC_BUSY_SIZE)
        storageName, _ = self._findStorage()
        m=self.getOwnerModel()
        m.appendToDelayedList(storageName,transact)
        # !!!
        self[TEMP_VALUE] = None

    def transactInner(self, currentTime, transact):
        # #

        # pylint: disable=unused-argument
        if self[TEMP_VALUE] is None:
            raise Exception(Must_before_call_FUNC_BUSY_SIZE)

        _, storage = self._findStorage()
        v = self[TEMP_VALUE]
        storage.enter(transact=transact, busySize=v, currentTime=currentTime)
        # !!!
        self[TEMP_VALUE] = None
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
