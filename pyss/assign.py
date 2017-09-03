# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока, задания значения параметра транзакта.
"""

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

class Assign(Block):
    """Блок задания значения параметра транзакта.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)
    parametrName - наименование изменяемого параметра транзакта
    modificatorFunc - определяет функцию вычисления параметра транзакта.
        Функция modificatorFunc вызывается при прохождении транзакта через блок (Assign).
        Сигнатура f(owner,transact)

Например, блок

assign.Assign(sgm, parametrName='ASSEMBLY_SET',
    modificatorFunc=lambda owner,transact: 'ASSEMBLE_001',
    label=None)

устанавливает наименование семейства транзакта в 'ASSEMBLE_001'.

Атрибуты блока Assign (в дополнение к атрибутам block.Block):
bl = Assign(...)
bl[PARAMETR_NAME] - количество объединяемых транзактов
bl[MODIFICATOR] - функция вычисления параметра транзакта

    """
    
    def __init__(self, ownerSegment=None, label=None, parametrName=None, modificatorFunc=None):

        # pylint:disable=too-many-arguments

        super(Assign, self).__init__(ASSIGN, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [parametrName is None or parametrName.strip() == "", modificatorFunc is None])
        self[PARAMETR_NAME] = parametrName
        self[MODIFICATOR] = modificatorFunc

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]

        # pylint:disable=unused-argument
        transact[self[PARAMETR_NAME]] = self[MODIFICATOR](self, transact)
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
