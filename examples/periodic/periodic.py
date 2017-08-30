# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
periodic.py - Моделирование системы инвентаризации с периодической проверкой

**Постановка проблемы**

Контроль над объемом готовой продукции осуществляется с помощью системы проверок, 
с интервалом, составляющим одну неделю. 

Начальный объем составляет 1000 единиц.
 
Ежедневная потребность в товарах составляет от 40 до 63 единиц продукции.

Исходным значение объема продукции составляет 1000 единиц, 
определение того, что был осуществлен заказ, 
происходит в результате сравнения исходного значения объема продукции и текущего значения.
 
Если в текущий момент значение составляет 800 и более единиц, 
то это значит, что на этой недели не поступали заказы.
 
Длительность недели, в рамках которой работает компании, составляет 5 дней.
 
Время доставки заказа равняется одной неделе.

Необходимо смоделировать систему инвентаризации в течение 200 дней и определить, 
не появится ли дефицит товаров.

Условие задачи взято из "Учебное руководство по системе GPSS World"
; GPSS World Sample File - PERIODIC.GPS, by Gerard F. Cummings

Дополнительно постоить график ежедневного объема продукции на складе.

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
from pyss.pyss_const import *

from pyss.func_discrete import FuncDiscrete
from pyss.func_exponential import Exponential
from pyss.plot_func import PlotFunc

from pyss.simpleobject import SimpleObject


def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m, "Periodic Review")
    sgmDaily = Segment(m, label="The daily demand decrements quantity on hand")    
    sgmMes = Segment(m, label="SEGM_MEASURE")
    
    #
    m[OPTIONS].setAllFalse()

    #-------------------------------
    # Время моделирования
    MAX_TIME = 200
    #-----------------------------
    TARGET = 1000  # Initial stock level
    REORDER = 800  # Reorder point
    #-------------------------------
    STORAGE_NAME = "Stock"
    STORAGE_SIZE = 10000
    
    # сразу инициализируем initBusySize=TARGET
    # в примере GPSS, но нам не нужно
    # ****************************************************************
    # *******
    # * Initialize the inventory
    # GENERATE ,,,1,10 ;Set initial stock
    # ENTER Stock,Target ;Set init stock level=target
    # TERMINATE ;Xact is terminated
    stor = Storage(m, storageName=STORAGE_NAME, storageSize=STORAGE_SIZE, initBusySize=TARGET)
    #-----------
    TABLE_NAME = "Stock"
    def tableArgFunc(owner, transact):
        return stor.getBusySize()
    
    tbl = Table(m, tableName=TABLE_NAME, argFunc=tableArgFunc, limitUpFirst=100, widthInt=100, countInt=20)
    
    TABLE_NAME_MSR = "store_by_time"
    PARAMETR_NAME = TABLE_NAME_MSR
    tblm = Table(m, tableName=TABLE_NAME_MSR, argFunc=lambda o, t: m.getCurTime(), limitUpFirst=1, widthInt=1, countInt=MAX_TIME)
    # не печатать таблицу
    tblm[DISPLAYING] = False
    #--------------------------
    def generateFunc(owner, currentTime):
        return 0
    #-----------
    # Orderqty VARIABLE Target-S$Stock ;Order quantity
    def orderqty(o, t):
        return TARGET - stor.getBusySize()
    # Demand VARIABLE RN1@24+40 ;Daily demand
    def demand(o, t):
        return 40 + random.randint(0, 23)

    ### MODEL --------------------------------------------------------------
    #------------------------  
    # так в примере      
#     m.addSegment(
#         segment.Segment(label="Initialization",options_val=None)
#         .addBlock(generate.Generate(1,modificatorFunc=None,first_tx=0, max_amount=1, priority=10,label=None))
#         .addBlock(enter.Enter(storageName=STORAGE_NAME,funcBusySize=TARGET,label=None))
#         .addBlock(terminate.Terminate(deltaTerminate=0)))

    #---------------------------
    Generate(sgm, med_value=5, modificatorFunc=generateFunc, priority=1)
    Test(sgm, funcCondition=lambda o, t:stor.getBusySize() < REORDER, move2block="Skip")
    Assign(sgm, parametrName="OrderQuantity", modificatorFunc=orderqty)
    Bprint(sgm, outputFunc=lambda owner, transact: "OrderQuantity: %s" % 
           transact['OrderQuantity'])
    Advance(sgm, label="Custwait", meanTime=5, modificatorFunc=None)
    Enter(sgm, storageName=STORAGE_NAME, funcBusySize=lambda o, t:t["OrderQuantity"])
    Terminate(sgm, deltaTerminate=0, label="Skip")
    #------------------------
    Generate(sgmDaily, med_value=1, modificatorFunc=None, priority=1)
    Assign(sgmDaily, parametrName="DailyDemand", modificatorFunc=demand)
    Tabulate(sgmDaily, table=tbl, valFunc=tableArgFunc)
    Test(sgmDaily, funcCondition=lambda o, t:stor.getBusySize() >= t["DailyDemand"], move2block="Stokout")
    Leave(sgmDaily, storageName=STORAGE_NAME, funcBusySize=lambda o, t:t["DailyDemand"])
    Terminate(sgmDaily, deltaTerminate=0, label="Stokout")
    #--------------------
    Generate(sgmMes, med_value=1, modificatorFunc=None, priority=0)
    Assign(sgmMes, parametrName=PARAMETR_NAME, modificatorFunc=tableArgFunc)
    Tabulate(sgmMes, table=tblm, valFunc=lambda o, t: stor.getBusySize())
    Terminate(sgmMes, deltaTerminate=0)
    
# * Definitions of non Block entities
# RMULT 39941
# Stock STORAGE 10000 ;Warehouse can hold 10000
# Stock TABLE S$Stock,100,100,20 ;Table for inventory amts
# Orderqty VARIABLE Target-S$Stock ;Order quantity
# Demand VARIABLE RN1@24+40 ;Daily demand
# Target EQU 1000 ;Initial stock level
# Reorder EQU 800 ;Reorder point
# ****************************************************************
# *******
# * The reorder process
# GENERATE 5,,,,1 ;Review xact, Priority=1
# TEST L S$Stock,Reorder,Skip ;Is stock < Reorderpt
# ASSIGN 2,V$Orderqty ;Parameter 2=Order quantity
# Custwait ADVANCE 5 ;Lead time is 5 days
# ENTER Stock,P2 ;Stock increases by P2
# Skip TERMINATE ;Ordering xact is finished    

# * The daily demand decrements quantity on hand
# GENERATE 1 ;Daily demand Transaction
# ASSIGN 1,V$Demand ;Parameter 1(P1)=daily demand
# TABULATE Stock ;Record daily stock
# TEST GE S$Stock,P1,Stockout ;Can order be filled
# LEAVE Stock,P1 ;Remove demand from stock
# TERMINATE 1 ;Daily timer
# Stockout TERMINATE 1 ;Daily timer
# ****************************************************************
# *******
# * Initialize the inventory
# GENERATE ,,,1,10 ;Set initial stock
# ENTER Stock,Target ;Set init stock level=target
# TERMINATE ;Xact is terminated
    
    ### ДИАГРАММЫ ----------------------
    m.initPlotTable(title="Product store")
    m.initPlotTransactLifeLine()
    m.initPlotStorageLifeLine()
    
    # РАСЧЁТ --------------------------
    logger.info(str(m))
    m.start(terminationCount=300, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
