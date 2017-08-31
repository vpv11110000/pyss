# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Пример 3.4

Б.Я.Советов, Моделирование систем. Практикум: Учеб пособие для вузов/Б.Я. Советов, С.А. Яковлев.- 2-е изд., перераб. и доп.-М.:Высш. шк., 2003.-295 с.: ил.

В систему массового обслуживания поступает и обрабатывается фиксированное число заявок. Примем, что заявки поступают в систему по равномерному закону из интервала времени, равного от 3 мин до 7 мин. Обработка заявок осуществляется также по равномерному закону в интервале времени от 5 до 9 мин. Необходимо смоделировать работу системы при поступлении и обработке 100 заявок.

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
        return random.uniform(3.0, 7.0)   
    Generate(sgm,
             med_value=0.0, modificatorFunc=modificatorFunc001,
             max_amount=100,
             priority=1)
    F_1="F_1"
    Seize(sgm, facilityName=F_1)
    #
    def modificatorFunc002(owner, currentTime):
        return random.uniform(5.0, 9.0)   
    Advance(sgm, meanTime=0.0, modificatorFunc=modificatorFunc002)
    Release(sgm, facilityName=F_1)
    #
    Terminate(sgm, deltaTerminate=1)
    return m

def main():
    logger.info("-------------------------------------")
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10000

    # for test
    list_all_transact = []
    def funcTransactTo_list_all_transact(owner, transact):
        # складируем транзакты в список
        list_all_transact.append(transact)
    #
    
    ### MODEL ----------------------------------
    m = buildModel()
    
    ### КАРТИНКИ ----------------------
    # таблицы
#     m.initPlotTable()
#     m.initPlotQueueLifeLine()
    m.initPlotTransactLifeLine()
    m.initPlotFacilityLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    #m.getPlotSubsystem().plotByModulesAndSave("1_example_3_4")

    
if __name__ == '__main__':
    main()
