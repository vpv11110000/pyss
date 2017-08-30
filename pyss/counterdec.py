##!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль класса счётчик
"""

class CounterDec(object):
    """Счётчик декрементный

    Args:
        initValue - начальное значение сётчика

    """
    def __init__(self, initValue):
        self.value=initValue

    def dec(self,delta=0):
        self.value-=delta
        if self.value<0:
            self.value=0
        return self.isEmpty()

    def isEmpty(self):
        return self.value<=0

    def reset(self,initValue):
        self.value=initValue

    def __str__(self):
        return "GpssCounter.value=%d"%self.value
