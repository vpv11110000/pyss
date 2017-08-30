# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
periodic.py - Моделирование системы инвентаризации с периодической проверкой

**Постановка проблемы**

Производство компонента осуществляется в три стадии, 
после каждой происходит короткая инспекция длиной в две минуты. 

Первый процесс требует переработки 20% компонентов. 

Второй и третий процессы требуют переработки 15% и 5%, соответственно.

60% компонентов превращаются в металлолом, 
а оставшиеся 40% необходимо переобработать, используя процесс, отклонивший данный компонент.

Создание нового компонента занимает, в среднем, 30 минут, 
распределяемых по экспоненциальному закону. 

Время для первого процесса приведено в следующей таблице.

Время для первого процесса
Frequency     .05  .13 .16  .22  .29  .15
Process time   10  14  21   32   38   45
  

Время работы второго процесса занимает 15±6 минут, 
а время обработки финальным процессом распределено по стандартному закону, 
и занимает 24 минут при стандартном отклонении в 4 минуты.

1. Смоделируйте процесс производства 100 завершенных компонентов.

2. Определите время, которое понадобилось на производство указанных выше компонентов, и количество компонентов, которые были отклонены.

Условие задачи взято из "Учебное руководство по системе GPSS World"
; GPSS World Sample File - PERIODIC.GPS, by Gerard F. Cummings

Дополнительно постоить график ежедневного объема продукции на складе.

"""

import sys
import os
import random
import unittest
from urllib import addbase

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
from pyss.func_normal import Normal
from pyss.plot_func import PlotFunc

from pyss.simpleobject import SimpleObject

def main():
    logger.info("-------------------------------------")
    
    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m, "QControl")
    
    #
    m[OPTIONS].setAllFalse()
    
    #-------------------------------
    # Время моделирования
    MAX_TIME = 500

    #-------------------------------
    # Process FUNCTION RN1,D7
    # 0,0/.05,10/.18,14/.34,21/.56,32/.85,38/1.0,45
    
    funcDiscrete = FuncDiscrete(
        randomGenerator=random.random,
        dictValues={0:0, .05:10, .18:14, .34:21, .56:32, .85:38, 1.0:45})

    funcNormal = Normal(meanVal=24.0, stdDev=4.0)

    # диаграмма функции funcDiscrete 
    PlotFunc(m, funcObj=funcDiscrete, maxPoints=1000, countIntervals=20,
             title="Discrete: 0:0,.05:10,.18:14,.34:21,.56:32,.85:38,1.0:45")
    
    # диаграмма функции funcNormal 
    PlotFunc(m, funcObj=funcNormal, maxPoints=1000, countIntervals=20,
             title="Normal 24.0 4.0")
    
    #----------------------------------    
    # Transit TABLE M1,100,100,20 ;Transit Time
    TABLE_NAME = "Transit"
    def tableArgFunc(owner, transact):
        # Время пребывания в модели активного транзакта. 
        # Равно разности  текущего значения абсолютного времени и 
        # времени рождения активного транзакта.
        return m.getCurTime() - transact[TIME_CREATED]
    
    tbl = Table(m, tableName=TABLE_NAME,
                argFunc=tableArgFunc, limitUpFirst=100,
                widthInt=100, countInt=20)
    #------------------------
    def transferStatisMode(value, labelIfLEValue=None, labelIfGreatValue=None):
        def transferFunc(o, t):
            if random.random() <= value:
                if labelIfLEValue is None:
                    return None
                return o.findBlockByLabel(labelIfLEValue)
            else:
                if labelIfGreatValue is None:
                    return None
                return o.findBlockByLabel(labelIfGreatValue)
        return transferFunc

    ### MODEL --------------------------------------------------------------
    #---------------------------
    MACHINE_1 = "Machine1"
    MACHINE_2 = "Machine2"
    MACHINE_3 = "Machine3"
    
    # Exponential(1,0,30)
    # GENERATE (Exponential(1,0,30))
    funcExponential = Exponential(timeForEvent=30.0, scale=1.0)
    funcExponentialGet = funcExponential.get
    PlotFunc(m, funcObj=funcExponential, maxPoints=1000, countIntervals=20,
             title="Exponential(m, timeForEvent=30.0, scale=1.0)")
    
    
    Generate(sgm, med_value=funcExponentialGet, modificatorFunc=None, priority=1)
    # ASSIGN 1,FN$Process ;Process time in P1
    Assign(sgm, parametrName="P1", modificatorFunc=lambda o, t: funcDiscrete.get())
    
    #---
    # Stage1 SEIZE Machine1
    Seize(sgm, facilityName=MACHINE_1, label="Stage1")
    # ADVANCE P1 ;Process 1
    Advance(sgm, meanTime=0, modificatorFunc=lambda o, c:m.getCurrentTransact()["P1"])
    
    # RELEASE Machine1
    Release(sgm, facilityName=MACHINE_1)
    # ADVANCE 2 ;Inspection
    Advance(sgm, meanTime=2, modificatorFunc=None)
    # TRANSFER .200,,Rework1 ;20% Need rework
    Transfer(sgm, funcTransfer=transferStatisMode(0.2, labelIfLEValue="Rework1"))
    
    #---
    # Stage2 SEIZE Machine2
    Seize(sgm, label="Stage2", facilityName=MACHINE_2)        
    # ADVANCE 15,6 ;Process 2
    Advance(sgm, meanTime=15,
            modificatorFunc=lambda o, t:random.uniform(-6.0, 6.0))
    # RELEASE Machine2
    Release(sgm, facilityName=MACHINE_2)
    # ADVANCE 2 ;Inspection
    Advance(sgm, meanTime=2, modificatorFunc=None)
    # TRANSFER .150,,Rework2 ;15% Need rework
    Transfer(sgm, funcTransfer=transferStatisMode(0.15, labelIfLEValue="Rework2"))
    
    #---                  
    # Stage3 SEIZE Machine3
    Seize(sgm, label="Stage3", facilityName=MACHINE_3)        
    # ADVANCE (Normal(1,24,4)) ;Process 3
    Advance(sgm, meanTime=0, modificatorFunc=lambda o, t:funcNormal.get())
    # RELEASE Machine3
    Release(sgm, facilityName=MACHINE_3)
    # ADVANCE 2 ;Inspection 3
    Advance(sgm, meanTime=2, modificatorFunc=None)
    # TRANSFER .050,,Rework3 ;5% need rework
    Transfer(sgm, funcTransfer=transferStatisMode(0.05, labelIfLEValue="Rework3"))
    # TABULATE Transit ;Record transit time
    Tabulate(sgm, table=tbl)
    # TERMINATE 1
    Terminate(sgm, deltaTerminate=1, label="T_FINISH")

    # ****************************************************************
    # *
    # Rework1 TRANSFER .400,,Stage1
    Transfer(sgm, label="Rework1", funcTransfer=transferStatisMode(0.4, labelIfLEValue="Stage1"))
    # TERMINATE
    Terminate(sgm, label="T_REWORK_1", deltaTerminate=0)
    # Rework2 TRANSFER .400,,Stage2
    Transfer(sgm, label="Rework2", funcTransfer=transferStatisMode(0.4, labelIfLEValue="Stage2"))
    # TERMINATE
    Terminate(sgm, label="T_REWORK_2", deltaTerminate=0)
    # Rework3 TRANSFER .400,,Stage3
    Transfer(sgm, label="Rework3", funcTransfer=transferStatisMode(0.4, labelIfLEValue="Stage3"))
                                 
    # TERMINATE
    Terminate(sgm, label="T_REWORK_3", deltaTerminate=0)
    #------------------------
    
# * Definitions of non Block entities
# Transit TABLE M1,100,100,20 ;Transit Time
# Process FUNCTION RN1,D7
# 0,0/.05,10/.18,14/.34,21/.56,32/.85,38/1.0,45
# GENERATE (Exponential(1,0,30))
# ASSIGN 1,FN$Process ;Process time in P1
# Stage1 SEIZE Machine1
# ADVANCE P1 ;Process 1
# RELEASE Machine1
# ADVANCE 2 ;Inspection
# TRANSFER .200,,Rework1 ;20% Need rework
# ****************************************************************
# *
# Stage2 SEIZE Machine2
# ADVANCE 15,6 ;Process 2
# RELEASE Machine2
# ADVANCE 2 ;Inspection
# TRANSFER .150,,Rework2 ;15% Need rework
# ****************************************************************
# *
# Stage3 SEIZE Machine3
# ADVANCE (Normal(1,24,4)) ;Process 3
# RELEASE Machine3
# ADVANCE 2 ;Inspection 3
# TRANSFER .050,,Rework3 ;5% need rework
# TABULATE Transit ;Record transit time
# TERMINATE 1
# ****************************************************************
# *
# Rework1 TRANSFER .400,,Stage1
# TERMINATE
# Rework2 TRANSFER .400,,Stage2
# TERMINATE
# Rework3 TRANSFER .400,,Stage3
# TERMINATE
    
    ### КАРТИНКИ ----------------------
    # таблицы
    m.initPlotTable()
    
    def funcAnnotate(transact):
        s = "%d" % (transact[NUM])
        return s
    m.initPlotTransactLifeLine(
        # all terminate
        # terminateBlockLabels=None,
        terminateBlockLabels=["T_FINISH", "T_REWORK_1", "T_REWORK_2", "T_REWORK_3"],
        transactFilter=True, title="Active ",
        funcAnnotate=funcAnnotate)
    
    m.initPlotFacilityLifeLine(facilityNames=None, title="OCF", funcAnnotate=None)
        
    # РАСЧЁТ --------------------------
    logger.info(str(m))
    m.start(terminationCount=300, maxTime=MAX_TIME)

    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()
    
if __name__ == '__main__':
    main()
