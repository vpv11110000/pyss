# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации оспобождения памяти или многоканального устройства
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss.pyss_const import *
from pyss.statisticalseries import StatisticalSeries
from pyss.pyssstateobject import PyssStateObject

#
T123 = "$$$123"
T124 = "$$$124"

class Storage(PyssStateObject):
    """Объект Storage для представления памяти или многоканального устройства.

Память storage добавляется в модель при выполнии метода pyss_model.PyssModel(...).addStorage(storage).

Можно назначать обработчики изменения состояния (см. PyssStateObject).
Обработчик вызывается при изменении значения атрибута BUSY_SIZE в методах Enter и Leave.
Значение старого состояния равно старому значению атрибута BUSY_SIZE.

Args:
    ownerModel - объект модели-владельца
    storageName=None - строка с наименованием памяти
    storageSize=32767 - размер памяти или число каналов многоканального устройства
    initBusySize=0 - начальное значение занятого объёма. Значение сразу заносится в атрибут 

Владельцем Storage является модель.

Например, строка

storage.Storage(m, storageName="mcd",storageSize=2)

создаёт память из 2-х ячеек.

Пример использования см. tests/test_enter_leave.py.

См. также enter.py, storage.py

Атрибуты объекта Storage (в дополнение к атрибутам block.Block):
bl = Leave(...)
bl[STORAGE_NAME] - имя памяти или функция без параметров, возвращающая имя памяти.
bl[FUNC_BUSY_SIZE] - число занимаемых единиц памяти или функция, возвращающая указанное число
bl[BUSY_SIZE]=0 - число зянятых единиц памяти
bl[R] = self[S] #$j – свободная емкость памяти j;
bl[SR] = 0 #$j – коэффициент использования памяти j;
bl[SM] = 0 #$j – максимальное заполнение памяти j;
bl[SA] = 0 #$j – среднее заполнение памяти j;
bl[SC] = 0 #$j – число входов в память j;
bl[ST] = 0 #$j – среднее время пребывания транзакта в памяти j.
bl[MIN] - минимальное значение занятого пространства

Память имеет также стандартные логические атрибуты,
которые используются для проверки состояния памяти:
bl[SE] = True #$j – память j пуста;
bl[NE] = not self[SE] #$j – память j не пуста;
bl[SF] = False #$j – память j заполнена;
bl[SNF] = not self[SF] #$j – память j не заполнена.
bl[DATA]=StatisticalSeries()
bl[RETRY]=0
bl[DELAY]=0
bl[ENTRIES]=0
bl[AVL]=True #  The availability state of the Storage entity. 1 means available, 0 means unavailable
bl[TRANSACT_LIST]=[] - перечень длительностей нахождения транзактов в памяти
bl[LIFE_TIME_LIST] - список меток времени и состояний активности МКУ
    """

    def __init__(self, ownerModel=None, storageName=None, storageSize=32767, initBusySize=0):
        # #Поле метки строки STORAGE содержит номер или метку памяти,
        # поле операции - слово STORAGE, а поле A указывает емкость памяти.
        # Емкость памяти должна выражаться целым числом.
        # вызывать recalc для обновления значений self[SR], self[SA], self[ST]

        # С объектом STORAGE связаны следующие СЧА:
        # S$j – ёмкость памяти j;
        # R$j – свободная емкость памяти j;
        # SR$j – коэффициент использования памяти j;
        # SM$j – максимальное заполнение памяти j;
        # SA$j – среднее заполнение памяти j;
        # SC$j – число входов в память j;
        # ST$j – среднее время пребывания транзакта в памяти j.

        # Память имеет также стандартные логические атрибуты,
        # которые используются для проверки состояния памяти:
        # SE$j – память j пуста;  NE$j – память j не пуста;
        # SF$j – память j заполнена; SNF$j – память j не заполнена.

        # pylint:disable=too-many-arguments

        super(Storage, self).__init__(STORAGE, label=None, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [storageName is None or storageName.strip() == "",
                                     storageSize < 1,
                                     initBusySize is None,
                                     initBusySize >= storageSize])
        self[STORAGE_NAME] = storageName
        self[TITLE] = storageName
        self[S] = storageSize
        self[INIT_BUSY_SIZE] = initBusySize
        self[STORAGE_TRANSACT_KEY] = STORAGE_TRANSACT_KEY + storageName
        self.reset()
        ownerModel.addStorage(self)
        

    def storageEmpty(self):
        return self[BUSY_SIZE] == 0

    def storageNotEmpty(self):
        return self[BUSY_SIZE] > 0

    def storageFull(self):
        return self[BUSY_SIZE] == self[S]

    def storageNotFull(self):
        return self[BUSY_SIZE] < self[S]
    
    def getBusySize(self):
        return self[BUSY_SIZE]

    def getStorageSize(self):
        return self[S]
    
    def reset(self):
        self[MIN] = self[INIT_BUSY_SIZE]        
        self[BUSY_SIZE] = self[INIT_BUSY_SIZE]
        self[R] = self[S]  # $j – свободная емкость памяти j;
        self[SR] = 0  # $j – коэффициент использования памяти j;
        self[SM] = 0  # $j – максимальное заполнение памяти j;
        self[SA] = 0  # $j – среднее заполнение памяти j;
        self[SC] = 0  # $j – число входов в память j;
        self[ST] = 0  # $j – среднее время пребывания транзакта в памяти j.

        # Память имеет также стандартные логические атрибуты,
        # которые используются для проверки состояния памяти:
        self[SE] = True  # $j – память j пуста;
        self[NE] = not self[SE]  # $j – память j не пуста;
        self[SF] = False  # $j – память j заполнена;
        self[SNF] = not self[SF]  # $j – память j не заполнена.
        self[DATA] = StatisticalSeries()
        self[RETRY] = 0
        self[DELAY] = 0
        self[ENTRIES] = 0
        self[AVL] = True  #  The availability state of the Storage entity. 1 means available, 0 means unavailable
        self[TRANSACT_LIST] = []
        # в STATE записываем сколько занято
        self[LIFE_TIME_LIST] = [{START:self[OWNER].getCurTime(), STATE:self[BUSY_SIZE]}]


    def recalc(self, timeValue=None):
        # # вызывать recalc для обновления значений self[SR], self[SA], self[ST]
        if timeValue is None:
            timeValue = self[OWNER].getCurTime()
        self[SR] = self.utilization(timeValue=timeValue)
        self[SA] = self.meanMemoryFill(timeValue=timeValue)
        self[ST] = self.meanTimeForTransact(timeValue=timeValue)

    def meanTimeForTransact(self, timeValue=0):
        # pylint: disable=unused-argument
        t = self[TRANSACT_LIST]
        rv = StatisticalSeries().extend(t).mean()
        return rv

    def _volume(self, timeValue=0):
        if not self[DATA][DATA]:
            return 0.0
        v = 0.0
        last = 0.0
        d = self[DATA][DATA]
        values = sorted(d)
        i = 0
        lastV = d[values[0]]
        while i < len(values) and last < timeValue:
            if values[i] > timeValue:
                t = timeValue
            else:
                t = values[i]
            p = (t - last) * lastV
            v += p
            last = t
            lastV = d[t]
            i += 1
        return v

    def meanMemoryFill(self, timeValue=0):
        if not timeValue:
            return None
        return self._volume(timeValue) / timeValue

    def utilization(self, timeValue=0):
        # # Коэффициент использования памяти
        if not timeValue:
            return None
        m = float(self[S]) * float(timeValue)
        return self._volume(timeValue) / m

    def _sla(self):
        self[SE] = self[BUSY_SIZE] == 0
        self[NE] = not self[SE]  # $j – память j не пуста;
        self[SF] = self[BUSY_SIZE] == self[S]  # $j – память j заполнена;
        self[SNF] = not self[SF]  # $j – память j не заполнена.

    def enter(self, transact=None, busySize=1, currentTime=None):

        # Когда транзакт входит в блок ENTER (см. блок-диаграмму),
        # планировщик выполняет следующие действия:

        # увеличивает на 1 счетчик входов МКУ;
        # увеличивает на значение операнда B (по умолчанию на 1 ) текущее содержимое МКУ;
        # уменьшает на значение операнда B (по умолчанию на 1 ) доступную емкость МКУ.
        # транзакт помечается currentTime по ключу self[STORAGE_TRANSACT_KEY], см.
        # __init__
        if not busySize:
            raise Exception("Illegal busySize")
        
        c = self[BUSY_SIZE] + busySize
        if c > self[S]:
            raise Exception("Illegal operation")
        if currentTime is None:
            currentTime = self[OWNER].getCurTime()
        if transact:
            transact[self[STORAGE_TRANSACT_KEY]] = currentTime
        self[ENTRIES] += 1
        oldState = self[BUSY_SIZE]
        self[BUSY_SIZE] = c
        # в STATE записываем сколько занято
        self[LIFE_TIME_LIST].append({START:self[OWNER].getCurTime(), STATE:self[BUSY_SIZE]})        
        self[R] = self[S] - self[BUSY_SIZE]
        self[SM] = c if self[SM] < c else self[SM]
        self[DATA].append(currentTime, c)
        self[SC] += 1
        self._sla()
        self.fireHandlerOnStateChange(oldState)


    def leave(self, transact=None, busySize=1, currentTime=None):
        # # если транзакт помечен временем входа (self.enter), то будет вестись
        # статистика среднего времени пребывания танзакта в Storage
        # transact[self[STORAGE_TRANSACT_KEY]] по завершении будет содержать
        # время пребывания в Storage
        # если входит и выходит несколько раз, то
        # transact[self[STORAGE_TRANSACT_KEY]] содержит только последнее
        # время пребывания в Storage

        c = self[BUSY_SIZE] - busySize
        if c < 0:
            raise Exception("Illegal operation")
        if not currentTime:
            currentTime = self[OWNER].getCurTime()
        if transact:
            if self[STORAGE_TRANSACT_KEY] in transact:
                delta = currentTime - transact[self[STORAGE_TRANSACT_KEY]]
                self[TRANSACT_LIST].append(delta)
                transact[self[STORAGE_TRANSACT_KEY]] = delta
        oldState = self[BUSY_SIZE]
        self[BUSY_SIZE] = c
        # в STATE записываем сколько занято
        self[LIFE_TIME_LIST].append({START:self[OWNER].getCurTime(), STATE:self[BUSY_SIZE]})         
        self[MIN] = min(c, self[MIN])
        self[R] = self[S] - self[BUSY_SIZE]
        self[DATA].append(self[OWNER].getCurTime(), c)
        self[SC] -= 1
        self._sla()
        self.fireHandlerOnStateChange(oldState)

if __name__ == '__main__':
    def main():
        print "?"

    main()
