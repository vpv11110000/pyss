# -*- coding: utf-8 -*-

"""
Модуль реализации управления логическим ключём
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss import queue_event_priorities
from pyss.block import Block
from pyss.logic_object import LogicObject

def invert(owner, logicObject):
    """Инвертирование состояния логического ключа logicObject"""
    logicObject.stateInvert()

def reset(owner, logicObject):
    """Выключение логического ключа logicObject"""
    logicObject.stateReset()

def set(owner, logicObject):
    """Включение логического ключа logicObject"""
    logicObject.stateSet()

class Logic(Block):
    """Блок Logic управляет логическим ключом (LogicObject). 
    
Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)  
    actionFunc=invert - функция изменения состояния логического ключа.
                 Сигнатура str f(owner, logicObject).
                 Можно использовать функции logic.invert, logic.reset, logic.set
    logicObjectName=None - наименование логическогот ключа

Например, блок

logic.Logic(sgm, actionFunc=invert, logicObjectName="LOGIC_1")

при прохождении транзакта будет переключать логический ключ.

См. также gate.py, logic_object.py

Атрибуты блока Logic (в дополнение к атрибутам block.Block):
bl = Logic(...)
bl[LOGIC_OBJECT_NAME] - имя логического ключа.
bl[ACTION_FUNC] - функция изменения состояния логического ключа.
                  Сигнатура str f(owner, logicObject).

    """

    def __init__(self, ownerSegment=None, label=None, actionFunc=invert, logicObjectName=None):
        # # funcBusySize(transact) - функция, возвращающая необходимый объем МКУ
        super(Logic, self).__init__(LOGIC, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [logicObjectName is None or logicObjectName == "", actionFunc is None])
        self[LOGIC_OBJECT_NAME] = logicObjectName
        if ownerSegment.getOwner().findLogicObject(logicObjectName) is None:
            LogicObject(ownerSegment.getOwner(), logicObjectName)
        self[ACTION_FUNC]=actionFunc

    def _findLogicObject(self):
        """return tuple (logicObjectName, logicObject)"""
        s = self[LOGIC_OBJECT_NAME]
        return s, self.getOwnerModel().findLogicObject(s)

    def transactInner(self, currentTime, transact):

        # pylint: disable=unused-argument
        _, t = self._findLogicObject()
        self[ACTION_FUNC](self, t)
        return transact

if __name__ == '__main__':
    pass
