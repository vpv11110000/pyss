# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long, bad-whitespace, missing-docstring

# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

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

from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss.handle import Handle
from pyss.advance import Advance

from pyss import logger
 
from pyss.pyss_const import *

class TestAdvance(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Advance(None, meanTime=1, modificatorFunc=None)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Advance(sgm, meanTime=1, modificatorFunc=None)    

    # @unittest.skip("testing skipping test_advance_001")
    def test_advance_001(self):
        """
        Сегмент тестовый
        Формируется один транзакт в момент времени 0.
        Обрабатывается 2 единицы времени.
        Завершается обработка транзакта в модели в момент 2.
        
        """
        logger.info("--- test_advance_001 ----------------------------------")
        
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        
        # FOR TEST
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)        
        
        # тестовый сегмент ----------
        Generate(sgm, med_value=1, modificatorFunc=None,
                 first_tx=0,
                 max_amount=1,
                 priority=1)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(t[SCHEDULED_TIME], None))
        Handle(sgm, handlerFunc=lambda o, t:
               self.assertNotIn(t, m.getFel().transactList))
        # 
        Advance(sgm, meanTime=2, modificatorFunc=lambda o, c:0)
        # test
        Handle(sgm, handlerFunc=lambda o, t:
               self.assertNotIn(t, m.getFel().transactList))
        #            
        Terminate(sgm, deltaTerminate=0)
        # сегмент наблюдения -----------------------
        # наблюдаем за: 
        #         components.FEL
        #         list_all_transact[0]
        def testFunc(o, t):
            # t - не из тестового сегмента!
            c = m.getCurTime()
            if c == 0:
                self.assertIn(list_all_transact[0], m.getFel().transactList) 
            elif c == 1:
                self.assertIn(list_all_transact[0], m.getFel().transactList)
            else:
                self.assertNotIn(list_all_transact[0], m.getFel().transactList)
            
        sgmControl = Segment(m)
        Generate(sgmControl, med_value=1)
        # test
        Handle(sgmControl, handlerFunc=testFunc)
        Handle(sgmControl, handlerFunc=lambda o, t:
               self.assertEqual(list_all_transact[0][SCHEDULED_TIME], 2))
        Terminate(sgmControl, deltaTerminate=1)
        
        # ЗАПУСК ----------------------        
        m.start(terminationCount=10, maxTime=20)

    # @unittest.skip("testing skipping test_advance_002")
    def test_advance_002(self):
        """
        Сегмент тестовый
        Формируется один транзакт в момент времени 0.
        Обрабатывается 2 единицы времени.
        Завершается обработка транзакта в модели в момент 2.
        
        """
        logger.info("--- test_advance_001 ----------------------------------")
        
        ### MODEL ----------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()
        fel = m.getFel()

        MAX_TIME = 20
        
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)        
        
        #
        Generate(sgm, med_value=1, modificatorFunc=None,
                 first_tx=0,
                 max_amount=1,
                 priority=1)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(t[SCHEDULED_TIME], None))
        Handle(sgm, handlerFunc=lambda o, t:
               self.assertNotIn(t, fel.transactList))
        #            
        Advance(sgm, meanTime=2, modificatorFunc=0)
        # test
        Handle(sgm, handlerFunc=lambda o, t:
               self.assertNotIn(t, fel.transactList))
        #            
        Terminate(sgm, deltaTerminate=0)

        # сегмент наблюдения -----------------------
        # наблюдаем за: 
        #         components.FEL
        #         list_all_transact[0]
        def testFunc(o, t):
            # t - не из тестового сегмента!
            c = m.getCurTime()
            if c == 0:
                self.assertIn(list_all_transact[0], fel.transactList) 
            elif c == 1:
                self.assertIn(list_all_transact[0], fel.transactList)
            else:
                self.assertNotIn(list_all_transact[0], fel.transactList)
            
        sgmControl = Segment(m)
        Generate(sgmControl, med_value=1)
        # test
        Handle(sgmControl, handlerFunc=testFunc)
        Handle(sgmControl, handlerFunc=lambda o, t:self.assertEqual(list_all_transact[0][SCHEDULED_TIME], 2))
        
        Terminate(sgmControl, deltaTerminate=1)
                    
        
        # ЗАПУСК ----------------------        
        m.start(terminationCount=10, maxTime=20)

    # @unittest.skip("testing skipping test_advance_003")
    def test_advance_003(self):
        """
        Формируется транзакт в момент времени 1.
        Обрабатывается 2 единицы времени.
        Завершается обработка транзакта в модели в момент 3.

        Формируется транзакт в момент времени 5.
        Обрабатывается 3 единицы времени.
        Завершается обработка транзакта в модели в момент 8.
        
        """
        logger.info("--- test_advance_001 ----------------------------------")
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()
        fel = m.getFel()

        MAX_TIME = 20
        
        # FOR TEST ---------------
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)        
        
        
        # сегмент моделирования
        Generate(sgm, med_value=None,
                 modificatorFunc=[1, 5],
                 first_tx=None,
                 max_amount=None,
                 priority=1)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(t[SCHEDULED_TIME], None))
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(t, fel.transactList))
        #            
        Advance(sgm, meanTime=[2, 3], modificatorFunc=None)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(t, fel.transactList))
        #            
        Terminate(sgm, deltaTerminate=0)

        # ЗАПУСК ----------------------        
        m.start(terminationCount=10, maxTime=20)

        # ТЕСТЫ ----------------------
        for t in list_all_transact: 
            # Формируется транзакт в момент времени 1.
            # Обрабатывается 2 единицы времени.
            # Завершается обработка транзакта в модели в момент 3.
            # 
            # Формируется транзакт в момент времени 5.
            # Обрабатывается 3 единицы времени.
            # Завершается обработка транзакта в модели в момент 8.        
                
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])

            if t[NUM] == 1:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[TERMINATED_TIME], 3)
            elif t[NUM] == 2:
                self.assertEqual(t[TIME_CREATED], 5)
                self.assertEqual(t[TERMINATED_TIME], 8)

if __name__ == '__main__':
    unittest.main(module="test_advance")
