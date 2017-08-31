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
from _ast import Dict

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *
from pyss import generate
from pyss import terminate
from pyss import logger
from pyss import handle
from pyss import file_save
from pyss import qtable
from pyss import counterdec
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import tabulate
from pyss import options
from pyss import components
from pyss import queue
from pyss import assign
from pyss import advance
from pyss import seize
from pyss import depart
from pyss import release
from pyss import storage
from pyss import gate
from pyss import enter
from pyss import leave
from pyss import transfer
from pyss import preempt
from pyss import g_return


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
    #-------------------------------
    options.flags.logCel = True
    options.flags.logFel = True
    options.flags.logDelaiedList = True
    # -------------------------------
    GEN_OVERHAUL = [1]
    ADV_OVERHAUL = 50
    
    GEN_SPOT = [5]
    ADV_SPOT = 5
    
    GEN_REPAIR = [3]
    ADV_REPAIR = 20
    
    #GEN_DAY_MED_VALUE = 8
    #-------------------------------
    PRIORITY_OVERHAUL = 1
    PRIORITY_SPOT = 2
    PRIORITY_REPAIR = 3
    #-------------------------------
    m = pyss_model.PyssModel()
    #-------------------------------
    # MAX_TIME = 100 * 50 * 8 * 60
    MAX_TIME = 100
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
    tblOverhaul = qtable.Qtable(queueName=QUEUE_OVERHAUL, limitUpFirst=10, widthInt=10, countInt=20)
    # Spot QTABLE Spot,10,10,20
    tblSpot = qtable.Qtable(queueName=QUEUE_SPOT, limitUpFirst=10, widthInt=10, countInt=20)
    # Service QTABLE Service,10,10,20
    tblService = qtable.Qtable(queueName=QUEUE_SERVICE, limitUpFirst=10, widthInt=10, countInt=20)
    # Alljobs QTABLE Alljobs,10,10,20
    tblAlljobs = qtable.Qtable(queueName=QUEUE_ALLJOBS, limitUpFirst=10, widthInt=10, countInt=20)
    
    m.addQtable(tblOverhaul)
    m.addQtable(tblSpot)
    m.addQtable(tblService)
    m.addQtable(tblAlljobs)
    #---------
    FAC_MAINTENANCE = "Maintenance"
    
    # -----------------------------------------------------
    # модель в рамках одного сегмента
    # model
    segment001 = segment.Segment(label="TVREPAIR", options_val=options.flags)
    
    TRANSACT_GROUP = "TRANSACT_GROUP"
    GEN_1 = "GEN_O"
    GEN_2 = "GEN_S"
    GEN_3 = "GEN_R"
    GEN_4 = "Day"
    # ------------------------------------------------------
    # Починка телевизионного оборудования компании осуществляется каждые 40±8 часов
    # и занимает 10±1 часов.
    # капитальный ремонт (Overhaul)
    # GENERATE 2400,480,,,1 ;Overhaul of a rented set
    segment001.addBlock(generate.Generate(med_value=None,
                                          modificatorFunc=GEN_OVERHAUL,
                                          first_tx=None,
                                          priority=PRIORITY_OVERHAUL,
                                          label=GEN_1))
    #
    def funcHandle1(o, t):
        t[TRANSACT_GROUP] = GEN_1
        print GEN_1
    segment001.addBlock(handle.Handle(handlerFunc=funcHandle1))    
    # QUEUE Overhaul ;Queue for service
    segment001.addBlock(queue.Queue(queueName=QUEUE_OVERHAUL, deltaIncrease=1, label=None))
    # QUEUE Alljobs ;Collect global statistics
    segment001.addBlock(queue.Queue(queueName=QUEUE_ALLJOBS, deltaIncrease=1, label=None))
    # SEIZE Maintenance ;Obtain TV repairman
    segment001.addBlock(seize.Seize(facilityName=FAC_MAINTENANCE, label=None))
    # DEPART Overhaul ;Leave queue for man
    segment001.addBlock(depart.Depart(queueName=QUEUE_OVERHAUL, deltaDecrease=1, label=None))
    # DEPART Alljobs ;Collect global statistics
    segment001.addBlock(depart.Depart(queueName=QUEUE_ALLJOBS, deltaDecrease=1, label=None))
    # ADVANCE 600,60 ;Complete job 10+/-1 hours
    segment001.addBlock(advance.Advance(meanTime=ADV_OVERHAUL, modificatorFunc=None))
    # RELEASE Maintenance ;Free repairman
    segment001.addBlock(release.Release(facilityName=FAC_MAINTENANCE, label=None))
    # TERMINATE ;Remove one Transaction
    segment001.addBlock(terminate.Terminate(deltaTerminate=0, label="OVERHAUL"))
    
    #--------
    # * On the spot repairs
    # GENERATE 90,10,,,3 ;On-the-spot repairs
    segment001.addBlock(generate.Generate(med_value=None,
                                          modificatorFunc=GEN_SPOT,
                                          first_tx=None,
                                          priority=PRIORITY_SPOT,
                                          label=GEN_2))
    def funcHandle2(o, t):
        t[TRANSACT_GROUP] = GEN_2
        print GEN_2
    segment001.addBlock(handle.Handle(handlerFunc=funcHandle2))    
    # QUEUE Spot ;Queue for spot repairs
    segment001.addBlock(queue.Queue(queueName=QUEUE_SPOT, deltaIncrease=1, label=None))
    # QUEUE Alljobs ;Collect global statistics
    segment001.addBlock(queue.Queue(queueName=QUEUE_ALLJOBS, deltaIncrease=1, label=None))
    # PREEMPT Maintenance,PR ;Get the TV repairman
    segment001.addBlock(preempt.Preempt(facilityName=FAC_MAINTENANCE, label=None))
    # DEPART Spot ;Depart the ‘spot’ queue
    segment001.addBlock(depart.Depart(queueName=QUEUE_SPOT, deltaDecrease=1, label=None))
    # DEPART Alljobs ;Collect global statistics
    segment001.addBlock(depart.Depart(queueName=QUEUE_ALLJOBS, deltaDecrease=1, label=None))
    # ADVANCE 15,5 ;Time for tuning/fuse/fault
    segment001.addBlock(advance.Advance(meanTime=ADV_SPOT, modificatorFunc=None))
    # RETURN Maintenance ;Free maintenance man
    segment001.addBlock(g_return.GReturn(facilityName=FAC_MAINTENANCE, label=None))
    # TERMINATE
    segment001.addBlock(terminate.Terminate(deltaTerminate=0, label="SPOT"))
    
    #****************************************************************
    # * Normal repairs on customer owned sets
    # GENERATE 300,60,,,2 ;Normal TV Repairs
    segment001.addBlock(generate.Generate(med_value=None,
                                          modificatorFunc=GEN_REPAIR,
                                          first_tx=None,
                                          priority=PRIORITY_REPAIR,
                                          label=GEN_3))
    def funcHandle3(o, t):
        t[TRANSACT_GROUP] = GEN_3
        print GEN_3
    segment001.addBlock(handle.Handle(handlerFunc=funcHandle3))    
    # QUEUE Service ;Queue for service
    segment001.addBlock(queue.Queue(queueName=QUEUE_SERVICE, deltaIncrease=1, label=None))
    # QUEUE Alljobs ;Collect global statistics
    segment001.addBlock(queue.Queue(queueName=QUEUE_ALLJOBS, deltaIncrease=1, label=None))
    # PREEMPT Maintenance,PR ;Preempt maintenance man
    segment001.addBlock(preempt.Preempt(facilityName=FAC_MAINTENANCE, label=None))
    # DEPART Service ;Depart the ‘service’ queue
    segment001.addBlock(depart.Depart(queueName=QUEUE_SERVICE, deltaDecrease=1, label=None))
    # DEPART Alljobs ;Collect global statistics
    segment001.addBlock(depart.Depart(queueName=QUEUE_ALLJOBS, deltaDecrease=1, label=None))
    # ADVANCE 120,30 ;Normal service time
    segment001.addBlock(advance.Advance(meanTime=ADV_REPAIR, modificatorFunc=None))
    # RETURN Maintenance ;Release the man
    segment001.addBlock(g_return.GReturn(facilityName=FAC_MAINTENANCE, label=None))
    # TERMINATE
    segment001.addBlock(terminate.Terminate(deltaTerminate=0, label="REPAIRS"))
    
    #****************************************************************
    # *
    # GENERATE 480 ;One xact each 8 hr. day
#     day = [0]
#     segment001.addBlock(generate.Generate(med_value=GEN_DAY_MED_VALUE,
#                                           # modificatorFunc=DATS[3],
#                                           modificatorFunc=None,
#                                           first_tx=0,
#                                           priority=100,
#                                           label="GEN_4"))
#     def funcHandle4(o, t):
#         t["Day"] = day[0]
#         day[0] = day[0] + 1
#         t[TRANSACT_GROUP] = GEN_4
#         print GEN_4
#     segment001.addBlock(handle.Handle(handlerFunc=funcHandle4))    
#     # TERMINATE 1
#     X_LABEL = "DAYLY"
#     segment001.addBlock(terminate.Terminate(deltaTerminate=1, label=X_LABEL))
    # * Day counter
    #-------
    m.addSegment(segment001)
    
    ### КАРТИНКИ ----------------------
    # таблицы
    # m.getPlotSubsystem().appendPlotTable(tblAlljobs, title="All Jobs")    
    # m.getPlotSubsystem().appendPlotTable(tblOverhaul, title="Overhaul")    
    # m.getPlotSubsystem().appendPlotTable(tblSpot, title="Spot")    
    # m.getPlotSubsystem().appendPlotTable(tblService, title="Service")    
    
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
        #terminateBlockLabels=["OVERHAUL", "SPOT", "REPAIRS", X_LABEL],
        terminateBlockLabels=["OVERHAUL", "SPOT", "REPAIRS"],
        transactFilter=transactFilter, title="Active ",
        funcAnnotate=funcAnnotate)
    
    m.initPlotFacilityLifeLine(facilityNames=None, title="OCF", funcAnnotate=None)
    
    # РАСЧЁТ --------------------------
    m.start(terminationCount=1000000, maxTime=MAX_TIME)
    
    # ПОКАЗ КАРТИНОК ------------------------
    m.getPlotSubsystem().plotByModules()
    m.getPlotSubsystem().show()

if __name__ == '__main__':
    main()
