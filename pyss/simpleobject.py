# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Очень простой объект модели
"""

# pylint: disable=line-too-long

class SimpleObject(object):
    """Простой объект модели

    Args:
        value - значение

    """

    def __init__(self, value=None):
        self.value = value
        
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def addValue(self, value):
        self.value = self.value + value

    def decValue(self, value):
        self.value = self.value - value
                
    def __str__(self):
        return "%s" % str(self.value)
    
if __name__ == '__main__':
    pass
 
