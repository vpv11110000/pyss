# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с "нормальной" функцией pyss
"""

# pylint: disable=line-too-long

import random
from collections import OrderedDict
from pyss import pyssobject
from pyss.pyss_const import *

class Normal(dict):
    """Функция Нормального распределения случайного события

Args:
    meanVal=None - математическое ожидание 
    stdDev=None - стандартное отклонение
    
Декларация функции:
ex = Exponential(timeForEvent=2, scale=1.0)
print ex.get()

Пример, см. tests/test_func_exponential.py    
    
    """
    def __init__(self, meanVal=0.0, stdDev=1.0):
        super(Normal, self).__init__()
        self[MEAN_VAL] = float(meanVal)
        self[STDDEV_VAL] = float(stdDev)
        

    def get(self):
        y=random.normalvariate(self[MEAN_VAL], self[STDDEV_VAL])
        while y<0:
            y=random.normalvariate(self[MEAN_VAL], self[STDDEV_VAL])
        return y 
        
if __name__ == '__main__':
    def main():
        print "?"

    main()
