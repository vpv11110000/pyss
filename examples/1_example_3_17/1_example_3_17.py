# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.17

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

Смоделировать процесс обслуживания потока заявок с интервалом 5+/-1 мин. дыумя каналами: обслуживание в 1-м канале длится 9+/-1 мин, 2-го 13+/-1 мин. Причём в течение первых 100 мин обслуживание производит 2-й канал, а по истечении 100 мин. - 1-й канал

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
    Поток заявок поступает в накопитель с допустимой ёмкостью, равной 3 единицам, равномерно каждые 5+/-1 мин. Если 1-й канал (устройсто) занят, то они поступают на обработку во второй канал. Время обработки 1-го канала равно 9+/-1 мин, 2-го 13+/-1 мин. 
     
    """
    logger.info("-------------------------------------")
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    # это наименование каналов
    F1 = "F1"
    F2 = "F2"
    
    #
    EXIT = "EXIT"
    FACIL2 = "FACIL2"
    
    #-----------------------------
    Generate(sgm,
             med_value=5.0, modificatorFunc=lambda o, c:random.uniform(-1.0, 1.0),
             first_tx=0.0,
             max_amount=100,
             priority=1)
    def ft(o, t):
        return m.findBlockByLabel(FACIL2) if m.getCurTime() <= 100 else m.findBlockByLabel(F1)
    # здесь не так как в примере книги Б.Я.Советов  
    Transfer(sgm, funcTransfer=ft)
    Seize(sgm, F1, facilityName=F1)
    Advance(sgm, meanTime=9, modificatorFunc=1)
    Release(sgm, facilityName=F1)
    Transfer(sgm, funcTransfer=EXIT)
    #
    Seize(sgm, FACIL2, facilityName=F2)
    Advance(sgm, meanTime=13, modificatorFunc=1)
    Release(sgm, facilityName=F2)
    Terminate(sgm, EXIT, deltaTerminate=1)
    return m

def main():
    logger.info("-------------------------------------")
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10000
    TERMINATION_COUNT = 100
    
    ### MODEL ----------------------------------
    m = buildModel()

    ### КАРТИНКИ ----------------------
    # таблицы
    m.initPlotTable()
    m.initPlotQueueLifeLine()
    
    # проаннотируем наименованием устройства
    m.initPlotTransactLifeLine()
    m.initPlotFacilityLifeLine()
    m.initPlotStorageLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=TERMINATION_COUNT, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.plotByModulesAndSave("")
    m.plotByModulesAndShow()

    
if __name__ == '__main__':
    main()
