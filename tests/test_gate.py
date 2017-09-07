# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
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
from pyss.test import Test
from pyss.gate import Gate
from pyss.pyss_const import *

class TestGate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Gate(None, condition=GATE_LOGIC_SET, objectName="F1", nextBlockLabel="L1")

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Gate(sgm, condition=GATE_LOGIC_SET, objectName="F1", nextBlockLabel="L1")
        
    def test_init_003(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Gate(sgm, condition=None, objectName="F1", nextBlockLabel="L1")

    def test_init_004(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Gate(sgm, condition=GATE_FACILITY_USED, objectName=None, nextBlockLabel="L1")
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Gate(sgm, condition=GATE_FACILITY_USED, objectName="", nextBlockLabel="L1")
         
    def test_001(self):
        """Моделирование устройства с потерями
        
        Транзакт 1 - занимает устройство
        Транзакт 2 - в потери
        Транзакт 3 - занимает устройство
        Транзакт 4 - в потери
        
        """
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        # FOR TEST
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)             
        #
        F1 = "F1"
        f = Facility(m, facilityName=F1)
        #
        Generate(sgm, modificatorFunc=[1, 2, 3, 4])
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)        
        LAB_1 = "LAB_1"
        Gate(sgm, condition=GATE_FACILITY_NOT_USED, objectName=F1, nextBlockLabel=LAB_1)
        Seize(sgm, facilityName=F1)
        Advance(sgm, meanTime=2.0)
        Release(sgm, facilityName=F1)
        Terminate(sgm)
        #
        Terminate(sgm, LAB_1)
        
        # ЗАПУСК ----------------------        
        m.start(terminationCount=10, maxTime=20)      
        
        print sgm.strBlocksDebug(None)  
        
        # ТЕСТЫ ----------------------
        for t in list_all_transact: 
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])
            print t.strTrack()

            if t[NUM] == 1:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[TERMINATED_TIME], 3)
                expected = "[1]:[1]:[GENERATE]; [1]:[2]:[HANDLE]; [1]:[3]:[GATE]; [1]:[4]:[SEIZE]; [1]:[5]:[ADVANCE]; [3]:[6]:[RELEASE]; [3]:[7]:[TERMINATE]"
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 2:
                self.assertEqual(t[TIME_CREATED], 2)
                self.assertEqual(t[TERMINATED_TIME], 2)
                expected = ("[2]:[1]:[GENERATE]; [2]:[2]:[HANDLE]; [2]:[3]:[GATE]; [2]:[LAB_1]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 3:
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t[TERMINATED_TIME], 5)
                expected = ("[3]:[1]:[GENERATE]; [3]:[2]:[HANDLE]; [3]:[3]:[GATE]; [3]:[4]:[SEIZE]; [3]:[5]:[ADVANCE]; [5]:[6]:[RELEASE]; [5]:[7]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 4:
                self.assertEqual(t[TIME_CREATED], 4)
                self.assertEqual(t[TERMINATED_TIME], 4)        
                expected = ("[4]:[1]:[GENERATE]; [4]:[2]:[HANDLE]; [4]:[3]:[GATE]; [4]:[LAB_1]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
                                
    def test_002(self):
        """Моделирование устройства
        
        Транзакт 1 - занимает устройство
        Транзакт 2 - ждёт
        Транзакт 3 - ждёт
        Транзакт 4 - ждёт
        
        """
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        # FOR TEST
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)             
        #
        F1 = "F1"
        f = Facility(m, facilityName=F1)
        #
        Generate(sgm, modificatorFunc=[1, 2, 3, 4])
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)        
        Gate(sgm, condition=GATE_FACILITY_NOT_USED, objectName=F1, nextBlockLabel=None)
        Seize(sgm, facilityName=F1)
        Advance(sgm, meanTime=2.0)
        Release(sgm, facilityName=F1)
        Terminate(sgm)
        
        # ЗАПУСК ----------------------        
        m.start(terminationCount=10, maxTime=20)      
        
        print sgm.strBlocksDebug(None)  
        
        # ТЕСТЫ ----------------------
        print 49*"="
        for t in list_all_transact: 
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])
            print t.strTrack()
        print 49*"="
        for t in list_all_transact: 
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])
            print t.strTrack()

            if t[NUM] == 1:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[TERMINATED_TIME], 3)
                expected = ("[1]:[1]:[GENERATE]; [1]:[2]:[HANDLE]; [1]:[3]:[GATE]; [1]:[4]:[SEIZE]; [1]:[5]:[ADVANCE]; [3]:[6]:[RELEASE]; [3]:[7]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 2:
                self.assertEqual(t[TIME_CREATED], 2)
                self.assertEqual(t[TERMINATED_TIME], 5)
                expected = ("[2]:[1]:[GENERATE]; [2]:[2]:[HANDLE]; [3]:[3]:[GATE]; [3]:[4]:[SEIZE]; [3]:[5]:[ADVANCE]; [5]:[6]:[RELEASE]; [5]:[7]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 3:
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t[TERMINATED_TIME], 7)
                expected = ("[3]:[1]:[GENERATE]; [3]:[2]:[HANDLE]; [5]:[3]:[GATE]; [5]:[4]:[SEIZE]; [5]:[5]:[ADVANCE]; [7]:[6]:[RELEASE]; [7]:[7]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                
            elif t[NUM] == 4:
                self.assertEqual(t[TIME_CREATED], 4)
                self.assertEqual(t[TERMINATED_TIME], 9)        
                expected = ("[4]:[1]:[GENERATE]; [4]:[2]:[HANDLE]; [7]:[3]:[GATE]; [7]:[4]:[SEIZE]; [7]:[5]:[ADVANCE]; [9]:[6]:[RELEASE]; [9]:[7]:[TERMINATE]")
                self.assertEqual(t.strTrack(), expected)                                   
                                
if __name__ == '__main__':
    unittest.main(module="test_gate")
