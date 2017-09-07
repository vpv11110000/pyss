##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Запуск:
    python ./discrete_uniform_distribution.py

Пример дискретного равномерного распределения.

Каждую единицу времени моделируется бросок симметричного кубика. Событием является выпавшее число.

Формируется 5 одинаковых моделей с 5 таблицами, собирающими факты возникновения событий.

После моделирования выполняется построение графиков возникновения событий.

"""

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import random
import math

import os

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
    logger.info("--- Дискретное равномерное распределение (кубик) ---")
    random.seed()
    #
    def valFunc_T_1(owner, transact):
        return random.choice([1,2,3,4,5,6])    
    
    CAPTION="Discrete_6"
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True       


    #
    MAX_TIME=20
    # tables
    F_1="F_1"
    def argFunc_T_1(owner, transact):
        return transact[TIME_CREATED]

    tables = Table(m,
                   tableName="T_1",
                   argFunc=argFunc_T_1,
                   limitUpFirst=1,
                   widthInt=1,
                   countInt=MAX_TIME).setDisplaying(displaying=False)

    #
    def mf(owner, currentTime):
        #бросок монеты
        return 1
    
    #генерится см. mf()
    Generate(sgm, med_value=0, modificatorFunc=mf,first_tx=0, max_amount=1000)
    Tabulate(sgm, table=m.getTables()[0],valFunc=valFunc_T_1)
    Terminate(sgm, deltaTerminate=0)
    #
    m.initPlotTable(title=CAPTION)
    
    #
    m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)
    
    #
    m.plotByModulesAndSave(CAPTION)
    m.plotByModulesAndShow()

if __name__ == '__main__':
    main()
