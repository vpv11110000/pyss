##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Две модели гипергеометрическое распределение (N=2 и N=40)

Запуск:
    python ./hypergeometric_distribution.py

Пример визуализации возникновения событий в соответствии с гипергеометрическим распределением.

Гипергеометрическое распределение моделирует количество удачных выборок без возвращения из конечной совокупности.

Его параметры:
- T (в модели константа T) - совокупность объектов
- D - количество объектов с заданным свойством в совокупности T
- n - количество объектов в выборке
- k - количество объектов с заданным свойством в выборке n

См. https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D0%BF%D0%B5%D1%80%D0%B3%D0%B5%D0%BE%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5

ЦИТАТА:

"Классическим применением гипергеометрического распределения является выборка без возвращения. 
Рассмотрим урну с двумя типами шаров: черными и белыми. 
Определим вытягивание белого шара как успех, а черного как неудачу. 
Если N является числом всех шаров в урне и D является числом белых шаров, 
то N − D является числом черных шаров.
Теперь предположим, что в урне находятся WHITE = 5 белых и BLACK = 45 черных шаров. 
Стоя рядом с урной, вы закрываете глаза и вытаскиваете 10 шаров."

Модель показывает количество вытянутых белых шаров.
Белые шары моделируются числом 1.
Чёрные шары моделируются числом 0.

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
    logger.info("--- Гипергеометрические распределение ---")
    random.seed()
    
    #
    N=10
    WHITE = 5
    BLACK = 45
    # совокупность
    T=[0]*BLACK
    T.extend([1]*WHITE)
    print T

    def valFunc_T_1(owner, transact):
        l=[random.choice(T) for x in range(N)]
        print "Выбрано: %s"%str(l)
        return sum(l)
    
    CAPTION="hypergeometricDistribution"
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    
    #
    m[OPTIONS].setAllFalse()
    m[OPTIONS].printResult = True       


    #
    MAX_TIME=24*4
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
