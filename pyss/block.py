# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль родительского класса для блоков и других сущностей модели
"""

# pylint: disable=line-too-long

from pyss.pyssownerobject import PyssOwnerObject
from pyss import logger
from pyss.pyss_const import *

class Block(PyssOwnerObject):
    """Базовый класс для блоков

Параметр entityType задает строку, идентифицирующую блок модели.

Параметр label задаёт метку, по которой можно найти блок в сегменте модели:

m.findBlockByLabel('labelOfBlock')

или

block.findBlockByLabel('labelOfBlock')

Атрибуты базового класса блока (в дополнение к атрибутам pyssownerobject.PyssOwnerObject):
bl = <наследник от Block>(...)
bl[ENTRY_COUNT]=0 - количество входов транзактов в блок
bl[CURRENT_COUNT]=0 - текущее количество транзактов в блоке
bl[RETRY]=0 - количество повторных входов транзактов
bl[BLOCK_NEXT]=None - следующий блок в модели, может меняться в ходе моделирования
bl[BLOCK_PREV]=None - предыдущий блок в модели, может меняться в ходе моделирования

    """

    def __init__(self, entityType, label=None, ownerSegment=None):
        super(Block, self).__init__(entityType, label=label, owner=ownerSegment)
        self[ENTRY_COUNT] = 0
        self[CURRENT_COUNT] = 0
        self[RETRY] = 0
        self[BLOCK_NEXT] = None
        self[BLOCK_PREV] = None
        ownerSegment.addBlock(self)
        
    def canEnter(self, transact):
        # pylint: disable=unused-argument, no-self-use
        return True

    def handleCanNotEnter(self, transact):
        pass

    def transactInner(self, currentTime, transact):
        # # must be override
        # pylint: disable=unused-argument, no-self-use
        return transact

    def transactHandle(self, currentTime, transact):

        # pylint: disable=unsubscriptable-object
        m = self.getOwnerModel()
        cs = m.getCurrentSegment()

        rv = False
        b = transact
        if not transact[HANDLED]:
            if cs[OPTIONS]:
                if cs[OPTIONS].logTransactTrace:
                    logger.info("[%s] handle transact\n    [%s] " % (str(self[ENTITY_TYPE]), str(transact)))
            if self.canEnter(transact):
                nextBlock = transact[BLOCK_NEXT]
                transact[BLOCK_NEXT] = None
                transact[HANDLED] = True
                if self[ENTITY_TYPE] != GENERATE:
                    self[ENTRY_COUNT] += 1
                    self[CURRENT_COUNT] += 1
                # transact[BLOCK_NEXT] - может меняться, например в transferto
                b = self.transactInner(currentTime, transact)
                if transact[BLOCK_NEXT] is None and not transact[TRANSACT_DELETED]:
                    transact[BLOCK_NEXT] = nextBlock
            else:
                self.handleCanNotEnter(transact)
        # not join!
        # b can change!
        if b and transact[HANDLED]:
            rv = True
            if transact[BLOCK_NEXT]:
                if transact[BLOCK_NEXT].canEnter(transact):
                    self.transactOut(transact)
                else:
                    transact[BLOCK_NEXT].handleCanNotEnter(transact)
                    rv = False
            else:
                if self[BLOCK_NEXT]:
                    if self[BLOCK_NEXT].canEnter(transact):
                        self.transactOut(transact)
                    else:
                        self[BLOCK_NEXT].handleCanNotEnter(transact)
                        rv = False
                else:
                    rv = False
        return rv

    def moveToNextBlock(self, transact):
        if transact[BLOCK_NEXT]:
            transact[CURRENT_BLOCK] = transact[BLOCK_NEXT]
            transact[BLOCK_NEXT] = None
        else:
            transact[CURRENT_BLOCK] = self[BLOCK_NEXT]
        transact[HANDLED] = False

    def transactOut(self, transact):
        self[CURRENT_COUNT] -= 1
        if self[CURRENT_COUNT] <0:
            # TODO УБРАТЬ
            print "BAD"
        self.moveToNextBlock(transact)

    def getOwnerSegment(self):
        """Получить объект сегмента владельца этого блока"""

        return self[OWNER]
        
    def getOwnerModel(self):
        """Получить объект модели владельца сегмента и соответственно этого блока"""
         
        return self[OWNER][OWNER]

    def __str__(self):
        s = ""
        for key in self:
            if key not in [OWNER, BLOCK_NEXT, BLOCK_PREV]:
                if s:
                    s += ";"
                s += key + ":" + str(self[key])
        return s
    
    def findBlockByLabel(self, label):
        if label is None:
            return None
        return self.getOwnerModel().findBlockByLabel(label)

if __name__ == '__main__':
    pass
    
