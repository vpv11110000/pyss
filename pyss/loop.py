##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока организации циклического прохождения транзакта
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.block import Block
from pyss.pyss_const import *

class Loop(Block):
    """Блок организации циклического прохождения транзактов
    
Args:
    parametrName=None - наименование параметра транзакта (параметр цикла), управляющего завершением цикла.
    toBlockLabel=None - метка блока, на который пересылается транзакт, если параметр цикла не равен 0.
    label - метка блока, см. block.py.

При входе транзакта в блок Loop, происходит декремент значения, записанного в параметре parametrName.
Если результат декремента не равен 0, то происходит направление транзакта в блок с меткой toBlockLabel,
иначе в следующий на блоком Loop блок.

Например, блок

loop.Loop(parametrName="COUNT_LOOP_CIKL",toBlockLabel="BEGIN_LOOP",label=None)

направляет транзакт tr на блок с меткой "BEGIN_LOOP", если атрибут tr["COUNT_LOOP_CIKL"] не равен 0.

Пример использования см. tests/test_loop.py.

Атрибуты блока Loop (в дополнение к атрибутам block.Block):
bl = Loop(...)
bl[PARAMETR_NAME] - наименование параметра транзакта (параметр цикла), управляющего завершением цикла
bl[TO_BLOCK_LABEL] - метка блока, на который пересылается транзакт
bl[firstBlock_4365643] - внутреннее использование
bl[secBlock_4365643] - внутреннее использование

    """
    
    def __init__(self, ownerSegment=None, label=None, parametrName=None, toBlockLabel=None):
        # #modificatorFunc is function(parametrName)

        # pylint:disable=too-many-arguments

        super(Loop, self).__init__(LOOP, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [parametrName is None or parametrName.strip() == "", toBlockLabel is None or toBlockLabel.strip() == ""])
        self[PARAMETR_NAME] = parametrName
        self[TO_BLOCK_LABEL] = toBlockLabel
        self[firstBlock_4365643] = None
        self[secBlock_4365643] = None

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]

        # pylint:disable=unused-argument
        if not self[firstBlock_4365643]:
            block = self.findBlockByLabel(self[TO_BLOCK_LABEL])
            self[firstBlock_4365643] = block
            self[secBlock_4365643] = self[BLOCK_NEXT]

        if self[PARAMETR_NAME] in transact:
            p = transact[self[PARAMETR_NAME]]
            p -= 1
            transact[self[PARAMETR_NAME]] = p
            if p > 0:
                block = self[firstBlock_4365643]
            elif p == 0:
                block = self[secBlock_4365643]
            else:
                raise Exception("Transact [%s] eq or less 0" % self[PARAMETR_NAME])
            if block is None:
                raise Exception("Block not found, label is [%s]" % self[TO_BLOCK_LABEL])
            self[BLOCK_NEXT] = block

        else:
            raise Exception("Transact hasnt [%s]" % self[PARAMETR_NAME])
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
