# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long

import inspect
from pyss.pyss_const import *
from pyss import logger

class ErrorIsNone(Exception):
    pass

class ErrorIsNotStr(Exception):
    pass

class ErrorIsTrue(Exception):
    pass

class ErrorIsFalse(Exception):
    pass

class ErrorIsZero(Exception):
    pass

class ErrorInvalidArg(Exception):
    pass

class ErrorKeyExists(Exception):
    pass

class ErrorSegmentExists(Exception):
    pass

class ErrorPlotExists(Exception):
    pass

class ErrorQueueObjectExists(Exception):
    pass

class TerminationCounterIsEmpty(Exception):
    pass


def raiseIsNone(arg):
    if arg is None:
        raise ErrorIsNone("arg is None")

def raiseIsTrue(arg):
    if arg is True:
        raise ErrorIsTrue("arg is bad")

def raiseIsFalse(arg):
    if arg is False:
        raise ErrorIsFalse("arg is bad")
    
def raiseIsZero(arg):
    if arg is None:
        raise ErrorIsZero("arg is 0")

def floatEquals(a, b, allowed_error=ALLOWED_ERROR):
    return abs(a - b) <= allowed_error

def isfunction(v):
    return inspect.isfunction(v) or inspect.ismethod(v)

class ObjectNumber(object):
    def __init__(self):
        self.number = 0

    def buildObjectNumber(self):
        self.number += 1
        return self.number

    def reset(self):
        self.number = 0

class PyssObject(dict):
    """Базовый класс для объектов модели

    Args:
        entityType - задает строку, идентифицирующую объект модели.
        objectNumber - номер объекта
        label - задаёт метку, по которой можно найти объект в контейнерах модели:

    Атрибуты базового класса объекта модели:
    bl = <наследник от PyssObject>(...)
    bl[ENTITY_TYPE] - идентификатор типа объекта (см. pyss_const.REGISTERED_BLOCK_ENTITY_TYPE)
    bl[LABEL]=None - метка объекта
    bl[NUM] - номер объекта, значение формируется генератором номеров objectNumber. 
              Нумерация начинается с 1.

    """

    def __init__(self, entityType, label=None):
        super(PyssObject, self).__init__(self)
        self[ENTITY_TYPE] = entityType
        if label is not None and not isinstance(label, basestring):
            raise ErrorIsNotStr("label must be str [%s]" % entityType)
        self[LABEL] = label
        self[NUM] = None
        
    def setlabel(self, label):
        """Устанавливает метку объекта. Возвращает объект"""
        
        self[LABEL] = label
        return self

    def __str__(self):
        return "%s:%s:%s" % (self[NUM], self[LABEL], self[ENTITY_TYPE])

if __name__ == '__main__':
    pass
