# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока вывода на экран параметров сущностей модели
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class Bprint(Block):
    """Блок вывода на экран параметров сущностей модели.

При входе транзакта в блок, инициируется вызов функции, задаваемой
параметром outputFunc, и печать результата её выполнения.

Под сущностями модели понимаются любые объекты, например транзакт, устройство или блок,
любые другие данные или их совокупность.

Вывод полностью определяется функцией передаваемой в outputFunc.

Если outputFunc равен None, то никакой обработки не происходит.

Args:
    outputFunc - функция с сигнатурой str function(owner,transact).
        Возвращает строку, выводимую на экран.
    ifExpr - функция беp параметров, возвращающая True/False. Если True - то разрешается вывод.
             Значение ifExpr == None разрешает вывод.

Описание параметра label см. block.py.

Например, блок

bprint.Bprint(outputFunc=lambda owner,transact: str(transact),
    label=None)

выведет на экран данные транзакта transact.

Пример использования см. tests/test_assign.py.

Атрибуты блока Bprint (в дополнение к атрибутам block.Block):
bl = Bprint(...)
bl[OUTPUT_FUNC] - функция, возвращающая строку, выводимую на экран.
bl[IF_EXPR] - функция без параметров, возвращающая True/False. Если True - то разрешается вывод.
              Можно использовать, например bl.setIfExpr(lambda: True)

    """

    def __init__(self, ownerSegment=None, label=None, outputFunc=None, ifExpr=None):
        # #outputFunc is function(owner,transact)

        # pylint:disable=too-many-arguments

        super(Bprint, self).__init__(BPRINT, label=label, ownerSegment=ownerSegment)
        self[OUTPUT_FUNC] = outputFunc
        self[IF_EXPR] = ifExpr

    def transactInner(self, currentTime, transact=None):
        # pylint:disable=unused-argument
        b = self[IF_EXPR] is None
        if not b:
            b = bool(self[IF_EXPR]())
        if b:
            logger.printLine(self[OUTPUT_FUNC](self, transact))
        return transact

    def setIfExpr(self, ifExpr=None):
        self[IF_EXPR] = ifExpr
        return self

if __name__ == '__main__':
    def main():
        print "?"

    main()
