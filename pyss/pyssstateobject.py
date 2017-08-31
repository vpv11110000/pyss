# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long

import inspect
from pyss.pyss_const import *
from pyss import pyssobject
from pyss.pyssownerobject import PyssOwnerObject
from pyss import logger

class PyssStateObject(PyssOwnerObject):
    """Базовый класс для объектов модели с обработкой состояний 

    Args:
        entityType - задает строку, идентифицирующую объект модели.
        objectNumber - номер объекта
        label - задаёт метку, по которой можно найти объект в контейнерах модели:

    Атрибуты базового класса объекта модели (в дополнение к атрибутам pyssobject.PyssObject):
    bl = <наследник от PyssOwnerObject>(...)
    bl[OWNER] - объект-владелец

    """

    def __init__(self, entityType, label=None, owner=None):
        super(PyssStateObject, self).__init__(entityType, label=label, owner=owner)
        self[ON_STATE_CHANGE] = {}
        
    def existsHandlerOnStateChange(self, handlerName):
        return handlerName in self[ON_STATE_CHANGE].keys() 
        
    def addHandlerOnStateChange(self, handlerName=None, handler=None):
        """Добавление (если не добавлен ранее) обработчика изменения состояния
        
        Args:
            handlerName - наименование обработчика
            handler - функция f(obj,oldState).
                      obj - объект, изменивший состояние
                      oldState - значение старого состояния        
        
        """
        
        if handlerName is None:
            raise pyssobject.ErrorIsNone("handlerName is None")
        
        if handler.__name__ not in self[ON_STATE_CHANGE].keys():
            self[ON_STATE_CHANGE][handlerName] = handler
        
    def removeHandlerOnStateChange(self, handlerName):
        """Удаление обработчика изменения состояния
        
        Args:
            handler - функция, ранее добавленная как обработчик изменения состояния        
        
        """
        
        if handlerName in self[ON_STATE_CHANGE].keys():
            self[ON_STATE_CHANGE].pop(handlerName, None)
        else:
            logger.warn("Попытка удаления несуществующего обработчика изменения состояния")
        

    def fireHandlerOnStateChange(self, oldState):
        """Вызов обработчиков изменения состояния
        
        Args:
            oldSate - старое значение состояния        
        
        """
        
        for h in self[ON_STATE_CHANGE].itervalues():
            h(self, oldState)    
