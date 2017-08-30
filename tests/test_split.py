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
from pyss import logger
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.assign import Assign
from pyss.storage import Storage
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
from pyss.pyss_const import *

class TestEnterLeave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Split(None, funcCountCopies=2, funcNextBlockLabel="A", paramName=P1)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Split(sgm, funcCountCopies=2, funcNextBlockLabel="A", paramName=P1)

    def test_001(self):
        """
        Создаётся один транзакт.
        При проходе через блок split создаётся одна копия транзакта.
        Копия транзакта движется в следующий блок.

        """

        logger.info("--- test_001 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20

        #
        list_all_transact = []

        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        ### SEGMENT ----------------------
        Generate(sgm, modificatorFunc=[0])
        # sgm.addBlock(advance.Advance())
        COPY_NUM = "COPY_NUM"
        Split(sgm, funcCountCopies=1, funcNextBlockLabel=None, paramName=COPY_NUM)
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        Terminate(sgm, deltaTerminate=1)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)

        # ТЕСТЫ ----------------------
        parentTransact = None
        for i, t in enumerate(list_all_transact):
            if i == 0:
                parentTransact = t
                self.assertTrue(COPY_NUM not in t)
                self.assertEqual(t[ASSEMBLY_SET], 1)
                self.assertEqual(t[PARENT], None)
                self.assertEqual(t.strTrack(),
                                 '[0]:[1]:[GENERATE]; [0]:[2]:[SPLIT]; [0]:[3]:[HANDLE]; [0]:[4]:[TERMINATE]')

            elif i == 1:
                self.assertTrue(COPY_NUM in t)
                self.assertEqual(t[COPY_NUM], 1)
                self.assertEqual(t[NUM], 2)
                self.assertEqual(t[ASSEMBLY_SET], parentTransact[NUM])  # pylint: disable=unsubscriptable-object
                self.assertEqual(t[PARENT], parentTransact)
                self.assertEqual(t[TIME_CREATED], 0)
                self.assertEqual(t.strTrack(),
                                 "[0]:[3]:[HANDLE]; [0]:[4]:[TERMINATE]")


    def test_002(self):
        """
        Создаётся один транзакт.
        Задерживается на 3 единицы времени.
        При проходе через блок split создаётся одна копия транзакта.
        Копия транзакта движется в следующий блок.
        Время создания копии - 3.
        Родитель - транзакт 1.
        И т.д.

        """

        logger.info("--- test_002 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        list_all_transact = []

        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        ### SEGMENT ----------------------

        Generate(sgm, modificatorFunc=[0])
        Advance(sgm, meanTime=3)
        COPY_NUM = "COPY_NUM"
        Split(sgm, funcCountCopies=1, funcNextBlockLabel=None, paramName=COPY_NUM)
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        Terminate(sgm, deltaTerminate=1)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)

        # ТЕСТЫ ----------------------
        parentTransact = None
        for i, t in enumerate(list_all_transact):
            if i == 0:
                parentTransact = t
                self.assertTrue(COPY_NUM not in t)
                self.assertEqual(t[ASSEMBLY_SET], 1)
                self.assertEqual(t[PARENT], None)
                self.assertEqual(t.strTrack(),
                                 "[0]:[1]:[GENERATE]; [0]:[2]:[ADVANCE]; [3]:[3]:[SPLIT]; [3]:[4]:[HANDLE]; [3]:[5]:[TERMINATE]")

            elif i == 1:
                self.assertTrue(COPY_NUM in t)
                self.assertEqual(t[COPY_NUM], 1)
                self.assertEqual(t[NUM], 2)
                self.assertEqual(t[ASSEMBLY_SET], parentTransact[NUM])  # pylint: disable=unsubscriptable-object
                self.assertEqual(t[PARENT], parentTransact)
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t.strTrack(), "[3]:[4]:[HANDLE]; [3]:[5]:[TERMINATE]")

    def test_003(self):
        """
        Создаётся один транзакт.
        Задерживается на 3 единицы времени.
        При проходе через блок split создаётся одна копия транзакта.
        Копия транзакта движется в блок с меткой ALTERNATIVE.
        Транзакт-родитель переходит в следующий блок.
        Время создания копии - 3.
        Родитель - транзакт 1.
        И т.д.

        """

        logger.info("--- test_003 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()
        m[OPTIONS].printResult = True

        MAX_TIME = 20
        #
        list_all_transact = []

        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        ### MODEL ----------------------

        Generate(sgm, modificatorFunc=[0])
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #

        Advance(sgm, meanTime=3)
        COPY_NUM = "COPY_NUM"
        ALTERNATIVE = "ALTER"
        Split(sgm, funcCountCopies=1, funcNextBlockLabel=ALTERNATIVE, paramName=COPY_NUM)
        
        # здесь только родитель
        # for test
        MY_PARENT = "my_parent"
        def handlerFunc(o, t):
            t[MY_PARENT] = None
        Handle(sgm, handlerFunc=handlerFunc)
        #
        
        Terminate(sgm, deltaTerminate=1)
        # for test
        Handle(sgm, label=ALTERNATIVE, handlerFunc=funcTransactTo_list_all_transact)
        Terminate(sgm, deltaTerminate=1)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)

        # ТЕСТЫ ----------------------
        parentTransact = None
        for i, t in enumerate(list_all_transact):
            if i == 0:
                self.assertTrue(MY_PARENT in t, "MY_PARENT in t")
                    
                parentTransact = t
                self.assertTrue(COPY_NUM not in t)
                # родитель получает ASSEMBLY_SET равный NUM
                self.assertEqual(t[ASSEMBLY_SET], 1)
                self.assertEqual(t[ASSEMBLY_SET], t[NUM])
                self.assertEqual(t[PARENT], None)
                self.assertEqual(t.strTrack(),
                                 "[0]:[1]:[GENERATE]; [0]:[2]:[HANDLE]; [0]:[3]:[ADVANCE]; [3]:[4]:[SPLIT]; [3]:[5]:[HANDLE]; [3]:[6]:[TERMINATE]")

            elif i == 1:
                self.assertTrue(MY_PARENT not in t, "MY_PARENT in t")
                self.assertTrue(COPY_NUM in t)
                self.assertEqual(t[COPY_NUM], 1)
                self.assertEqual(t[NUM], 2)
                self.assertEqual(t[ASSEMBLY_SET], parentTransact[NUM])  # pylint: disable=unsubscriptable-object
                self.assertEqual(t[PARENT], parentTransact)
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t.strTrack(), 
                                 "[3]:[ALTER]:[HANDLE]; [3]:[8]:[TERMINATE]")

    def test_004(self):
        """
        Создаётся один транзакт.
        Задерживается на 3 единицы времени.
        При проходе через блок split создаётся одна копия транзакта.
        Копия транзакта движется в блок с меткой вычисленной функцией alter.
        Время создания копии - 3.
        Родитель - транзакт 1.
        И т.д.

        """

        logger.info("--- test_004 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()
        #
        list_all_transact = []
        #
        MAX_TIME = 20
        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        ### MODEL ----------------------

        Generate(sgm, modificatorFunc=[0])
        Advance(sgm, meanTime=3)
        COPY_NUM = "COPY_NUM"
        ALTERNATIVE = "ALTER"
        def alter(t):
            return ALTERNATIVE
        Split(sgm, funcCountCopies=1, funcNextBlockLabel=alter, paramName=COPY_NUM)
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        Terminate(sgm, deltaTerminate=1)
        Terminate(sgm, deltaTerminate=1, label=ALTERNATIVE)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)

        # ТЕСТЫ ----------------------
        parentTransact = None
        for i, t in enumerate(list_all_transact):
            if i == 0:
                parentTransact = t
                self.assertTrue(COPY_NUM not in t)
                self.assertEqual(t[ASSEMBLY_SET], 1)
                self.assertEqual(t[PARENT], None)
                self.assertEqual(t.strTrack(),
                                 "[0]:[1]:[GENERATE]; [0]:[2]:[ADVANCE]; [3]:[3]:[SPLIT]; [3]:[4]:[HANDLE]; [3]:[5]:[TERMINATE]")

            elif i == 1:
                self.assertTrue(COPY_NUM in t)
                self.assertEqual(t[COPY_NUM], 1)
                self.assertEqual(t[NUM], 2)
                self.assertEqual(t[ASSEMBLY_SET], parentTransact[NUM])  # pylint: disable=unsubscriptable-object
                self.assertEqual(t[PARENT], parentTransact)
                self.assertEqual(t[TIME_CREATED], 3)
                self.assertEqual(t.strTrack(), "[3.000000]:[6]:[HANDLE]; [3.000000]:[ALTERNATIVE]:[TERMINATE]")



if __name__ == '__main__':
    unittest.main(module="test_split")
