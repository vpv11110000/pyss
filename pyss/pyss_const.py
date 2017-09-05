# #!/usr/bin/python
# -*- coding: utf-8 -*-

ALLOWED_ERROR = 1e-07

ID = "ID"

ENTITY_TYPE = "entityType"
NOT_DEFINED = "not_defined"

BLOCK_NEXT = "blockNext"
BLOCK_PREV = "blockPrev"
BLOCK_NEXT_BACKUP = "blockNextBackup"

OPTIONS = "OPT"

BEFORE_BLOCK = "BEFORE_BLOCK"
AFTER_BLOCK = "AFTER_BLOCK"

ALL = "$$ALL"

DISPLAYING = "DISPLAYING"

####################
NAME = "name"
OBJECT_NAME = "objectName"
NUM = "num"
LABEL = "label"
BLOCK_LABELS_LIST = "blockLabelList"
ACTION_FUNC = "actionFunc"
######################
SYSTEM = "SYSTEM"
C1 = "C1"
AC1 = "AC1"
TG1 = "TG1"
Z1 = "Z1"


###############
TRANSACT = "TRANSACT"
HANDLED = "handled"
PARENT = "parent"
NUM_GENERATOR = "numGenerator"
TRANSACT_DELETED = "deleted"
TERMINATED_TIME = "terminatedTime"
# PREEMPT_TIME_LIST = "preemptTimeList"
LIFE_TIME_LIST = "lifeTimeList"
TRACK = "track"

REMAIND_TIME = "remaindTime"

# Related SNAs

# The SNAs associated with Transactions are:

# · A1 - Assembly Set. A1 returns the Assembly Set of the Active Transaction.

# · MBEntnum - Match at Block. MBEntnum returns a 1 if there is a Transaction at Block Entnum which is in the same Assembly Set as the Active Transaction. MBEntnum returns a 0 otherwise. This SNA class should not be used in a Refuse Mode GATE or TEST Block condition test, you should use MATCH Blocks instead.

# · MPParameter - Transit Time, Parameter. Current absolute system clock value minus value in Transaction Parameter Parameter.

# · M1 - Transit Time. M1 returns the absolute system clock minus the "Mark Time" of the Transaction.

# · PParameter or *Parameter - Parameter value. PParameter or *Parameter returns the value of Parameter Parameter of the Active Transaction.

# · PR - Transaction priority. The value of the priority of the Active Transaction.

# · XN1 - Active Transaction. The Transaction Number of the Active Transaction.

# PR - Transaction priority. The value of the priority of the Active Transaction.
PR = "PR"

# M1 - Transit Time. M1 returns the absolute system clock minus the "Mark Time" of the Transaction.
TRANSIT_TIME = "transitTime"
M1 = "M1"
P = "P"
P1 = "P1"
P2 = "P2"
P3 = "P3"
P4 = "P4"
P5 = "P5"
P6 = "P6"
P7 = "P7"
P8 = "P8"
P9 = "P9"
P0 = "P0"

MP = "MP"

# XN1 - Active Transaction. The Transaction Number of the Active Transaction
XN1 = "XN1"

SCHEDULED_TIME = "scheduled_time"
CURRENT_BLOCK = "currentBlock"
DELAYED = "delayed"
ACTIVED = "actived"
PREEMPTED = "preempted"

ENTRY_COUNT = "ENTRY_COUNT"
CURRENT_COUNT = "CURRENT_COUNT"
ASSEMBLE_COUNT = "ASSEMBLE_COUNT"
RETRY = "RETRY"

BLOCK = "BLOCK"

# A1 - Assembly Set. A1 returns the Assembly Set of the Active Transaction.
A1 = "A1"

# Mark Time - The absolute clock time that the Transaction first entered the simulation or entered a MARK Block with no A operand
MARK_TIME = "markTime"

TIME_CREATED = "timeCreated"

#####################################
# GENERATE
GENERATE = "GENERATE"
MED_VALUE = "med_value"
DEVIATION = "deviation"
FIRST_TX = "first_tx"
MAX_AMOUNT = "max_amount"
PRIORITY = "pr"
NEXT_TIME = "nextTime"
COUNT_TRANSACT = "COUNT_TRANSACT"
ENABLED = "enabled"

###################
TERMINATE = "TERMINATE"

ITEMS = "ITEMS"
DELTA_TERMINATE = "deltaTerminate"
ON_DELETED = "onDeleted"

DEFAULT_INIT_TERMINATE_COUNTER = 100

###########################
SEGMENT = "segment"
SEGMENT_CURRENT_EVENT_LIST = "currentEventList"
SEGMENT_FUTURE_EVENT_LIST = "futureEventList"
GENERATES = "GENERATES"
OWNER = "owner"
PLOT_MODULE = "PLOT_MODULE"
PLOT_MODULES = "PLOT_MODULES"

##################################
TABLE = "TABLE"
TABLENAME = "tableName"
TITLE = "TITLE"
ARG = "arg"
ARG_FUNC = "argFunc"
LIMITUPFIRST = "limitUpFirst"
WIDTHINT = "widthInt"
COUNTINT = "countInt"
INTERVALS = "intervals"
TOTAL = "total"
POSITIVE_INFINITY = "positiveInfinity"
NEGATIVE_INFINITY = "negativeInfinity"
VALUES = "values"
MIN_BOUND = "minBound"
MAX_BOUND = "maxBound"
ACTION_VIEW = "actionView"

QTABLE = "QTABLE"

#####################################
TABULATE = "TABULATE"
COEF = "coef"

VAL_FUNC = "VAL_FUNC"


##########################
MODEL = "MODEL"

QUEUE_OBJECTS = "QUEUE_LIST"
SEGMENTS = "SEGMENTS"

START_TIME = "start_time"
END_TIME = "end_time"
TERMINATION_CRITERIA = "TERMINATION_CRITERIA"
MAX_TIME_STR = "max_time"
BLOCKS = "blocks"
FACILITIES = "facilities"
STORAGES = "storages"
PRINT_EVENT_LIST = "printEventList"
START = "start"
END = "end"

TRANSACT_FAMILIES = "TRANSACT_FAMILIES"

CURRENT_TIME = "CURRENT_TIME"
CURRENT_TRANSACT = "CURRENT_TRANSACT"
CURRENT_SEGMENT = "CURRENT_SEGMENT"
DELAYED_LIST = "DELAYED_LIST"

# current event list
CURRENT_EVENT_LIST = "CEL"
# future event list
FUTURE_EVENT_LIST = "FEL"

#
STORAGE = "STORAGE"
BUSY_SIZE = "busySize"
FUNC_BUSY_SIZE = "funcBusySize"
S = "S"  # S$j – ёмкость памяти j;
R = "R"  # R$j – свободная емкость памяти j;
SR = "SR"  # SR$j – коэффициент использования памяти j;
SM = "SM"  # SM$j – максимальное заполнение памяти j;
SA = "SA"  # SA$j – среднее заполнение памяти j;
SC = "SC"  # SC$j – число входов в память j;
ST = "ST"  # ST$j – среднее время пребывания транзакта в памяти j.

# Память имеет также стандартные логические атрибуты,
# которые используются для проверки состояния памяти:
SE = "SE"  # SE$j – память j пуста;
NE = "NE"  # NE$j – память j не пуста;
SF = "SF"  # SF$j – память j заполнена;
SNF = "SNF"  # SNF$j – память j не заполнена.
MIN = "MIN"  #
ENTRIES = "ENTRIES"
AVL = "AVL"
INIT_BUSY_SIZE = "initBusySize"

STORAGE_TRANSACT_KEY = "$$storage_"
TRANSACT_LIST = "trList"

STORAGE_NAME = "STORAGE_NAME"

#
SWITCH = "SWITCH"
RANDOM = "RANDOM"
FUNCTION = "FUNCTION"
VARIABLE = "VARIABLE"
GROUP_NUM = "GROUP_NUM"
TRANSACT_GROUP = "TRANSACT_GROUP"
ASSEMBLY_SET = "ASSEMBLY_SET"
#
FACILITY = "FACILITY"
UTIL = "util"
DELAY = "delay"
RETRY_ATTEMP_LIST = "retryAttempList"
#
SEIZE = "SEIZE"
STATE = "state"
STATE_FREE = "free"
STATE_BUSY = "busy"
STATE_NOT_ACCESS = "notAccess"
TIME_BUSY_START = "timeBusyStart"
TIME_NOT_ACCESS_START = "timeNotAccessStart"
FACILITY_NAME = "FACILITY_NAME"
FACILITY_OBJECT = "FACILITY_OBJECT"

DATA = "d"
DATA_1 = "e"
COUNT_BUSY = "countBusy"
COUNT_NOT_ACCESS = "countNotAccess"
LISTTIMES = "listTimes"
LISTTRANSACT = "listTransact"
LISTPREEMPT = "listPreempt"
LISTTIMES_NOT_ACCESS = "listtimesNotAccess"

ON_STATE_CHANGE = "onStateChange"

#
RELEASE = "RELEASE"

#
ADVANCE = "ADVANCE"
MEAN_TIME = "meanTime"
MODIFICATOR = "modificator"
OUTPUT_FUNC = "OUTPUT_FUNC"
IF_EXPR = "IF_EXPR"

# Очереди
QUEUE = "QUEUE"
QUEUE_NAME = "queueName"
QUEUE_OBJECT = "QUEUE_OBJECT"
STATISTICAL_SERIES = "STATISTICAL_SERIES"
# Q
# Текущая длина очереди. Целочисленное значение.
QUEUE_LENGTH = "queueLength"
# QM
# Максимальная длина очереди. Целочисленное значение.
QUEUE_LENGTH_MAX = "queueLengthMax"
DELTA_INCREASE = "deltaIncrease"
DELTA_DECREASE = "deltaDecrease"
# QZ
# Число нулевых входов в очередь. Целочисленное значение.
ENTRY_ZERO = "entryZero"
# QA
# Взвешенная по времени средняя длина очереди. Вещественное значение.
QUEUE_MEAN_LENGTH_BY_TIME = "queueMeanLengthByTime"

# QC - уже есть для каждого блока ENTRY_COUNT
# Общее число входов в очередь. Целочисленное значение.

# QT
# Среднее время пребывания транзактов в очереди (включая нулевые входы). Вещественное значение.
TIME_MEAN = "timeMean"
# QX
# Среднее время пребывания сообщения в очереди (без нулевых входов). Вещественное значение.
TIME_MEAN_WITHOUT_ZERO = "timeMeanWithoutZero"

DEPART = "DEPART"

#
TRANSFER = "TRANSFER"
FUNC_TRANSFER = "funcTransfer"

TO_BLOCK_LABEL = "toBlockLabel"

PROBABILITY_TO_FIRST_BLOCK = "probability"
LIST = "list"

# inner
firstBlock_4365643 = "__firstBlock_4365643"
# inner
secBlock_4365643 = "__secBlock_4365643"
# inner
TEMP_VALUE = "_$$F312$"
# inner
TEMP_KEYS = "_$$T72$"

#
ASSIGN = "ASSIGN"
PARAMETR_NAME = "parametrName"

HANDLE = "HANDLE"
HANDLER_FUNC = "handlerFunc"

BPRINT = "BPRINT"
OUTPUT_FUNC = "OUTPUT_FUNC"

Must_before_call_FUNC_BUSY_SIZE = "Must before call FUNC_BUSY_SIZE"

#
GATE = "GATE"

# В поле операции блока GATE записывается слово GATE и через пробел - символ проверяемого условия.
# Существует десять условий, которые проверяются в блоке GATE для оборудования:
# NU - устройство свободно (т.е. не используется),
GATE_NOT_USED = "NOT_USED"
NU = GATE_NOT_USED
# U - устройство не свободно (т.е. используется),
GATE_USED = "U"
U = GATE_USED
# NI - устройство не захвачено,
GATE_NOT_INTERRUPTED = "NI"
NI = GATE_NOT_INTERRUPTED
# I - устройство захвачено,
GATE_INTERRUPTED = "I"
I = GATE_INTERRUPTED
# SE - память пуста (все единицы памяти свободны),
GATE_STORAGE_EMPTY = "SE"
SE = GATE_STORAGE_EMPTY
# SNE - память не пуста,
GATE_STORAGE_NOT_EMPTY = "SNE"
SNE = GATE_STORAGE_NOT_EMPTY
# SF - память заполнена (все единицы заняты),
GATE_STORAGE_FULL = "SF"
SF = GATE_STORAGE_FULL
# SNF - память не заполнена,
GATE_STORAGE_NOT_FULL = "SNF"
SNF = GATE_STORAGE_NOT_FULL
# LR - ключ выключен,
GATE_LOGIC_RESET = "LR"
LR = GATE_LOGIC_RESET
# LS - ключ включен.
GATE_LOGIC_SET = "LS"
LS = GATE_LOGIC_SET

CONDITION = "condition"
NEXT_BLOCK_LABEL = "nextBlockLabel"

#
MARK = "MARK"

#
LOOP = "LOOP"
#
TEST = "TEST"
FUNC_CONDITION = "funcCondition"
# ключ задержки при работе с блоками test, для components.delayedList 
KEY_TEST_BLOCK_IF_NOT_CAN_ENTER = "KEY_TEST_BLOCK_IF_NOT_CAN_ENTER"
RESULT_TEST_BLOCK = "resultTestBlock"

AS_LABEL = "AS_LABEL"

ENTER = "ENTER"
LEAVE = "LEAVE"

SPLIT = "SPLIT"
FUNC_COUNT_COPIES = "funcCountCopies"

ASSEMBLE = "ASSEMBLE"
FIRST = "first"

DICT_VALUES = "dictValues"
RANDOM_GENERATOR = "randomGenerator"
LAMBDA_VAL = "lambdaVal"
SCALE_VAL = "scaleVal"

MEAN_VAL = "mean"
STDDEV_VAL = "stdDev"

TERMINATE_BLOCK = "TERMINATE_BLOCK"

LOGIC = "LOGIC"
LOGIC_OBJECT = "LOGIC_OBJECT"
LOGIC_OBJECTS = "LOGIC_OBJECTS"
LOGIC_OBJECT_NAME = "logicObjectName"

FILE_SAVE = "FILE_SAVE"
FILE_READ = "FILE_READ"
FILENAME = "filename"
FUNC_SAVE = "funcSave"
MODE = "mode"
MODE_WRITE = "write"
MODE_APPEND = "append"

FUNC_ANNOTATE = "funcAnnotate"

LIFE_STATES = [ACTIVED, PREEMPTED, DELAYED, TRANSACT_DELETED]
LIFE_STATES_FACILITY = [STATE_BUSY, STATE_FREE, STATE_NOT_ACCESS]


FUNC_OBJ = "funcObj"

MAX_POINT = "maxPoint"

##############
REGISTERED_BLOCK_ENTITY_TYPE = [GENERATE, TERMINATE,
                                TABULATE, SEIZE, RELEASE, ADVANCE, QUEUE,
                                DEPART, TRANSFER, ASSIGN,
                                GATE, MARK, LOOP, TEST, ENTER, LEAVE, SPLIT, ASSEMBLE,
                                BPRINT, HANDLE, FILE_SAVE, FILE_READ, LOGIC]



