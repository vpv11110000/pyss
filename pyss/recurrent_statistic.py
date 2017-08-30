##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
DRAFT Модуль реализации вычисления статистических параметров на основе рекурентных формул.

НЕ ИСПОЛЬЗОВАТЬ

большие погрешности или ошибки

"""

from pyss.pyss_const import *
from pyss import logger
import math

class RecurrentStatistic(object):
    ## Вычисляет среднее арифметическое, дисперчию, стандартное отклонение рекуррентно
    def __init__(self):
        self.n=0
        self.mean=None
        self.dispersion=None
        self.standartDeviation=None

    def reset(self):
        self.n=0
        self.mean=None
        self.dispersion=None
        self.standartDeviation=None
        return self

    def addValue(self,x):
        if self.n==0:
            self.mean=float(x)
            self.dispersion=0.0
            self.standartDeviation=0.0
            self.n=1
        else:
            n1=self.n+1
            self.mean=(float(x)+self.mean*self.n)/n1
            a=float(x)-self.mean
            self.dispersion=(self.n*self.dispersion+a*a)/n1
            self.standartDeviation=math.sqrt(self.dispersion)
            self.n=n1
            raise Exception("Here bad formulas")
        return self

