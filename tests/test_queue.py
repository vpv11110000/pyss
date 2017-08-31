# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *
from pyss import pyssobject

from pyss.pyss_model import PyssModel
from pyss.segment import Segment 
from pyss.queue import Queue

class TestEnterLeave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Queue(None, queueName="Q1", deltaIncrease=1, initLength=0)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Queue(sgm, queueName="Q1", deltaIncrease=1, initLength=0) 

        
if __name__ == '__main__':
    unittest.main(module="test_queue")
