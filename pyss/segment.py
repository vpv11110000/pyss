# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль класса сегмента модели
"""

# pylint: disable=line-too-long

import sys
from pyss.pyssstateobject import PyssStateObject
from pyss.pyssobject import *
from pyss import pyssobject
from pyss.pyss_const import *
from pyss.generate import Generate
from pyss.terminate import Terminate

class Segment(PyssStateObject):
    """Сегмент - контейнер для блоков модели
    
Сегменты увеличивают автономию частей модели друг от друга.
Приоритеты транзактов, сформированных в разных сегментах, не обрабатываются.

Транзакты сегментов обрабатываются в порядке следования сегментов в модели.
Нумерация транзактов сквозная в рамках модели.

Можно назначать обработчики изменения состояния (см. PyssStateObject).
Под значением старого состояния понимается значение ссылки 
на предыдущий обрабатываемый транзакт.

Args:
    ownerModel=None - объект модели-владельца
    label=None - заголовок сегмента
    options_val - опции сегмента
    ownerModel=None - объект модели, в которую добавляется сегмент
    
Атрибуты (в дополнение к pyssownerobject.):
s=Segment(...)
s[BLOCK_LABELS_LIST] = {} - словарь меток и блоков модели
s[GENERATES]=[] - список блоков Generate
s[BLOCKS] - блоки сегмента
s[OPTIONS]=options_val - опции модели:
    options_val.logCel - вывод текущего содержимого списка текущих событий
    options_val.logFel - вывод текущего содержимого списка будущих событий
s[BEFORE_BLOCK]=None - обработчик события перед вызовом block.transactHandle (сигнатура void f(block))
s[AFTER_BLOCK]=None - обработчик события после вызова block.transactHandle (сигнатура void f(block))

    """
    
    def __init__(self, ownerModel=None, label=None, options_val=None):
        super(Segment, self).__init__(SEGMENT, label=label, owner=ownerModel)
        
        # Генератор номеров блоков
        self.blockNumber = ObjectNumber()
        
        self[BLOCK_LABELS_LIST] = {}
        self[GENERATES] = []
        self[BLOCKS] = []
        self[OPTIONS] = options_val
        self[BEFORE_BLOCK] = None
        self[AFTER_BLOCK] = None
        self[BLOCK_TESTS]=[]
        ownerModel.addSegment(self)

    def addBlock(self, block):
        """Добавляет блок обработки транзакта в модель
        
        Не использовать напрямую.
        При попытке добавления блока с меткой, 
        уже существующей в сегменте формируется исключение с сообщением "LABEL is exists: [%s]".
        
        В добавленном в сегмент блоке атрибуту OWNER присваивается ссылка на обхъект сегмента, владельца блока.
        
        """
        
        if block[ENTITY_TYPE] not in REGISTERED_BLOCK_ENTITY_TYPE:
            raise Exception("Not registered %s in %s" % (block[ENTITY_TYPE], str(REGISTERED_BLOCK_ENTITY_TYPE)))
        if block[LABEL] in self[BLOCK_LABELS_LIST]:
            raise Exception("LABEL is exists: [%s]" % (block[LABEL]))
        if block[ENTITY_TYPE] == GENERATE:
            self[GENERATES].append(block)
            if self.getModel():
                self.getModel().generates.append(block)
        if block[ENTITY_TYPE] == TEST:
            self[BLOCK_TESTS].append(block)
        lastBlock = None
        if self[BLOCKS]:
            lastBlock = self[BLOCKS][-1]
        self[BLOCKS].append(block)
        block[NUM] = len(self[BLOCKS])
        if lastBlock:
            if lastBlock[ENTITY_TYPE] != TERMINATE:
                lastBlock[BLOCK_NEXT] = block
        # if block[ENTITY_TYPE] != GENERATE:
        block[BLOCK_PREV] = lastBlock
        block[BLOCK_NEXT] = None
        if block[LABEL]:
            self[BLOCK_LABELS_LIST][block[LABEL]] = block
        # block[OWNER] = self - уже сделано в PyssOwnerObject
        return self

    def handle(self, currentTime):
        """Обработка транзактов модели в заданный момент времени"""
        
        m = self.getOwner()
        
        # move from FEL to CEL
        m.moveTransactFromFelToCel(currentTime)
        # handle GENERATEs
        for g in [z for z in self[GENERATES] if z[ENABLED]]:
            if g.findNextTime() == currentTime:
                if self[BEFORE_BLOCK] is not None:
                    self[BEFORE_BLOCK](g)
                g.transactHandle(currentTime, None)
                if self[AFTER_BLOCK] is not None:
                    self[AFTER_BLOCK](g)

        opt = self[OPTIONS]

        # free FACILITIES
        # handle components.CEL
        cel = m.getCel()
        fel = m.getFel()
        if opt and opt.logCel and not cel.isEmpty():
            logger.info("---CEL BEGIN:\n%s\n--- CEL END" % str(cel))
        if opt and opt.logFel and not m.getFel().isEmpty():
            logger.info("---FEL BEGIN:\n%s\n--- FEL END" % str(fel))
        t = cel.extractFirst()
        oldTransact = None
        while t:
            t.refreshAttr(self.getModel().getCurTime())
            # if not t[BLOCK_NEXT]:
            if t[CURRENT_BLOCK] is not None:
                block = t[CURRENT_BLOCK]
            elif t[BLOCK_NEXT] is not None:
                # TODO ПРОБЛЕМА transfer seize
                block = t[BLOCK_NEXT]
            else:
                raise ErrorIsNone("t[CURRENT_BLOCK] and t[BLOCK_NEXT] are None ")
            m.setCurrentTransact(t)
            self.fireHandlerOnStateChange(oldTransact)
            while block:
                if not t[HANDLED]:
                    t[TRACK].append((currentTime, block))
                if self[BEFORE_BLOCK] is not None:
                    self[BEFORE_BLOCK](block)
                try:
                    r = block.transactHandle(currentTime, t)
                    if self[AFTER_BLOCK] is not None:
                        self[AFTER_BLOCK](block)
                    for z in self[BLOCK_TESTS]:
                        if z.checkFuncCondition() is True:
                            z.moveTransactFromDelayedListToCel()                            
                    if r:
                        if not t[TRANSACT_DELETED]:
                            block = t[CURRENT_BLOCK]
                    else:
                        break
                except Exception as e:
                    _, tr = t[TRACK][-1]
                    logger.warn("\n\n*** ERROR TRACE START *" 
                                + 45 * "*" 
                                + "\n\n" 
                                + self.strBlocksDebug(tr[NUM])
                                # + self.getModel().strBlocksHandleDebug()
                                + "\n\n=== TRACK TRANSACT t[NUM]=%d ===\n" % (t[NUM]) + t.strTrackDebug() + "\n"
                                + "\n*** ERROR TRACE END *" 
                                + 45 * "*" 
                                + "\n")
                    raise e, None, sys.exc_info()[2]
                    
            if self.getModel().terminateCounter.isEmpty():
                raise pyssobject.TerminationCounterIsEmpty("Finish")
            oldTransact = t
            t = cel.extractFirst()
        m.setCurrentTransact(None)
        
    def strBlocks(self):
        """Строка с данными о блоках"""
        l = ["[%s]:[%s]" % (r[LABEL] if r[LABEL] else str(r[NUM]), r[ENTITY_TYPE]) for r in self[BLOCKS]]
        s = reduce((lambda x, y: x + "; " + y), l)
        return s         
    
    def strBlocksDebug(self, lastBlockNum):
        """Строка с данными о блоках"""
        rv = "=== BLOCKS in segemnt ===\n"
        rv += "LABEL or NUM   BLOCK TYPE     ENTRY COUNT   CURRENT COUNT   RETRY\n"
        rv += "%10s   %12s %s\n" % (self[LABEL] if self[LABEL] else str(self[NUM]),
                                    self[ENTITY_TYPE], 35 * "-")
        for b in self[BLOCKS]:
            if b[NUM] != lastBlockNum:
                rv += "%10s   %12s   %10s   %10s   %10s\n" % ("%d/%s" % (b[NUM], b[LABEL]) if b[LABEL] else str(b[NUM]),
                                                              b[ENTITY_TYPE],
                                                              b[ENTRY_COUNT],
                                                              b[CURRENT_COUNT],
                                                              b[RETRY])
            else:
                rv += "\nlast block --> \n%10s   %12s   %10s   %10s   %10s\n\n" % ("%d/%s" % (b[NUM], b[LABEL]) if b[LABEL] else str(b[NUM]),
                                                              b[ENTITY_TYPE],
                                                              b[ENTRY_COUNT],
                                                              b[CURRENT_COUNT],
                                                              b[RETRY])
                
        return rv

    def setOnBeforeBlock(self, handlerFunc):
        """Установка обработчика события перед вызовом block.transactHandle (сигнатура void f(block))
        
        Сигнатура f(block)
        
        """
        
        self[BEFORE_BLOCK] = handlerFunc
        return self

    def setOnAfterBlock(self, handlerFunc):
        """Установка обработчика события после вызова block.transactHandle (сигнатура void f(block))
        
        Сигнатура f(block)
        
        """
        
        self[AFTER_BLOCK] = handlerFunc
        return self
    
    def getModel(self):
        """Объект модели-владельца сегмента"""
        return self.getOwner()

if __name__ == '__main__':
    pass

