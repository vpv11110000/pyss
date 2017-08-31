# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации освобождения памяти или многоканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block

# Занятие и освобождение МКУ имитируется блоками ENTER (войти) и LEAVE (выйти)

class Leave(Block):
    """Блок Leave освобождает память или многоканальное устройство.

Память должна существовать в списке памятей pyss_model.PyssModel()[STORAGES].

При прохождении транзакта через блок Leave:
- из components.delayedList[storageName] в список текущих событий переносится ранее задержанный транзакт;
- значение по атрибуту transact[DELAYED] (задержанного транзакта) устанавливается в False;
- освобождается память на значение, рассчитанное или полученное функцией funcBusySize

Args:
    storageName=None - строка с наименованием памяти
    funcBusySize=1 - число освобождаемых единиц памяти или функция, возвращающая указанное число.  Сигнатура функции f(owner,transact).
    label - см. block.py.

Например, блок

leave.Leave(storageName="mcd",funcBusySize=1,label=None)

или

leave.Leave(storageName="mcd",funcBusySize=funcBusySize=lambda x: 1, label=None)

при прохождении транзакта будет освобождать память на одну единицу.

Пример использования см. tests/test_enter_leave.py.

См. также enter.py, storage.py

Атрибуты блока Enter (в дополнение к атрибутам block.Block):
bl = Leave(...)
bl[STORAGE_NAME] - имя памяти или функция без параметров, возвращающая имя памяти.
bl[FUNC_BUSY_SIZE] - число занимаемых единиц памяти или функция, возвращающая указанное число

    """

    def __init__(self, ownerSegment=None, label=None, storageName=None, funcBusySize=None):
        # # funcBusySize(transact) - функция, возвращающая необходимый объем МКУ
        super(Leave, self).__init__(LEAVE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [storageName is None or storageName.strip() == "", funcBusySize is None])
        self[STORAGE_NAME] = storageName
        self[FUNC_BUSY_SIZE] = funcBusySize
        # self[firstBlock_4365643]=None

    def _findStorage(self):
        rv = None
        storageLabel = self[STORAGE_NAME]
        s = self.getOwnerModel().getStorages()
        if storageLabel in s:
            rv = s[storageLabel]
        else:
            raise Exception("Storage [%s] not found" % storageLabel)
        return storageLabel, rv

    def canEnter(self, transact):
        return True

    def handleCanNotEnter(self, transact):
        pass

    def transactInner(self, currentTime, transact):
        # #

        # pylint: disable=unused-argument

        if pyssobject.isfunction(self[FUNC_BUSY_SIZE]):
            v = self[FUNC_BUSY_SIZE](self, transact)
        else:
            v = self[FUNC_BUSY_SIZE]
        _, storage = self._findStorage()
        storage.leave(transact=transact, busySize=v, currentTime=currentTime)
        # перемещаем один транзакт из списка задержки ОКУ или МКУ в список текущих событий
        t = self.getOwnerModel().extractFromDelayedListFirst(self[STORAGE_NAME])
        if t:
            t.setLifeState(delayed=False, dstState=ACTIVED, timeTick=currentTime)
            self.getOwnerModel().getCel().put(t)

        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
