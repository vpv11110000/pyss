# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# manufact.py – Моделирование системы производства электронных изделий

**Постановка проблемы**

Отдел производства электроники занимается созданием цифровых часов. 
В отделе отгрузки часы упаковываются автоматической упаковывающей машиной в пакеты, в объеме, указанном розничными дистрибьюторами.

Размер заказа определяется следующей функцией.

Размер заказа
Frequency .10 .25 .30 .15 .12 .05 .03
Order Size 6 12 18 24 30 36 48

Среднее время прибытия заказов составляет 15 минут, распределенных по экспоненциальному закону. 
Время упаковки заказа занимает 120 секунд плюс 10 секунды на каждый экземпляр часов заказа. 
Производственный отдел производит по 60 часов каждые 455 минут.
Смоделируйте 5 дней работы компании для получения следующей информации

1. Среднее количество заказов, ожидающих очереди в отделе упаковки
2. Количество часов, отгружаемых ежедневно.
3. Распределение времени поступления заказов.

---

Условие задачи взято из "Учебное руководство по системе GPSS World"
GPSS World Sample File - ORDERPNT.GPS, by Gerard F. Cummings


"""

# pylint --rcfile ./.pylintrc ./tvrepair.py

# pylint: disable=line-too-long, bad-whitespace, missing-docstring
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position, invalid-name
# pylint: disable=unused-wildcard-import, too-many-locals, unused-import


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
from pyss.pyss_const import *

from pyss.func_discrete import FuncDiscrete
from pyss.func_exponential import Exponential
from pyss.plot_func import PlotFunc

from pyss.simpleobject import SimpleObject


# ; GPSS World Sample File - MANUFACT.GPS, by Gerard F. Cummings
# ****************************************************************
# *******
# * Manufacturing Company *
# ****************************************************************
# *******
# * Time Unit is one hour *
# Sizeorder FUNCTION RN1,D7 ;Order size
# .10,6/.35,12/.65,18/.80,24/.92,30/.97,36/1.0,48
# Transit TABLE M1,.015,.015,20 ;Transit time
# Numbe r TABLE X1,100,100,20 ;No. packed each day
# Ptime VARIABLE .0028#P1+0.0334 ;Packing time
# Amount EQU 1000 ;Initial stock amount
# Stock STORAGE 4000 ;Warehouse holds
# ; 4000 units
# ****************************************************************
# *******
# GENERATE (Exponential(1,0,0.25)) ;Order arrives
# ASSIGN 1,Sizeorder ;P1=order size
# TEST GE S$Stock,P1,Stockout ;Is stock sufficient?
# LEAVE Stock,P1 ;Remove P1 from stock
# QUEUE Packing
# SEIZE Machine ;Get a machine
# DEPART Packing
# ADVANCE V$Ptime ;Packing time
# RELEASE Machine ;Free the machine
# SAVEVALUE 1+,P1 ;Accumulate no. packed
# TABULATE Transit ;Record transit time
# TERMINATE
# Stockout TERMINATE
# ****************************************************************
# *******
# GENERATE 0.75,0.08334,1 ;Xact every 40+/-5 mins
# ENTER Stock,60 ;Make 60, Stock
# ; increased by 60
# Stockad TERMINATE
# ****************************************************************
# *******
# GENERATE 8 ;Xact every day
# TABULATE Number
# SAVEVALUE 1,0
# TERMINATE 1
# ****************************************************************
# *******
# GENERATE ,,,1,10 ;Initial stock xact
# ENTER Stock,Amount ;Set initial stock
# TERMINATE
# ****************************************************************
# *******

def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    #
    m[OPTIONS].setAllFalse()

    #-------------------------------
    MAX_TIME = 5 * 8
    #-------------------------------
    # * Time Unit is one hour *
    # Sizeorder FUNCTION RN1,D7 ;Order size
    # .10,6/.35,12/.65,18/.80,24/.92,30/.97,36/1.0,48
    sizeorder = FuncDiscrete(randomGenerator=random.random,
                             dictValues={.1:6, .35:12, .65:18, .8:24, 0.92:30, 1.0:48})
    
    # диаграмма функции funcDiscrete 
    p = PlotFunc(m, funcObj=sizeorder, maxPoints=1000, countIntervals=20,
                 title="Discrete")
        
    # Transit TABLE M1,.015,.015,20 ;Transit time
    TRANSIT = "Transit"
    tblTransit = Table(m, tableName=TRANSIT,
                     argFunc=lambda ownerTable, trans: trans[M1],
                     limitUpFirst=0.015,
                     widthInt=0.015,
                     countInt=20)
    # ячейка X1
    X1 = SimpleObject(0)
    # Number TABLE X1,100,100,20 ;No. packed each day
    NUMBER = "Number"
    tblNumber = Table(m, tableName=NUMBER,
                    argFunc=lambda ownerTable, trans: X1.getValue(),
                    limitUpFirst=100.0,
                    widthInt=100.0,
                    countInt=20)
    
    # Ptime VARIABLE .0028#P1+0.0334 ;Packing time
    # Время упаковки заказа занимает 120 секунд плюс 10 секунды на каждый экземпляр часов заказа
    # в часе 3600 секунд
    def Ptime(param):
        return float(120.0 + 10 * param) / 3600

    # Amount EQU 1000 ;Initial stock amount
    amount = 1000
    
    # Stock STORAGE 4000 ;Warehouse holds 4000 units
    STOCK = "Stock"
    stock = Storage(m, storageName=STOCK, storageSize=4000, initBusySize=amount)

    # ФУНКЦИИ -------------------
    medValue = Exponential(timeForEvent=15.0 / 60.0)
    
    # диаграмма функции funcDiscrete 
    p = PlotFunc(m, funcObj=medValue, maxPoints=1000, countIntervals=20,
                           title="Exponential")

    # SEGMENT -------------------------------------------------
    # GENERATE (Exponential(1,0,0.25)) ;Order arrives
    Generate(sgm, med_value=lambda: medValue.get(),
                    modificatorFunc=None,
                    first_tx=0,
                    max_amount=None)
    # ASSIGN 1,Sizeorder ;P1=order size
    # запись в параметр транзакта P1 значения 
    Assign(sgm, parametrName=P1, modificatorFunc=lambda o, t: sizeorder.get())
    # TEST GE S$Stock,P1,Stockout ;Is stock sufficient?
    STOCKOUT = "Stockout"
    Test(sgm, funcCondition=lambda o, t:stock[BUSY_SIZE] >= t[P1], move2block=STOCKOUT)
    # LEAVE Stock,P1 ;Remove P1 from stock
    Leave(sgm, storageName=STOCK, funcBusySize=lambda o, t:t[P1])
    # QUEUE Packing
    QUEUE_PACKING = "Packing"
    Queue(sgm, queueName=QUEUE_PACKING)
    # SEIZE Machine ;Get a machine
    MACHINE = "Machine"
    Seize(sgm, facilityName=MACHINE)
    # DEPART Packing
    Depart(sgm, queueName=QUEUE_PACKING)
    # ADVANCE V$Ptime ;Packing time
    Advance(sgm, meanTime=lambda: Ptime(m[CURRENT_TRANSACT][P1]))
    # RELEASE Machine ;Free the machine
    Release(sgm, facilityName=MACHINE)
    # SAVEVALUE 1+,P1 ;Accumulate no. packed
    Handle(sgm, handlerFunc=lambda o, t:X1.addValue(t[P1]))
    # TABULATE Transit ;Record transit time
    Tabulate(sgm, table=tblTransit, valFunc=1)
    # TERMINATE
    Terminate(sgm, deltaTerminate=0)
    # Stockout TERMINATE
    Terminate(sgm, deltaTerminate=0, label=STOCKOUT)
    
    # ****************************************************************
    # GENERATE 0.75,0.08334,1 ;Xact every 40+/-5 mins
    Generate(sgm, med_value=40.0 / 60.0,
        modificatorFunc=lambda o, t:random.uniform(-5.0 / 60, 5.0 / 60),
        first_tx=1)
    # ENTER Stock,60 ;Make 60, Stock
    Enter(sgm, storageName=STOCK, funcBusySize=60)
    # ; increased by 60
    # Stockad TERMINATE
    STOCKAD = "Stockad"
    Terminate(sgm, label=STOCKAD, deltaTerminate=0)
    
    # ****************************************************************
    # GENERATE 8 ;Xact every day
    Generate(sgm, med_value=8)    
    # TABULATE Number
    Tabulate(sgm, table=tblNumber)
    # SAVEVALUE 1,0
    Handle(sgm, handlerFunc=lambda o, t:X1.setValue(0))
    # TERMINATE 1
    Terminate(sgm, deltaTerminate=1)

    # ****************************************************************
    # GENERATE ,,,1,10 ;Initial stock xact
    # ENTER Stock,Amount ;Set initial stock
    # TERMINATE
    # нициализируем значением 1000 см. конструктор
    # stock[BUSY_SIZE] = amount

    # *************************************************************
    # ТАБЛИЦЫ
    m.initPlotTable()
    # ------------------------    
    # активность
    def transactFilter(transact):
        return True
    def funcAnnotate(transact):
        s = "%d" % (transact[NUM])
        return s
    m.initPlotTransactLifeLine(
        terminateBlockLabels=None,
        transactFilter=transactFilter, title="TransactLifeLine",
        funcAnnotate=funcAnnotate)
    
    m.initPlotStorageLifeLine()
    m.initPlotQueueLifeLine()
        
    # РАСЧЁТ --------------------------
    m.start(terminationCount=5, maxTime=MAX_TIME)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
