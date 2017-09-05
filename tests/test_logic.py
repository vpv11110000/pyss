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
from pyss.mark import Mark
from pyss.loop import Loop
from pyss.handle import Handle
from pyss.advance import Advance
from pyss.assign import Assign
from pyss import logic
from pyss.logic import Logic
from pyss.logic_object import LogicObject
from pyss import bprint_blocks

from pyss import logger
 
from pyss.pyss_const import *

class TestLoop(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Logic(None, actionFunc=logic.invert, logicObjectName="L_1")

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Logic(sgm, actionFunc=logic.invert, logicObjectName="L_1") 

    def test_init_003(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Logic(sgm, actionFunc=None, logicObjectName="L_1") 

    def test_init_004(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Logic(sgm, actionFunc=logic.invert, logicObjectName=None) 

    def test_001(self):
        logger.info("--- test_001 ----------------------------------")
        
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        L1="L1"
        lk=LogicObject(m, logicObjectName=L1, initialState=False)
        
        m[OPTIONS].setAllFalse()

        MAX_TIME = 50
        
        LOGIC_LABEL ="LOGIC_LABEL"
        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)
        def testBlockBefore(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()
            if b[LABEL] == LOGIC_LABEL:
                o=m.findLogicObject(b[LOGIC_OBJECT_NAME])
                if d==1:
                    self.assertFalse(o[STATE], "assertFalse(o[STATE],...")
                elif d==2:
                    self.assertTrue(o[STATE], "assertTrue(o[STATE],...")

        # проверка после обработки транзакта в блоки (block.transactHandle)
        def testBlockAfter(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()
            if b[LABEL] == LOGIC_LABEL:
                o=m.findLogicObject(b[LOGIC_OBJECT_NAME])
                if d==1:
                    self.assertTrue(o[STATE], "assertTrue(o[STATE],...")
                elif d==2:
                    self.assertFalse(o[STATE], "assertFalse(o[STATE],...")
        
        ### SEGMENT ------------------------------------------
        Generate(sgm, med_value=None, modificatorFunc=[1,2], first_tx=None, max_amount=None)
        Logic(sgm, LOGIC_LABEL, actionFunc=logic.invert, logicObjectName=L1)
        Terminate(sgm, deltaTerminate=1)
        
        # test
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)
        
        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=MAX_TIME)

if __name__ == '__main__':
    unittest.main(module="test_loop")
