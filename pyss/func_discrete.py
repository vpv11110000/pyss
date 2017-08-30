# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с дискретной функцией pyss
"""

# pylint: disable=line-too-long

import random
from collections import OrderedDict
from pyss import pyssobject
from pyss.pyss_const import *

class FuncDiscrete(dict):
    """Дискретная функция распределения случайного события
    
Синтаксис:
discrete({<правая граница суммарной частоты случайного события1>:<значение функции1>,
          <правая граница суммарной частоты случайного события2>:<значение функции2>,
          ...})
          
Левая граница суммарной частоты случайного события не входит в интервал между 
левой границей суммарной частоты случайного события и правой границей суммарной 
частоты случайного события.
Правая граница интервала входит в интервал между 
левой границей суммарной частоты случайного события и правой границей суммарной 
частоты случайного события.

Пусть событие А принимает упорядоченные по возрастанию вещественные значения.

Тогда, относительная частота случайного события А:
Sotn = количество случайных событий А / общее количество испытаний

Суммарная частота случайного события является суммой относительных частот 
при значениях событий менее или равно значению события А.  

Пример распределения суммарных частот:

Интервал поступления транзактов  Относительная частота    Суммарная частота
2                                  0,10                        0,10
3                                  0,20                        0,30
4                                  0,40                        0,70
5                                  0,10                        0,80
6                                  0,20                        1,00

Декларация функции:
fd = FuncDiscrete(randomGenerator=random.random, dictValues={.1:2,.3:3,.7:4,.8:5,1.0:6})
print fd.get()

Пример, см. tests/test_func_discrete.py

    """
    def __init__(self, randomGenerator=random.random, dictValues=None):
        super(FuncDiscrete, self).__init__()
        map(pyssobject.raiseIsTrue, [not dictValues])
        # OrderedDict([(.1, 2), (.3, 3), (.7, 4), (.8, 5), (1,6)])
        self[DICT_VALUES] = OrderedDict(sorted(dictValues.items(), key=lambda t: t[0]))
        self[RANDOM_GENERATOR] = randomGenerator    

    def get(self):
        r = self[RANDOM_GENERATOR]()
        for key, value in self[DICT_VALUES].iteritems():
            if r <= key:
                return value
        # fail
        return None
        
if __name__ == '__main__':
    def main():
        print "?"

    main()
