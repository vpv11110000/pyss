# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import unittest
import random

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import pyssobject
from pyss.pyss_model import PyssModel
from pyss.segment import Segment

from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss import logger
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.table import Table
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
from pyss.transact import Transact
from pyss.pyss_const import *

class TestTable(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Table(None, tableName="T1", argFunc=lambda o, t: "P1", limitUpFirst=1.0, widthInt=1.0, countInt=20)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        #
        Table(m, tableName="T1", argFunc=lambda o, t: "P1", limitUpFirst=1.0, widthInt=1.0, countInt=20)      
    

    def test_001(self):
        logger.info("--- test_001 ----------------------------------")
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        
        with self.assertRaises(Exception) as e:
            Table(m, tableName=None, argFunc=None, limitUpFirst=None, widthInt=None, countInt=None)

    def test_002(self):
        logger.info("--- test_002 ----------------------------------")
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        
        with self.assertRaises(Exception) as e:
            Table(m, tableName="table_stat", argFunc="P1", limitUpFirst=1, widthInt=0, countInt=2)

    def test_003(self):
        logger.info("--- test_003 ----------------------------------")
        
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()

        def argFunc(owner, transact):
            return random.randint(1, 9)
        tbl = Table(m, tableName="table_stat", argFunc=argFunc, limitUpFirst=None, widthInt=None, countInt=None)
        timeCreated = 0
        while timeCreated < 1000:
            t = Transact(None, timeCreated, priority=0)
            # t[P1]=0.1
            tbl.handleTransact(t, coef=1)
            timeCreated += 1
        logger.info(tbl.table2str())

    def test_004(self):
        logger.info("--- test_004 ----------------------------------")
        
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()

        ARGUMENT = "ARGUMENT"
        def argFunc(owner, tranzact):
            return tranzact[ARGUMENT]
        tbl = Table(m, tableName="table_stat", argFunc=argFunc, limitUpFirst=1.0, widthInt=1.0, countInt=10)
        
        for timeCreated in xrange(1, 7):
            t = Transact(None, timeCreated, priority=0)
            t[NUM] = timeCreated
            t[ARGUMENT] = timeCreated % 7
            # t[P1]=0.1
            tbl.handleTransact(t, coef=1)
        
        self.assertEqual(tbl[INTERVALS][POSITIVE_INFINITY], 0, "tbl[INTERVALS][POSITIVE_INFINITY], 0")
        self.assertEqual(tbl[INTERVALS][NEGATIVE_INFINITY], 0, "tbl[INTERVALS][NEGATIVE_INFINITY], 0")
        
        self.assertListEqual(tbl[LIST], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
        l = tbl[LIST]
        for z in l:
            y = tbl[INTERVALS][z]
            if (z>1) and (z < 8):
                self.assertEqual(y, 1, "x=%f y=%f" % (z, y))
            else:
                self.assertEqual(y, 0)

    def test_005(self):
        logger.info("--- test_005 ----------------------------------")
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        
        def argFunc(owner, transact):
            return random.randint(1, 8)
        tbl = Table(m, tableName="table_stat", argFunc=argFunc, limitUpFirst=2, widthInt=1, countInt=8)
        timeCreated = 0
        while timeCreated < 1000:
            t = Transact(None, timeCreated, priority=0)
            # t[P1]=0.1
            tbl.handleTransact(t, coef=1)
            timeCreated += 1
        logger.info(tbl.table2str())

    def test_006(self):
        logger.info("--- test_006 ----------------------------------")
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        def argFunc(owner, transact):
            return random.randint(1, 2)
        tbl = Table(m, tableName="table_stat", argFunc=argFunc, limitUpFirst=2, widthInt=1, countInt=1)
        timeCreated = 0
        while timeCreated < 1000:
            t = Transact(None, timeCreated, priority=0)
            # t[P1]=0.1
            tbl.handleTransact(t, coef=1)
            timeCreated += 1
        logger.info(tbl.table2str())

if __name__ == '__main__':
    unittest.main(module="test_table")
