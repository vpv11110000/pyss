# #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

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

class TestAssign(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Assign(None, parametrName=P1, modificatorFunc=lambda o, t: "Parametr 1")

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Assign(sgm, parametrName=P1, modificatorFunc=lambda o, t: "Parametr 1")
        
    # @
    # unittest.skip("testing skipping test_001")
    def test_assign_001(self):
        """
        Формируется 5 транзактов в моменты времени 0,1,2,3,4
        В транзактs в параметр "Новый параметр транзакта" записывается 
        строковое представление текущего времени
        
        """

        logger.info("--- test_assign_001 ----------------------------------")
        
        ### MODEL ----------------------------
        m = PyssModel()
        sgm = Segment(m, label="MODEL_SEGMENT")
        #
        m[OPTIONS].setAllFalse()
        fel = m.getFel()

        MAX_TIME_VAL = 20

        #

        Generate(sgm, med_value=1, modificatorFunc=None, max_amount=4)
        def assignFunc(o, t):
            if t[NUM] == 1:
                return "a"
            elif t[NUM] == 2:
                return "b"
            elif t[NUM] == 3:
                return "c"
            elif t[NUM] == 4:
                return "d"
        Assign(sgm, parametrName="Новый параметр транзакта", modificatorFunc=assignFunc)
        # test
        Handle(sgm,
               handlerFunc=lambda o, t:self.assertIn(t["Новый параметр транзакта"],
                                                    "a" if t[NUM] == 1 else "b" if t[NUM] == 2 else "c" if t[NUM] == 3 else "d"
                                                    ))
            
        #                                              
        Terminate(sgm, deltaTerminate=1)
        
        ### ЗАПУСК ----------------------        
        m.start(terminationCount=20, maxTime=MAX_TIME_VAL)

if __name__ == '__main__':
    unittest.main(module="test_assign")
