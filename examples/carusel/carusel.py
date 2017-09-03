# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# carusel.py – Моделирование кассы в случае нестационарного потока покупателей

**Постановка проблемы**

Время           Интенсивность,    Количество покупок    Относительная частота     Суммарная частота 
                чел/мин    
 9:00 - 11:00   2                (0-5]                   0.2                     0.3
 2*60 мин                        (5-20]                  0.3                     0.5    
                                 (20-50]                 0.2                     0.7
                                 (50-100]                0.2                     0.9
                                 (100..120]              0.1                     1.0

11:00 - 15:00   5                (0-5]                   0.2                     0.3
 4*60 мин                        (5-20]                  0.2                     0.4    
                                 (20-50]                 0.25                    0.65
                                 (50-100]                0.25                    0.9
                                 (100..120]              0.1                     1.0

15:00 - 17:00   3                (0-5]                   0.4                     0.4
 2*60 мин                        (5-20]                  0.3                     0.7    
                                 (20-50]                 0.18                    0.88
                                 (50-100]                0.1                     0.98
                                 (100..120]              0.02                    1.0

Необходимо смоделировать систему инвентаризации в течение дня.

Построить гистограмму длины очереди.

------
"""

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *
from pyss import generate, bprint
from pyss import terminate
from pyss import logger
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import enter
from pyss import leave 
from pyss import tabulate
from pyss import options
from pyss import queue
from pyss import assign
from pyss import advance
from pyss import seize
from pyss import test
from pyss import depart
from pyss import release
from pyss import storage

def main():
    logger.info("-------------------------------------")
    #-------------------------------
    # TODO ДЕЛАТЬ carusel
    
if __name__ == '__main__':
    main()
