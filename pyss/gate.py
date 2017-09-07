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
        GATE_FACILITY_NOT_USED или NU - устройство свободно (т.е. не используется),
        GATE_FACILITY_USED или U - устройство не свободно (т.е. используется),
        GATE_FACILITY_NOT_INTERRUPTED или NI - устройство не захвачено,
        GATE_FACILITY_INTERRUPTED или I - устройство захвачено,
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
bl[CONDITION] - функция вычисления условия, сигнатура: bool f(transact)
bl[NEXT_BLOCK_LABEL] - метка блока, к которому будет направляться транзакт, 
                     если условие не будет выполняться
bl[OBJECT_NAME] - наименование объекта, м.б. facility, память, ключ.
self[TEMP_KEYS] - внутреннее использование (контролируемый объект)
self[KEY_FOR_DELAYED_LIST] - ключ данных в списке задержанных транзактов

Может быть заменён на блок Test или Transfer.
    
    """
   
    def __init__(self, ownerSegment=None, label=None, condition=None, objectName=None, nextBlockLabel=None):
        # #modificatorFunc is function(parametrName)

        # pylint:disable=too-many-arguments

        super(Gate, self).__init__(GATE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [condition not in [U, NU, NI, I, SE, SNE, SF, SNF, LR, LS], objectName is None or objectName.strip() == ""])
        self[CONDITION] = condition
        self[NEXT_BLOCK_LABEL] = nextBlockLabel
        # may be facility, память, ключ
        self[OBJECT_NAME] = objectName
        self[TEMP_KEYS] = None
        self[KEY_FOR_DELAYED_LIST] = None

    def _refreshCash(self):
        if self[TEMP_KEYS] is None:
            if self[CONDITION] in [NU, U, NI, I]:
                self[TEMP_KEYS] = self.getOwnerModel().findFacility(self[OBJECT_NAME])
            elif self[CONDITION] in [SE, SNE, SF, SNF]:
                self[TEMP_KEYS] = self.getOwnerModel().getStorages()[self[OBJECT_NAME]]
            elif self[CONDITION] in [LS, LR]:
                self[TEMP_KEYS] = self.getOwnerModel().getLogicObject()[self[OBJECT_NAME]]
            else:
                raise Exception("Not implemented [%s]" % self[CONDITION])
            # TODO ДЕЛАТЬ обработчик изменения состояния

    def _calcCondition(self):
        """Проверка выполнения условия на контролируемом объекте"""
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
        if self[NEXT_BLOCK_LABEL] is not None:
            return True
        #
        b = self._calcCondition()
        transact[RESULT_TEST_BLOCK] = b
        return b
    
    def _buildKeyForDelayedList(self):
        if self[KEY_FOR_DELAYED_LIST] is None:
            self[KEY_FOR_DELAYED_LIST] = "$$" + self.getOwner()[ENTITY_TYPE] + "_" + str(self.getOwner()[NUM]) + "_" + self[ENTITY_TYPE] + "_" + str(self[NUM]) 
        return self[KEY_FOR_DELAYED_LIST]

    def handleCanNotEnter(self, transact):
        # # При работе в режиме отказа блок GATE не пропускает транзакты,
        
        # TODO Gate.handleCanNotEnter 

        # если задан атрибут self[NEXT_BLOCK_LABEL], 
        #    то транзакт переходит в указанный в параметре блок (см. transactInner);
        # если атрибут self[NEXT_BLOCK_LABEL] не задан, то транзакт задерживается в предыдущем блоке.
        if self[NEXT_BLOCK_LABEL] is None:
            k = self._buildKeyForDelayedList()
            m = self.getOwnerModel()
            if k not in m.getDelayedList():
                def onStateChange(obj, oldState):
                    b = self._calcCondition()
                    if b:
                        while True:
                            t = m.extractFromDelayedListFirst(k)
                            if t is None:
                                break
                            m.getCel().put(t)
                self[TEMP_KEYS].addHandlerOnStateChange(handlerName=k, handler=onStateChange)    
            m.appendToDelayedList(k, transact)
        transact[RESULT_TEST_BLOCK] = None


    def transactInner(self, currentTime, transact=None):
        c = self._calcCondition()
        if self[NEXT_BLOCK_LABEL] is not None:
            if not c:
                block = self.findBlockByLabel(self[NEXT_BLOCK_LABEL])
            else:
                block = self[BLOCK_NEXT]
        else:
            if c is True:
                block = self[BLOCK_NEXT]
            else:
                raise pyssobject.ErrorBadAlgorithm("Gate().transactInner")
        transact[BLOCK_NEXT] = block
        return transact

if __name__ == '__main__':
    pass
