# #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import logger
from pyss.pyss_const import *
from pyss.storage import Storage
from pyss import pyss_model
from pyss.transact import Transact
from pyss import pyssobject

class TestStorage(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Storage(None, storageName=STORAGE_NAME, storageSize=0, initBusySize=0)

    def test_init_002(self):
        m = pyss_model.PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        #
        Storage(m, storageName=STORAGE_NAME, storageSize=2, initBusySize=0)  
    
    # @unittest.skip("skip test_001")
    def test_001(self):
        """
        Попытка создать МКУ с <1 каналом           
        """
        
        logger.info("--- test_001 ----------------------------------")

        # Модель
        m = pyss_model.PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        #
        STORAGE_NAME = "S_1"
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Storage(m, storageName=STORAGE_NAME, storageSize=0, initBusySize=0)

        self.assertTrue('arg is bad' in context.exception)
        
        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Storage(m, storageName=STORAGE_NAME, storageSize=None, initBusySize=0)

        self.assertTrue('arg is bad' in context.exception)        

        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Storage(m, storageName="", storageSize=1, initBusySize=0)

        self.assertTrue('arg is bad' in context.exception)

        with self.assertRaises(pyssobject.ErrorIsTrue) as context:
            Storage(m, storageName=STORAGE_NAME, storageSize=4, initBusySize=5)

        self.assertTrue('arg is bad' in context.exception)  

    def test_002(self):
        """
        Попытка создать МКУ с <1 каналом           
        """
        
        logger.info("--- test_001 ----------------------------------")

        # Модель
        m = pyss_model.PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        #
        STORAGE_NAME = "S_1"
        Storage(m, storageName=STORAGE_NAME, storageSize=5, initBusySize=0)
        
        with self.assertRaises(pyssobject.ErrorKeyExists) as context:
            Storage(m, storageName=STORAGE_NAME, storageSize=3, initBusySize=0)

        self.assertTrue('Key exists: [S_1]' in context.exception)        

    def test_101(self):
        logger.info("--- test_001 ----------------------------------")
        #
        m = pyss_model.PyssModel(optionz=None)
        t = Storage(m, storageName="S_1", storageSize=3)
        
        logger.info("STORAGE_NAME=%s" % t[STORAGE_NAME])
        expected = "S_1"
        self.assertEqual(t[STORAGE_NAME], expected)
        #
        expected = 3
        self.assertEqual(t[S], expected)
        expected = 0
        self.assertEqual(t[BUSY_SIZE], expected)
        # self[R] = self[S] #$j – свободная емкость памяти j;
        expected = 3
        self.assertEqual(t[R], expected)
        # self[SR] = 0.0 #$j – коэффициент использования памяти j;
        expected = 0
        self.assertEqual(t[SR], expected)

        # self[SM] = 0 #$j – максимальное заполнение памяти j;
        expected = 0
        self.assertEqual(t[SM], expected)

        # self[SA] = 0 #$j – среднее заполнение памяти j;
        expected = 0
        self.assertEqual(t[SA], expected)

        # self[SC] = 0 #$j – число входов в память j;
        expected = 0
        self.assertEqual(t[SC], expected)

        # self[ST] = 0 #$j – среднее время пребывания транзакта в памяти j.
        expected = 0
        self.assertEqual(t[ST], expected)

        # Память имеет также стандартные логические атрибуты,
        # которые используются для проверки состояния памяти:
        # self[SE] = True #$j – память j пуста;
        expected = True
        self.assertEqual(t[SE], expected)

        # self[NE] = not self[SE] #$j – память j не пуста;
        expected = False
        self.assertEqual(t[NE], expected)

        # self[SF] = False #$j – память j заполнена;
        expected = False
        self.assertEqual(t[SF], expected)

        # self[SNF] = not t[SF] #$j – память j не заполнена.
        expected = True
        self.assertEqual(t[SNF], expected)

        # self[DATA]=StatisticalSeries()

    def test_102(self):
        logger.info("--- test_002 ----------------------------------")
        #
        m = pyss_model.PyssModel(optionz=None)
        t = Storage(m, storageName="S_1", storageSize=3)

        logger.info("STORAGE_NAME=%s" % t[STORAGE_NAME])
        expected = "S_1"
        self.assertEqual(t[STORAGE_NAME], expected)
        #
        with self.assertRaises(Exception):
            t.enter(transact=None, busySize=0)
            logger.info("storage=%s" % str(t))

    def test_103(self):
        logger.info("--- test_003 ----------------------------------")
        #
        m = pyss_model.PyssModel(optionz=None)
        t = Storage(m, storageName="S_1", storageSize=3)

        logger.info("STORAGE_NAME=%s" % t[STORAGE_NAME])
        expected = "S_1"
        self.assertEqual(t[STORAGE_NAME], expected)
        #
        with self.assertRaises(Exception):
            t.enter(transact=None, busySize=5)
            logger.info("storage=%s" % str(t))

    def test_104(self):
        logger.info("--- test_004 ----------------------------------")
        #
        m = pyss_model.PyssModel(optionz=None)
        t = Storage(m, storageName="S_1", storageSize=3)

        logger.info("STORAGE_NAME=%s" % t[STORAGE_NAME])
        expected = "S_1"
        self.assertEqual(t[STORAGE_NAME], expected)
        #
        m.setCurrentTime(0)
        transact = Transact(None, timeCreated=m[CURRENT_TIME], priority=0)
        t.enter(transact=transact, busySize=1, currentTime=m[CURRENT_TIME])
        logger.info("enter transact=%s" % repr(transact))
        logger.info("storage=%s" % repr(t))
        #
        expected = 3
        self.assertEqual(t[S], expected)
        expected = 1
        self.assertEqual(t[BUSY_SIZE], expected)
        # self[R] = self[S] #$j – свободная емкость памяти j;
        expected = 2
        self.assertEqual(t[R], expected)
        # self[SM] = 0 #$j – максимальное заполнение памяти j;
        expected = 1
        self.assertEqual(t[SM], expected)
        # self[SC] = 0 #$j – число входов в память j;
        expected = 1
        self.assertEqual(t[SC], expected)
        # Память имеет также стандартные логические атрибуты,
        # которые используются для проверки состояния памяти:
        # self[SE] = True #$j – память j пуста;
        expected = False
        self.assertEqual(t[SE], expected)
        # self[NE] = not self[SE] #$j – память j не пуста;
        expected = True
        self.assertEqual(t[NE], expected)
        # self[SF] = False #$j – память j заполнена;
        expected = False
        self.assertEqual(t[SF], expected)
        # self[SNF] = not t[SF] #$j – память j не заполнена.
        expected = True
        self.assertEqual(t[SNF], expected)
        #
        m[CURRENT_TIME] = 1.0
        t.leave(transact=transact, busySize=1, currentTime=m[CURRENT_TIME])
        logger.info("leave transact=%s" % repr(transact))
        t.recalc(m[CURRENT_TIME])
        # self[SR] = 0.0 #$j – коэффициент использования памяти j;
        expected = 0.3333333333333333
        self.assertAlmostEqual(t[SR], expected, places=4)
        # self[SA] = 0 #$j – среднее заполнение памяти j;
        expected = 1.0
        self.assertEqual(t[SA], expected)
        #
        # self[ST] = 0 #$j – среднее время пребывания транзакта в памяти j.
        expected = 1.0
        self.assertEqual(t[ST], expected)

        # Память имеет также стандартные логические атрибуты,
        # которые используются для проверки состояния памяти:
        # self[SE] = True #$j – память j пуста;
        expected = True
        self.assertEqual(t[SE], expected)

        # self[NE] = not self[SE] #$j – память j не пуста;
        expected = False
        self.assertEqual(t[NE], expected)

        # self[SF] = False #$j – память j заполнена;
        expected = False
        self.assertEqual(t[SF], expected)

        # self[SNF] = not t[SF] #$j – память j не заполнена.
        expected = True
        self.assertEqual(t[SNF], expected)

if __name__ == '__main__':
    unittest.main(module="test_storage")
