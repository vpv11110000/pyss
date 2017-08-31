# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
day_no_stacionar_one_kassa.py – Моделирование кассы с нестационарным потоком заявок


исходные данные
с 0-100 заявка приходит по 1 в 4 единицы времени
с 101-119 заявка приходит по 1 в единицу времени
с 120 заявка приходит по 1 в 4 единицы времени
время обработки 2 единицы времени

Цель: построить зависимость длины очереди от времени

"""

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep + "pyss" + os.sep)

print sys.path

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


def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m, "SEGM_FACILITY")
    sgmSecond = Segment(m, "SEGM_MEASURE")
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    #-------------------------------
    PRIORITY_MODEL = 10
    PRIORITY_MEASURE = 0
    #-------------------------------
    MAX_TIME = 200
    #-------------------------------
    QUEUE_NAME = "Q1"
    def queue_len_by_timeFunc(owner, transact):
        q = m[QUEUE_OBJECTS][QUEUE_NAME]
        if q:
            return q[QUEUE_LENGTH]
        else:
            raise "Queue [%s] not found" % QUEUE_NAME

    TABLE_NAME = "queue_len_by_time"
    PARAMETR_NAME = TABLE_NAME
    KASSA = "kassa"
    #-----------

    tbl = Table(m, tableName=TABLE_NAME, argFunc=lambda o, t: m.getCurTime(),
          limitUpFirst=1, widthInt=1, countInt=MAX_TIME)
    #--------------------------
    def advanceModFunc(o, timeValue):
        # обработка заявок
        # return random.randint(1,3)
        # return random.normalvariate(1.9,0.5)
        return 0.0

    def coefFunc(owner, transact):
        if transact:
            return transact[PARAMETR_NAME]

    def modFunc(owner, currentTime):
        # генерация заявок
        if (currentTime > 100) and (currentTime < 120):
            return 0
        else:
            return 3
        # return random.normalvariate(2.0,.5)
        # Poisson process
        # return random.expovariate(1.0)

        # return random.paretovariate(2.0)
        # return random.weibullvariate(1.0,1.5)

    ### SEGMENT ---------------------------
    Generate(sgm, med_value=1, modificatorFunc=modFunc, priority=PRIORITY_MODEL)
    Queue(sgm, queueName=QUEUE_NAME, deltaIncrease=1)
    Seize(sgm, facilityName=KASSA)
    Depart(sgm, queueName=QUEUE_NAME, deltaDecrease=1)
    Advance(sgm, meanTime=2, modificatorFunc=advanceModFunc)
    Release(sgm, facilityName=KASSA)
    Terminate(sgm, deltaTerminate=1)
    
    ### SEGMENT ---------------------------
    Generate(sgmSecond, med_value=1, modificatorFunc=None, priority=PRIORITY_MEASURE)
    Assign(sgmSecond, parametrName=PARAMETR_NAME, modificatorFunc=queue_len_by_timeFunc)
    Tabulate(sgmSecond, table=tbl, valFunc=coefFunc)
    Terminate(sgmSecond, deltaTerminate=0)
    
    ### КАРТИНКИ ----------------------
    m.initPlotTable()
    m.initPlotQueueLifeLine()

    # активность
    def transactFilter(transact):
        return True
    def funcAnnotate(transact):
        s = "Day: " + str(transact["Day"])
        return s
    X_LABEL = "DAYLY"
    m.initPlotTransactLifeLine(
        terminateBlockLabels=["OVERHAUL", "SPOT", "REPAIRS", X_LABEL],
        transactFilter=transactFilter, title="Active ",
        funcAnnotate=funcAnnotate)
    
    m.initPlotFacilityLifeLine(facilityNames=None, title="OCF", funcAnnotate=None)
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=1000000, maxTime=MAX_TIME)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
