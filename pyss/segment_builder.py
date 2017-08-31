# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль формирования встроенных сегментов
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *
from pyss import segment
from pyss import generate
from pyss import bprint_blocks
from pyss import terminate
from pyss import tabulate

def buildSegmentTimeTiker(ownerModel=None, table=None, valFunc=None, maxTime=None):
    """Формирует сегмент с транзактами, формируемыми в моменты времени, заданные целым числом.
    
При выполнении модели печатается текущее время в формате "=== Time: [%.12f]"
    
Args:
    table - если передаётся объект таблицы, то будет встроен блок tabulate.Tabulate для указанной таблицы
    maxTime=None - максимальное время. Обычно  параметр maxTime в старте модели (m.start) должен совпадать с этим параметром
    
    """
    
    if (table is None and valFunc is not None) or (valFunc is None and table is not None):
        raise Exception("Bad table or valFunc")
    sgm = segment.Segment(ownerModel)
    sgm.addBlock(generate.Generate(sgm, med_value=1, modificatorFunc=None, max_amount=maxTime, label=None))
    sgm.addBlock(bprint_blocks.buildBprintCurrentTime(sgm, strFormat="=== Time: [%.12f]", label=None))
    if table:
        sgm.addBlock(tabulate.Tabulate(sgm, table=table, valFunc=valFunc, label=None))
    sgm.addBlock(terminate.Terminate(sgm, deltaTerminate=1, label=None))
    return sgm

def buildSegmentTimeTikerWithoutTimeOutput(ownerModel=None, table=None, valFunc=None, maxTime=None):
    """Формирует сегмент с транзактами, формируемыми в моменты времени, заданные целым числом.
    
Args:
    table - если передаётся объект таблицы, то будет встроен блок tabulate.Tabulate для указанной таблицы
    maxTime=None - максимальное время. Обычно  параметр maxTime в старте модели (m.start) должен совпадать с этим параметром
    
    """
    if (table is None and valFunc is not None) or (valFunc is None and table is not None):
        raise Exception("Bad table or valFunc")
    sgm = segment.Segment(ownerModel=ownerModel, label=None, options_val=None)
    sgm.addBlock(generate.Generate(sgm, med_value=1, modificatorFunc=None, max_amount=maxTime, label=None))
    if table:
        sgm.addBlock(tabulate.Tabulate(sgm, table=table, valFunc=valFunc, label=None))
    sgm.addBlock(terminate.Terminate(sgm, deltaTerminate=1, label=None))
    return sgm

if __name__ == '__main__':
    pass
