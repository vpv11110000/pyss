# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока создания копий транзактов
"""

# pylint: disable=line-too-long

import copy
from pyss import pyssobject
from pyss.transact import Transact
import logger
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

class Split(Block):
    """Блок создания копий транзактов.

При входе транзакта в блок производится создание его копий. 

Количество копий определяется параметром funcCountCopies конструктора блока
или атрибутом FUNC_COUNT_COPIES.

Каждая новая копия становится членом семейства транзактов,
порожденного одним исходным транзактом, который был создан блоком GENERATE.

Имя семейства (ASSEMBLY_SET) устанавливается равным атрибуту NUM транзакта-родителя.
Атрибут ASSEMBLY_SET транзакта-родителя устанавливается равным значению своего атрибута NUM.

При указании paramName в атрибуте PARAMETR_NAME форируется отдельная нумерация (начало с 1).

Копии транзакта содержат в атрибуте PARENT ссылку на породивший их транзакт.
Копии транзакта содержат в атрибуте NUM новые номера от общего генератора номеров транзактов.

Копии транзакта содержат в атрибуте TRACK свой собственный маршрут. 
Начало маршрута определяется атрибутом NEXT_BLOCK_LABEL блока split.

Копии транзакта содержат в атрибуте TIME_CREATED время создания копии. 

Объекдинение транзактов одного семества происходит в блоке assemble.Assemble.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)    
    funcCountCopies=None - функция или целое число, определяющее количество копий текущего транзакта
                           Сигнатура int f(transact), возвращает количество копий текущего транзакта.
                           
    funcNextBlockLabel=None - метка следующего блока или функция вычисления метки блока, к которому 
                              переходят копии исходного транзакта.
                              Исходный транзакт перемещается к следующему блоку.
                              Если None, то переход 
                              производится к следующему блоку. 
                              Сигнатура: str f(transact), возвращает строку, содержащую метку блока.

    paramName=None - наименование параметра, используемого для присвоения 
                     копиям последовательных номеров.
                     В атрибут NUM записывается 
                     очередной номер PyssModel().transactnumber.buildObjectNumber().
                     Если paramName is not None, то в атрибут PARAMETR_NAME
                     копии транзакта записывается значение 
                     transact[NUM_GENERATOR].buildObjectNumber().
                     Где transact - исходный транзакт.

Например, блок

split.Split(sgm, funcCountCopies=2,funcNextBlockLabel=None,paramName=None)
split.Split(sgm, funcCountCopies=lambda: 2,funcNextBlockLabel=None,paramName=None)

создаёт две копии транзакта.

Пример использования см. tests/test_assemble.py.

Атрибуты блока Split (в дополнение к атрибутам block.Block):
bl = Split(...)
bl[FUNC_COUNT_COPIES] - функция, определяющее количество копий текущего транзакта
                        Сигнатура: int f(transact), возвращает количество копий текущего транзакта.
bl[NEXT_BLOCK_LABEL] - функция получения метки блока для перемещения копий исходного транзакта
                       Сигнатура: str f(transact), возвращает строку, содержащую метку блока.
bl[PARAMETR_NAME] - наименование параметра, используемого для присвоения копиям последовательных номеров

См. также assemble.py

    """
    def __init__(self, ownerSegment=None, label=None, funcCountCopies=None, funcNextBlockLabel=None, paramName=None):
        # # funcCountCopies is funcCountCopies(transact)
        # funcNextBlockLabel is funcNextBlockLabel(transact)

        # pylint:disable=too-many-arguments

        super(Split, self).__init__(SPLIT, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [funcCountCopies is None])
        self[FUNC_COUNT_COPIES] = funcCountCopies

        if pyssobject.isfunction(funcNextBlockLabel):
            self[NEXT_BLOCK_LABEL] = funcNextBlockLabel
        else:
            self[NEXT_BLOCK_LABEL] = lambda t: funcNextBlockLabel
        # may be facility, память, ключ
        self[PARAMETR_NAME] = paramName

    def _refreshCash(self):
        pass

    def canEnter(self, transact):
        return True

    def handleCanNotEnter(self, transact):
        # #
        pass

    def transactInner(self, currentTime, transact=None):
        # # calc modificatorFunc on current transact[self[PARAMETR_NAME]]
        # and set new value to transact[self[PARAMETR_NAME]]
        n = self[NEXT_BLOCK_LABEL](transact)
        block = None
        if n is not None:
            block = self.findBlockByLabel(n)
        if block is None:
            block = self[BLOCK_NEXT]
        m = self.getOwnerModel()
        cel = m.getCel()
        if pyssobject.isfunction(self[FUNC_COUNT_COPIES]):
            c = self[FUNC_COUNT_COPIES](transact)
        else:
            c = self[FUNC_COUNT_COPIES]
        while c > 0:
            t = copy.deepcopy(transact)
            t[PARENT] = transact
            t[CURRENT_BLOCK] = block
            t[HANDLED] = False
            t[BLOCK_NEXT] = None
            t[ASSEMBLY_SET] = transact[NUM]
            transact[ASSEMBLY_SET] = transact[NUM]            
            t[TIME_CREATED] = currentTime
            t[TRACK] = []
            if self[PARAMETR_NAME]:
                if not transact[NUM_GENERATOR]:
                    transact[NUM_GENERATOR] = pyssobject.ObjectNumber()
                t[self[PARAMETR_NAME]] = transact[NUM_GENERATOR].buildObjectNumber()
            t[NUM] = self.getOwnerModel().transactNumber.buildObjectNumber()
            cel.put(t)
            if transact[NUM] not in m[TRANSACT_FAMILIES]:
                m[TRANSACT_FAMILIES][transact[NUM]] = []
            m[TRANSACT_FAMILIES][transact[NUM]].append(t)
            c -= 1

        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
