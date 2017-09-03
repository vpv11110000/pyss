##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока обработки элементов модели
"""

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

class Handle(Block):
    """Блок обработки элементов модели.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    handlerFunc - определяет функцию обработки.
        Функция handlerFunc вызывается при прохождении транзакта через блок.
        Сигнатура f(owner,transact)

Например, блок

handle.Handle(sgm, handlerFunc=lambda owner,transact: print transact)

печатает объект транзакта.

Пример использования см. demo/demo_assemble.py.

Атрибуты блока Handle (в дополнение к атрибутам block.Block):
bl = Handle(...)
bl[HANDLER_FUNC] - функция вычисления параметра транзакта

    """
    
    def __init__(self, ownerSegment=None, label=None, handlerFunc=None):
        ##modificatorFunc is function(owner,transact)

        #pylint:disable=too-many-arguments

        super(Handle, self).__init__(HANDLE, ownerSegment=ownerSegment, label=label)
        map(pyssobject.raiseIsTrue,[handlerFunc is None])
        self[HANDLER_FUNC]=handlerFunc

    def transactInner(self,currentTime,transact=None):

        #pylint:disable=unused-argument
        self[HANDLER_FUNC](self,transact)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
