# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=unused-argument

import sys
import os
import random
import unittest
import traceback

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_model import PyssModel
from pyss.segment import Segment 

from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss.handle import Handle
from pyss.advance import Advance
from pyss.assign import Assign
from pyss.assemble import Assemble

from pyss import logger
from pyss import pyssobject
from pyss.pyss_const import *

def excepthook(tpe, value, trceback):
    trceback.print_stack()

sys.excepthook = excepthook

def findAssembleItemInAssembleSetDict(assembleSetDict, xactNum):
    b = False
    # каждый элемент: key: <assemble set>, value: <объект AssembleItem>
    for assembleSet, assembleItem in assembleSetDict.iteritems():
        if assembleItem.transact[NUM] == xactNum:
            b = assembleItem
            break
    return b

def findTransactNumInAssembleSetDict(assembleSetDict, xactNum):
    b = False
    # каждый элемент: key: <assemble set>, value: <объект AssembleItem>
    for assembleSet, assembleItem in assembleSetDict.iteritems():
        b = assembleItem.transact[NUM] == xactNum
        if b is True:
            break
    return b

class TestAssemble(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Assemble(None, countTransact=2)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Assemble(sgm, countTransact=2) 

    def test_init_003(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Assemble(sgm, countTransact=None)
            
             
    # @unittest.skip("skip test_assemble_001")
    def test_assemble_001(self):
        """
        Создаётся 3 транзакта
        Транзакт 1 - создаётся в момент времени 0, инициирует сбор ещё 2 транзактов
        Транзакты 2..3 - создаются в момент времени 1..2, уничтожаются в моменты 1..2
        Транзакт 1 - уничтожается в момент времени 2
        
        Значения атрибутов блока Assemble (bl) перед обработкой транзактов:
            момент времени 0:
                assembleSetDict    dict: {}    
            момент времени 1:
                bl[COUNT_TRANSACT] == 3
                bl.transact == Транзакт 1
                bl.assembleCount == 2         
            момент времени 2:
                bl[COUNT_TRANSACT] == 3
                bl.transact == Транзакт 1
                bl.assembleCount == 1         
        
        Значения атрибутов блока Assemble (bl) после обработки транзактов:
            момент времени 0:
                bl[COUNT_TRANSACT] == 3
                bl.transact == Транзакт 1
                bl.assembleCount == 2         
            момент времени 1:
                bl[COUNT_TRANSACT] == 3
                bl.transact == Транзакт 1
                bl.assembleCount == 1         
            момент времени 2:
                assembleSetDict    dict: {}

        """
        
        logger.info("--- test_assemble_001 ----------------------------------")

        ### MODEL ----------------------------
        m = PyssModel()
        sgm = Segment(m, label="MODEL_SEGMENT")
        #
        m[OPTIONS].setAllFalse()
        fel = m.getFel()

        MAX_TIME_VAL = 20
        #
        list_all_transact = []
        after_assemble_nums = [1, 7]
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)
        
        # MODEL ----------------------------
        Generate(sgm, med_value=1,
                 modificatorFunc=None,
                 first_tx=0,
                 max_amount=3)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        Assign(sgm, parametrName='ASSEMBLY_SET',
               modificatorFunc=lambda owner, transact: 1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(t[ASSEMBLY_SET], 1))
        #
        Assemble(sgm, "labAssemble", countTransact=3)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertIn(t[NUM], after_assemble_nums))
        #
        Terminate(sgm, deltaTerminate=0)
        
        logger.info("Segment[0]: " + m[SEGMENTS][0].strBlocks())        
        
        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME_VAL, maxTime=MAX_TIME_VAL)
        
        # ТЕСТЫ ----------------------
        for t in list_all_transact: 
            # Транзакт 1 - создаётся в момент времени 0, инициирует сбор ещё 2 транзактов
            # Транзакты 2..3 - создаются в момент времени 1..5, уничтожаются в моменты 1..2
            # Транзакт 1 - уничтожается в момент времени 5.
            if t[NUM] == 1:
                self.assertEqual(t[TIME_CREATED], 0)
                self.assertEqual(t[TERMINATED_TIME], 2)
            elif t[NUM] == 2:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[TERMINATED_TIME], 1)
            elif t[NUM] == 3:
                self.assertEqual(t[TIME_CREATED], 2)
                self.assertEqual(t[TERMINATED_TIME], 2)
                
            print str(["%s:%s" % (k, t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED, TERMINATED_TIME]])

if __name__ == '__main__':
    unittest.main(module="test_assemble")
