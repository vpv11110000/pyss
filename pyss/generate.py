# -*- coding: utf-8 -*-

"""
Модуль блока формирования транзактов модели
"""

# pylint: disable=line-too-long

import random
from pyss import pyssobject
from pyss.transact import Transact
from pyss import logger
from pyss.pyss_const import *
from pyss.block import Block

class Generate(Block):
    """Блок формирования транзактов модели

В один момент времени формируется один транзакт.
Для создания транзактов, входящих в модель, служит блок Generate (генерировать),

Транзакты модели не должны входить в блок GENERATE.

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py) 
    med_value=1 - среднее время формирования транзактов (вещественное число),
                  или функция float f()
                  Если задано вещественное число, 
                  то в атрибут MED_VALUE записыватся функция lambda: med_value
                  Значение параметров med_value, first_tx, 
                  если задан список или кортеж в modificatorFunc, будет игнорироваться.
    modificatorFunc=None - функция модификации времени следующего формирования транзакта 
                           (float f(owner,currenttime)).
                           По сути этот параметр определяет смещение от model.getCurTime()+значение(med_value)
                           Если задано число, 
                           то в атрибут MODIFICATOR записыватся функция lambda owner,currenttime: modificatorFunc
                           Если задан список или кортеж, то при каждом вызове функции модификации времени
                           будет браться следующее значение. 
                           Значение параметров med_value, first_tx, если задан список или кортеж, будет игнорироваться. 
    first_tx=0 - время формирования первого транзакта.
                 Если задано None и modificatorFunc не является списком или кортежем,
                 то значение вычисляется как случайное число,
                 сформированное по равномерному распределению на интервале
                 [0,"среднее время формирования транзактов (см. med_value)"
                 +"результат вызова функции модификации времени 
                 следующего формирования транзакта (см. modificatorFunc)"]
                 Значение параметров med_value, first_tx, 
                 если задан список или кортеж в modificatorFunc, будет игнорироваться.
    max_amount=None - максимальное количество транзактов формируемых блоком.
                      Если параметр max_amount равен 0 или None,
                      то блок генерирует неограниченное число транзактов до завершения моделирования,
                      или количеством, равным размеру списка modificatorFunc (если задан)
    priority=0 - приоритет.
                 Число уровней приоритетов неограничено,
                 самый низкий приоритет - нулевой.
                 Если параметр priority равен None,
                 то формируемые транзакты имeют нулевой приоритет.

Простейший вызов имеет следующий формат:
from pyss import generate
 ...
# model
m = pyss_model.PyssModel()
sgm=segment.Segment()
generate.Generate(sgm, med_value=1, modificatorFunc=None, first_tx=0, max_amount=None, priority=0)
terminate.Terminate(sgm, deltaTerminate=1)
m.start(10, maxTime=20)

Параметр med_value задает среднее значение интервала времени
между моментами поступления
в модель двух последовательных транзактов.
Если этот интервал (med_value) постоянен, то параметр modificatorFunc
может быть None или быть функцией, возвращающей значение 0 (см. modificatorfunc.py).
Если же интервал поступления транзактов в модель является случайной величиной,
то в параметре modificatorFunc указывается
модификатор-функция среднего значения (med_value), например: lambda owner, currentTime: random.uniform(0,5.0)

Например, блок

generate.Generate(sgm, med_value=100, modificatorFunc=lambda owner, currentTime: random.uniform(-40.0,40.0), first_tx=0, max_amount=None, priority=0)

создает транзакты через случайные интервалы времени, равномерно распределенные на отрезке [60;140].

Атрибуты блока Generate (в дополнение к атрибутам block.Block):
bl = Generate(...)
bl[MED_VALUE] - функция возвращающая среднее время генерации транзакта 
bl[MODIFICATOR] - функция модификации времени следующего формирования транзакта по формуле 
                  bl[MED_VALUE]()+bl[MODIFICATOR](bl, currentTime)
bl[FIRST_TX] - время формирования первого транзакта
bl[MAX_AMOUNT] - максимальное количество транзактов формируемых блоком
bl[PRIORITY] - функция, вычисляющая приоритет формируемых транзактов
bl[NEXT_TIME] - метка времени, для формирования следующего транзакта, 
                или None, если больше формирование транзактов не предполагается
bl[COUNT_TRANSACT] - количество сформированных транзактов
bl[ENABLED] - флаг, если True, то блок может формировать транзакты
                    если False, то блок не может формировать транзакты 
    
Может быть заменён на блок Test или Transfer.

    """

    def __init__(self, ownerSegment=None, label=None, med_value=0,
                 modificatorFunc=None,
                 first_tx=0,
                 max_amount=None,
                 priority=0):

        # pylint:disable=too-many-arguments

        super(Generate, self).__init__(GENERATE, label=label, ownerSegment=ownerSegment)

        if pyssobject.isfunction(modificatorFunc):
            self[MODIFICATOR] = modificatorFunc
        else:
            if type(modificatorFunc) is list or type(modificatorFunc) is tuple:
                _list = modificatorFunc
                def f():
                    for x in _list:
                        yield x
                g = f()
                self[MODIFICATOR] = lambda o, c: next(g, None)
                med_value, first_tx = None, None
                logger.warn("Generate: med_value, first_tx set to None ")
            elif modificatorFunc is not None:
                # число
                self[MODIFICATOR] = lambda o, c: modificatorFunc
            else:
                # число
                self[MODIFICATOR] = lambda o, c: 0

        if pyssobject.isfunction(med_value):
            self[MED_VALUE] = med_value
        else:
            map(pyssobject.raiseIsTrue, [med_value is not None and med_value < 0,
                                     med_value is not None and med_value > 0 and max_amount is not None and max_amount < 1,
                                     med_value is None and max_amount != 1 and not (type(modificatorFunc) is list or type(modificatorFunc) is tuple),
                                     (type(modificatorFunc) is list or type(modificatorFunc) is tuple) and len(modificatorFunc) == 0,
                                     (type(modificatorFunc) is list or type(modificatorFunc) is tuple) and med_value is not None])
            if med_value is not None:
                self[MED_VALUE] = lambda: med_value
            else:
                self[MED_VALUE] = None                
        
        if first_tx is None:
            if self[MED_VALUE] is not None:
                self[FIRST_TX] = random.uniform(0, self[MED_VALUE]() + self[MODIFICATOR](self, 0))
            else:
                if type(modificatorFunc) is list or type(modificatorFunc) is tuple:
                    self[FIRST_TX] = self[MODIFICATOR](self, 0)
                else:
                    self[FIRST_TX] = random.uniform(0, self[MODIFICATOR](self, 0))
        else:
            self[FIRST_TX] = first_tx
        self[MAX_AMOUNT] = max_amount
        self[PRIORITY] = lambda: priority
        self[NEXT_TIME] = self[FIRST_TX]
        self[COUNT_TRANSACT] = 0
        self[ENABLED] = True
        
    def modifiedValue(self, currentTime):
        t = self[MED_VALUE]
        m = self[MODIFICATOR]
        if t is not None:
            if pyssobject.isfunction(t):
                if m:
                    return t() + m(self, currentTime)
                else:
                    return t()
            if m:
                return t() + m(self, currentTime)
            else:
                return t()
        else:
            if m:
                return m(self, currentTime)
            else:
                return None

    def findNextTime(self):
        return self[NEXT_TIME]

    def mustGenerateTransact(self, currentTime):
        if self[NEXT_TIME] is None:
            return False
        m = self[MAX_AMOUNT]
        if (m is not None) and m > 0 and self[COUNT_TRANSACT] >= m:
            return False
        return currentTime >= self[NEXT_TIME]

    def generateTransact(self, currentTime):
        r = None
        if not self[ENABLED]:
            return None
        if self[NEXT_TIME] is None:
            self[ENABLED] = False
            return None
        if self[MAX_AMOUNT] is not None: 
            if self[NEXT_TIME] is not None and self[COUNT_TRANSACT] >= self[MAX_AMOUNT]:
                self[NEXT_TIME] = None
                self[ENABLED] = False
                return None
            
        if self.mustGenerateTransact(currentTime):
            if self[MED_VALUE] is not None:
                self[NEXT_TIME] = self[NEXT_TIME] + self.modifiedValue(currentTime)
            else:
                if self[MODIFICATOR] is not None:
                    self[NEXT_TIME] = self[MODIFICATOR](self, currentTime)
                else:
                    self[NEXT_TIME] = None
            r = Transact(self, currentTime, priority=self[PRIORITY]())
            r[NUM] = self.getOwnerModel().transactNumber.buildObjectNumber()
            r[TRACK].append((currentTime, self))
            r[HANDLED] = True
            r[BLOCK_NEXT] = None
            self[COUNT_TRANSACT] += 1
            self[ENABLED] = self.howMuchIsStillLeft() > 0
            # logger.info("Generate transact  (%d/%d)"%(self[COUNT_TRANSACT],self[MAX_AMOUNT]))
        return r

    def transactInner(self, currentTime, transact=None):

        # pylint:disable=unused-argument

        tr = self.generateTransact(currentTime)
        if tr:
            self[ENTRY_COUNT] += 1
            self[CURRENT_COUNT] += 1
            sgm = self.getOwnerSegment()
            m = self.getOwnerModel()
            m.getCel().put(tr)
            # pylint: disable=unsubscriptable-object
            if sgm[OPTIONS]:
                if sgm[OPTIONS].logTransactGenerate:
                    logger.info("Generate transact to CEL: [%s]" % str(tr))
        return tr

    def transactHandle(self, currentTime, transact):
        if transact and not transact[HANDLED]:
            raise Exception("Транзакт не должен входить в блок GENERATE")
        rv = False
        if transact is None:
            # режим генерации
            self.transactInner(currentTime, transact=None)
            return True
        else:
            # режим обработки
            rv = True
            transact[HANDLED] = True
            if self[BLOCK_NEXT]:
                if self[BLOCK_NEXT].canEnter(transact):
                    self.transactOut(transact)
                else:
                    self[BLOCK_NEXT].handleCanNotEnter(transact)
                    rv = False
            else:
                rv = False
        return rv
    
    def howMuchIsStillLeft(self):
        """Сколько ещё осталось сформировать транзактов
        
        Если self[MAX_AMOUNT] is not None:
        Возвращает self[MAX_AMOUNT] - self[COUNT_TRANSACT]
        иначе возвращает float('inf') (не ограничено)
        """
        if self[MAX_AMOUNT] is not None and self[MAX_AMOUNT] > 0:
            return self[MAX_AMOUNT] - self[COUNT_TRANSACT]
        else:
            return float('inf')

def buildForListTimes(ownerSegment, label=None, listOfTimes=None, priority=None):
    if listOfTimes is None:
        raise pyssobject.ErrorIsNone("listOfTimes don't is None")
    return Generate(ownerSegment, label=label, med_value=None,
                    modificatorFunc=listOfTimes,
                    first_tx=None,
                    max_amount=None,
                    priority=priority
                    )        

if __name__ == '__main__':
    pass
