# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с экспоненциальной функцией pyss
"""

# pylint: disable=line-too-long

import random
import math
from collections import OrderedDict
from pyss import pyssobject
from pyss.pyss_const import *

class Exponential(dict):
    """Экспоненциальная функция распределения случайного события

Args:
    timeForEvent=None - среднее количество единиц времени на событие 
    scale=1 - масштабный коэффициент
    
Декларация функции:
ex = Exponential(timeForEvent=2, scale=1.0)
print ex.get()

Пример, см. tests/test_func_exponential.py    
    
    """
    def __init__(self, timeForEvent=None, scale=1.0):
        super(Exponential, self).__init__()
        map(pyssobject.raiseIsTrue,[not timeForEvent])
        self[LAMBDA_VAL] = 1.0/timeForEvent
        self[SCALE_VAL] = float(scale)
        

    def get(self):
        if self[SCALE_VAL]==1.0:
            return random.expovariate(self[LAMBDA_VAL])
            # интенсивность 1 событие за 24 единицы времени
            # return -math.log(1-random.random())/self[LAMBDA_VAL]
        else:
            return self[SCALE_VAL]*random.expovariate(self[LAMBDA_VAL])
        
if __name__ == '__main__':
    def main():
        print "?"

    main()
