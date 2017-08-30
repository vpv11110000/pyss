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
from pyss.handle import Handle
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
            Handle(None, label="a", handlerFunc=lambda o, t: None)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Handle(sgm, label="a", handlerFunc=lambda o, t: None)
        
    def test_001(self):
        """
        Регресс. Проверка присвоения label
        
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

        Generate(sgm, modificatorFunc=[1.0])
        LABELKA="LABELKA"
        Handle(sgm, LABELKA,handlerFunc=lambda o,t: None)
        #                                              
        Terminate(sgm, deltaTerminate=1)
        
        ### test ----------------------        
        m.beforeStart(terminationCount=20, maxTime=MAX_TIME_VAL)
        
        b=m.findBlockByLabel(LABELKA)
        self.assertTrue(b is not None, "b is not None")

if __name__ == '__main__':
    unittest.main(module="test_assign")
