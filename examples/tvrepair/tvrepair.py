# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
tvrepair.py – Моделирование отдела ремонта телевизионного оборудования

**Постановка проблемы**

Магазин по продаже телевизионного оборудования обладает одним сотрудником,
который осуществляет починку взятых напрокат телевизоров, обслуживает телевизоры
клиентов и производит поверхностный осмотр на предмет неисправностей.

Починка телевизионного оборудования компании осуществляется каждые 40±8 часов
и занимает 10±1 часов.

Быстрые починки, такие как замена предохранителей и настройка,
осуществляются немедленно.

Подобные заказы прибывают каждые 90±10 минут и
занимают 15±5 минут.

Обработка клиентского оборудования требует нормального
обслуживания.

Интенсивность прибытия составляет 5±1 час, а время починки - 120±30
минут.

Обслуживание клиентского оборудования имеет более высокий приоритет, чем
починка взятого напрокат оборудования.

1. Смоделируйте работу ремонтного отдела на интервале в 50 дней.
2. Определите коэффициент занятости ремонтника и время задержки клиентов в
очереди на обслуживание.

Условие задачи взято из "Учебное руководство по системе GPSS World"
GPSS World Sample File - TVREPAIR.GPS, by Gerard F. Cummings

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


# ; GPSS World Sample File - TVREPAIR.GPS, by Gerard F. Cummings
#****************************************************************
# *
# * Television Maintenance Man Model *
#****************************************************************
# *
# * Repair of rented sets, one each week *
# * Time unit is one minute *
#****************************************************************
# *
# GENERATE 2400,480,,,1 ;Overhaul of a rented set
# QUEUE Overhaul ;Queue for service
# QUEUE Alljobs ;Collect global statistics
# SEIZE Maintenance ;Obtain TV repairman
# DEPART Overhaul ;Leave queue for man
# DEPART Alljobs ;Collect global statistics
# ADVANCE 600,60 ;Complete job 10+/-1 hours
# RELEASE Maintenance ;Free repairman
# TERMINATE ;Remove one Transaction
#****************************************************************
# *
# * On the spot repairs
# GENERATE 90,10,,,3 ;On-the-spot repairs
# QUEUE Spot ;Queue for spot repairs
# QUEUE Alljobs ;Collect global statistics
# PREEMPT Maintenance,PR ;Get the TV repairman
# DEPART Spot ;Depart the ‘spot’ queue
# DEPART Alljobs ;Collect global statistics
# ADVANCE 15,5 ;Time for tuning/fuse/fault
# RETURN Maintenance ;Free maintenance man
# TERMINATE
#****************************************************************
# * Normal repairs on customer owned sets
# GENERATE 300,60,,,2 ;Normal TV Repairs
# QUEUE Service ;Queue for service
# QUEUE Alljobs ;Collect global statistics
# PREEMPT Maintenance,PR ;Preempt maintenance man
# DEPART Service ;Depart the ‘service’ queue
# DEPART Alljobs ;Collect global statistics
# ADVANCE 120,30 ;Normal service time
# RETURN Maintenance ;Release the man
# TERMINATE
#****************************************************************
# *
# GENERATE 480 ;One xact each 8 hr. day
# TERMINATE 1
# * Day counter
#****************************************************************
# *
# * Tables of queue statistics
# Overhaul QTABLE Overhaul,10,10,20
# Spot QTABLE Spot,10,10,20
# Service QTABLE Service,10,10,20
# Alljobs QTABLE Alljobs,10,10,20
#****************************************************************

def main():
    logger.info("-------------------------------------")

    ### MODEL ----------------------------------
    m = PyssModel()
    sgm = Segment(m, "TVREPAIR")
    
    #
    m[OPTIONS].setAllFalse()
    
    #-------------------------------
    PRIORITY_MODEL = 1
    PRIORITY_SPOT = 3
    PRIORITY_SERVICE = 2
    
    TRANSACT_GROUP = "TRANSACT_GROUP"
    GEN_1 = "GEN_O"
    GEN_2 = "GEN_S"
    GEN_3 = "GEN_R"
    GEN_4 = "Day"    

    #-------------------------------
    MAX_TIME = 50 * 8 * 60
    #-------------------------------
    QUEUE_OVERHAUL = "Overhaul"
    QUEUE_ALLJOBS = "Alljobs"
    QUEUE_SPOT = "Spot"
    QUEUE_SERVICE = "Service"

    # def queue_len_by_timeFunc(owner,transact):
        # q=m[QUEUE_OBJECTS][QUEUE_NAME]
        # if q:
            # return q[QUEUE_LENGTH]
        # else:
            # raise "Queue [%s] not found"%QUEUE_NAME

    #-----------
    #****************************************************************
    # *
    # * Tables of queue statistics
    # Overhaul QTABLE Overhaul,10,10,20
    tblOverhaul = Qtable(m, queueName=QUEUE_OVERHAUL, limitUpFirst=10, widthInt=10, countInt=20)
    # Spot QTABLE Spot,10,10,20
    tblSpot = Qtable(m, queueName=QUEUE_SPOT, limitUpFirst=10, widthInt=10, countInt=20)
    # Service QTABLE Service,10,10,20
    tblService = Qtable(m, queueName=QUEUE_SERVICE, limitUpFirst=10, widthInt=10, countInt=20)
    # Alljobs QTABLE Alljobs,10,10,20
    tblAlljobs = Qtable(m, queueName=QUEUE_ALLJOBS, limitUpFirst=10, widthInt=10, countInt=20)
    
    #---------
    FAC_MAINTENANCE = "Maintenance"
    # -----------------------------------------------------
    # модель в рамках одного сегмента
    
    # Починка телевизионного оборудования компании осуществляется каждые 40±8 часов
    # и занимает 10±1 часов.
    # GENERATE 2400,480,,,1 ;Overhaul of a rented set
    def generateFunc001(owner, currentTime):
        return random.uniform(-480.0, 480.0)    
    Generate(sgm, label="GEN_1",
             med_value=2400, modificatorFunc=generateFunc001,
             first_tx=None,
             priority=PRIORITY_MODEL)
    # segment001.addBlock(file_save.FileSave(fileName=FILENAMES[0], funcSave=funcSave, mode="write", label=None))
    def funcHandle1(o, t):
        t[TRANSACT_GROUP] = GEN_1
        print GEN_1
    Handle(sgm, handlerFunc=funcHandle1)
    # QUEUE Overhaul ;Queue for service
    Queue(sgm, queueName=QUEUE_OVERHAUL, deltaIncrease=1)
    # QUEUE Alljobs ;Collect global statistics
    Queue(sgm, queueName=QUEUE_ALLJOBS, deltaIncrease=1)
    # SEIZE Maintenance ;Obtain TV repairman
    Seize(sgm, facilityName=FAC_MAINTENANCE)
    # DEPART Overhaul ;Leave queue for man
    Depart(sgm, queueName=QUEUE_OVERHAUL, deltaDecrease=1)
    # DEPART Alljobs ;Collect global statistics
    Depart(sgm, queueName=QUEUE_ALLJOBS, deltaDecrease=1)
    # ADVANCE 600,60 ;Complete job 10+/-1 hours
    def advanceCall(owner, timeValue):
        x = random.uniform(-1.0 * 60, 1.0 * 60)
        # file_save.appendToFile(FILENAMES[4], str(x))
        return x
    Advance(sgm, meanTime=600.0, modificatorFunc=advanceCall)
    # RELEASE Maintenance ;Free repairman
    Release(sgm, facilityName=FAC_MAINTENANCE)
    # TERMINATE ;Remove one Transaction
    Terminate(sgm, label="OVERHAUL", deltaTerminate=0)
    
    #--------
    # * On the spot repairs
    # GENERATE 90,10,,,3 ;On-the-spot repairs
    def generateFunc002(owner, currentTime):
        return random.uniform(-10.0, 10.0)    
    Generate(sgm, label="GEN_2",
             med_value=90, modificatorFunc=generateFunc002,
             first_tx=90 + generateFunc002(None, None),
             priority=PRIORITY_SPOT)
    # segment001.addBlock(file_save.FileSave(fileName=FILENAMES[1], funcSave=funcSave, mode="write", label=None))
    def funcHandle2(o, t):
        t[TRANSACT_GROUP] = GEN_2
        print GEN_2
    Handle(sgm, handlerFunc=funcHandle2) 
    # QUEUE Spot ;Queue for spot repairs
    Queue(sgm, queueName=QUEUE_SPOT, deltaIncrease=1)
    # QUEUE Alljobs ;Collect global statistics
    Queue(sgm, queueName=QUEUE_ALLJOBS, deltaIncrease=1)
    # PREEMPT Maintenance,PR ;Get the TV repairman
    Preempt(sgm, facilityName=FAC_MAINTENANCE)
    # DEPART Spot ;Depart the ‘spot’ queue
    Depart(sgm, queueName=QUEUE_SPOT, deltaDecrease=1)
    # DEPART Alljobs ;Collect global statistics
    Depart(sgm, queueName=QUEUE_ALLJOBS, deltaDecrease=1)
    # ADVANCE 15,5 ;Time for tuning/fuse/fault
    def advanceCall002(owner, timeValue):
        x = random.uniform(-1.0 * 5, 1.0 * 5)
        # file_save.appendToFile(FILENAMES[5], str(x))
        return x
    Advance(sgm, meanTime=15.0, modificatorFunc=advanceCall002)
    # RETURN Maintenance ;Free maintenance man
    GReturn(sgm, facilityName=FAC_MAINTENANCE)
    # TERMINATE
    Terminate(sgm, label="SPOT", deltaTerminate=0)
    
    #****************************************************************
    # * Normal repairs on customer owned sets
    # GENERATE 300,60,,,2 ;Normal TV Repairs
    def generateFunc003(owner, currentTime):
        return random.uniform(-60.0, 60.0)    
    Generate(sgm, label="GEN_3",
             med_value=300, modificatorFunc=generateFunc003,
             first_tx=300 + generateFunc003(None, None),
             priority=PRIORITY_SERVICE)
    # segment001.addBlock(file_save.FileSave(fileName=FILENAMES[2], funcSave=funcSave, mode="write", label=None))
    def funcHandle3(o, t):
        t[TRANSACT_GROUP] = GEN_3
        print GEN_3
    Handle(sgm, handlerFunc=funcHandle3) 
    # QUEUE Service ;Queue for service
    Queue(sgm, queueName=QUEUE_SERVICE, deltaIncrease=1)
    # QUEUE Alljobs ;Collect global statistics
    Queue(sgm, queueName=QUEUE_ALLJOBS, deltaIncrease=1)
    # PREEMPT Maintenance,PR ;Preempt maintenance man
    Preempt(sgm, facilityName=FAC_MAINTENANCE)
    # DEPART Service ;Depart the ‘service’ queue
    Depart(sgm, queueName=QUEUE_SERVICE, deltaDecrease=1)
    # DEPART Alljobs ;Collect global statistics
    Depart(sgm, queueName=QUEUE_ALLJOBS, deltaDecrease=1)
    # ADVANCE 120,30 ;Normal service time
    def advanceCall003(owner, timeValue):
        x = random.uniform(-1.0 * 30, 1.0 * 30)
        # file_save.appendToFile(FILENAMES[6], str(x))
        return x    
    Advance(sgm, meanTime=120.0, modificatorFunc=advanceCall003)
    # RETURN Maintenance ;Release the man
    GReturn(sgm, facilityName=FAC_MAINTENANCE)
    # TERMINATE
    Terminate(sgm, label="REPAIRS", deltaTerminate=0)
    #****************************************************************
    # *
    # GENERATE 480 ;One xact each 8 hr. day
    day = [0]
    generate.Generate(sgm, label="GEN_4",
                      med_value=480,
                      # modificatorFunc=DATS[3],
                      modificatorFunc=None,
                      first_tx=0,
                      priority=100)
    def funcHandle4(o, t):
        t["Day"] = day[0]
        day[0] = day[0] + 1
        t[TRANSACT_GROUP] = GEN_4
        print GEN_4
    Handle(sgm, handlerFunc=funcHandle4)    
    # TERMINATE 1
    X_LABEL = "DAYLY"
    Terminate(sgm, label=X_LABEL, deltaTerminate=1)
    # * Day counter
    #-------
    
    ### КАРТИНКИ ----------------------
    m.initPlotTable()
    m.initPlotQueueLifeLine()

#     m.getPlotSubsystem().appendPlotTable(tblAlljobs, title="All Jobs")    
#     m.getPlotSubsystem().appendPlotTable(tblOverhaul, title="Overhaul")    
#     m.getPlotSubsystem().appendPlotTable(tblSpot, title="Spot")    
#     m.getPlotSubsystem().appendPlotTable(tblService, title="Service")    
    
    # активность
    def transactFilter(transact):
        return True
    def funcAnnotate(transact):
        if transact[TRANSACT_GROUP] != GEN_4:
            if transact[TERMINATED_TIME] != transact[TIME_CREATED]: 
                s = "%s:%d (%.2f)" % (transact[TRANSACT_GROUP], transact[NUM], transact[TERMINATED_TIME] - transact[TIME_CREATED])
            else:
                s = "%s:%d" % (transact[TRANSACT_GROUP], transact[NUM])
        else:
            s = "Day: " + str(transact["Day"])
        return s
    m.initPlotTransactLifeLine(
        terminateBlockLabels=["OVERHAUL", "SPOT", "REPAIRS", X_LABEL],
        transactFilter=transactFilter, title="Active ",
        funcAnnotate=funcAnnotate)
    
    m.initPlotFacilityLifeLine(facilityNames=None, title="OCF", funcAnnotate=None)
    # РАСЧЁТ --------------------------
    m.start(terminationCount=1000000, maxTime=MAX_TIME)
    print "Wait..."
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
