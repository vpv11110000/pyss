# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с типовыми функциями модификации
"""

# pylint: disable=line-too-long

import random

def none(owner, currentTime):
    """Возвращает None"""
    
    return None

def zero(owner, currentTime):
    """Возвращает 0"""
    return 0

def uniform(owner, currentTime):
    """Probable distribution, 0 <= N <= 1.0"""
    return random.uniform(0, 1.0)

if __name__ == '__main__':
    def main():
        print "?"

    main()
