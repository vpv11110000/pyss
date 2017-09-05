# -*- coding: utf-8 -*-

"""
Модуль объекта "логический ключ"
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssstateobject import PyssStateObject
from pyss import logger
from pyss.pyss_const import *

class LogicObject(PyssStateObject):
    """Объект LogicObject предназначен для представления логического ключа.

Логический ключ имеет два состояния "выключен" (False) или "включен" (True).

Владельцем LogicObject является модель.

Args:
    ownerModel=None - объект модели-владельца 
    logicObjectName - строка с наименованием логического ключа

Например, строка

logic_object.LogicObject(m, logicObjectName="L_1")

создаёт логический ключ  c именем L_1.

См. также gate.py, logic.py

Атрибуты объекта LogicObject (в дополнение к атрибутам pyssstateobject.PyssStateObject):
f = LogicObject(...)
f[LOGIC_NAME] - имя логического ключа.
f[STATE] - текущее состояние логического ключа (м.б. False, True).
f[LIFE_TIME_LIST] - список меток времени и состояний

    """

    def __init__(self, ownerModel=None, logicObjectName=None, initialState=False):
        # # state (STATE_FREE or STATE_BUSY or STATE_NOT_ACCESS)
        super(LogicObject, self).__init__(LOGIC_OBJECT, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [logicObjectName is None or logicObjectName == ""])
        self[LOGIC_OBJECT_NAME] = logicObjectName
        self[STATE] = initialState
        self[LIFE_TIME_LIST] = [{START:self[OWNER].getCurTime(), STATE:self[STATE]}]
        ownerModel.addLogicObject(self)

    def stateInvert(self):
        """Инвертировать состояние ключа"""
         
        self.setLifeState(not bool(self[STATE]), self.getOwner().getCurTime())

    def stateReset(self):
        """Выключить ключ"""
        
        self.setLifeState(False, self.getOwner().getCurTime())

    def stateSet(self):
        """Включить ключ"""
         
        self.setLifeState(True, self.getOwner().getCurTime())

    def setLifeState(self, dstState, timeTick=None):
        """
        Args:
            dstState=None - True, False
            timeTick=None - метка времени
        """
        
        self[STATE] = dstState
        if timeTick is None:
            raise Exception("timeTick is None")
        if dstState not in [True, False]:
            logger.warn("dstState not in [True, False]")
        if self[LIFE_TIME_LIST][-1][STATE] != dstState:
            self[LIFE_TIME_LIST].append({START:timeTick, STATE:dstState})

if __name__ == '__main__':
    def main():
        print "?"

    main()
