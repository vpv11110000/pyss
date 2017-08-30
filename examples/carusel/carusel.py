# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# carusel.py – Моделирование кассы в случае нестационарного потока покупателей

**Постановка проблемы**

Время           Интенсивность,    Количество покупок    Относительная частота     Суммарная частота 
                чел/мин    
 9:00 - 11:00   2                (0-5]                   0.2                     0.3
 2*60 мин                        (5-20]                  0.3                     0.5    
                                 (20-50]                 0.2                     0.7
                                 (50-100]                0.2                     0.9
                                 (100..120]              0.1                     1.0

11:00 - 15:00   5                (0-5]                   0.2                     0.3
 4*60 мин                        (5-20]                  0.2                     0.4    
                                 (20-50]                 0.25                    0.65
                                 (50-100]                0.25                    0.9
                                 (100..120]              0.1                     1.0

15:00 - 17:00   3                (0-5]                   0.4                     0.4
 2*60 мин                        (5-20]                  0.3                     0.7    
                                 (20-50]                 0.18                    0.88
                                 (50-100]                0.1                     0.98
                                 (100..120]              0.02                    1.0

Необходимо смоделировать систему инвентаризации в течение дня.

Построить гистограмму длины очереди.

------
"""

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *
from pyss import generate, bprint
from pyss import terminate
from pyss import logger
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import enter
from pyss import leave 
from pyss import tabulate
from pyss import options
from pyss import components
from pyss import queue
from pyss import assign
from pyss import advance
from pyss import seize
from pyss import test
from pyss import depart
from pyss import release
from pyss import storage

def main():
    logger.info("-------------------------------------")
    #-------------------------------
    options.flags.logCel = False
    options.flags.logFel = False
    #-------------------------------
    # Время моделирования
    MAX_TIME = 200
    #-----------------------------
    m = pyss_model.PyssModel()
    #-------------------------
    TARGET = 1000  # Initial stock level
    REORDER = 800  # Reorder point
    #-------------------------------
    STORAGE_NAME = "Stock"
    STORAGE_SIZE = 10000
    stor = storage.Storage(storageName=STORAGE_NAME, storageSize=STORAGE_SIZE)
    m.addStorage(stor)
    #-----------
    TABLE_NAME = "Stock"
    def tableArgFunc(owner, transact):
        return stor.getBusySize()
    
    tbl = table.Table(tableName=TABLE_NAME, argFunc=tableArgFunc, limitUpFirst=100, widthInt=100, countInt=20)
    m.addTable(tbl)
    
    TABLE_NAME_MSR = "store_by_time"
    PARAMETR_NAME = TABLE_NAME_MSR
    tblm = table.Table(tableName=TABLE_NAME_MSR, argFunc=lambda o, t: components.curTime, limitUpFirst=1, widthInt=1, countInt=MAX_TIME)
    # не печатать таблицу
    tblm[DISPLAYING] = False
    m.addTable(tblm)
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
    # так в примере, но сделаем по простому      
#     m.addSegment(
#         segment.Segment(label="Initialization",options_val=None)
#         .addBlock(generate.Generate(1,modificatorFunc=None,first_tx=0, max_amount=1, priority=10,label=None))
#         .addBlock(enter.Enter(storageName=STORAGE_NAME,funcBusySize=TARGET,label=None))
#         .addBlock(terminate.Terminate(deltaTerminate=0)))
    # делаем по простому
    stor[BUSY_SIZE]=TARGET
    #---------------------------
    m.addSegment(
        segment.Segment(label="Periodic Review", options_val=options.flags)
        .addBlock(generate.Generate(5, modificatorFunc=generateFunc, priority=1))
        .addBlock(test.Test(funcCondition=lambda t:stor.getBusySize() < REORDER, move2block="Skip", label=None))
        .addBlock(assign.Assign(parametrName="OrderQuantity", modificatorFunc=orderqty))
        .addBlock(bprint.Bprint(outputFunc=lambda owner, transact: "OrderQuantity: %s" % 
                                transact['OrderQuantity'],
                                label=None))
        .addBlock(advance.Advance(5, modificatorFunc=None, label="Custwait"))
        .addBlock(enter.Enter(storageName=STORAGE_NAME, funcBusySize=lambda o, t:t["OrderQuantity"], label=None))
        .addBlock(terminate.Terminate(deltaTerminate=0, label="Skip")))
    #------------------------
    m.addSegment(
        segment.Segment(label="The daily demand decrements quantity on hand", options_val=options.flags)
        .addBlock(generate.Generate(1, modificatorFunc=None, priority=1))
        .addBlock(assign.Assign(parametrName="DailyDemand", modificatorFunc=demand))
        .addBlock(tabulate.Tabulate(table=tbl, valFunc=tableArgFunc, label=None))
        .addBlock(test.Test(funcCondition=lambda t:stor.getBusySize() >= t["DailyDemand"], move2block="Stokout", label=None))
        .addBlock(leave.Leave(storageName=STORAGE_NAME, funcBusySize=lambda o, t:t["DailyDemand"], label=None))
        .addBlock(terminate.Terminate(deltaTerminate=0, label="Stokout")))
    #--------------------
    m.addSegment(
        segment.Segment(label="SEGM_MEASURE", options_val=None)
        .addBlock(generate.Generate(1, modificatorFunc=None, priority=0, label=None))
        .addBlock(assign.Assign(parametrName=PARAMETR_NAME, modificatorFunc=tableArgFunc, label=None))
        .addBlock(tabulate.Tabulate(table=tblm, valFunc=lambda o, t: stor.getBusySize(), label=None))
        .addBlock(terminate.Terminate(deltaTerminate=0)))
    
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
    
    ### КАРТИНКИ ----------------------
    # таблицы
    m.getPlotSubsystem().appendPlotTable(tblm, title="Product store")
    
    
    # РАСЧЁТ --------------------------
    logger.info(str(m))
    m.start(terminationCount=300, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
