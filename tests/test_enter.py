# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import generate
from pyss import terminate
from pyss import logger
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss import storage
from pyss import pyssobject
from pyss import advance
from pyss import options
from pyss.pyss_const import *

class TestEnterLeave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Enter(None, storageName="S1", funcBusySize=1)

    def test_init_002(self):
        m = pyss_model.PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = segment.Segment(m)
        #
        Enter(sgm, storageName="S1", funcBusySize=1) 

        
if __name__ == '__main__':
    unittest.main(module="test_enter")
