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

class Test(Block):
    """Блок проверки условия и выбора дальнейшего маршрута транзакта

Если условие выполняется (self[FUNC_CONDITION](transact) is True), транзакту разрешается вход и прохождение блока.
Если условие не выполняется (self[FUNC_CONDITION](transact) is not True):
- если задан параметр move2block, то транзакт переходит в указанный в параметре move2block блок;
- если параметр move2block не задан, то транзакт задерживается в предыдущем блоке. 

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    funcCondition=None - функция вычисления условия, сигнатура: bool f(owner)
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
    
    """
    
    def __init__(self, ownerSegment=None, label=None, funcCondition=None, move2block=None):
        
        # pylint:disable=too-many-arguments

        super(Test, self).__init__(TEST, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [funcCondition is None])
        self[FUNC_CONDITION] = funcCondition
        self[TO_BLOCK_LABEL] = move2block
        self[firstBlock_4365643] = None
        self[secBlock_4365643] = None
        self[KEY_FOR_DELAYED_LIST] = None
        
    def _buildKeyForDelayedList(self):
        if self[KEY_FOR_DELAYED_LIST] is None:
            self[KEY_FOR_DELAYED_LIST] = "$$" + self.getOwner()[ENTITY_TYPE] + "_" + str(self.getOwner()[NUM]) + "_" + self[ENTITY_TYPE] + "_" + str(self[NUM]) 
        return self[KEY_FOR_DELAYED_LIST]        
        
    def checkFuncCondition(self):
        """
        Return:
            None - self[TO_BLOCK_LABEL] is not None, условие не проверяется
            True - условие выполняется
            False - условие не выполняется
        """
        
        if self[TO_BLOCK_LABEL] is not None:
            return None
        return self[FUNC_CONDITION](self) is True
        
    def canEnter(self, tranzact):
        b = self.checkFuncCondition()
        if b is None:
            return True
        return b     
    
    def moveTransactFromDelayedListToCel(self):
        m = self.getOwnerModel()
        m.moveFromDelayedListForKey_toCel(self._buildKeyForDelayedList())   

    def handleCanNotEnter(self, transact):
        # если задан атрибут self[TO_BLOCK_LABEL], 
        #    то транзакт переходит в указанный в параметре блок (см. transactInner);
        # если атрибут self[TO_BLOCK_LABEL] не задан, то транзакт задерживается в предыдущем блоке.
        
        if self[TO_BLOCK_LABEL] is None:
            k = self._buildKeyForDelayedList()
            m = self.getOwnerModel()
            m.appendToDelayedList(k, transact)

    def transactInner(self, currentTime, tranzact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]

        # pylint:disable=unused-argument
        c = self[FUNC_CONDITION](self)
        if self[TO_BLOCK_LABEL] is not None:
            if not c:
                block = self.findBlockByLabel(self[TO_BLOCK_LABEL])
            else:
                block = self[BLOCK_NEXT]
        else:
            if c is True:
                block = self[BLOCK_NEXT]
            else:
                raise pyssobject.ErrorBadAlgorithm("Test().transactInner")
        tranzact[BLOCK_NEXT] = block
        return tranzact

if __name__ == '__main__':
    def main():
        print "?"

    main()
