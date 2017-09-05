# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long

import random
from pyss import pyssobject, plot_subsystem, counterdec
from pyss.pyssobject import ErrorSegmentExists, ErrorQueueObjectExists, ObjectNumber
from pyss.pyssownerobject import PyssOwnerObject
from pyss import plot_table, plot_storage_lifeline, plot_queue_lifeline
from pyss import plot_facility_lifeline
from pyss.pyssobject import PyssObject
from pyss.pyssobject import ErrorKeyExists
from pyss.transact import Transact
from pyss import logger
from pyss import queue_event_priorities
from pyss import queue_event_by_time
from pyss.pyss_const import *  # @UnusedWildImport
from pyss import facility
from pyss import options
from pyss import plot_transact_lifeline
from pyss.statisticalseries import StatisticalSeries
from pyss.pyssstateobject import PyssStateObject

debugRandomValue = False

if debugRandomValue:
    logger.info("=== GENERATE in DEBUG mode")
    random.seed(1)
else:
    logger.info("=== GENERATE in PRODUCT mode")
    random.seed()

class PyssModel(PyssStateObject):
    """Объект модели

Содержит сегменты модели.
Последовательность сегментов формируется в соответствии с порядком их добавления.
Приоритеты транзактов учитываются только в рамках обработки текущего сегмента модели.

Можно назначать обработчики изменения состояния (см. PyssStateObject).
Под значением старого состояния понимается старое значение модельного времени.

    """

    def __init__(self, optionz=None):
        super(PyssModel, self).__init__(MODEL, label=None, owner=MODEL)

        if optionz is None:
            self[OPTIONS] = options.Options()
        else:
            self[OPTIONS] = optionz
            
        # Генератор номеров транзактов
        self.transactNumber = ObjectNumber()  

        self.plotSubsystem = plot_subsystem.PlotSubsystem()
        self[PLOT_MODULES] = []

        self[SEGMENTS] = []
        # Текущее значение счетчика завершений
        self.terminateCounter = counterdec.CounterDec(DEFAULT_INIT_TERMINATE_COUNTER)

        # list of all GENERATE
        self.generates = []

        #
        self[QUEUE_OBJECTS] = {}
        self.qtableList = {}
        self.tableList = {}

        # памяти или многоканальные устройства
        self[STORAGES] = {}


        # {transactParent1[NUM]:[transactCopy001,transactCopy002,...,transactCopyN],
        # transactParent1[NUM]:[...],
        # ...}
        self[TRANSACT_FAMILIES] = {}

        # dict of entitytype.label, all without transact
        # {FACILITY.FAC_1:Facility(...),...,QUEUE.Q_1:Queue(...),...}
        self.entitytypeWithLabel = {}

        # переменные модели
        self.variables = {}

        #
        self[MAX_TIME_STR] = 1000
        self[START_TIME] = None
        self[END_TIME] = None
        # Словарь устройств
        self[FACILITIES] = {}
        # словарь логических ключей
        self[LOGIC_OBJECTS] = {}
        # перечень всех блоков модели
        # инициализируется из сегментов при вызове метода старт
        self[BLOCKS] = []
        # текущий активный транзакт
        self[CURRENT_TRANSACT] = None
        # текущая секция
        self[CURRENT_SEGMENT] = None
        # Список задержки ОКУ или МКУ;
        # {facilityName:queue_event_priorities.QueueEventPriorities(reverse=True)}
        self[DELAYED_LIST] = {}
        # # Список текущих событий;
        # {"name of fac": state (STATE_FREE or STATE_BUSY or STATE_NOT_ACCESS)}
        # self[SEGMENT_CURRENT_EVENT_LIST]=queue_event_priorities.QueueEventPriorities(reverse=True)
        self[CURRENT_EVENT_LIST] = queue_event_priorities.QueueEventPriorities(reverse=True)

        # # Список будущих событий;
        # self[SEGMENT_FUTURE_EVENT_LIST]=queue_event_by_time.QueueEventByTime(reverse=False)
        self[FUTURE_EVENT_LIST] = queue_event_by_time.QueueEventByTime(reverse=False)

        # Текущее значение условного времени.
        # Автоматически изменяется в модели  и  устанавливается
        # в  0 управляющими операторами CLEAR или RESET. Вещественное значение.
        self[CURRENT_TIME] = 0

    def getOptions(self):
        return self[OPTIONS]

    def getQueueList(self):
        return self[QUEUE_OBJECTS]

    def addQueueObject(self, queueObject):
        if queueObject[QUEUE_NAME] in self[QUEUE_OBJECTS].keys():
            raise ErrorQueueObjectExists("queueObject also exists [%s]" % queueObject[QUEUE_NAME])
        self[QUEUE_OBJECTS][queueObject[QUEUE_NAME]] = queueObject
        queueObject[NUM] = len(self[QUEUE_OBJECTS].keys())

    def getCurTime(self):
        """Текущее значение условного времени.

    Автоматически изменяется в модели. Вещественное значение.

        """

        return self[CURRENT_TIME]

    def getCurrentTransact(self):
        """Текущий активный транзакт.

    Транзакт, который, в текущий момент curTime, перемещается  по модели.

        """
        return self[CURRENT_TRANSACT]

    def setCurrentTransact(self, newCurrentTransact):
        self[CURRENT_TRANSACT] = newCurrentTransact

    def addSegment(self, segm):
        """Добавить сегмент

        Не используйте прямой вызов
        Вызывается в конструкторе сегмента segment.Segment
        """

        if segm in self[SEGMENTS]:
            raise ErrorSegmentExists("Segment exists")

        self[SEGMENTS].append(segm)
        segm[NUM] = len(self[SEGMENTS])
        # segm[OWNER] = self - уже
        for g in segm[GENERATES]:
            if g not in self.generates:
                self.generates.append(g)
        return self

    def addPlotModule(self, plotModule):
        self[PLOT_MODULES].append(plotModule)

    def getCurrentSegment(self):
        """Текущая секция.

    Секция, в которой, в текущий момент curTime, перемещаются транзакты

        """
        return self[CURRENT_SEGMENT]

    def setCurrentSegment(self, currentSegment):
        """Установить значение текущей секции"""

        self[CURRENT_SEGMENT] = currentSegment

    def getOptionForCurrentSegment(self):
        return self[CURRENT_SEGMENT][OPTIONS]

    def getCel(self):
        return self[CURRENT_EVENT_LIST]

    def getFel(self):
        return self[FUTURE_EVENT_LIST]

    def getStorages(self):
        return self[STORAGES]

    def getFacilities(self):
        return self[FACILITIES]
    
    def getLogicObject(self):
        return self[LOGIC_OBJECTS]

    def findFacility(self, facilityName):
        if facilityName not in self[FACILITIES]:
            return None
        return self[FACILITIES][facilityName]

    def findLogicObject(self, logicObjectName):
        if logicObjectName not in self[LOGIC_OBJECTS]:
            return None
        return self[LOGIC_OBJECTS][logicObjectName]
    
    def getDelayedList(self):
        return self[DELAYED_LIST]

    def appendToDelayedList(self, key, transact):
        transact.setLifeState(delayed=True, dstState=DELAYED, timeTick=self[CURRENT_TIME])
        if key not in self[DELAYED_LIST]:
            self[DELAYED_LIST][key] = queue_event_priorities.QueueEventPriorities(reverse=True)
        self[DELAYED_LIST][key].put(transact)

    def removeAllFromDelayedList(self, tranzact):
        if tranzact is None:
            return
        for _, qep in self[DELAYED_LIST].iteritems():
            qep.remove(tranzact)

    def extractFromDelayedListFirst(self, key):
        t=self[DELAYED_LIST][key].extractFirst()
        if t is not None:
            # исключить t из всех списков
            self.removeAllFromDelayedList(t)
        return t

    def initDelayedListForKey(self, key):
        if key not in self[DELAYED_LIST]:
            self[DELAYED_LIST][key] = queue_event_priorities.QueueEventPriorities(reverse=True)

    def moveTransactFromFelToCel(self, currentTime):
        cur_el = self[CURRENT_EVENT_LIST]
        fut_el = self[FUTURE_EVENT_LIST]
        currentSegment = self[CURRENT_SEGMENT]
        t = fut_el.extractByTime(currentTime)
        while t:
            if t[SCHEDULED_TIME] <= currentTime:
                if currentSegment:
                    if currentSegment[OPTIONS]:
                        if currentSegment[OPTIONS].logTransactMoveFromFelToCel:
                            logger.info("move transact from FEL to CEL: [%s]" % str(t))
                b = t[CURRENT_BLOCK]
                if b:
                    if b[ENTITY_TYPE] == ADVANCE:
                        b.transactOut(t)
                cur_el.put(t)
            t = fut_el.extractByTime(currentTime)

    def moveFromDelayedList_KEY_TEST_BLOCK_IF_NOT_CAN_ENTER_toCel(self):
        delayedList = self[DELAYED_LIST]
        cel = self[CURRENT_EVENT_LIST]
        if KEY_TEST_BLOCK_IF_NOT_CAN_ENTER in delayedList:
            t = delayedList[KEY_TEST_BLOCK_IF_NOT_CAN_ENTER].extractFirst()
            while t:
                cel.put(t)
                t = delayedList[KEY_TEST_BLOCK_IF_NOT_CAN_ENTER].extractFirst()

    def addTable(self, table):
        """Добавить таблицу"""
        key = table[TABLENAME]
        if key in self.tableList:
            raise ErrorKeyExists("Key exists: [%s]" % key)
        self.tableList[key] = table
        table[NUM] = len(self.tableList.keys())
        return self

    def addQtable(self, qtable):
        """Добавить таблицу с данными очереди"""
        key = qtable[QUEUE_NAME]
        if key in self.qtableList:
            raise ErrorKeyExists("Key exists: [%s]" % key)
        self.qtableList[key] = qtable
        return self

    def addStorage(self, storage):
        key = storage[STORAGE_NAME]
        if key in self[STORAGES]:
            raise ErrorKeyExists("Key exists: [%s]" % key)
        self[STORAGES][key] = storage
        storage[NUM] = len(self[STORAGES].keys())
        delayedList = self[DELAYED_LIST]
        if key not in delayedList:
            delayedList[key] = queue_event_priorities.QueueEventPriorities(reverse=True)
        else:
            raise Exception("Name is exists in delayedList")
        return self

    def addLogicObject(self, logicObject):
        """Добавление логического ключа в модель

        Напрямую не вызывать.
        Вызывается конструктором LogicObject.
        """
        
        key = logicObject[LOGIC_OBJECT_NAME]
        if key in self[LOGIC_OBJECTS]:
            raise ErrorKeyExists("Key exists: [%s]" % key)
        self[LOGIC_OBJECTS][key] = logicObject
        logicObject[NUM] = len(self[LOGIC_OBJECTS].keys())
        return self        

    def addFacility(self, faclity):
        """Добавление устройства в модель

        Напрямую не вызывать.
        Вызывается конструктором Facility.
        """
        
        key = faclity[FACILITY_NAME]
        if key in self[FACILITIES]:
            raise ErrorKeyExists("Key exists: [%s]" % key)
        delayedList = self[DELAYED_LIST]
        # faclity[OWNER] = self - уже сделано
        if key not in delayedList:
            delayedList[key] = queue_event_priorities.QueueEventPriorities(reverse=True)
        else:
            raise Exception("Name is exists")
        self[FACILITIES][key] = faclity
        faclity[NUM] = len(self[FACILITIES].keys())
        return self
    
    def addPlot(self, plotModule):
        """Добавление диаграммы в модель

        Напрямую не вызывать.
        Вызывается конструкторами диаграмм Plot.*.
        """

        self.plotSubsystem.append(plotModule)

    def setCurrentTime(self, currentTime):
        # ВАЖНО использовать, есть компоненты обращающиеся к components.curTime
        # напрямую
        self[CURRENT_TIME] = currentTime

    def getPlotSubsystem(self):
        return self.plotSubsystem

    def initPlotTransactLifeLine(self,
                                 terminateBlockLabels=None,
                                 transactFilter=True,
                                 title="Active time",
                                 funcAnnotate=None):
        """Настраивает подсистему диаграмм для отображения линий жизни транзактов для блоков Terminate.

        Все транзакты отображаются на одной диаграмме.

        Args:
            terminateBlockLabels=None - список меток блоков Terminate.
                                        None - все блоки Terminate.
                                        [] - ни одного блока Terminate.
                                        ["label1",...] - блоки Terminate с метками "label1" и т.д.
            transactFilter=True - фильтр транзактов (True - обрабатывать все транзакты
                                  или функция bool f(transact))
            title=None - название диаграммы
            funcAnnotate=None - функция аннторирования линии жизни транзакта.
                                По умолчанию: lambda transact:str(transact[NUM])

        """
        blocks = self.getBlocks()
        if terminateBlockLabels is None:
            b = [t for t in blocks if t[ENTITY_TYPE] == TERMINATE]
        else:
            b = [t for t in blocks if t[LABEL] in terminateBlockLabels]
        if transactFilter is True:
            tf = lambda t:True
        else:
            tf = transactFilter
        p = plot_transact_lifeline.PlotTransactLifeLine(self, terminateBlock=b,
                                                        transactFilter=tf,
                                                        title=title,
                                                        funcAnnotate=funcAnnotate)
        for x in b:
            x[ON_DELETED] = p.append

    def initPlotFacilityLifeLine(self, facilityNames=None, title=None, funcAnnotate=None):
        """Настраивает подсистему диаграмм для отображения линий жизни ОКУ.

Все ОКУ отображаются на одной диаграмме.

Args:
    facilities=None - ОКУ или список наименований ОКУ. Если None, то диаграмма строится для всех ОКУ.
    title - заголовок диаграммы
    funcAnnotate - функция аннторирования линии жизни ОКУ.
                   По умолчанию: lambda faclty:facility[FACILITY_NAME]

        """
        if facilityNames is None:
            b = [self[FACILITIES][t] for t in sorted(self[FACILITIES].keys())]
        else:
            b = [self[FACILITIES][t] for t in sorted(self[FACILITIES].keys()) if t[FACILITY_NAME] in facilityNames]
        plot_facility_lifeline.PlotFacilityLifeLine(self, facilities=b,
                                                    title=title,
                                                    funcAnnotate=funcAnnotate)

    def initPlotStorageLifeLine(self, storageNames=None, title=None, funcAnnotate=None):
        """Настраивает подсистему диаграмм для отображения линий жизни МКУ.

Args:
    storageNames=None - МКУ или список наименований ОКУ. Если None, то диаграмма строится для всех МКУ.
    title - заголовок диаграммы
    funcAnnotate - функция аннторирования линии жизни ОКУ.

        """
        if storageNames is None:
            b = [self[STORAGES][t] for t in sorted(self[STORAGES].keys())]
        else:
            b = [self[STORAGES][t] for t in sorted(self[STORAGES].keys()) if t[STORAGE_NAME] in storageNames]
        for t in b:
            plot_storage_lifeline.PlotStorageLifeLine(self, stor=t,
                                                      title=(title + " " + t[STORAGE_NAME]) if title is not None else t[STORAGE_NAME],
                                                      funcAnnotate=funcAnnotate)

    def initPlotQueueLifeLine(self, queueNames=None, title=None, funcAnnotate=None):
        """Настраивает подсистему диаграмм для отображения линий жизни Очередей.

Args:
    queueNames=None - список наименований очередей. Если None, то диаграмма строится для всех очередей.
    title - заголовок диаграммы
    funcAnnotate - функция аннторирования линии жизни Очереди.

        """
        if queueNames is None:
            b = [self[QUEUE_OBJECTS][t] for t in sorted(self[QUEUE_OBJECTS].keys())]
        else:
            b = [self[QUEUE_OBJECTS][t] for t in sorted(self[QUEUE_OBJECTS].keys()) if t[STORAGE_NAME] in queueNames]
        for t in b:
            plot_queue_lifeline.PlotQueueLifeLine(self, queueObject=t,
                                                  title=(title + " " + t[QUEUE_NAME]) if title is not None else t[QUEUE_NAME],
                                                  funcAnnotate=funcAnnotate)


    def initPlotTable(self, tableNames=None, title="Table:"):
        """Настраивает подсистему диаграмм для отображения данных таблиц Table.

Args:
    tableNames=None - список наименований таблиц.
                      Если None, то диаграммы строятся для всех таблиц модели.
    title - заголовок диаграммы

        """
        if tableNames is None:
            b = [self.tableList[t] for t in sorted(self.tableList.keys())]
        else:
            b = [self.tableList[t] for t in sorted(self.tableList.keys()) if t[TABLENAME] in tableNames]
        for t in b:
            plot_table.PlotTable(self, t, (title + "\n" + t[TABLENAME]) if title is not None else t[TABLENAME])

    def _firstTx(self):
        g = []
        for seg in self[SEGMENTS]:
            for gg in seg[GENERATES]:
                g.append(gg[FIRST_TX])
        return min(g)

    def run(self):

        self[START_TIME] = self._firstTx()
        currentTime = self[START_TIME]
        # ВАЖНО использовать, есть компоненты обращающиеся к components.curTime
        # напрямую
        self.setCurrentTime(currentTime)
        self[START_TIME] = currentTime
        while True:
            if self[OPTIONS].logTransactTrace:
                logger.info("### Time=%s " % str(currentTime) + 40 * "#")
            # else:
                # logger.display("\r>>> Time=%s"%str(currentTime))
            try:
                for s in self[SEGMENTS]:
                    self.setCurrentSegment(s)
                    if self[OPTIONS].printSegmentLabel and s[LABEL]:
                        logger.info("--- Segment: %s " % str(s[LABEL]) + 20 * "-")
                    s.handle(currentTime)
            except pyssobject.TerminationCounterIsEmpty:
                pass
            if self.terminateCounter.isEmpty():
                logger.info("\nStop by terminateCounter is Zero")
                break
            nextTime = self.findMinTime()
            if nextTime <= currentTime or not nextTime:
                logger.info("\nextTime<=currentTime or not nextTime")
                break
            if self[TERMINATION_CRITERIA] is not None and self[TERMINATION_CRITERIA]():
                break
            if self[MAX_TIME_STR]:
                if nextTime > self[MAX_TIME_STR]:
                    logger.info("\nStop by Max Time")
                    break
            oldTime = currentTime
            currentTime = nextTime
            # ВАЖНО использовать, есть компоненты обращающиеся к components.curTime
            # напрямую
            self.setCurrentTime(currentTime)
            self.fireHandlerOnStateChange(oldState=oldTime)
        self[END_TIME] = currentTime

    def beforeStart(self, terminationCriteria=None, terminationCount=None, maxTime=1000):
        if not self[SEGMENTS]:
            raise "Segments not exists"
        logger.reset()
        #
        self.initBlocksFromSegments()

        self[TERMINATION_CRITERIA] = terminationCriteria
            
        self[MAX_TIME_STR] = maxTime
        # Текущее значение счетчика завершений
        self.terminateCounter.reset(terminationCount)
        

    def start(self, terminationCriteria=None, terminationCount=None, maxTime=1000):
        if not self[SEGMENTS]:
            raise "Segments not exists"
        self.beforeStart(terminationCriteria, terminationCount, maxTime)

        logger.info("*** Start simulation with [%d]" % terminationCount)
        self.printHeader()
        # ВЫПОЛНЕНИЕ МОДЕЛИРОВАНИЯ -----------------------------
        self.run()
        logger.info("*** Stop simulation")
        # ПЕЧАТЬ РЕЗУЛЬТАТА
        self.printResult()

    def printHeader(self):
        logger.info(40 * "=")
        logger.info("terminationCount=%d" % self.terminateCounter.value)
        logger.info("MaxTime=%d" % self[MAX_TIME_STR])
        logger.info(logger.dump(self[OPTIONS], objName="options", excl=["setAll", "setAllFalse", "setAllTrue"]))
        logger.info(40 * "=")

    def strBlocksHandle(self):
        rv = "=== BLOCKS ===\n"
        rv += "LABEL          BLOCK TYPE     ENTRY COUNT   CURRENT COUNT   RETRY\n"
        for s in self[SEGMENTS]:
            rv += "%10s   %12s %s\n" % (s[LABEL] if s[LABEL] else "", s[ENTITY_TYPE], 35 * "-")
            for b in s[BLOCKS]:
                rv += "%10s   %12s   %10s   %10s   %10s\n" % (b[LABEL] if b[LABEL] else "", b[ENTITY_TYPE], b[ENTRY_COUNT], b[CURRENT_COUNT], b[RETRY])
        return rv

    def strBlocksHandleDebug(self):
        rv = "=== BLOCKS ===\n"
        rv += "LABEL          BLOCK TYPE     ENTRY COUNT   CURRENT COUNT   RETRY\n"
        for s in self[SEGMENTS]:
            rv += "%10s   %12s %s\n" % (s[LABEL] if s[LABEL] else "", s[ENTITY_TYPE], 35 * "-")
            for b in s[BLOCKS]:
                rv += "%10s   %12s   %10s   %10s   %10s\n" % (b[LABEL] if b[LABEL] else str(b[NUM]),
                                                              b[ENTITY_TYPE],
                                                              b[ENTRY_COUNT],
                                                              b[CURRENT_COUNT],
                                                              b[RETRY])
        return rv

    def strQueueHandle(self):
        if not self[QUEUE_OBJECTS]:
            return ""
        rv = "%10s   %12s   %10s   %10s   %10s      %10s   %10s\n" % ("QUEUE",
                                                                      "MAX", "ENTRY", "ENTRY(0)",
                                                                      "AVE.TIME", "AVE.(-0)", "RETRY")
        l = sorted(self[QUEUE_OBJECTS])
        for qn in l:
            q = self[QUEUE_OBJECTS][qn]
            a = q[TIME_MEAN]
            b = q[TIME_MEAN_WITHOUT_ZERO]
            rv += "%10s   %12s   %10s   %10s     %10s   %10s   %10s\n" % (qn,
                                                                        q[QUEUE_LENGTH_MAX],
                                                                        q[ENTRY_COUNT],
                                                                        q[ENTRY_ZERO],
                                                                        str(a),
                                                                        str(b),
                                                                        q[RETRY])
        return rv

    def strTransactFamilies(self):
        if not self[OPTIONS].reportTransactFamilies:
            return ""
        if not self[TRANSACT_FAMILIES]:
            return ""
        rv = "=== Transact Families ===\n"
        s = ""
        l = sorted(self[TRANSACT_FAMILIES])
        for k in l:
            if s:
                s += "\n"
            s += "Parent:%d\n" % k
            for t in self[TRANSACT_FAMILIES][k]:
                s += str(t) + "//"
        return rv + s

    def strCel(self):
        if not self[OPTIONS].reportCel:
            return ""
        rv = "=== Current Event List ===\n"
        cel = self[CURRENT_EVENT_LIST]
        s = str(cel)
        if s:
            return rv + s
        else:
            return ""


    def strFacilities(self):
        if not self[FACILITIES]:
            return ""

        # FACILITY ENTRIES UTIL. AVE. TIME AVAIL. OWNER PEND INTER RETRY DELAY
        # FACILITY1   51  0.937    95.278    1      51    0    0     0     9
        # FACILITY2   51  0.853    86.719    1      51    0    0     0     0
        # FACILITY3   51  0.949    96.523    1      51    0    0     0     0
        rv = "%10s   %12s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s\n" % ("FACILITY",
                                                                             "ENTRIES", "UTIL.", "AVE. TIME", "AVAIL.", "OWNER", "PEND", "INTER", "RETRY", "DELAY")
        ttm = self.getCurTime()
        # ttm = self[END_TIME]
        
        l = sorted(self[FACILITIES])
        for ff in l:
            f = self[FACILITIES][ff]
            a = StatisticalSeries().extend(f[LISTTIMES]).mean()
            rv += "%10s   %12s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s\n" % (
                f[FACILITY_NAME], f[COUNT_BUSY],
                '{0:.3f}'.format(float(f[UTIL]) / float(ttm)), str(a), 0, 0, 0, 0, f[RETRY], f[DELAY])
        return rv

    def strStorages(self):

        # STORAGE CAP. REM. MIN. MAX. ENTRIES AVL. AVE.C. UTIL. RETRY DELAY
        # POOL    400  400    0  150    5000   1   23.628 0.059   0     0

        # · STORAGE. Name or number of the Storage entity.

        # · CAP. The Storage capacity of the Storage entity defined in the STORAGE statement.

        # · REM. The number of unused Storage units at the end of the simulation.

        # · MIN. The minimum number of Storage units in use during the measurement period. A measurement period begins with the Translation of a model or the issuing of a RESET or CLEAR command.

        # · MAX. The maximum number of Storage units in use during the measurement period.

        # · ENTRIES. The number of "entries" into the Storage entity during the measurement period. The total accumulation of operand B of ENTER statements.

        # · AVL. The availability state of the Storage entity at the end of the simulation. 1 means available, 0 means unavailable.

        # · AVE.C. The time weighted average of the Storage content during the measurement period. The space-time product divided by the time duration of the measurement period.

        # · UTIL. The fraction of the total space-time product of the Storage entity utilized during the measurement period.

        # · RETRY. The number of Transactions waiting for a specific condition depending on the state of this Storage entity.

        # · DELAY. The number of Transactions waiting to enter ENTER blocks on behalf of this Storage entity.

        # STORAGE CAP. REM. MIN. MAX. ENTRIES AVL. AVE.C. UTIL. RETRY DELAY
        # POOL    400  400    0  150    5000   1   23.628 0.059   0     0
        if not self[STORAGES]:
            return ""

        rv = "%10s   %12s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s\n" % ("STORAGE",
                                                                             "CAP.", "REM.", "MIN.", "MAX.", "ENTRIES", "AVL.", "AVE.C.", "UTIL.", "RETRY", "DELAY")
        ttm = self.getCurTime()
        l = sorted(self[STORAGES])
        for ss in l:
            s = self[STORAGES][ss]
            s.recalc(timeValue=ttm)
            rv += "%10s  %12s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s   %10s\n" % (
                s[LABEL], s[S], s[R], s[MIN], s[SM], s[ENTRIES], s[AVL], s[SA], '{0:.3f}'.format(s[SR]), s[RETRY], s[DELAY])
        return rv

    def strTables(self):
        if not self.tableList:
            return ""

        # TABLE         MEAN      STD.DEV.   RANGE    RETRY    FREQUENCY CUM.%
        # TRANSIT      553.184     307.992
        # 0 - 200.000   8      16.00
        # 200.000 - 400.000  10      36.00
        # 400.000 - 600.000   7      50.00
        # 600.000 - 800.000  12      74.00
        # 800.000 - 1000.000 11      96.00
        # 1000.000 - 1200.000 2     100.00
        rv = ""
        keys = self.tableList.keys()
        keys.sort()

        for each in keys:
            t = self.tableList[each]
            if t[DISPLAYING] is True:
                rv += t.table2str()
        return rv

    def strQtables(self):
        if not self.qtableList:
            return ""

        # QTABLE        MEAN      STD.DEV.   RANGE    RETRY    FREQUENCY CUM.%
        # TRANSIT      553.184     307.992
        # 0 - 200.000   8      16.00
        # 200.000 - 400.000  10      36.00
        # 400.000 - 600.000   7      50.00
        # 600.000 - 800.000  12      74.00
        # 800.000 - 1000.000 11      96.00
        # 1000.000 - 1200.000 2     100.00
        rv = ""
        keys = self.qtableList.keys()
        keys.sort()

        for each in keys:
            t = self.qtableList[each]
            if t[DISPLAYING] is True:
                rv += t.table2str()
        return rv

    def printResult(self):
        if self[OPTIONS].printResult:
            logger.printLine("=== REPORT ===")
            logger.printLine(self.commonInfo())
            logger.printLine(self.strBlocksHandle())
            logger.printLine(self.strFacilities())
            logger.printLine(self.strQueueHandle())
            logger.printLine(self.strQtables())
            logger.printLine(self.strStorages())
            logger.printLine(self.strTables())
            logger.printLine(self.strTransactFamilies())
            logger.printLine(self.strCel())


    def commonInfo(self):
        s = "Start time      End time        Blocks       Facilities      Storages\n%10s    %10s    %10s       %10s    %10s"
        s = s % (str(self[START_TIME]),
                 str(self[END_TIME]),
                 str(len(self[BLOCKS])),
                 str(len(self[FACILITIES])),
                 str(len(self[STORAGES])))
        return s


    def __str__(self):
        rv = "Segments:\n"
        if not self[SEGMENTS]:
            rv += "-\n"
        else:
            for s in self[SEGMENTS]:
                rv += str(s) + "\n"
        return rv
    
    def getBlocks(self):
        r = []
        for s in self[SEGMENTS]:
            for b in s[BLOCKS]:
                r.append(b)
        return r

    def findBlockByLabel(self, label):
        """Ищет блок модели по метке.

        Возвращает первый найденый блок.
        Если не найден возвращает None, иначе объект блока

        """
        
        if label is None:
            return None

        for s in self[SEGMENTS]:
            for b in s[BLOCKS]:
                if b[LABEL] == label:
                    return b
        return None

    def initBlocksFromSegments(self):
        self[BLOCKS] = []
        for s in self[SEGMENTS]:
            for b in s[BLOCKS]:
                self[BLOCKS].append(b)

#     def initQueueFromSegments(self):
#         bl = [b for b in [s[BLOCKS] for s in self[SEGMENTS]]]
#         self[QUEUE_OBJECTS] = {q[QUEUE_NAME] : q for q in [b[QUEUE_OBJECT] for b in bl if b[ENTITY_TYPE] == QUEUE]}

#     def initFacilitiesFromSegments(self):
#         bl = [b for b in [s[BLOCKS] for s in self[SEGMENTS]]]
#         self[FACILITIES] = {q[FACILITY_NAME] : q[FACILITY_OBJECT] for q in [b[QUEUE_OBJECT] for b in bl if b[ENTITY_TYPE] == ENTER]}

    def findMinTimeFromGenerates(self):
        # # mintime by list of all GENERATE
        l = [g.findNextTime() for g in self.generates if g[ENABLED] and g[NEXT_TIME] is not None]
        t = None
        if l:
            t = min(l)
        return t

    def findMinTime(self):
        # # mintime by list of all GENERATE and FEL
        tr = self[FUTURE_EVENT_LIST].first()
        t = self.findMinTimeFromGenerates()
        if t and tr:
            return min(t, tr[SCHEDULED_TIME])
        elif t:
            return t
        else:
            if tr is not None:
                return tr[SCHEDULED_TIME]
            else:
                return None
            
    def existsQueue(self, queueName):
        return queueName in self[QUEUE_OBJECTS].keys()
    
    def findQueue(self, queueName):
        if queueName in self[QUEUE_OBJECTS].keys():
            return self[QUEUE_OBJECTS][queueName]
        else:
            return None

    def logTransactTrace(self, strValue):
        """

        Траса транзактов, если включен флаг self[OPTIONS].logTransactTrace
        """

        if self[OPTIONS].logTransactTrace:
            logger.info(strValue)
            
    def plotByModulesAndSave(self, filename):
        self.plotSubsystem.plotByModulesAndSave(filename)

    def plotByModulesAndShow(self):
        self.getPlotSubsystem().plotByModules()
        self.getPlotSubsystem().show()
        
if __name__ == '__main__':
    pass
