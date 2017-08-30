# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
turnstil.py – Моделирование турникета на стадионе

Постановка проблемы

Зрители прибывают к турникету перед входом на стадион каждые 7 -6.99/+7 секунд, и
становятся в очередь.

Время прохода через турникет составляет 5±3 секунды.

Требуется определить, какой объем времени займет прохождения 300 человек
через турникет.

Условие задачи взято из "Учебное руководство по системе GPSS World"
GPSS World Sample File - TURNSTIL.GPS, by Gerard F. Cummings
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
    sgm = Segment(m, "SEGMENT_FACILITY")
    sgmMes = Segment(m, "SEGM_MEASURE")    
    
    #
    m[OPTIONS].setAllFalse()
    
    #-------------------------------
    PRIORITY_MODEL = 10
    PRIORITY_MEASURE = 0
    #-------------------------------
    MAX_TIME = 2500
    MAX_MEN = 300
    #-------------------------------
    QUEUE_NAME = "Q1"
    #-----------

    TABLE_NAME = "queue_len_by_time"
    PARAMETR_NAME = TABLE_NAME
    TURNSTILE = "turnstile"
    tbl = Table(m, tableName=TABLE_NAME, argFunc=lambda o, t: m.getCurTime(),
          limitUpFirst=1, widthInt=1, countInt=MAX_TIME)
    #--------------------------
    def advanceModFunc(owner, timeValue):
        # генерация времени проходв
        return random.uniform(-3, 3)

    def generateFunc(owner, currentTime):
        # генерация входов зрителей
        return random.uniform(-6.99, 7)

    # --------------------------------------------------------------
    
    Generate(sgm, med_value=7, modificatorFunc=generateFunc, priority=PRIORITY_MODEL)
    Queue(sgm, queueName=QUEUE_NAME, deltaIncrease=1)
    Seize(sgm, facilityName=TURNSTILE)
    Depart(sgm, queueName=QUEUE_NAME, deltaDecrease=1)
    Advance(sgm, meanTime=5, modificatorFunc=advanceModFunc)
    Release(sgm, facilityName=TURNSTILE)
    Terminate(sgm, deltaTerminate=1)
        #------------------------
    Generate(sgmMes, med_value=1, modificatorFunc=None, priority=PRIORITY_MEASURE)
    def queue_len_by_timeFunc(owner, transact):
        q = m[QUEUE_OBJECTS][QUEUE_NAME]
        if q:
            return q[QUEUE_LENGTH]
        else:
            raise "Queue [%s] not found" % QUEUE_NAME
    Assign(sgmMes, parametrName=PARAMETR_NAME, modificatorFunc=queue_len_by_timeFunc)
    
    def coefFunc(owner, transact):
        if transact:
            return transact[PARAMETR_NAME]
    Tabulate(sgmMes, table=tbl, valFunc=coefFunc)
    Terminate(sgmMes, deltaTerminate=0)
    
    ### КАРТИНКИ ----------------------
    # линии жизни транзактов
    m.initPlotTransactLifeLine(title="Active")
    # таблицы
    m.initPlotTable(title="queue_len_by_time")
    
    m.initPlotFacilityLifeLine(title="Facility")
    m.initPlotQueueLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=MAX_MEN, maxTime=MAX_TIME)
    print "Wait, it build diagrams for long time..."
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
