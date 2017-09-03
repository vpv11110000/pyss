# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока проверки условия и выбора дальнейшего маршрута транзакта
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss.transact import Transact
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

T123 = "$$$123"
T124 = "$$$124"

class Test(Block):
    """Блок проверки условия и выбора дальнейшего маршрута транзакта

Если условие выполняется (self[FUNC_CONDITION](transact) is True), транзакту разрешается вход и прохождение блока.
Если условие не выполняется (self[FUNC_CONDITION](transact) is not True):
- если задан параметр move2block, то транзакт переходит в указанный в параметре move2block блок;
- если параметр move2block не задан, то транзакт задерживается в предыдущем блоке. 

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    funcCondition=None - функция вычисления условия, сигнатура: bool f(owner, transact)
    move2block=None - метка блока, к которому будет направляться транзакт, если условие не будет выполняться

Например, блок

test.Test(sgm, funcCondition=lambda t: getCurrentTransact()[NUM] % 2 != 0,move2block="IF_EVEN")

будет направлять транзакты с чётными номерами в блок с меткой "IF_EVEN", 
а транзактам с нечётными номерами входит в блок.

Пример использования см.:
- tests/test_test.py

Атрибуты блока Test (в дополнение к атрибутам block.Block):
bl = Test(...)
bl[FUNC_CONDITION] - функция вычисления условия, сигнатура: bool f(transact)
bl[TO_BLOCK_LABEL] - метка блока, к которому будет направляться транзакт, 
                     если условие не будет выполняться
bl[firstBlock_4365643] - кеш, внутреннее использование
bl[secBlock_4365643] - кеш, внутреннее использование
    
    """
    
    def __init__(self, ownerSegment=None, label=None, funcCondition=None, move2block=None):
        
        # pylint:disable=too-many-arguments

        super(Test, self).__init__(TEST, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [funcCondition is None])
        self[FUNC_CONDITION] = funcCondition
        self[TO_BLOCK_LABEL] = move2block
        self[firstBlock_4365643] = None
        self[secBlock_4365643] = None
        
    def canEnter(self, transact):
        b = self[FUNC_CONDITION](self, transact) is True
        transact[RESULT_TEST_BLOCK] = b
        return b or self[TO_BLOCK_LABEL] is not None

    def handleCanNotEnter(self, transact):
        # если задан атрибут self[TO_BLOCK_LABEL], 
        #    то транзакт переходит в указанный в параметре блок (см. transactInner);
        # если атрибут self[TO_BLOCK_LABEL] не задан, то транзакт задерживается в предыдущем блоке.
        if self[TO_BLOCK_LABEL] is None:
            m = self.getOwnerModel()
            m.appendToDelayedList(KEY_TEST_BLOCK_IF_NOT_CAN_ENTER, transact)
        transact[RESULT_TEST_BLOCK] = None

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]

        # pylint:disable=unused-argument
        if not self[firstBlock_4365643]:
            block = self.findBlockByLabel(self[TO_BLOCK_LABEL])
            self[firstBlock_4365643] = block
            self[secBlock_4365643] = self[BLOCK_NEXT]

        if RESULT_TEST_BLOCK in transact: 
            if transact[RESULT_TEST_BLOCK] is True:
                # Если условие выполняется (self[FUNC_CONDITION](transact) is True), 
                # транзакту разрешается вход и прохождение блока.
                block = self[secBlock_4365643]
            elif transact[RESULT_TEST_BLOCK] is False: 
                # изменение маршрута
                # если задан атрибут self[TO_BLOCK_LABEL], 
                # то транзакт переходит в указанный в параметре move2block блок
                block = self[firstBlock_4365643]
            else:
                raise Exception("Transact [%s] eq or less 0" % self[PARAMETR_NAME])
            if block is None:
                raise Exception("Block not found, label is [%s]" % self[TO_BLOCK_LABEL])
            self[BLOCK_NEXT] = block
            transact[RESULT_TEST_BLOCK] = None
        else:
            raise Exception("Transact hasnt [%s]" % RESULT_TEST_BLOCK)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
