# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока, проверяющий состояния устройств, памятей, логических ключей
"""

# pylint: disable=line-too-long


from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss.transact import Transact
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block
from pyss import facility

# pylint: disable=line-too-long

class Gate(Block):
    """Блок, проверяющий состояния устройств, памятей, логических ключей
    
Если проверяемое условие для объекта выполняется (True), то транзакт входит в блок GATE. 

Если проверяемое условие не выполняется (False), то возможны два случая:
1. если параметр nextBlockLabel задан (is not None), то транзакт идет в соответствующий блок;
2) если параметр nextBlockLabel is None, то транзакт ждет в предыдущем блоке, пока не выполнится условие. 

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    condition - условие
        GATE_NOT_USED или NU - устройство свободно (т.е. не используется),
        GATE_USED или U - устройство не свободно (т.е. используется),
        GATE_NOT_INTERRUPTED или NI - устройство не захвачено,
        GATE_INTERRUPTED или I - устройство захвачено,
        GATE_STORAGE_EMPTY или SE - память пуста (все единицы памяти свободны),
        GATE_STORAGE_NOT_EMPTY или SNE - память не пуста,
        GATE_STORAGE_FULL или SF - память заполнена (все единицы заняты),
        GATE_STORAGE_NOT_FULL или SNF - память не заполнена,
        GATE_LOGIC_RESET или LR - ключ выключен,
        GATE_LOGIC_SET или LS - ключ включен.    
    
    objectName - наименование объекта, м.б. facility, память, ключ.
        
    nextBlockLabel - метка блока, кода будет направлен транзакт если условие не выполняется
        Если параметр nextBlockLabel не задан, то проверка проводится в режиме отказа.
        Если результат этой проверки не будет "истина",
        то транзакт помещается в список повторных попыток проверяемого объекта.
        Когда состояние любого из объектов меняется,
        заблокированный транзакт снова активизируется,
        повторяется проверка заданного блоком Gate условия.

Например, блок

gate.Gate(sgm, "Again", condition=SNF,objectName="STORAGE_NAME",nextBlockLabel="Occupied")

будет пропускать транзакты если память не заполнена, и направлять их в блок с меткой "Occupied",
если память заполнена.

Пример использования см.:
- examples/telephone/telephone.py

Атрибуты блока Gate (в дополнение к атрибутам block.Block):
bl = Test(...)
bl[FUNC_CONDITION] - функция вычисления условия, сигнатура: bool f(transact)
bl[TO_BLOCK_LABEL] - метка блока, к которому будет направляться транзакт, 
                     если условие не будет выполняться
bl[firstBlock_4365643] - кеш, внутреннее использование
bl[secBlock_4365643] - кеш, внутреннее использование
    
Может быть заменён на блок Test или Transfer.
    
    """
   
    def __init__(self, ownerSegment=None, label=None, condition=None, objectName=None, nextBlockLabel=None):
        # #modificatorFunc is function(parametrName)

        # pylint:disable=too-many-arguments

        super(Gate, self).__init__(GATE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [condition not in [U, NU, NI, I, SE, SNE, SF, SNF, LR, LS], objectName is None or objectName.strip() == ""])
        if nextBlockLabel is None:
            raise pyssobject.ErrorNotImplemented("Ограничение текущей версии (не допускается nextBlockLabel is None)")
        self[CONDITION] = condition
        self[NEXT_BLOCK_LABEL] = nextBlockLabel
        # may be facility, память, ключ
        self[OBJECT_NAME] = objectName
        self[TEMP_KEYS] = None
        self[firstBlock_4365643] = None
        self[secBlock_4365643] = None

    def _refreshCash(self):
        if self[TEMP_KEYS] is None:
            if self[CONDITION] in [NU, U, NI, I]:
                self[TEMP_KEYS] = self.getOwnerModel().findFacility(self[OBJECT_NAME])
            elif self[CONDITION] in [SE, SNE, SF, SNF]:
                self[TEMP_KEYS] = self.getOwnerModel().getStorages()[self[OBJECT_NAME]]
            else:
                raise Exception("Not implemented [%s]" % self[CONDITION])

    def _calcCondition(self):
        self._refreshCash()
        f = self[TEMP_KEYS]
        rv = False
        if self[CONDITION] == NU:
            if f.isFree():
                rv = True
        elif self[CONDITION] == U:
            if not f.isFree():
                rv = True
        elif self[CONDITION] == NI:
            if not f.isNotAccess():
                rv = True
        elif self[CONDITION] == I:
            if f.isNotAccess():
                rv = True
        # TODO
        elif self[CONDITION] == SE:
            rv = f.storageEmpty()
        elif self[CONDITION] == SNE:
            rv = f.storageNotEmpty()
        elif self[CONDITION] == SF:
            rv = f.storageFull()
        elif self[CONDITION] == SNF:
            rv = f.storageNotFull()
        else:
            raise Exception("Not known condition")
        return rv

    def canEnter(self, transact):
        rv = False
        if self[NEXT_BLOCK_LABEL] is not None:
            return True
        # TODO Gate.canEnter 
        return rv

    def handleCanNotEnter(self, transact):
        # # При работе в режиме отказа блок GATE не пропускает транзакты,
        
        # TODO Gate.handleCanNotEnter 

        f = self[TEMP_KEYS]
        if self[CONDITION] in [NU, U, NI, I, SE, SNE, SF, SNF]:
            f.moveToRetryAttempList(transact)
        else:
            raise Exception("Not known condition")

    def transactInner(self, currentTime, transact=None):
        
        if self[NEXT_BLOCK_LABEL] is not None:
            c = self._calcCondition()
            if not c:
                block = self.findBlockByLabel(self[NEXT_BLOCK_LABEL])
            else:
                block = self[BLOCK_NEXT]
                
        transact[BLOCK_NEXT] = block
                
        # TODO Gate.transactInner 
        return transact

if __name__ == '__main__':
    pass
