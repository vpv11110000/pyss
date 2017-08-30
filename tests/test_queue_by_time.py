##!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import random
import unittest


DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import generate
from pyss import terminate
from pyss import logger
from pyss import pyssobject
from pyss import counterdec
from pyss import pyss_model
from pyss import segment
from pyss import table
from pyss import tabulate
from pyss import seize
from pyss import release
from pyss import advance
from pyss import queue
from pyss import depart
from pyss import options
from pyss import bprint_blocks
from pyss import qtable
from pyss import queue_event_by_time
from pyss.transact import Transact
from pyss.pyss_const import *

#DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))+"/"
#sys.path.append(DIRNAME_MODULE)

class TestQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #@
    #unittest.skip("testing skipping test_queue_001")
    def test_queue_by_time_001(self):
        logger.info("--- test_queue_by_time_001 ----------------------------------")
        #
        q = queue_event_by_time.QueueEventByTime()
        #
        self.assertTrue(q.isEmpty())
        tm=1
        t1 = Transact(block=None, timeCreated=tm, priority=0).setScheduledTime(tm)
        q.put(t1)
        self.assertFalse(q.isEmpty())
        q.clear()
        
        self.assertTrue(q.isEmpty())
        q.put(t1)
        
        tm=2
        t2 = Transact(block=None, timeCreated=tm, priority=0).setScheduledTime(tm)
        q.put(t2)
        self.assertFalse(q.isEmpty())
        self.assertEqual(len(q.transactList), 2)
        t=q.first()
        self.assertEqual(t1, t)
        q.remove(t)
        self.assertEqual(len(q.transactList), 1)
        t=q.first()
        self.assertEqual(t2, t)
        q.remove(t)
        self.assertTrue(q.isEmpty())
        q.put(t2)
        q.put(t1)
        t=q.first()
        self.assertEqual(t1, t)
        q.remove(t)
        self.assertEqual(len(q.transactList), 1)
        t=q.first()
        self.assertEqual(t2, t)
        q.remove(t)
        self.assertTrue(q.isEmpty())
        
    def test_queue_by_time_002(self):
        logger.info("--- test_queue_by_time_002 ----------------------------------")
        #
        q = queue_event_by_time.QueueEventByTime(reverse=True)
        #
        self.assertTrue(q.isEmpty())
        tm=1
        t1 = Transact(block=None, timeCreated=tm, priority=0).setScheduledTime(tm)
        q.put(t1)
        self.assertFalse(q.isEmpty())
        q.clear()
        
        self.assertTrue(q.isEmpty())
        q.put(t1)
        
        tm=2
        t2 = Transact(block=None, timeCreated=tm, priority=0).setScheduledTime(tm)
        q.put(t2)
        self.assertFalse(q.isEmpty())
        self.assertEqual(len(q.transactList), 2)
        t=q.first()
        self.assertEqual(t2, t)
        q.remove(t)
        self.assertEqual(len(q.transactList), 1)
        t=q.first()
        self.assertEqual(t1, t)
        q.remove(t)
        self.assertTrue(q.isEmpty())
        q.put(t2)
        q.put(t1)
        t=q.first()
        self.assertEqual(t2, t)
        q.remove(t)
        self.assertEqual(len(q.transactList), 1)
        t=q.first()
        self.assertEqual(t1, t)
        q.remove(t)
        self.assertTrue(q.isEmpty())        
        
if __name__ == '__main__':
    unittest.main(module="test_queue_by_time")
