# -*- coding: utf-8 -*-

"""
Модуль объекта "устройства"
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssstateobject import PyssStateObject
from pyss import logger
from pyss.pyss_const import *

class Facility(PyssStateObject):
    """Объект Facility предназначен для представления одноканального устройства.

Объект Facility добавляется в модель при прохождении транзактом
блоков seize.Seize, preempt.Preempt, а также методом addFacility.

Можно назначать обработчики изменения состояния (см. PyssStateObject).
Под значением старого состояния понимается старое значение self[STATE].


Устройство может находиться в состояниях:
    STATE_FREE - устройство свободно
    STATE_BUSY - устройство занято
    STATE_NOT_ACCESS - устройство не доступно

Владельцем Facility является модель.

Args:
    ownerModel=None - объект модели-владельца 
    facilityName - строка с наименованием одноканального устройства

Например, строка

facility.Facility(m, facilityName="F_1")

создаёт объект одноканальное устройство c именем F_1.

Особенности см. tests/test_preempt_return.py

См. также seize.py, preempt.py, release.py

Атрибуты объекта Facility (в дополнение к атрибутам pyssstateobject.PyssStateObject):
f = Facility(...)
f[FACILITY_NAME] - имя одноканального устройства.
f[STATE] - текущее состояние одноканального устройства (м.б. STATE_FREE, STATE_BUSY, STATE_NOT_ACCESS).
f[TIME_BUSY_START] - метка времени занятия устройства
f[TIME_NOT_ACCESS_START] - метка времени недоступности устройства
f[LISTTIMES] - список длительностей интервалов занятия устройства
f[COUNT_BUSY] - количество фактов занятий устройства
f[COUNT_NOT_ACCESS] - количество фактов недоступности устройства
f[LISTTIMES_NOT_ACCESS] - список длительностей интервалов недоступности устройства
f[UTIL] - суммарное время использования устройства (сумма всех элементов f[LISTTIMES])
f[RETRY] - РЕЗЕРВ
f[DELAY] - РЕЗЕРВ
f[ON_STATE_CHANGE] - список функций-обработчиков изменения состояния устройства
f[RETRY_ATTEMP_LIST] - список повторных попыток - список транзактов, ожидающих изменения состояния ОКУ
f[LISTPREEMPT] - список прерванных транзактов на обработке устройством
f[LISTTRANSACT]=[] - список транзактов на устройстве
f[TRANSACT]=None - транзакт на обработке устройством в текущий момент времени
f[LIFE_TIME_LIST] - список меток времени и состояний активности ОКУ

    """

    def __init__(self, ownerModel=None, facilityName=None):
        # # state (STATE_FREE or STATE_BUSY or STATE_NOT_ACCESS)
        super(Facility, self).__init__(FACILITY, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [facilityName is None or facilityName == ""])
        self[FACILITY_NAME] = facilityName
        self[STATE] = STATE_FREE
        self[TIME_BUSY_START] = None
        self[TIME_NOT_ACCESS_START] = None
        self[LISTTIMES] = []
        self[LISTTIMES_NOT_ACCESS] = []
        self[COUNT_BUSY] = 0
        self[COUNT_NOT_ACCESS] = 0
        self[UTIL] = 0
        self[RETRY] = 0
        self[DELAY] = 0
        # список повторных попыток - список транзактов, ожидающих изменения состояния ОКУ.
        self[RETRY_ATTEMP_LIST] = []
        # список прерванных транзактов на обработке устройством
        self[LISTPREEMPT] = []
        # список транзактов на устройстве
        self[LISTTRANSACT] = []
        # текущий обрабатываемый транзакт
        self[TRANSACT] = None
        self[LIFE_TIME_LIST] = [{START:0, STATE:self[STATE]}]
        ownerModel.addFacility(self)

    def setLifeState(self, dstState=None, timeTick=None):
        """
        Args:
            dstState=None - LIFE_STATES = [ACTIVED, PREEMPTED, DELAYED, TRANSACT_DELETED]
            timeTick=None - метка времени
        """
        
        self[STATE] = dstState
        if timeTick is None:
            raise Exception("timeTick is None")
        if dstState not in LIFE_STATES_FACILITY:
            logger.warn("dstState not in [ACTIVED,PREEMPTED,DELAYED,TRANSACT_DELETED]")
        if self[LIFE_TIME_LIST][-1][STATE] != dstState:
            self[LIFE_TIME_LIST].append({START:timeTick, STATE:dstState})
            
    def toFree(self, currentTime, transact):
        oldState = self[STATE]
        self.setLifeState(dstState=STATE_FREE, timeTick=currentTime)
        # remove transact if it not preempted
        if self[TRANSACT] == transact:
            self[LISTTRANSACT].remove(transact)
            self[TRANSACT] = None
        else:
            raise Exception("Attemp to free facility by not same transact [%s]-[%s]" % (str(self[TRANSACT]), str(transact)))
        a = self[TIME_BUSY_START]
        if a is not None:
            t = currentTime - a
            self[UTIL] += t
            self[LISTTIMES].append(t)
            self[TIME_BUSY_START] = None
        a = self[TIME_NOT_ACCESS_START]
        if a is not None:
            t = currentTime - a
            if self[TIME_BUSY_START] is None:
                self[UTIL] += t
            self[LISTTIMES_NOT_ACCESS].append(t)
            self[TIME_NOT_ACCESS_START] = None
        self.fireHandlerOnStateChange(oldState)

    def isFree(self):
        # # свободен и не в обработке прерывания
        return self[STATE] == STATE_FREE

    def isBusy(self):
        # # либо занят, либо в обработке прерывания
        return self[STATE] == STATE_BUSY

    def toBusy(self, currentTime, transact):
        oldState = self[STATE]
        self.setLifeState(dstState=STATE_BUSY, timeTick=currentTime)
        # self[LISTTRANSACT].append(transact)
        self[TIME_BUSY_START] = currentTime
        self[TIME_NOT_ACCESS_START] = None
        self[COUNT_BUSY] += 1
        self.fireHandlerOnStateChange(oldState)
        self[TRANSACT] = transact
        self[LISTTRANSACT].append(transact)

    def canPreempt(self, forTransact):
        # isPreempt
        # forTransact is not None: транзакт, для которого определяется
        # состояние прерывания
        pyssobject.raiseIsNone(forTransact)
        if self[TRANSACT]:
            # приоритет обрабатываемого транзакта меньше
            # приоритета входящего
            return self[TRANSACT][PR] <= forTransact[PR]
        else:
            return True

    def toPreempt(self, currentTime, transact):

        # pylint: disable=unused-argument

        # # в обработку прерывания
        # замена обрабатываемого транзакта на новый
        if self[TRANSACT]:
            t = self[TRANSACT]
            d = t[SCHEDULED_TIME]
            # number that's bigger than all others
            t[SCHEDULED_TIME] = float('inf')
            # остаток времени обработки
            t[REMAIND_TIME] = d - currentTime
            t.setLifeState(delayed=True, dstState=PREEMPTED, timeTick=self.getOwner().getCurTime())
            self[LISTPREEMPT].append(t)
        self[TRANSACT] = transact
        # эти транзакты на устройстве
        self[LISTTRANSACT].append(transact)

        oldState = self[STATE]
        self.setLifeState(dstState=STATE_NOT_ACCESS, timeTick=currentTime)
        # self[LISTTRANSACT].append(transact)
        # self[TIME_BUSY_START]
        self[TIME_NOT_ACCESS_START] = currentTime
        self[COUNT_NOT_ACCESS] += 1
        self.fireHandlerOnStateChange(oldState)

    def toReturn(self, currentTime, transact):

        # pylint: disable=unused-argument

        # # из обработки прерывания
        oldTransact = None
        if self[LISTPREEMPT]:
            oldTransact = self[LISTPREEMPT].pop()
        if oldTransact:
            # обработка закончится (с учётом остатка времени обработки) в
            oldTransact[SCHEDULED_TIME] = currentTime + oldTransact[REMAIND_TIME]

            oldState = self[STATE]
            self.setLifeState(dstState=STATE_BUSY, timeTick=currentTime)
            self[LISTTRANSACT].remove(transact)
            self[TRANSACT] = oldTransact
            # self[LISTTRANSACT].append(transact)
            # self[TIME_BUSY_START]
            a = self[TIME_NOT_ACCESS_START]
            if a is not None:
                tm = currentTime - a
                self[LISTTIMES_NOT_ACCESS].append(tm)
                self[TIME_NOT_ACCESS_START] = None
            self.fireHandlerOnStateChange(oldState)
        else:
            self.toFree(currentTime, transact)

    def isNotAccess(self, currentTime):
        # pylint: disable=unused-argument
        return self[STATE] == STATE_NOT_ACCESS

    def toNotAccess(self, currentTime):
        oldState = self[STATE]
        self.setLifeState(dstState=STATE_NOT_ACCESS, timeTick=currentTime)
        self[TIME_NOT_ACCESS_START] = currentTime
        self[TIME_BUSY_START] = None
        self[COUNT_NOT_ACCESS] += 1
        self.fireHandlerOnStateChange(oldState)

    def moveToRetryAttempList(self, transact):
        if transact not in self[RETRY_ATTEMP_LIST]:
            self[OWNER].getCel().remove(transact)
            self[RETRY_ATTEMP_LIST].append(transact)

    def moveToCel(self, transact):
        if transact in self[RETRY_ATTEMP_LIST]:
            self[RETRY_ATTEMP_LIST].remove(transact)
            self[OWNER].getCel().put(transact)

if __name__ == '__main__':
    pass