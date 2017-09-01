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

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))+os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE+"pyss"+os.sep)

from pyss import generate
from pyss import terminate
from pyss import logger
from pyss import pyssobject
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import tabulate
from pyss import seize
from pyss import release
from pyss import advance
from pyss import queue
from pyss import depart
from pyss import options
from pyss import facility
from pyss import components
from pyss import segment_builder
from pyss import bprint_blocks
from pyss.pyss_const import *

def main():
    logger.info("--- Дискретное равномерное распределение (кубик) ---")
    random.seed()
    #
    options.flags.logTransactTrace = False
    #
    MAX_TIME=24*4
    # tables
    F_1="F_1"
    def argFunc_T_1(owner, transact):
        return transact[TIME_CREATED]
    def valFunc_T_1(owner, transact):
        return random.choice([1,2,3,4,5,6])
    # запускаем несколько раз на разных таблицах
    # всего 5 таблиц
    TBL_COUNT=5
    tables = [table.Table(tableName="T_%d"%count, argFunc=argFunc_T_1, limitUpFirst=1, widthInt=1, countInt=MAX_TIME).setDisplaying(displaying=False) for count in xrange(TBL_COUNT)]

    #
    # ОКУ
    facility_1 = facility.Facility(facilityName=F_1)
    #
    def mf(owner, currentTime):
        #бросок монеты
        return 1
    #
    for tbl in tables:
        logger.printLine(msg=3*"*"+" Table [%s] "%tbl[TITLE]+60*"*")
        first_tx=0 #mf(None,None)
        # model
        m = pyss_model.PyssModel()
        m.addFacility(facility_1)
        m.addTable(tbl)
        m.addSegment(
            segment.Segment()
            #генерится см. mf()
            .addBlock(generate.Generate(med_value=0, modificatorFunc=mf,first_tx=first_tx, max_amount=1000))
            .addBlock(tabulate.Tabulate(table=tbl,valFunc=valFunc_T_1))
            .addBlock(terminate.Terminate(deltaTerminate=0))
            )
        logger.info(str(m))
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)
    # график занятости ОКУ
    from pyss import plot_table
    pl=plot_table.PlotTable()
    pl.extend(tables)
    pl.plot()

if __name__ == '__main__':
    main()