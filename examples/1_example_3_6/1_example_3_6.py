# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.6

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

В систему массового обслуживания поступают пакеты заявок по равномерному закону в интервале 5+/- 2 мин. 

Обработка заявок осуществляется двумя обслуживающими каналами.

Поступление заявок в тот или иной канал происходит с вероятностью 0.3 и 0.7

Обслуживание заявок каждым каналом происходит по  равномерному закону со временем 7+/-2 мин.

Необходимо смоделировать работу системы по обработке 100 заявок и двух прогонах программы.
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
    m[OPTIONS].printResult=True    
    
    #
    PROBABLY_TO_CHANEL_1 = SimpleObject(0.3)
    PROBABLY_TO_CHANEL_2 = SimpleObject(0.7)
    
    #-----------------------------
    def modificatorFunc001(owner, currentTime):
        return random.uniform(-2.0, 2.0)   
    Generate(sgm,
             med_value=5, modificatorFunc=modificatorFunc001,
             first_tx=None,
             max_amount=100,
             priority=1)
    
    CHAN1="CHAN1"
    CHAN2="CHAN2"
    def transfer001(o,t):
        x=random.uniform(0.0,1.0)
        if x<=PROBABLY_TO_CHANEL_2.getValue():
            return m.findBlockByLabel(CHAN2)
        else:
            return m.findBlockByLabel(CHAN1)
    Transfer(sgm, funcTransfer=transfer001)
    F1 = "F1"
    Seize(sgm, CHAN1, facilityName=F1)
    Advance(sgm, meanTime=7.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F1)
    EXIT="EXIT"
    Transfer(sgm, funcTransfer=EXIT)
    
    F2 = "F2"
    Seize(sgm, CHAN2, facilityName=F2)
    Advance(sgm, meanTime=7.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F2)
    
    Terminate(sgm, EXIT, deltaTerminate=1)

    ### КАРТИНКИ ----------------------
    # таблицы
#     m.initPlotTable()
#     m.initPlotQueueLifeLine()
#     m.initPlotTransactLifeLine()
#     m.initPlotFacilityLifeLine()
    
    return m

def main():
    logger.info("-------------------------------------")
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10000
	
    ### MODEL ----------------------------------
    m = buildModel()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
#     m.getPlotSubsystem().plotByModules()
#     m.getPlotSubsystem().show()

    ### MODEL ----------------------------------
    m = buildModel()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
#     m.getPlotSubsystem().plotByModules()
#     m.getPlotSubsystem().show()

    
if __name__ == '__main__':
    main()
