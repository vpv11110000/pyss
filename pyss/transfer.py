# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока изменения маршрута движения транзакта в модели
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss.transact import Transact
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class Transfer(Block):
    """Блок изменения маршрута движения транзакта в модели

Для определения следующего блока вычисляется функция, возвращающая блок, 
на который должен быть перемещён транзакт.

Args:
    funcTransfer=None - строка с меткой блока или функция вычисления следующего блока, 
                        сигнатура: <extend Block> f(owner, transact).
                        Если функция возвращает None, то транзакт переходт к следующему за текущим блоку. 
    label - см. block.py.

Например, блок

transfer.Transfer(funcTransfer=lambda o,t: o.findBlockByLabel("ВСЕГДА СЛЕДУЮЩИЙ БЛОК"), label=None)

будет направлять транзакты на блок, помеченный меткой "ВСЕГДА СЛЕДУЮЩИЙ БЛОК".

Пример использования см.:
- tests/test_test.py

Атрибуты блока Transfer (в дополнение к атрибутам block.Block):
bl = Test(...)
bl[FUNC_TRANSFER] - функция вычисления следующего блока, сигнатура: <extend Block> f(owner, transact)
bl[secBlock_4365643] - внутреннее использование, копия оригинального значения следующего блока
    
    """
    
    def __init__(self, ownerSegment=None, label=None, funcTransfer=None):
        # #

        # pylint:disable=too-many-arguments

        super(Transfer, self).__init__(TRANSFER, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [funcTransfer is None,
                                     not (pyssobject.isfunction(funcTransfer) 
                                          or isinstance(funcTransfer, basestring))])
        if pyssobject.isfunction(funcTransfer):
            self[FUNC_TRANSFER] = funcTransfer
        elif isinstance(funcTransfer, basestring):
            blockName = funcTransfer
            self[FUNC_TRANSFER] = lambda o, t: self.findBlockByLabel(blockName)
        self[secBlock_4365643] = None

    def transactInner(self, currentTime, transact=None):

        # pylint:disable=unused-argument
        if not self[secBlock_4365643]:
            self[secBlock_4365643] = self[BLOCK_NEXT]
        block = self[FUNC_TRANSFER](self, transact)
        if block is None:
            block = self[secBlock_4365643]
        transact[BLOCK_NEXT] = block
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
