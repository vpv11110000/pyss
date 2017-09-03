# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока формирования отметки времени в транзакте
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

class Mark(Block):
    """Блок формирования отметки времени в транзакте
    
При входе транзакта в блок Mark, созданный с параметром parametrName = None, 
в параметр MARK_TIME записывается текущее значение абсолютного времени.

При входе транзакта в блок Mark, созданный с параметром parametrName = <НАИМЕНОВАНИЕ АТРИБУТА>, 
в параметр с наименованием <НАИМЕНОВАНИЕ АТРИБУТА> записывается текущее значение абсолютного времени, 
значение ранее записанное в параметр MARK_TIME не изменяется.
  
Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    parametrName=None - наименование параметра транзакта (параметр цикла), управляющего завершением цикла.
    toBlockLabel=None - метка блока, на который пересылается транзакт, если параметр цикла не равен 0.

При входе транзакта в блок Loop, происходит декремент значения, записанного в параметре parametrName.
Если результат декремента не равен 0, то происходит направление транзакта в блок с меткой toBlockLabel,
иначе в следующий на блоком Loop блок.

Например, блок

mark.Mark(sgm, parametrName="TIKET_TIME")

записывает время прохода блока Mark в параметр "TIKET_TIME".

Пример использования см. tests/test_loop.py.

Атрибуты блока Mark (в дополнение к атрибутам block.Block):
bl = Mark(...)
bl[PARAMETR_NAME] - наименование параметра транзакта (параметр цикла), управляющего завершением цикла

    """
    
    def __init__(self, ownerSegment=None, label=None, parametrName=None):

        # pylint:disable=too-many-arguments

        super(Mark, self).__init__(MARK, label=label, ownerSegment=ownerSegment)
        self[PARAMETR_NAME] = parametrName

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]

        # pylint:disable=unused-argument
        if self[PARAMETR_NAME] is not None:
            transact[self[PARAMETR_NAME]] = self.getOwnerModel().getCurTime()
        else:
            transact[MARK_TIME] = self.getOwnerModel().getCurTime()
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
