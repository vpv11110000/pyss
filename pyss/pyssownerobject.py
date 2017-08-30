# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long

import inspect
from pyss.pyss_const import *
from pyss import pyssobject
from pyss.pyssobject import PyssObject
from pyss import logger

class PyssOwnerObject(PyssObject):
    """Базовый класс для объектов модели с атрибутом OWNER 

    Args:
        entityType - задает строку, идентифицирующую объект модели.
        objectNumber - номер объекта
        label - задаёт метку, по которой можно найти объект в контейнерах модели:

    Атрибуты базового класса объекта модели (в дополнение к атрибутам pyssobject.PyssObject):
    bl = <наследник от PyssOwnerObject>(...)
    bl[OWNER] - объект-владелец

    """

    def __init__(self, entityType, label=None, owner=None):
        super(PyssOwnerObject, self).__init__(entityType, label=label)
        map(pyssobject.raiseIsNone,[owner])
        self[OWNER] = owner
        
    def getOwner(self):
        """Получить объект владельца"""

        return self[OWNER]        
