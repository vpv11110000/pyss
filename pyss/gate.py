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
    
При работе в режиме отказа блок GATE не пропускает транзакты,
если соответствующий объект не находится в требуемом состоянии.

Если же поставленное в блоке GATE условие удовлетворяется,
то активный транзакт входит в него и затем переходит к
следующему по порядку блоку.

Args:
    condition - условие
        NU - устройство свободно (т.е. не используется),
        U - устройство не свободно (т.е. используется),
        NI - устройство не захвачено,
        I - устройство захвачено,
        SE - память пуста (все единицы памяти свободны),
        SNE - память не пуста,
        SF - память заполнена (все единицы заняты),
        SNF - память не заполнена,
        LR - ключ выключен,
        LS - ключ включен.    
    
    objectName - наименование объекта, м.б. facility, память, ключ.
        
    nextBlockLabel - метка блока, кода будет направлен транзакт если условие не выполняется
        Если параметр nextBlockLabel не задан, то проверка проводится в режиме отказа.
        Если результат этой проверки не будет "истина",
        то транзакт помещается в список повторных попыток проверяемого объекта.
        Когда состояние любого из объектов меняется,
        заблокированный транзакт снова активизируется,
        повторяется проверка заданного блоком Gate условия.
    
    label - см. block.py.

Например, блок

gate.Gate(condition=SNF,objectName="STORAGE_NAME",nextBlockLabel="Occupied",label="Again")

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

    def canEnter(self, transact):
        if self[OBJECT_NAME] is not None:
            return True
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

    def handleCanNotEnter(self, transact):
        # # При работе в режиме отказа блок GATE не пропускает транзакты,
        f = self[TEMP_KEYS]
        if self[CONDITION] in [NU, U, NI, I, SE, SNE, SF, SNF]:
            f.moveToRetryAttempList(transact)
        else:
            raise Exception("Not known condition")

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]
        if not self[firstBlock_4365643]:
            block = self.findBlockByLabel(self[NEXT_BLOCK_LABEL])
            if block is None:
                raise Exception("Block not found, label is [%s]" % self[NEXT_BLOCK_LABEL])
            self[firstBlock_4365643] = block
            self[secBlock_4365643] = self[BLOCK_NEXT]

        # pylint:disable=unused-argument
        self._refreshCash()
        block = self[secBlock_4365643]
        if self[OBJECT_NAME]:
            if self[CONDITION] == NU:
                if not self[TEMP_KEYS].isFree():
                    # если условие ложно
                    block = self[firstBlock_4365643]
            elif self[CONDITION] == U:
                if self[TEMP_KEYS].isFree():
                    # если условие ложно
                    block = self[firstBlock_4365643]
            elif self[CONDITION] == SNF:
                # если не полный, то к secBlock_4365643
                # иначе к firstBlock_4365643
                if self[TEMP_KEYS].storageFull():
                    # если условие ложно
                    block = self[firstBlock_4365643]
            elif self[CONDITION] == SF:
                # если полный, то к secBlock_4365643
                # иначе, если не полный, к firstBlock_4365643
                if self[TEMP_KEYS].storageNotFull():
                    # если условие ложно
                    block = self[firstBlock_4365643]
            else:
                raise Exception("Not known condition")
        else:
            pass
        self[BLOCK_NEXT] = block
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
