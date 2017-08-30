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
from pyss import logger
from pyss.pyss_model import PyssModel
from pyss.segment import Segment 
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.storage import Storage
from pyss import pyssobject
from pyss.advance import Advance
from pyss.preempt import Preempt
from pyss.g_return import GReturn
from pyss.facility import Facility
from pyss.seize import Seize
from pyss.release import Release
from pyss.transfer import Transfer
from pyss.test import Test
from pyss.pyss_const import *

class TestSeize(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Seize(None, facilityName="F1")

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Seize(sgm, facilityName="F1") 

    # @
    # unittest.skip("testing skipping test_queue_001")
    def test_seize_001(self):
        """
        Формируется 3 транзакта в моменты времени 1,2,3
        Транзакт 1 создаётся в момент 1.
        Транзакт 1 входит в устройство F_1 и занимает его на 5 единиц времени
        Транзакт 1 исключается из модели в момент времени 6.

        Транзакт 2 создаётся в момент 2.
        Транзакт 2 задерживается в блоке G_1 до момента 6.
        Транзакт 2 входит в момент 6 в устройство F_1 и занимает его на 5 единиц времени
        Транзакт 2 исключается из модели в момент времени 11.
        
        Транзакт 3 создаётся в момент 3.
        Транзакт 3 задерживается в блоке G_1 до момента 11.
        Транзакт 3 входит в момент 11 в устройство F_1 и занимает его на 5 единиц времени
        Транзакт 3 исключается из модели в момент времени 16.
        
        """
        
        logger.info("--- test_seize_001 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20

        # ОКУ -------------------------------------------------
        F_1 = "F_1"
        facility_1 = Facility(m, facilityName=F_1)
        # for test
        list_all_transact = []
       
        # MODEL ------------------------------------
        # генерится максимум 3 заявки
        Generate(sgm, med_value=1, modificatorFunc=None, first_tx=1, max_amount=3)
        # test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)        
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        Handle(sgm, "G_1", handlerFunc=lambda o, t:
               self.assertTrue(t[NUM] in [1, 2, 3]))
        #        
        Seize(sgm, facilityName=F_1, label="TEST_SEIZE")
        # обработка 5 единиц времени
        Advance(sgm, meanTime=5, modificatorFunc=0)
        Handle(sgm, handlerFunc=lambda o, t:
               self.assertTrue(m.getCurTime() in [6, 11, 16]))
        Release(sgm, facilityName=F_1, label=None)
        Terminate(sgm, deltaTerminate=1)
        #
        # test
        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)    
        def testBlockBefore(b):
            facilityName=facility_1[FACILITY_NAME]
            d=m.getCurTime()
            if b[LABEL]=="TEST_SEIZE":
                # проверка работы блока Seize
                if d==1:
                    self.assertEqual(b[FACILITY_NAME],F_1)
                    if facilityName in m.getDelayedList():
                        self.assertTrue(m.getDelayedList()[facilityName].isEmpty())
                elif (d==2):
                    self.assertEqual(m.getDelayedList()[facilityName].isEmpty(), True)
                elif (d==3):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),1)
                elif (d==6):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),1)
                elif (d==11):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),0)                    
        # проверка после обработки транзакта в блоки (block.transactHandle)    
        def testBlockAfter(b):
            facilityName=facility_1[FACILITY_NAME]
            d=m.getCurTime()
            if b[LABEL]=="TEST_SEIZE":
                # проверка работы блока Seize
                if d==1:
                    self.assertEqual(b[FACILITY_NAME],F_1)
                    if facilityName in m.getDelayedList():
                        self.assertTrue(m.getDelayedList()[facilityName].isEmpty())
                elif (d==2):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),1)
                elif (d==3):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),2)
                elif (d==6):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),1)
                elif (d==11):
                    self.assertEqual(len(m.getDelayedList()[facilityName].items[0]),0)                    
                
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)
        
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=20, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        self.assertEqual(len(list_all_transact), 3)
        for t in list_all_transact: 
            # Формируется 3 транзакта в моменты времени 1,2,3
            # Транзакт 1 создаётся в момент 1.
            # Транзакт 1 входит в устройство F_1 и занимает его на 5 единиц времени
            # Транзакт 1 исключается из модели в момент времени 6.
            # 
            # Транзакт 2 создаётся в момент 2.
            # Транзакт 2 задерживается в блоке G_1 до момента 6.
            # Транзакт 2 входит в момент 6 в устройство F_1 и занимает его на 5 единиц времени
            # Транзакт 2 исключается из модели в момент времени 11.
            # 
            # Транзакт 3 создаётся в момент 3.
            # Транзакт 3 задерживается в блоке G_1 до момента 11.
            # Транзакт 3 входит в момент 11 в устройство F_1 и занимает его на 5 единиц времени
            # Транзакт 3 исключается из модели в момент времени 16.          
            if t[NUM] == 1:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[TERMINATED_TIME], 6)
            elif t[NUM] == 2:
                self.assertEqual(t[TIME_CREATED], 2)
                self.assertEqual(t[TERMINATED_TIME], 11)
            elif t[NUM] == 3:
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t[TERMINATED_TIME], 16)
                
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])
        
        s = sgm.strBlocks()
        self.assertEqual(s, ("[1]:[GENERATE]; [2]:[HANDLE]; [G_1]:[HANDLE]; [TEST_SEIZE]:[SEIZE]; [5]:[ADVANCE]; [6]:[HANDLE]; [7]:[RELEASE]; [8]:[TERMINATE]"))


if __name__ == '__main__':
    unittest.main(module="test_seize")
