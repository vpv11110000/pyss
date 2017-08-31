# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока объединения транзактов, принадлежащих одному семейству (или ансамблю)
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block
from pyss import options
from pyss import logger

class AssembleItem(object):
    """Элемент данных для сбора транзактов
    <первый транзакт>, <сколько осталось до сбора всех транзактов>,<время начала сбора>
    """
    
    def __init__(self, xact=None, assembleCount=None, timeTick=None):
        
        self.transact = xact
        self.assembleCount = assembleCount
        self.timeTick = timeTick
        
    def __str__(self):
        return "t[NUM]:%d, assembleCount:%d, timeTick:%d"%(self.transact[NUM], self.assembleCount, self.timeTick)

class Assemble(Block):
    """Блок объединения транзактов по наименованию семейства (ансамбля)

Наименование семейства (ансамбля) определяется Transact[ASSEMBLY_SET].

Assemble(countTransact=None,label=None)

Параметр countTransact количество объединяемых транзактов.

Args:
    countTransact - количество объединяемых транзактов одного семейства.
    label - см. block.py.

Например, блок

assemble.Assemble(countTransact=2,label="Assemble001")

объединяет каждые два транзакта одного семейства.

Блок Assemble всегда принимает транзакты.
Первый вошедший в блок член семейства остается ждать в нем прибытия
других членов  этого же семейства. Каждый следующий член семейства,
входящий в блок, уничтожается  и количество членов семейства,
подлежащих объединению, уменьшается на единицу.

Если количество членов семейства, подлежащих объединению,
станет равным нулю, то первый вошедший в блок член
семейства пытается войти в следующий блок.

Если транзакт не принадлежит ожидаемому семейству,
то он не обрабатывается, проходит транзитом.

Если countTransact равен 0 или 1, то транзакт проходит транзитом.

Пример использования см. demo/demo_assemble.py.

Атрибуты блока Assemble (в дополнение к атрибутам block.Block):
bl = Assemble(...)
bl[COUNT_TRANSACT] - количество объединяемых транзактов
bl[ITEMS] - хранилище данных сбора транзактов (много семейст - много сборок),
            ключ - номер семейства, значение - объект AssembleItem
            (каждый элемент: key: <assemble set>, value: <объект AssembleItem>)

bl[ON_DELETED] - обработчик события "после удаления транзакта" (сигнатура void handle(transact)).
                 Обработчик устанавливается вне конструктора.

См. также split.py

    """

    def __init__(self, ownerSegment=None, label=None, countTransact=None):

        # pylint:disable=too-many-arguments

        super(Assemble, self).__init__(ASSEMBLE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [countTransact is None])
        self[COUNT_TRANSACT] = countTransact
        # здесь хранятся дванные для сбора семейств транзактов
        # каждый элемент: key: <assemble set>, value: <объект AssembleItem>
        self[ITEMS] = {}
        self[ON_DELETED] = None

    def _refreshCash(self):
        pass

    def canEnter(self, transact):
        return True

    def handleCanNotEnter(self, transact):
        # #
        pass

    def transactInner(self, currentTime, transact=None):
        if self[COUNT_TRANSACT] in [0, 1]:
            return transact
        a=transact[ASSEMBLY_SET]
        if a not in self[ITEMS]:
            # это первый транзакт из собираемых
            self[ITEMS][transact[ASSEMBLY_SET]] = AssembleItem(transact, self[COUNT_TRANSACT] - 1, currentTime)
            return None
        else:
            item=self[ITEMS][a]
            t = item.transact
            tf = t[ASSEMBLY_SET]
            if not tf:
                raise Exception("ASSEMBLY_SET not defined")
            if a == tf:
                item.assembleCount -= 1
                # уничтожаем пришедший транзакт
                transact[TRANSACT_DELETED] = True
                transact[TERMINATED_TIME] = currentTime
                transact.setLifeState(delayed=False, dstState=TRANSACT_DELETED, timeTick=currentTime)
                if item.assembleCount == 0:
                    self[ITEMS].pop(a, None)
                    # собрали self[COUNT_TRANSACT] транзактов семейства
                    # уничтожаем пришедший транзакт, возвращаем первый
                    t[HANDLED] = True
                    self.getOwnerModel().getCel().put(t)
                    self[CURRENT_COUNT] = 1
                elif item.assembleCount > 0:
                    # пришедший транзакт больше не обрабатывается
                    pass
                else:
                    raise Exception("Negative value")
                if self.getOwnerModel().getOptions().logTransactTrack:
                    logger.info("Assemble: Transact[%d] TRACK:%s " % (transact[NUM], transact.strTrack()))                
                if self[ON_DELETED]:
                    self[ON_DELETED](transact)    
                return None            
            else:
                # транзит, не принадлежит требуемому семейству
                return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
