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
    logger.info("--- Гипергеометрические распределение ---")
    random.seed()
    #
    options.flags.logTransactTrace = False
    options.flags.reportTransactFamilies = False
    options.flags.reportCel = False
    #
    N=10
    WHITE = 5
    BLACK = 45
    # совокупность
    T=[0]*BLACK
    T.extend([1]*WHITE)
    print T
    #
    MAX_TIME=24*4
    # tables
    def argFunc_T_1(owner, transact):
        return transact[TIME_CREATED]
    def valFunc_T_1(owner, transact):
        l=[random.choice(T) for x in range(N)]
        print "Выбрано: %s"%str(l)
        return sum(l)
    # запускаем несколько раз на разных таблицах
    # всего 5 таблиц
    TBL_COUNT=5
    tables = [table.Table(tableName="T_%d"%count, argFunc=argFunc_T_1, limitUpFirst=1, widthInt=1, countInt=MAX_TIME).setDisplaying(displaying=False) for count in xrange(TBL_COUNT)]
    #
    for tbl in tables:
        logger.printLine(msg=3*"*"+" Table [%s] "%tbl[TITLE]+60*"*")
        first_tx=0 #mf(None,None)
        # model
        m = pyss_model.PyssModel()
        m.addTable(tbl)
        m.addSegment(
            segment.Segment()
            #генерится см. mf()
            .addBlock(generate.Generate(med_value=1, modificatorFunc=None,first_tx=first_tx, max_amount=1000))
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
