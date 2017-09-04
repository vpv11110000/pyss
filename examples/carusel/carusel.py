# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# carusel.py – Моделирование кассы в случае нестационарного потока покупателей

**Постановка проблемы**

Время           Интенсивность,    Количество покупок    Относительная частота     Суммарная частота 
                чел/10 мин    
 9:00 - 11:00   2                (0-5]                   0.2                     0.2
 2*60 мин                        (5-20]                  0.3                     0.5    
                                 (20-50]                 0.2                     0.7
                                 (50-100]                0.2                     0.9
                                 (100..120]              0.1                     1.0

11:00 - 15:00   5                (0-5]                   0.2                     0.2
 4*60 мин                        (5-20]                  0.2                     0.4    
                                 (20-50]                 0.25                    0.65
                                 (50-100]                0.25                    0.9
                                 (100..120]              0.1                     1.0

15:00 - 17:00   3                (0-5]                   0.4                     0.4
 2*60 мин                        (5-20]                  0.3                     0.7    
                                 (20-50]                 0.18                    0.88
                                 (50-100]                0.1                     0.98
                                 (100..120]              0.02                    1.0

Каждая единица товара обрабатывается на кассе 5 сек.

Необходимо смоделировать систему инвентаризации в течение дня.

Построить гистограмму длины очереди.

------
"""

import sys
import os
import random
import unittest
import math

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep + "pyss" + os.sep)

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

PRODUCT_COUNT = "PRODUCT_COUNT"

def buildModel():
    logger.info("-------------------------------------")
    
    m = PyssModel()
    sgm = Segment(m, "SEGM_FACILITY")
    sgmSecond = Segment(m, "SEGM_MEASURE")
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    #-------------------------------
    PRIORITY_MODEL = 10
    
    #-------------------------------
    QUEUE_NAME = "Q1"
    def queue_len_by_timeFunc(owner, transact):
        q = m[QUEUE_OBJECTS][QUEUE_NAME]
        if q:
            return q[QUEUE_LENGTH]
        else:
            raise "Queue [%s] not found" % QUEUE_NAME

    KASSA = "kassa"
    PRODUCT_HANDLE_TIME = 5.0 / 60.0

    #-----------
    def modFunc(owner, currentTime):
        # генерация заявок
        # Время           Интенсивность,    Количество покупок    Относительная частота     Суммарная частота 
        #                 чел/мин    
        #  9:00 - 11:00   2                (0-5]                   0.2                     0.2
        #  2*60 мин                        (5-20]                  0.3                     0.5    
        #                                  (20-50]                 0.2                     0.7
        #                                  (50-100]                0.2                     0.9
        #                                  (100..120]              0.1                     1.0
        # 
        if (currentTime <= 2.0 * 60.0):
            # интенсивность 2 событие за 10 единиц времени
            LMBDA = 2.0 / 10.0
            tau = -math.log(1 - random.random()) / LMBDA
            return tau
        # 11:00 - 15:00   5                (0-5]                   0.2                     0.2
        #  4*60 мин                        (5-20]                  0.2                     0.4    
        #                                  (20-50]                 0.25                    0.65
        #                                  (50-100]                0.25                    0.9
        #                                  (100..120]              0.1                     1.0
        elif (currentTime <= (2.0 * 60.0 + 4.0 * 60.0)):
            # интенсивность 5 событие за 10 единиц времени
            LMBDA = 5.0 / 10.0
            tau = -math.log(1 - random.random()) / LMBDA
            return tau
        # 
        # 15:00 - 17:00   3                (0-5]                   0.4                     0.4
        #  2*60 мин                        (5-20]                  0.3                     0.7    
        #                                  (20-50]                 0.18                    0.88
        #                                  (50-100]                0.1                     0.98
        #                                  (100..120]              0.02                    1.0
        else:
            # интенсивность 3 событие за 10 единиц времени
            LMBDA = 3.0 / 10.0
            tau = -math.log(1 - random.random()) / LMBDA
            return tau
    
    # генерация количества товара
    def buildProductCount(owner, tranzact):
        # генерация заявок
        # Время           Интенсивность,    Количество покупок    Относительная частота     Суммарная частота 
        #                 чел/40 мин    
        #  9:00 - 11:00   2                (0-5]                   0.2                     0.2
        #  2*60 мин                        (5-20]                  0.3                     0.5    
        #                                  (20-50]                 0.2                     0.7
        #                                  (50-100]                0.2                     0.9
        #                                  (100..120]              0.1                     1.0
        # 
        f1 = FuncDiscrete(randomGenerator=random.random,
                          dictValues={.2:lambda:random.randint(0, 5),
                                      .5:lambda:random.randint(5, 20),
                                      .7:lambda:random.randint(20, 50),
                                      .9:lambda:random.randint(50, 100),
                                      1.0:lambda:random.randint(100, 120)})
        # 11:00 - 15:00   5                (0-5]                   0.2                     0.2
        #  4*60 мин                        (5-20]                  0.2                     0.4    
        #                                  (20-50]                 0.25                    0.65
        #                                  (50-100]                0.25                    0.9
        #                                  (100..120]              0.1                     1.0
        f2 = FuncDiscrete(randomGenerator=random.random,
                          dictValues={.2:lambda:random.randint(0, 5),
                                      .4:lambda:random.randint(5, 20),
                                      .65:lambda:random.randint(20, 50),
                                      .9:lambda:random.randint(50, 100),
                                      1.0:lambda:random.randint(100, 120)})
        # 15:00 - 17:00   3                (0-5]                   0.4                     0.4
        #  2*60 мин                        (5-20]                  0.3                     0.7    
        #                                  (20-50]                 0.18                    0.88
        #                                  (50-100]                0.1                     0.98
        #                                  (100..120]              0.02                    1.0
        f3 = FuncDiscrete(randomGenerator=random.random,
                          dictValues={.4:lambda:random.randint(0, 5),
                                      .7:lambda:random.randint(5, 20),
                                      .88:lambda:random.randint(20, 50),
                                      .98:lambda:random.randint(50, 100),
                                      1.0:lambda:random.randint(100, 120)})
        currentTime = m.getCurTime()
        if (currentTime <= 2.0 * 60.0):
            # количество товара у покупателя
            tranzact[PRODUCT_COUNT] = f1.get()
        # 11:00 - 15:00   5                (0-5]                   0.2                     0.2
        #  4*60 мин                        (5-20]                  0.2                     0.4    
        #                                  (20-50]                 0.25                    0.65
        #                                  (50-100]                0.25                    0.9
        #                                  (100..120]              0.1                     1.0
        elif (currentTime <= (2.0 * 60.0 + 4.0 * 60.0)):
            # количество товара у покупателя
            tranzact[PRODUCT_COUNT] = f2.get()
        # 
        # 15:00 - 17:00   3                (0-5]                   0.4                     0.4
        #  2*60 мин                        (5-20]                  0.3                     0.7    
        #                                  (20-50]                 0.18                    0.88
        #                                  (50-100]                0.1                     0.98
        #                                  (100..120]              0.02                    1.0
        else:
            # количество товара у покупателя
            tranzact[PRODUCT_COUNT] = f3.get()
            
    def advanceModificatorFunc(o, currentTime):
        t = m.getCurrentTransact()
        p = float(t[PRODUCT_COUNT])
        return float(PRODUCT_HANDLE_TIME) * p
        
    
    ### SEGMENT ---------------------------
    Generate(sgm, med_value=0, modificatorFunc=modFunc, priority=PRIORITY_MODEL)
    # количество товара у покупателя
    Handle(sgm, handlerFunc=buildProductCount)
    Queue(sgm, queueName=QUEUE_NAME, deltaIncrease=1)
    Seize(sgm, facilityName=KASSA)
    Depart(sgm, queueName=QUEUE_NAME, deltaDecrease=1)
    Advance(sgm, meanTime=0, modificatorFunc=advanceModificatorFunc)
    Release(sgm, facilityName=KASSA)
    Terminate(sgm, deltaTerminate=1)
    
    return m

def main():
    logger.info("-------------------------------------")

    # Время моделирования
    MAX_TIME = 2.0 * 60.0 + 4.0 * 60.0 + 2.0 * 60.0 
    
    ### MODEL ----------------------------------
    m = buildModel()
    
    ### КАРТИНКИ ----------------------
    # m.initPlotTable()
    m.initPlotQueueLifeLine()
    m.initPlotTransactLifeLine(funcAnnotate=lambda transact:"PRODUCT_COUNT: " + str(transact[PRODUCT_COUNT]))
    m.initPlotFacilityLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=1000000, maxTime=MAX_TIME)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
