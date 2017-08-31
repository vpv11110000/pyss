# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# orderpnt.py – Моделирование системы инвентаризации с точкой заказа

**Постановка проблемы**

Система инвентаризации управляется точкой заказа, устанавливаемой в 600 единиц, а значение экономического заказа составляет 500 единиц. 

Начальный объем продукции составляет 700 единиц. 

Ежедневный запрос составляет от 40 до 63 единиц, равномерно распределенный. 

Время доставки товаров составляет одну неделю (5 дней).

1. Смоделируйте системы инвентаризации за период в 100 дней.

2. Определите распределение товаров и значение объема ежедневных продаж.

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


# ; GPSS World Sample File - ORDERPNT.GPS, by Gerard F. Cummings
# ****************************************************************
# *****
# *
# * Order Point Inventory System
# *
# ****************************************************************
# *****
# * Initialize and define
# INITIAL X$EOQ,500 ;Economic order qty.
# INITIAL X$Point,600 ;Order point
# INITIAL X$Stock,700 ;Set initial stock=700
# Inventory TABLE X$Stock,0,50,20 ;Table of stock levels
# Sales TABLE P$Demand,38,2,20 ;Table of sales levels
# Var2 VARIABLE RN1@24+40
# ****************************************************************

# GENERATE ,,,1
# Again TEST L X$Stock,X$Point ;Order placed on successful test
# ADVANCE 5 ;Lead time = 1 week
# SAVEVALUE Stock+,X$EOQ ;Economic order
# TRANSFER ,Again ;Cycle transaction again
# ****************************************************************

# GENERATE 1 ;Daily demand xact
# ASSIGN Demand,V$Var2 ;Assign daily demand
# TABULATE Inventory ;Record inventory
# TEST GE X$Stock,P$Demand ;Make sure order can be
# filled
# SAVEVALUE Stock-,P$Demand ;Remove demand from stock
# SAVEVALUE Sold,P$Demand ;X$Sold=Daily demand
# TABULATE Sales ;Record daily sales
# TERMINATE 1 ;Daily timer
# ****************************************************************

def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m)
    #
    m[OPTIONS].setAllFalse()
    #-------------------------------
    MAX_TIME = 100
    #-------------------------------
    # INITIAL X$Stock,700 ;Set initial stock=700
    XStock = SimpleObject(700)
    # INITIAL X$EOQ,500 ;Economic order qty.
    XEOQ = SimpleObject(500)
    # INITIAL X$Point,600 ;Order point
    XPoint = SimpleObject(600)
    Sold = SimpleObject(0)
    
    # Var2 VARIABLE RN1@24+40
    def Var2():
        return random.randint(40, 63)

    #-----------
    # Inventory TABLE X$Stock,0,50,20 ;Table of stock levels
    INVENTORY = "Inventory"
    def argFuncInv(o, t):
        return m.getCurTime()
    tblInventory = Table(m, tableName=INVENTORY, argFunc=argFuncInv,
                               limitUpFirst=0, widthInt=1, countInt=MAX_TIME)

    # Sales TABLE P$Demand,38,2,20 ;Table of sales levels
    SALES = "Sales"
    DEMAND = "Demand"
    def argFuncSal(o, t):
        return m.getCurTime()
    
    tblSales = Table(m, tableName=SALES, argFunc=argFuncSal,
                               limitUpFirst=0, widthInt=1, countInt=MAX_TIME)

    #---------
    # модель в рамках одного сегмента

    # GENERATE ,,,1
    Generate(sgm, label="GEN_1",
             med_value=None,
             modificatorFunc=None,
             first_tx=0, max_amount=1, priority=1)
    # Again TEST L X$Stock,X$Point ;Order placed on successful test
    AGAIN = "Again"
    def funcConditionAgain(o, t):
        return XStock.getValue() < XPoint.getValue()
    Test(sgm, funcCondition=funcConditionAgain,
         move2block=None,
         label=AGAIN)
    # ADVANCE 5 ;Lead time = 1 week
    Advance(sgm, meanTime=5)
    # SAVEVALUE Stock+,X$EOQ ;Economic order
    Handle(sgm, handlerFunc=lambda o, t:XStock.setValue(XStock.getValue() + XEOQ.getValue()))
    # TRANSFER ,Again ;Cycle transaction again
    Transfer(sgm, funcTransfer=lambda o, t: o.findBlockByLabel(AGAIN))
    

    # ****************************************************************
    
    # GENERATE 1 ;Daily demand xact
    Generate(sgm, label="GEN_2",
             med_value=1, modificatorFunc=None, first_tx=0, priority=1)
    # ASSIGN Demand,V$Var2 ;Assign daily demand
    Assign(sgm, parametrName=DEMAND, modificatorFunc=lambda o, t:Var2())
                               
    # TABULATE Inventory ;Record inventory
    def valFuncInv(owner, transact):
        return XStock.getValue()    
    Tabulate(sgm, table=tblInventory, valFunc=valFuncInv)
    # TEST GE X$Stock,P$Demand ;Make sure order can be
    def funcConditionGE(o, t):
        return XStock.getValue() >= t[DEMAND]
    Test(sgm, funcCondition=funcConditionGE, move2block=None)    
    # filled
    # SAVEVALUE Stock-,P$Demand ;Remove demand from stock
    Handle(sgm, handlerFunc=lambda o, t:XStock.setValue(XStock.getValue() - t[DEMAND]))
    # SAVEVALUE Sold,P$Demand ;X$Sold=Daily demand
    Handle(sgm, handlerFunc=lambda o, t:Sold.setValue(t[DEMAND]))
    # TABULATE Sales ;Record daily sales
    def valFuncSales(owner, transact):
        return transact[DEMAND]
    Tabulate(sgm, table=tblSales, valFunc=valFuncSales)    
    # TERMINATE 1 ;Daily timer
    Terminate(sgm, deltaTerminate=1)    
    # ****************************************************************
    ### КАРТИНКИ ----------------------
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
    
    # здесь это не интересно
    #m.initPlotTransactLifeLine(
    #    terminateBlockLabels=None,
    #    transactFilter=transactFilter, title="TransactLifeLine",
    #    funcAnnotate=funcAnnotate)
    
    m.initPlotStorageLifeLine()
        
    # РАСЧЁТ --------------------------
    m.start(terminationCount=1000000, maxTime=MAX_TIME)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
