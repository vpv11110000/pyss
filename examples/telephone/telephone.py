# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
telephon.py – Моделирование простой телефонной системы

Постановка проблемы

Простая телефонная система имеет две внешние линии. 
Входящие звонки поступают каждые 100±60 секунд.
Когда линия занята, звонящий производит повторный набор номера по истечении 5±1 минут.
Длительность звонка составляет 3±1 минуты.

Требуется таблица распределения моментов времени, 
в которые звонящие смогли дозвониться.

Сколько времени уйдет на 200 успешных звонков?

Условие задачи взято из "Учебное руководство по системе GPSS World"
GPSS World Sample File - TELEPHON.GPS, by Gerard F. Cummings

"""

import sys
import os
import random

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

def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m, "SEGM_FACILITY")
    
    #
    m[OPTIONS].setAllFalse()
    #-------------------------------
    PRIORITY_MODEL = 10
    #-------------------------------
    MAX_TIME = 100000
    MAX_CALL = 200
    #-------------------------------
    QUEUE_NAME = "Q1"
    def queue_len_by_timeFunc(owner, transact):
        q = m[QUEUE_OBJECTS][QUEUE_NAME]
        if q:
            return q[QUEUE_LENGTH]
        else:
            raise "Queue [%s] not found" % QUEUE_NAME

    #-----------
    TABLE_NAME = "Transit"
    # Transit TABLE M1,.5,1,20 ;Transit times
    tbl = Table(m, tableName=TABLE_NAME, argFunc=lambda ownerTable, transact: transact[M1] / 60.0, limitUpFirst=1.0, widthInt=1.0, countInt=20)

    #---------
    STORAGE_NAME = "Sets"
    STORAGE_SIZE = 3
    # strg=storage.Storage(storageName=STORAGE_NAME,storageSize=2)
    strg = Storage(m, storageName=STORAGE_NAME, storageSize=STORAGE_SIZE)

    #--------------------------
    def advanceCall(owner, timeValue):
        # генерация времени звонка
        return random.uniform(-1.0 * 60, 1.0 * 60)

    def generateFunc(owner, currentTime):
        # генерация звонков
        return random.uniform(-1.0 * 60.0, 1.0 * 60.0)

    # Блок, формирующий телефонный звонок,
    # создается каждые 100±60 секунд.
    Generate(sgm, med_value=100, modificatorFunc=generateFunc, priority=PRIORITY_MODEL)
    # Again GATE SNF Sets,Occupied ;Try for a line
    Gate(sgm, label="Again", condition=SNF, objectName=STORAGE_NAME, nextBlockLabel="Occupied")
    # ENTER Sets ;Connect call
    Enter(sgm, storageName=STORAGE_NAME, funcBusySize=lambda owner, t:1)
    # ADVANCE 3,1 ;Speak for 3+/-1 min
    Advance(sgm, meanTime=3 * 60, modificatorFunc=advanceCall)
    # LEAVE Sets ;Free a line
    Leave(sgm, storageName=STORAGE_NAME, funcBusySize=lambda o, x:1)
    # TABULATE Transit ;Tabulate transit time
    Tabulate(sgm, table=tbl, valFunc=lambda ownerTabulate, transact:1)
    # TERMINATE 1 ;Remove a Transaction
    Terminate(sgm, deltaTerminate=1)
    # Occupied ADVANCE 5,1 ;Wait 5 minutes
    Advance(sgm, label="Occupied", meanTime=5 * 60, modificatorFunc=advanceCall)
    # TRANSFER ,Again ;Try again
    Transfer(sgm, funcTransfer=lambda o, t: o.findBlockByLabel("Again"))
    
    ### ДИАГРАММЫ ----------------------
    # линии жизни транзактов
    m.initPlotTransactLifeLine(transactFilter=lambda t: True, title="Active")
    # таблицы
    m.initPlotTable(title="Storage_size: [%d]" % STORAGE_SIZE)
    # storage
    m.initPlotStorageLifeLine()    
    # РАСЧЁТ --------------------------
    logger.info(str(m))
    m.start(terminationCount=MAX_CALL, maxTime=MAX_TIME)
    print "[%d] звонков обслужили за [%0.3f] минут" % (MAX_CALL, m[END_TIME] / 60.0)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
