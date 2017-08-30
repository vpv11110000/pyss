# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.8

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/
Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

В систему массового обслуживания поступают пакеты заявок по равномерному 
закону в интервале 5+/- 2 мин. 

Обработка заявок осуществляется в одном из четырёх каналов обслуживания, 
для которых времена обслуживания составляют: 
17+/-2 мин,
12+/-2 мин,
9+/-2 мин,
3+/-2 мин 
соответственно.

Необходимо смоделировать работу системы по обработке 100 заявок четырьмя каналами, 
когда вновь поступающая заявка обслуживается любым свободным каналом.
------

"""

import sys
import os
import random
import unittest


DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import pyssobject
from pyss.pyss_model import PyssModel
from pyss.segment import Segment

from pyss import generate 
from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss import logger
from pyss.table import Table
from pyss.assemble import Assemble
from pyss.qtable import Qtable
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.storage import Storage
from pyss.advance import Advance
from pyss.assign import Assign
from pyss.preempt import Preempt
from pyss.g_return import GReturn
from pyss.facility import Facility
from pyss.seize import Seize
from pyss.release import Release
from pyss.transfer import Transfer
from pyss.tabulate import Tabulate
from pyss.test import Test
from pyss.queue import Queue
from pyss.depart import Depart
from pyss.split import Split
from pyss.test import Test
from pyss.bprint import Bprint
from pyss.gate import Gate
from pyss.pyss_const import *

from pyss.func_discrete import FuncDiscrete
from pyss.func_exponential import Exponential
from pyss.func_normal import Normal
from pyss.plot_func import PlotFunc

from pyss.simpleobject import SimpleObject

def buildModel():
    logger.info("-------------------------------------")
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    #-----------------------------
    def modificatorFunc001(owner, currentTime):
        return random.uniform(-2.0, 2.0)   
    Generate(sgm,
             med_value=5, modificatorFunc=modificatorFunc001,
             first_tx=None,
             max_amount=100,
             priority=1)
    
    CHAN1 = "CHAN1"
    CHAN2 = "CHAN2"
    CHAN3 = "CHAN3"
    CHAN4 = "CHAN4"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    TRANSFER001_HANDLER_ON_STATE = "transfer001_handlerOnState"
    def transfer001(o, t):
        f1 = m.findFacility(F1)
        # проверим свободность F1
        if f1.isFree():
            # переход в первый канал
            return m.findBlockByLabel(CHAN1)
        # F1 занят, проверим свободность F2
        f2 = m.findFacility(F2)
        # проверим свободность F1
        if f2.isFree():
            # переход во второй канал
            return m.findBlockByLabel(CHAN2)
        # F1 занят, проверим свободность F2
        f3 = m.findFacility(F3)
        # проверим свободность F1
        if f3.isFree():
            # переход во второй канал
            return m.findBlockByLabel(CHAN3)
        # F1 занят, проверим свободность F2
        f4 = m.findFacility(F4)
        # проверим свободность F1
        if f4.isFree():
            # переход во второй канал
            return m.findBlockByLabel(CHAN4)
        # каналы заняты, 
        # транзакт в список задержки, ключ блок transfer
        hazh = str(o)
        m.appendToDelayedList(hazh, t)
        
        # если какналы освободятся, то вернуть из списка задержанных
        # добавим обработчики освобождения
        if not m.existsHandlerOnStateChange(TRANSFER001_HANDLER_ON_STATE):
            # обработчик события изменения состояний f1 и f2 (см. PyssStateObject)
            def transfer001_handlerOnState(obj, oldState):
                if obj.isFree():
                    t = m.extractFromDelayedListFirst(hazh)
                    if t is not None:
                        m.getCel().put(t)
            f1.addHandlerOnStateChange(TRANSFER001_HANDLER_ON_STATE, transfer001_handlerOnState)
            f2.addHandlerOnStateChange(TRANSFER001_HANDLER_ON_STATE, transfer001_handlerOnState)
            f3.addHandlerOnStateChange(TRANSFER001_HANDLER_ON_STATE, transfer001_handlerOnState)
            f4.addHandlerOnStateChange(TRANSFER001_HANDLER_ON_STATE, transfer001_handlerOnState)
        # это не влияет, транзакт в задержке
        return None
        
    Transfer(sgm, funcTransfer=transfer001)
    #
    Seize(sgm, CHAN1, facilityName=F1)
    Advance(sgm, meanTime=17.0, modificatorFunc=3.0)
    Release(sgm, facilityName=F1)
    EXIT = "EXIT"
    Transfer(sgm, funcTransfer=EXIT)
    #    
    Seize(sgm, CHAN2, facilityName=F2)
    Advance(sgm, meanTime=12.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F2)
    Transfer(sgm, funcTransfer=EXIT)
    #    
    Seize(sgm, CHAN3, facilityName=F3)
    Advance(sgm, meanTime=9.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F3)
    Transfer(sgm, funcTransfer=EXIT)
    #    
    Seize(sgm, CHAN4, facilityName=F4)
    Advance(sgm, meanTime=3.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F4)
    Transfer(sgm, funcTransfer=EXIT)
    #
    Terminate(sgm, EXIT, deltaTerminate=1)

    return m

def main():
    logger.info("-------------------------------------")
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10000
	
    ### MODEL ----------------------------------
    m = buildModel()

    ### КАРТИНКИ ----------------------
    # таблицы
#     m.initPlotTable()
#     m.initPlotQueueLifeLine()
#     m.initPlotTransactLifeLine()
#     m.initPlotFacilityLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    # m.getPlotSubsystem().plotByModules()
    # m.getPlotSubsystem().show()

    
if __name__ == '__main__':
    main()
