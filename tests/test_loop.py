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
            Loop(None, parametrName=P1, toBlockLabel=P2)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Loop(sgm, parametrName=P1, toBlockLabel=P2) 

    # @
    # unittest.skip("testing skipping test_queue_001")
    def test_loop_001(self):
        logger.info("--- test_loop_001 ----------------------------------")
        
        ### MODEL ------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 50
        #
        LOOP_COUNT = "LOOP_COUNT"
        BEGIN_CIKL = "BEGIN_CIKL"
        METKA = "Метка времени"

        # FOR TEST
        list_all_transact = []
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)   
                    
        #
        def mf(owner, currentTime):
            return 0
        ### SEGMENT ------------------------------------------
        # генерится максимум 1 заявка в момент времени 3
        Generate(sgm, med_value=None, modificatorFunc=None, first_tx=3, max_amount=1)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        # задаём параметр цикла - 5 раз пройти
        Assign(sgm, parametrName=LOOP_COUNT, modificatorFunc=lambda o, t:5)
        # печатаем время
        bprint_blocks.buildBprintCurrentTime(sgm, strFormat="=== Time: [%.12f]")
        
        # метка времени в параметр 
        Mark(sgm, label=BEGIN_CIKL, parametrName="Метка времени")
        # печатаем значение параметра цикла и метку времени транзакта 
        bprint_blocks.buildBprintCurrentTransact(sgm,
                                                 funcTransactToStr=lambda tr:"[%s][%s:%s][%s:%s]" % (tr[NUM], LOOP_COUNT, tr[LOOP_COUNT], METKA, tr[METKA]))
        Advance(sgm, meanTime=5, modificatorFunc=lambda o, t:0)
        Loop(sgm, parametrName=LOOP_COUNT, toBlockLabel=BEGIN_CIKL, label="END_CIKL")
        
        #
        Terminate(sgm, deltaTerminate=1)

        # ЗАПУСК ---------------------------
        m.start(terminationCount=10000, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        
        self.assertEqual(len(list_all_transact), 1)
        
        for t in list_all_transact:
            expected = ("[3]:[1]:[GENERATE]; [3]:[2]:[HANDLE]; [3]:[3]:[ASSIGN]; [3]:[4]:[BPRINT]; [3]:[BEGIN_CIKL]:[MARK]; [3]:[6]:[BPRINT]; [3]:[7]:[ADVANCE];"
                        + " [8]:[END_CIKL]:[LOOP]; [8]:[BEGIN_CIKL]:[MARK]; [8]:[6]:[BPRINT]; [8]:[7]:[ADVANCE];"
                        + " [13]:[END_CIKL]:[LOOP]; [13]:[BEGIN_CIKL]:[MARK]; [13]:[6]:[BPRINT]; [13]:[7]:[ADVANCE];"
                        + " [18]:[END_CIKL]:[LOOP]; [18]:[BEGIN_CIKL]:[MARK]; [18]:[6]:[BPRINT]; [18]:[7]:[ADVANCE];"
                        + " [23]:[END_CIKL]:[LOOP]; [23]:[BEGIN_CIKL]:[MARK]; [23]:[6]:[BPRINT]; [23]:[7]:[ADVANCE];"
                        + " [28]:[END_CIKL]:[LOOP]; [28]:[9]:[TERMINATE]")
            self.assertEqual(t.strTrack(), expected)
        
        s = sgm.strBlocks()
        self.assertEqual(s, ("[1]:[GENERATE]; [2]:[HANDLE]; [3]:[ASSIGN];"
                             + " [4]:[BPRINT]; [BEGIN_CIKL]:[MARK]; [6]:[BPRINT];"
                             + " [7]:[ADVANCE]; [END_CIKL]:[LOOP]; [9]:[TERMINATE]"))
        

if __name__ == '__main__':
    unittest.main(module="test_loop")
