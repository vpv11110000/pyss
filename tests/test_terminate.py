# #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import pyssobject
from pyss.pyss_model import PyssModel
from pyss.segment import Segment

from pyss import generate 
from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss import logger
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.storage import Storage
from pyss.advance import Advance
from pyss.preempt import Preempt
from pyss.g_return import GReturn
from pyss.facility import Facility
from pyss.seize import Seize
from pyss.release import Release
from pyss.transfer import Transfer
from pyss.test import Test
from pyss.queue import Queue
from pyss.depart import Depart
from pyss.split import Split
from pyss.pyss_const import *


class TestTerminate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Terminate(None, deltaTerminate=0)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Terminate(sgm, deltaTerminate=0)

    # @unittest.skip("testing skipping test_001")
    def test_001(self):
        """
        Попытка сформировать три транзакта во время 1,2,3.
        При вхождении транзакта в блок Terminate, счётчика завершений уменьшается на 5 (DELTA).
        Запуск c начальным значением счётчика завершений - 4.
        Время окончания моделирования - 1.
        Значение счётчика завершений по окончании - 0.
         
        """
        
        logger.info("--- test_001 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        DELTA = 5
        
        TERMINATION_COUNT_INIT = 4
        LIST_OF_TIMES = [1, 2, 3]

        ### SEGMENT ------------------            
        generate.buildForListTimes(sgm, listOfTimes=LIST_OF_TIMES)
        Terminate(sgm, deltaTerminate=DELTA)
        
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=TERMINATION_COUNT_INIT, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        self.assertEqual(m[END_TIME], 1)
        self.assertEqual(m.terminateCounter.value, 0)

    # @unittest.skip("testing skipping test_002")
    def test_002(self):
        """
        Попытка сформировать три транзакта во время 1,2,3.
        При вхождении транзакта в блок Terminate, счётчика завершений уменьшается на 5 (DELTA).
        Запуск c начальным значением счётчика завершений - 9.
        Время окончания моделирования - 2.
        Значение счётчика завершений по окончании - 0.
         
        """
        
        logger.info("--- test_002 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        DELTA = 5
        
        TERMINATION_COUNT_INIT = 9
        LIST_OF_TIMES = [1, 2, 3]
            
        ### SEGMENT ----------------------------
        generate.buildForListTimes(sgm, listOfTimes=LIST_OF_TIMES)
        Terminate(sgm, deltaTerminate=DELTA)
        
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=TERMINATION_COUNT_INIT, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        self.assertEqual(m[END_TIME], 2)
        self.assertEqual(m.terminateCounter.value, 0)

    def test_003(self):
        """
        Попытка сформировать три транзакта во время 1,2,3.
        При вхождении транзакта в блок Terminate, счётчика завершений уменьшается на 5 (DELTA).
        Запуск c начальным значением счётчика завершений - 15.
        Время окончания моделирования - 3.
        Значение счётчика завершений по окончании - 0.
         
        """
        
        logger.info("--- test_003 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        DELTA = 5
        
        TERMINATION_COUNT_INIT = 15
        LIST_OF_TIMES = [1, 2, 3]
            
        ### SEGMENT ----------------------------

        generate.buildForListTimes(sgm, listOfTimes=LIST_OF_TIMES)
        def handlerFunc(o, t):
            if t[NUM] == 1:
                self.assertEqual(m.terminateCounter.value, TERMINATION_COUNT_INIT)
            elif t[NUM] == 2:
                self.assertEqual(m.terminateCounter.value, TERMINATION_COUNT_INIT - DELTA)
            elif t[NUM] == 3:
                self.assertEqual(m.terminateCounter.value, TERMINATION_COUNT_INIT - 2 * DELTA)                
            else:
                self.assertTrue(False, "Неожиданные поведение")
                
        Handle(sgm, handlerFunc=handlerFunc)
        Terminate(sgm, deltaTerminate=DELTA)
       
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=TERMINATION_COUNT_INIT, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        self.assertEqual(m[END_TIME], 3)
        self.assertEqual(m.terminateCounter.value, 0)


if __name__ == '__main__':
    unittest.main(module="test_terminate")
