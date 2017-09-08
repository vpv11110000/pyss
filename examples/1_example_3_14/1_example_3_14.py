# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.14

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

Поток заявок поступает в накопитель с допустимой ёмкостью, равной 3 единицам, равномерно каждые 5+/-1 мин. Если заявки после накопителя застают 2-й канал (устройсто) занятым, то они поступают на обработку во второй канал. Время обработки 1-го канала равно 13+/-1 мин, 2-го 9+/-1 мин. 

Смоделировать обработку 100 заявок.

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

V_FACILITY = "V_FACILITY"

def buildModel():
    """
    Поток заявок поступает в накопитель с допустимой ёмкостью, равной 3 единицам, равномерно каждые 5+/-1 мин. Если заявки после накопителя застают 2-й канал (устройсто) занятым, то они поступают на обработку во второй канал. Время обработки 1-го канала равно 13+/-1 мин, 2-го 9+/-1 мин. 
    
    Время обработки 1-го канала равно 13+/-1 мин, 2-го 9+/-1 мин.
     
    """
    logger.info("-------------------------------------")
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    # Stock STORAGE 4000 ;Warehouse holds 4000 units
    NAK3 = "NAK3"
    nak3 = Storage(m, storageName=NAK3, storageSize=3, initBusySize=0)
    
    # это наименование очереди
    QUE2 = "QUE2"
    # это метка
    FACIL2 = "FACIL2"
    # это наименование устройств
    F1 = "F1"
    F2 = "F2"
    #-----------------------------
    Generate(sgm,
             med_value=5.0, modificatorFunc=lambda o, c:random.uniform(-1.0, 1.0),
             first_tx=0.0,
             max_amount=100,
             priority=1)
    Enter(sgm, storageName=NAK3)
    # если устройство F2 не занято, то пройдёт насковозь, иначе на блок QUE2
    Gate(sgm, condition=GATE_FACILITY_NOT_USED, objectName=F2, nextBlockLabel=QUE2)
    Q1 = "Q1"
    Queue(sgm, queueName=Q1)
    Seize(sgm, facilityName=F1)
    Leave(sgm, storageName=NAK3, funcBusySize=1)
    Depart(sgm, queueName=Q1)
    # поментим, что транзакт обрабатывается F1
    def h(o, t):
        t[V_FACILITY] = F1
    Handle(sgm, handlerFunc=h)
    Advance(sgm, meanTime=13, modificatorFunc=1)
    Release(sgm, facilityName=F1)
    Terminate(sgm, deltaTerminate=0)
    #
    Q2 = "Q2"
    Queue(sgm, QUE2, queueName=Q2)
    Seize(sgm, FACIL2, facilityName=F2)
    Leave(sgm, storageName=NAK3, funcBusySize=1)
    Depart(sgm, queueName=Q2)
    def h2(o, t):
        t[V_FACILITY] = F2
    Handle(sgm, handlerFunc=h2)
    Advance(sgm, meanTime=9, modificatorFunc=1)
    Release(sgm, facilityName=F2)
    Terminate(sgm, deltaTerminate=0)
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
    m.initPlotTable()
    m.initPlotQueueLifeLine()
    
    # проаннотируем наименованием устройства
    m.initPlotTransactLifeLine(funcAnnotate=lambda t:"%d-%s" % (t[NUM], t[V_FACILITY]))
    m.initPlotFacilityLifeLine()
    m.initPlotStorageLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.plotByModulesAndSave("")
    m.plotByModulesAndShow()

    
if __name__ == '__main__':
    main()
