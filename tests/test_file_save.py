# #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest
from test._mock_backport import DEFAULT
from nt import unlink

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
from pyss.file_save import FileSave

from pyss import logger
from pyss import file_save
from pyss.pyss_const import *

class TestFileSave(unittest.TestCase):

    #@unittest.skip("skip test_assemble_001")
    def test_assemble_001(self):
        """
        Создаётся 5 транзактов.
        
        В файл "default.dat" записыватеся текущее время.
        
        """
        
        logger.info("--- test_assemble_001 ----------------------------------")
        ### MODEL ----------------------------
        m = PyssModel()
        sgm = Segment(m, label="MODEL_SEGMENT")
        #
        m[OPTIONS].setAllFalse()
        fel = m.getFel()

        MAX_TIME = 20


        DEFAULT_DAT="default.dat"
        # EXPECTED from file
        expected=[]

        Generate(sgm, med_value=1, modificatorFunc=None, first_tx=1, max_amount=5)
        # test
        def funcSave(owner, transact):
            s=str(m.getCurTime())
            # for test
            expected.append(s)
            return s        
        FileSave(sgm, fileName=DEFAULT_DAT, funcSave=funcSave, mode="write")
        Terminate(sgm, deltaTerminate=1)
        #
        # test
        
        # ЗАПУСК --------------------------------------------        
        m.start(terminationCount=5, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        print "expected:"
        print expected
        
        with open(DEFAULT_DAT,'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]

        print "lines:"
        print lines

        self.assertListEqual(lines, expected)
        
        unlink(DEFAULT_DAT)
                
if __name__ == '__main__':
    unittest.main(module="test_file_save")
