# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с функциями создания блоков вывода на экран часто используемых параметров сущностей модели.

def buildBprintDelaiedList(strFormat="delayedList: [%s]", label=None):
def buildBprintCurrentTransact(strFormat="Transact: [%s]", label=None):
def buildBprintQueue(queueName = None,strFormat="Queue: [%s]", label=None):
def buildBprintFEL(strFormat="FEL: [%s]", label=None):
def buildBprintCurrentTime(strFormat="Time: [%.12f]", onlyOncePerCurrentTime = True,label=None):
def buildBprintDelaiedList(strFormat="delayedList: [%s]", label=None):

"""

from pyss.pyss_const import *
from pyss import bprint
from pyss import pyssobject

# pylint: disable=line-too-long

def buildBprintDelaiedList(ownerSegment=None, label=None, strFormat="delayedList: [%s]"):
    """Сформировать блок для вывода данных списка задержанных событий

    Args:
        strFormat - строка формата вывода
        label     - метка блока

    """
    return bprint.Bprint(ownerSegment, label, outputFunc=lambda owner, transact: strFormat % str(owner.getOwnerModel().delayedList))

def buildBprintCurrentTransact(ownerSegment=None, label=None, funcTransactToStr=None, strFormat="Transact: [%s]"):
    """Сформировать блок для вывода данных текущего транзакта

    Args:
        funcTransactToStr - функция преобразования к строке, сигнатура funcTransactToStr(transact)
        strFormat - строка формата вывода
        label     - метка блока

    """
    if funcTransactToStr is None:
        return bprint.Bprint(ownerSegment, label, outputFunc=lambda owner, transact: strFormat % str(transact))
    else:
        return bprint.Bprint(ownerSegment, label, outputFunc=lambda owner, transact: strFormat % funcTransactToStr(transact))

def buildBprintQueue(ownerSegment=None, label=None, queueName=None, strFormat="Queue: [%s]"):
    """Сформировать блок для вывода данных очереди

    Args:
        queueName - наименование очереди (см. queue)
        strFormat - строка формата вывода
        label     - метка блока

    Пример: test_queue.py

    """
    pyssobject.raiseIsTrue(queueName is None or queueName == "")
    def queue2str(owner, transact):
        m = owner.getOwnerModel()
        # pylint: disable=unused-argument
        if queueName in m[QUEUE_OBJECTS]:
            return strFormat % str(m[QUEUE_OBJECTS][queueName])
        else:
            return "Queue not found: [%s]" % str(queueName)

    return bprint.Bprint(ownerSegment, label, outputFunc=queue2str)

def buildBprintFEL(ownerSegment=None, label=None, strFormat="FEL: [%s]"):
    """Сформировать блок для вывода данных Списка будущих событий components.FEL

    Args:
        strFormat - строка формата вывода
        label     - метка блока

    Пример: test_queue.py

    """
    def fel2str(owner, transact):
        # pylint: disable=unused-argument
        m = owner.getOwnerModel()
        return strFormat % str(m.getFel())

    return bprint.Bprint(ownerSegment, label, outputFunc=fel2str)

def buildBprintCurrentTime(ownerSegment=None, label=None, strFormat="Time: [%.12f]", onlyOncePerCurrentTime=True):
    """Сформировать блок для вывода текущего времени

    Args:
        strFormat - строка формата вывода
        onlyOncePerCurrentTime - выводить текущее время только один раз
        label     - метка блока

    Пример: test_queue.py

    """
    def timeFunc(owner, transact):
        # pylint: disable=unused-argument
        m = owner.getOwnerModel()
        if onlyOncePerCurrentTime and hasattr(timeFunc, 'oldTime'):
            if timeFunc.oldTime != m.getCurTime():
                timeFunc.oldTime = m.getCurTime()
                return strFormat % m.getCurTime()
        else:
            timeFunc.oldTime = m.getCurTime()
            return strFormat % m.getCurTime()

    return bprint.Bprint(ownerSegment, label, outputFunc=timeFunc)

if __name__ == '__main__':
    def main():
        print "?"

    main()
