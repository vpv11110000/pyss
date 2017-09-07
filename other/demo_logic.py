# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Запуск:
    python ./demo_logic.py

"""

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import random
import math

import os
from pyss.logic_object import LogicObject

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
from pyss import logic
from pyss.logic import Logic

from pyss.simpleobject import SimpleObject


def buildModel():
    logger.info("-------------------------------------")
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True    
    
    #---------
    LK1 = "LK1"
    LK2 = "LK2"
    LogicObject(m, logicObjectName=LK1, initialState=False)
    LogicObject(m, logicObjectName=LK2, initialState=True)
    
    #-----------------------------
    Generate(sgm,
             med_value=1,
             max_amount=100,
             priority=1)

    Logic(sgm, actionFunc=logic.invert, logicObjectName=LK1)
    Logic(sgm, actionFunc=logic.invert, logicObjectName=LK2)
    Terminate(sgm, deltaTerminate=1)

    return m

def main():
    logger.info("-------------------------------------")
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 10

    ### MODEL ----------------------------------
    m = buildModel()
    
    ### КАРТИНКИ ----------------------
    # таблицы
#     m.initPlotTable()
#     m.initPlotQueueLifeLine()
    m.initPlotLogicObjectLifeLine()
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=100, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    # m.getPlotSubsystem().plotByModules()
    # m.getPlotSubsystem().show()
    m.plotByModulesAndSave("demo_logic")
    m.plotByModulesAndShow()
        
if __name__ == '__main__':
    main()
