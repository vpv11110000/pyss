# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.5

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

В систему массового обслуживания поступают пакеты заявок по равномерному закону в интервале 5+/- 2 мин. Обработка заявок, поступивших на первую сортировку, осуществляется также по равномерному закону в интервале 6+/-2 мин.

Далее рассортированные заявки проходят параллельную обработку с ещё одним этапом сортировки.

После обработки заявки собираются в один пакет и выводятся из системы.

Необходимо смоделировать работу системы по обработке 100 пакетов.Построить гистограмму длины очереди.

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

def main():
    logger.info("-------------------------------------")
    
	### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult=True	
    
	
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10000
    #-----------------------------
    def modificatorFunc001(owner, currentTime):
        return random.uniform(-3.0, 3.0)   
    Generate(sgm,
             med_value=5, modificatorFunc=modificatorFunc001,
             first_tx=None,
			 max_amount=100,
             priority=1)
    SHAN1 = "CHAN1"    
    Split(sgm, funcCountCopies=1, funcNextBlockLabel=SHAN1)

    F1 = "F1"
    Seize(sgm, facilityName=F1)
    Advance(sgm, meanTime=6.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F1)
    OUT3 = "OUT3"
    Transfer(sgm, funcTransfer=lambda o, t: m.findBlockByLabel(OUT3))
    
    CHAN2 = "CHAN2"
    Split(sgm, SHAN1, funcCountCopies=1, funcNextBlockLabel=CHAN2)
    F2 = "F2"
    Seize(sgm, facilityName=F2)
    Advance(sgm, meanTime=6.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F2)
    Transfer(sgm, funcTransfer=lambda o, t: m.findBlockByLabel(OUT3))

    F3 = "F3"
    Seize(sgm, CHAN2, facilityName=F3)
    Advance(sgm, meanTime=6.0, modificatorFunc=2.0)
    Release(sgm, facilityName=F3)
    Assemble(sgm, OUT3, countTransact=3)
    Terminate(sgm, deltaTerminate=1)
			 
    ### КАРТИНКИ ----------------------
    # таблицы
    m.initPlotTable()
    m.initPlotQueueLifeLine()
    m.initPlotTransactLifeLine()
    m.initPlotFacilityLifeLine()
    
    # РАСЧЁТ --------------------------
    logger.info(str(m))
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
