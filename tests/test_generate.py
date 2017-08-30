##!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *

from pyss import pyssobject
from pyss.pyss_model import PyssModel
from pyss.segment import Segment 

from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss.handle import Handle
from pyss.advance import Advance

from pyss import logger
from pyss import options


class TestGenerate(unittest.TestCase):

    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Generate(None, med_value=1, modificatorFunc=None, first_tx=0, max_amount=None, priority=1)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Generate(sgm, med_value=1, modificatorFunc=None, first_tx=0, max_amount=None, priority=1)   

    #@unittest.skip("test_generate_001")
    def test_generate_001(self):
        logger.info("--- test_generate_001 ----------------------------------")
        
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        
        g = Generate(sgm, med_value=1,
                     modificatorFunc=None,
                     first_tx=0,max_amount=5,
                     priority=0)
        logger.info(str(g))
        currentTime=0
        maxTime = 10
        deltaTime=1        
        while currentTime<maxTime:
            logger.info("Time: [%d]"%currentTime)
            if currentTime<5:
                self.assertTrue(g[ENABLED])
            else:
                self.assertFalse(g[ENABLED])
            t=g.generateTransact(currentTime)
            if currentTime<4:
                self.assertTrue(g[ENABLED])
            else:
                self.assertFalse(g[ENABLED])
            if currentTime<5:
                self.assertTrue(bool(t))
            else:
                self.assertEqual(t, None)
            logger.info(str(t))
            currentTime+=deltaTime
        logger.info("--- STOP test_generate_001 -----")

    #@unittest.skip("test_generate_002")
    def test_generate_002(self):
        logger.info("--- test_generate_002 ----------------------------------")
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        g = Generate(sgm, med_value=2,
                     modificatorFunc=None,
                     first_tx=0,
                     max_amount=5,
                     priority=0,
                     label=None)
        logger.info(str(g))
        currentTime=0
        maxTime = 20
        deltaTime=1
        countGenetatedTransact=0
        while currentTime<maxTime:
            logger.info("Time: [%d]"%currentTime)
            if currentTime<9:
                self.assertTrue(g[ENABLED])
            else:
                self.assertFalse(g[ENABLED])
            t=g.generateTransact(currentTime)
            if currentTime<8:
                self.assertTrue(g[ENABLED])
            else:
                self.assertFalse(g[ENABLED])
            
            if currentTime<9 and (currentTime % 2)==0:
                self.assertTrue(bool(t))
                countGenetatedTransact+=1
            else:
                self.assertEqual(t, None)
            logger.info(str(t))
            currentTime+=deltaTime
        self.assertEqual(countGenetatedTransact, 5)
        logger.info("--- STOP test_generate_002 ------------")

    #@unittest.skip("test_generate_003")
    def test_generate_003(self):
        logger.info("--- test_generate_003 ----------------------------------")
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        g = Generate(sgm, med_value=None,
                     modificatorFunc=None,
                     first_tx=3,
                     max_amount=1,
                     priority=0,
                     label=None)
        logger.info(str(g))
        currentTime=0
        maxTime = 20
        deltaTime=1
        result_CountGenetatedTransact=0
        result_first_tx=None
        
        while currentTime<maxTime:
            logger.info("Time: [%d]"%currentTime)
            t=g.generateTransact(currentTime)
            
            if currentTime==3:
                self.assertTrue(bool(t))
                result_CountGenetatedTransact+=1
                result_first_tx=currentTime
            else:
                self.assertEqual(t, None)
            logger.info(str(t))
            currentTime+=deltaTime
        self.assertEqual(result_CountGenetatedTransact, 1)
        self.assertEqual(result_first_tx, 3)
        logger.info("--- STOP test_generate_003 ------------")

    def test_generate_004(self):
        logger.info("--- test_generate_004 ----------------------------------")

        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        LIST_OF_TIMES=[1.1,2.1,3.1]
        # FOR TEST
        list_all_transact=[]
        def funcTransactTo_list_all_transact(owner,transact):
            # складируем транзакты в список
            list_all_transact.append(transact)
            
        # MODEL ----------------------------
        Generate(sgm, med_value=None,
                 modificatorFunc=LIST_OF_TIMES,
                 first_tx=None,
                 max_amount=None,
                 priority=0,
                 label=None)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        Terminate(sgm, deltaTerminate=1)
        
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=15, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        self.assertEqual(len(list_all_transact),3)
        for t in list_all_transact: 
            print str(["%s:%s"%(k,t[k]) 
                       for k in t.keys() if k 
                       in [TIME_CREATED,TERMINATED_TIME]])                

            if t[NUM]==1:
                self.assertEqual(t[TIME_CREATED], LIST_OF_TIMES[0])
            elif t[NUM]==2:
                self.assertEqual(t[TIME_CREATED], LIST_OF_TIMES[1])
            elif t[NUM]==3:
                self.assertEqual(t[TIME_CREATED], LIST_OF_TIMES[2])
                

if __name__ == '__main__':
    unittest.main(module="test_generate")
