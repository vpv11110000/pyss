##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль занесения текущих значений характеристик модели в таблицу
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss import table as moduleTable

class Tabulate(Block):
    """Блок Tabulate для результата вызова argFunc таблицы вычисляет valFunc и помещает в таблицу.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    table=None - объект таблицы, argFunc задаёт аргументы таблицы
    valFunc=1 - функция вычисления значения для аргумента таблицы.
                Если valFunc - число, то преобразуется в лямбду и охраняется в атрибут VAL_FUNC.

Например, блок

tabulate.Tabulate(sgm, table=tbl,valFunc=1)

при прохождении транзакта будет заполнять таблицу tbl.

Пример использования см. tests/test_enter_leave.py.

См. также test_enter_leave.py

Атрибуты блока Tabulate (в дополнение к атрибутам block.Block):
bl = Tabulate(...)
bl[TABLE] - объект таблицы.
bl[FUNC_BUSY_SIZE] - число занимаемых единиц памяти или функция, возвращающая указанное число
bl[VAL_FUNC] - функция вычисления значения.

    """

    def __init__(self, ownerSegment=None, label=None, table=None,valFunc=1):
        #coef - function(owner,transact)
        super(Tabulate, self).__init__(TABULATE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [not isinstance(table, moduleTable.Table)])
            
        self[TABLE] = table
        if pyssobject.isfunction(valFunc):
            self[VAL_FUNC]=valFunc
        else:
            self[VAL_FUNC]=lambda x,y: valFunc

    def transactInner(self,currentTime,transact):
        if self[VAL_FUNC] is not None:
            self[TABLE].handleTransact(transact, coef=self[VAL_FUNC](self,transact))
        else:
            self[TABLE].handleTransact(transact, 1)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
