# -*- coding: utf-8 -*-

"""
Модуль с классом моделирования заявок (транзактов)
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss import logger
from pyss.pyssobject import PyssObject
from pyss.pyss_const import *

# Транзакты
# PR
# Приоритет активного транзакта. Целочисленное значение.
# М1
# Время пребывания в модели активного транзакта. Равно разности  текущего значения абсолютного времени и времени рождения активного транзакта. Вещественное значение.
# MP
# Транзитное время пребывания  в модели активного транзакта. Равно разности  текущего значения абсолютного времени и содержимого параметра активного транзакта. Вещественное значение.
# XN1
# Номер активного транзакта. Целочисленное значение.

class Transact(PyssObject):
    """Объект Транзакт является моделью заявки

Транзакт вводится в модель системы с помощью блока Generate.

Args:
    block=None - блок, в котором находится созданный транзакт
    timeCreated=0 - время создания транзакта
    priority=0 - приоритет транзакта

Примеры использования см. tests/*.py

Атрибуты (параметры) объекта Transact (в дополнение к атрибутам pyssobject.PyssObject):
tr = transact.Transact(...)
tr[PR] - приоритет транзакта, действует только в рамках обработки текущего сегмента
tr[DELAYED] - True/False - индикатор задержки транзакта. 
              Для модификации использовать setLifeState(value).
tr[SCHEDULED_TIME] - время по расписанию (смысл зависит от контекста)
tr[TIME_CREATED] - время создания транзакта 
tr[M1] - Время пребывания в модели активного транзакта. 
    Равно разности  текущего значения абсолютного времени и времени рождения активного транзакта.
    Вещественное значение. 
tr[XN1] - номер транзакта (инциализируется из объекта модели transactNumber)
tr[MARK_TIME] - метка времени, инициализируется в блоке Generate, может меняться в блоке Mark 
tr[CURRENT_BLOCK] - блок, в котором находится транзакт (текущий блок) 
tr[FACILITY] - None или ОКУ, в котором находится транзакт 
tr[HANDLED] - True/False индикатор события полной обработки транзакта в блоке. 
              True - транзакт полностью обработан в текущем блоке
              False - в транзакте изменён текущий блок (tr[CURRENT_BLOCK]), 
              но обработка транзакта в нём ещё не проводилась  
tr[PARENT] - родительский транзакт 
tr[ASSEMBLY_SET] - None или семейство транзактов, к которому принадлежит транзакт tr.
                      По умолчанию (обычно) устанавливается равным t[NUM] родителя семейства
                      У владельца семейства transact[ASSEMBLY_SET] == transact[NUM]
                      См. Split, Assemble.
tr[BLOCK_NEXT] - предполагаемый блок, в который должен перейти транзакт 
                 из текущего блоки после полной обработки
tr[NUM_GENERATOR] - объект-генератор номеров, используется блоком split
tr[TRANSACT_DELETED] - индикатор исключения транзакта из модели 
tr[REMAIND_TIME] - остаток времени для обработки транзакта
tr[TERMINATED_TIME] - время исключения транзакта из модели
tr[TRACK] - список кортежей (<время входа>, <блок>). Блоки фиксируются в порядке вызова их метода transactHandle (за искл. generate)   
tr[LIFE_TIME_LIST]=[] - метка времени перехода транзакта состояние, задаваемое блоком Advance, Preempt и др.
                           Например [{"time":1.0,"state":"delayed"}, {"time":2.0,"state":"active"}, 
                           {"time":3.0,"state":"preempt"}, ... ] 
                           обработка транзакта прерывалась с 1 по 2, с 3 по 4 и т.д.
                        

ВНИМАНИЕ: по ходу выполнения моделирования в объект транзакта объектами модели 
могут быть добавлены другие атрибуты. 
Проверьте модель на отсутствие конфликтов имён атрибутов. 

    """

    def __init__(self, block=None, timeCreated=0, priority=0):
        super(Transact, self).__init__(TRANSACT)
        self[PR] = priority
        self[DELAYED] = False
        self[SCHEDULED_TIME] = None
        self[TIME_CREATED] = timeCreated
        self[M1] = 0
        self[XN1] = self[NUM]
        self[MARK_TIME] = None  # components.getCurTimeAbs()
        self[CURRENT_BLOCK] = block
        self[FACILITY] = []
        self[HANDLED] = False
        self[PARENT] = None
        self[ASSEMBLY_SET] = self[NUM]
        self[BLOCK_NEXT] = None
        self[NUM_GENERATOR] = None
        self[TRANSACT_DELETED] = False
        self[REMAIND_TIME] = 0
        self[TERMINATED_TIME] = None
        self[LIFE_TIME_LIST] = [{START:timeCreated, STATE:ACTIVED}]
        self[TRACK] = []
        
    def setScheduledTime(self, scheduled_time):
        self[SCHEDULED_TIME] = scheduled_time
        return self
    
    def getScheduledTime(self):
        return self[SCHEDULED_TIME]
        
    def setLifeState(self, delayed=None, dstState=None, timeTick=None):
        """
        Args:
            delayed=None - True/False 
            dstState=None - LIFE_STATES = [ACTIVED, PREEMPTED, DELAYED, TRANSACT_DELETED]
            timeTick=None - метка времени
        """
        
        if timeTick is None:
            raise Exception("timeTick is None")
        if delayed not in [True, False]:
            raise Exception("value must in [True,False]")
        if dstState not in LIFE_STATES:
            logger.warn("dstState not in [ACTIVED,PREEMPTED,DELAYED,TRANSACT_DELETED]")
        if self[DELAYED] != delayed or self[LIFE_TIME_LIST][-1][STATE] != dstState:
            self[DELAYED] = delayed
            self[LIFE_TIME_LIST].append({START:timeTick, STATE:dstState})
        return self

    def refreshAttr(self, currentTimeAbs):
        if self[MARK_TIME] is None:
            self[M1] = currentTimeAbs - self[TIME_CREATED]
        else:
            self[M1] = currentTimeAbs - self[MARK_TIME]
        return self

    def setCurrentBlock(self, block):
        self[CURRENT_BLOCK] = block
        return self

    def getNextSequentialBlock(self):
        return self[CURRENT_BLOCK].getNextSequentialBlock(self)

    def isDelayed(self):
        return self[DELAYED]

    def setFacility(self, fac):
        self[FACILITY].append(fac)
        return self

    def getFacilities(self, fac):
        return self[FACILITY]

    def getLastFacility(self, fac):
        if self[FACILITY]:
            return self[FACILITY][-1]
        else:
            return None

    def removeFacility(self, fac):
        # f=[x for x in self[FACILITY] if x == fac]
        # if f:
        if fac in self[FACILITY]:
            self[FACILITY].remove(fac)
        return self

    def __str__(self):
        return "%s:%s:%s:%s:%s:%s" % (self[NUM], self[LABEL], self[ENTITY_TYPE], PR + "_" + str(self[PR]), "Sch:" + str(self[SCHEDULED_TIME]), "Del:" + str(self[DELAYED]))
    
    def strTrack(self):
        """Вывод элементов <время>:<номер или метка блока>:<тип блока>"""
        l = ["[%s]:[%s]:[%s]" % (('%f' % ct).rstrip('0').rstrip('.'), r[LABEL] if r[LABEL] else str(r[NUM]), r[ENTITY_TYPE]) for ct, r in self[TRACK]]
        s = reduce((lambda x, y: x + "; " + y), l)
        return s 

    def strTrackDebug(self):
        """Вывод элементов <время>:<номер или метка блока>:<тип блока>"""
        l = ["            [%s]:[%s]:[%s]" % (('%f' % ct).rstrip('0').rstrip('.'), "%d/%s" % (r[NUM], r[LABEL]) if r[LABEL] else str(r[NUM]), r[ENTITY_TYPE]) for ct, r in self[TRACK]]
        if len(l)>1:
            s = reduce((lambda x, y: x + ";\n" + y), l[:-1])
        else:
            s = ""
        s += "\nlast block: " + l[-1].lstrip()
        return s 

if __name__ == '__main__':
    pass
