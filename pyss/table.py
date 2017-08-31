# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль реализации таблицы
"""

# pylint: disable=line-too-long

from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss.pyss_const import *
from pyss.pyssownerobject import PyssOwnerObject

class Table(PyssOwnerObject):
    """Объект таблицы

Таблица предназначена для сбора данных от элементов модели.

Аргумент таблицы (аналог оси 'x') разбивается на countInt интервалов.
Ширина интервала задаётся параметром widthInt.
Левая граница интервала принадлежит интервалу.
Правая граница интервала не принадлежит интервалу.
Правая граница первого интервала задаётся параметром limitUpFirst.
Аргумент таблицы вычисляется вызовом функции, хранимой в атрибуте ARG_FUNC.
Значение аргумента таблицы вычисляется в блоке tabulate.Tabulate вызовом
функции, хранимой в атрибуте VAL_FUNC блока Tabulate.

Таблица добавляется в модель с помощью вызова метода addTable контейнера pyss_model.PyssModel.

Args:
    ownerModel - модель-владелец
    tableName - имя таблицы
    argFunc=None - функция определения аргумента таблицы. Сигнатура argFunc(owner,transact).
    limitUpFirst=None - правая граница первого интервала аргумента таблицы
    widthInt=None - ширина интервалов
    countInt=None - количество интервалов


Например, объект

table.Table(tableName="T_1", argFunc=argFunc_T_1, limitUpFirst=1.0, widthInt=1.0, countInt=50)

определяет таблицу T_1, аргумент таблицы определяется функцией argFunc_T_1, первый интервал ограничен сверху значением 1.0, ширина интервала 1.0, количество инетрвалов 50.

Пример использования см. demo/demo_table.py, demo/demo_enter_leave.py, demo/demo_queue.py, 
demo/demo_plot_table.py,.

См. также tabulate.py.

Атрибуты объекта Table (в дополнение к атрибутам pyssobject.PyssObject):
tbl = Table(...)
tbl[TABLENAME] - имя таблицы.
tbl[TITLE] - дубль: имя таблицы.
tbl[DISPLAYING] - true - отображать результат обработки данных таблицы
tbl[ARG_FUNC] - функция вычисления аргумента таблицы, хранит значение параметра argFunc
tbl[LIMITUPFIRST] - правая граница первого интервала аргумента таблицы
tbl[WIDTHINT] - ширина интервалов
tbl[COUNTINT] - количество интервалов
tbl[TOTAL] - сумма всех значений вычисленных функции, хранимой в атрибуте VAL_FUNC блока Tabulate. Очень полезно, если значения аргемента таблица всехга равны, например, единице.
tbl[INTERVALS] - множество интервалов
tbl[MIN_BOUND] - левая граница таблицы
tbl[MAX_BOUND] - правая граница таблицы
tbl[LIST] - список правых границ всех интервалов
tbl[ACTION_FUNC] - функция занесения данных в таблицу, в зависимости от параметров может различаться для разных таблиц
tbl[ACTION_VIEW] - функция формата вывода, в зависимости от параметров может различаться для разных таблиц
tbl[LIST] - список правых границ всех интервалов
tbl[INTERVALS][POSITIVE_INFINITY] - величина значения справа от правой границы таблицы
tbl[INTERVALS][NEGATIVE_INFINITY] - величина значения слева от левой границы таблицы

    """
    def __init__(self, ownerModel=None, tableName=None, argFunc=None, limitUpFirst=None, widthInt=None, countInt=None):

        # # таблица
        # argFunc(owner,transact) - задает функцию для получения аргумента таблицы - элемент данных, чье частотное
        # распределение будет табулироваться.
        # Операнд функция, получающая значение из транзакта, из выражения,
        # СЧА или др. компонента системы.
        #
        # limitUpFirst is None - вся область определения, счётчик в self[TOTAL]
        #
        # limitUpFirst is not None and countInt == 0 - область значений разделена
        #   на две подобласти: до limitUpFirst (счётчик в self[INTERVALS][NEGATIVE_INFINITY])
        #   и после limitUpFirst, включая границу (счётчик в self[INTERVALS][POSITIVE_INFINITY])
        #
        # limitUpFirst is not None and countInt > 0 - область значений разделена:
        #    [NEGATIVE_INFINITY,self[MIN_BOUND]) - счётчик в self[INTERVALS][NEGATIVE_INFINITY]
        #    [self[MIN_BOUND],limitUpFirst) - счётчик в self[LIST][0]
        #    ...
        #    [MIN_BOUND+widthInt*(countInt-1),MIN_BOUND+widthInt*countInt) - счётчик в self[LIST][countInt-1]
        #    [MIN_BOUND+widthInt*countInt,POSITIVE_INFINITY) - счётчик в self[INTERVALS][POSITIVE_INFINITY]
        #

        # pylint: disable=too-many-arguments

        super(Table, self).__init__(TABLE, label=tableName, owner=ownerModel)
        map(pyssobject.raiseIsTrue, [not tableName, argFunc is None])
        map(pyssobject.raiseIsTrue, [limitUpFirst is None and (widthInt is not None or countInt is not None)])
        map(pyssobject.raiseIsTrue, [limitUpFirst is not None and (countInt is None or (countInt == 0 and widthInt is not None) or (countInt > 0 and (widthInt is None or widthInt == 0)))])
        #
        self[TABLENAME] = tableName
        self[TITLE] = tableName
        self[ARG_FUNC] = argFunc
        self[LIMITUPFIRST] = limitUpFirst
        self[WIDTHINT] = widthInt
        self[COUNTINT] = countInt
        self[TOTAL] = 0
        self[INTERVALS] = {}
        self[MIN_BOUND] = None
        self[MAX_BOUND] = None
        self[LIST] = []
        if limitUpFirst is None:
            self[ACTION_FUNC] = self.writeToIntervalsFunctionDomainFull
            self[ACTION_VIEW] = self.table2strFunctionDomainFull
        elif limitUpFirst is not None and countInt == 0:
            self[ACTION_FUNC] = self.writeToIntervalsFunctionDomainHalf
            self[ACTION_VIEW] = self.table2strFunctionDomainHalf
        else:
            self[MIN_BOUND] = limitUpFirst - widthInt
            self[MAX_BOUND] = self[MIN_BOUND] + countInt * widthInt
            self[ACTION_FUNC] = self.writeToIntervals
            self[ACTION_VIEW] = self.table2strInterv
            while countInt > 0:
                # интервалы
                self[LIST].append(limitUpFirst)
                self[INTERVALS][limitUpFirst] = 0
                limitUpFirst += widthInt
                countInt -= 1

        self[INTERVALS][POSITIVE_INFINITY] = 0
        self[INTERVALS][NEGATIVE_INFINITY] = 0
        self[DISPLAYING] = True
        ownerModel.addTable(self)

    def setDisplaying(self, displaying=False):
        self[DISPLAYING] = displaying
        return self

    def writeToIntervalsFunctionDomainFull(self, x, y):
        pass

    def writeToIntervalsFunctionDomainHalf(self, x, y):
        if x < self[LIMITUPFIRST]:
            self[INTERVALS][NEGATIVE_INFINITY] += y
        else:
            self[INTERVALS][POSITIVE_INFINITY] += y

    def writeToIntervals(self, x, y):
        # #
        # x - значение из области определения, ассоциируется с интервалом значений
        #     нижняя граница принадлежит, верхняя не принадлежит
        # y - значение из области значений, добавляется к счётчику
        #
        if x < self[MIN_BOUND]:
            self[INTERVALS][NEGATIVE_INFINITY] += y
        elif x >= self[MAX_BOUND]:
            self[INTERVALS][POSITIVE_INFINITY] += y
        else:
            l = self[LIST]
            for z in l:
                if x < z:
                    self[INTERVALS][z] += y
                    break

    def handleTransact(self, transact, coef=1):
        argFunc = self[ARG_FUNC]
        v = argFunc(self, transact)
        self[TOTAL] += coef
        self[ACTION_FUNC](v, coef)

    def table2strFunctionDomainFull(self):
        rv = "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def formatL(self, x, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % ("<%0.3f" % x, str(y))

    def formatG(self, x, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % (">=%0.3f" % x, str(y))

    def formatF(self, x0, x1, y):
        # pylint: disable=no-self-use
        return "! %8s ! %8s !" % ("%0.3f-%0.3f" % (x0, x1), str(y))

    def table2strFunctionDomainHalf(self):
        rv = "!   Value  !  Count   !" + "\n"
        rv += "=======================" + "\n"
        key = self[LIMITUPFIRST]
        v = self[INTERVALS][NEGATIVE_INFINITY]
        rv += self.formatL(key, v) + "\n"
        v = self[INTERVALS][POSITIVE_INFINITY]
        rv += self.formatG(key, v) + "\n"
        rv += "=======================" + "\n"
        rv += "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def table2strInterv(self):
        rv = "!   Value  !  Count   !" + "\n"
        rv += "=======================" + "\n"
        key = None
        oldKey = self[MIN_BOUND]
        l = self[LIST]
        v = self[INTERVALS][NEGATIVE_INFINITY]
        rv += self.formatL(self[MIN_BOUND], v) + "\n"
        for key in l:
            v = self[INTERVALS][key]
            rv += self.formatF(oldKey, key, v) + "\n"
            oldKey = key
        # rv+="! %8s ! %8s !"%(s,str(self[INTERVALS][POSITIVE_INFINITY]))+"\n"
        v = self[INTERVALS][POSITIVE_INFINITY]
        rv += self.formatG(self[MAX_BOUND], v) + "\n"
        rv += "=======================" + "\n"
        rv += "Total: %d" % self[TOTAL] + "\n"
        rv += "=======================" + "\n"
        return rv

    def table2str(self):
        rv = "=======================" + "\n"
        rv += "Table: %s" % self[TABLENAME] + "\n"
        rv += "=======================" + "\n"
        rv += self[ACTION_VIEW]()
        return rv

if __name__ == '__main__':
    def main():
        print "?"

    main()
