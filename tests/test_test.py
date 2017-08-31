# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import pyssobject
from pyss.pyss_model import PyssModel
from pyss.segment import Segment

from pyss import generate 
from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss import logger
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
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
from pyss.test import Test
from pyss.pyss_const import *

class TestTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_001(self):
        #
        with self.assertRaises(pyssobject.ErrorIsNone) as context:
            Test(None, funcCondition=lambda o, t: True, move2block=None)

    def test_init_002(self):
        m = PyssModel(optionz=None)
        m[OPTIONS].setAllFalse()
        sgm = Segment(m)
        #
        Test(sgm, funcCondition=lambda o, t: True, move2block=None)

    # @
    # -unittest.skip("show only test_002")
    def test_001(self):
        """
        
        Функция проверки условия запрещает вход транзакту с NUM равным 2 в блок Test до тех пор,
        пока через блок не пройдёт транзакт с NUM равным 3.
        Остальные транзакты проходят транзитом.
        
        Первый транзакт появился в модели в момент 0, исключён из модели в момент 0.
        Второй транзакт появился в модели в момент 1, исключён из модели в момент 2.
        Третий транзакт появился в модели в момент 2, исключён из модели в момент 2.
        
        """
        
        logger.info("--- test_001 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 10

        #
        list_all_transact = []

        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)
        
        # исходное состояние, переменная модели с названием "транзакт №3 прошёл блок Test"
        m.variables["транзакт №3 прошёл блок Test"] = False
        # функция проверки условия
        def checkTest(o, transact):
            if transact[NUM] == 2:
                return m.variables["транзакт №3 прошёл блок Test"]
            elif transact[NUM] == 3:
                m.variables["транзакт №3 прошёл блок Test"] = True
            return True
                
        ### SEGMENT ----------------------------

        # генерится максимум 3 заявки с интервалом 1
        Generate(sgm, med_value=1, modificatorFunc=None, max_amount=3)
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #        
        # .addBlock(bprint_blocks.buildBprintCurrentTime(strFormat="=== Time: [%.12f]"))
        Test(sgm, funcCondition=checkTest, move2block=None, label=None)
        Terminate(sgm, deltaTerminate=1, label=None)

        #
        m.start(terminationCount=3, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        for t in list_all_transact:
            if t[NUM] == 1:
                self.assertEqual(t.strTrack(), "[0]:[1]:[GENERATE]; [0]:[2]:[HANDLE]; [0]:[3]:[TEST]; [0]:[4]:[TERMINATE]")
            elif t[NUM] == 2:
                self.assertEqual(t.strTrack(), "[1]:[1]:[GENERATE]; [1]:[2]:[HANDLE]; [2]:[2]:[HANDLE]; [2]:[3]:[TEST]; [2]:[4]:[TERMINATE]")
            elif t[NUM] == 3:
                self.assertEqual(t.strTrack(), "[2]:[1]:[GENERATE]; [2]:[2]:[HANDLE]; [2]:[3]:[TEST]; [2]:[4]:[TERMINATE]")
        
    # @unittest.skip("show only test_002")
    def test_002(self):
        """Демонстрация работы блока Test
        
        Функция проверки условия направляет транзакт с NUM равным 2 в блок с меткой "ALT"
        Остальные транзакты проходят транзитом.
        
        Первый транзакт появился в модели в момент 0, исключён из модели в момент 0.
        Второй транзакт появился в модели в момент 1, исключён из модели в момент 6.
        Третий транзакт появился в модели в момент 2, исключён из модели в момент 2.        
        
        """
        
        logger.info("--- test_002 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 10

        #
        list_all_transact = []

        # for test
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)
        
        # функция проверки условия
        def checkTest(o, transact):
            # направляет транзакт с NUM равным 2 в блок с меткой "ALT"
            if transact[NUM] in [2]:
                return False
            else:
                return True
                
        # model
        LABEL_TERMINATE = "TERMINATE"
        LABEL_ALT = "ALT"
        
        # генерится максимум 3 заявки с интервалом 1
        Generate(sgm, med_value=1, modificatorFunc=None, max_amount=3)
        # for test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #        
        # направляет транзакт с NUM равным 2 в блок с меткой "ALT"
        Test(sgm, funcCondition=checkTest, move2block=LABEL_ALT, label=None)
        Terminate(sgm, deltaTerminate=1, label=LABEL_TERMINATE)        
        
        # ------------------------------------------------
        # ----- ветвь маршрута ALT
        Advance(sgm, meanTime=5, modificatorFunc=None, label=LABEL_ALT)
        # направлять все транзакты на блок с меткой "TERMINATE"
        Transfer(sgm, funcTransfer=lambda o, t: o.findBlockByLabel(LABEL_TERMINATE), label=None)
        #
        m.start(terminationCount=3, maxTime=MAX_TIME)
        
        # ТЕСТЫ ----------------------
        for t in list_all_transact:
            if t[NUM] == 1:
                self.assertEqual(t.strTrack(), "[0]:[1]:[GENERATE]; [0]:[2]:[HANDLE]; [0]:[3]:[TEST]; [0]:[TERMINATE]:[TERMINATE]")
            elif t[NUM] == 2:
                self.assertEqual(t.strTrack(), "[1]:[1]:[GENERATE]; [1]:[2]:[HANDLE]; [1]:[3]:[TEST]; [1]:[ALT]:[ADVANCE]; [6]:[6]:[TRANSFER]; [6]:[TERMINATE]:[TERMINATE]")
            elif t[NUM] == 3:
                self.assertEqual(t.strTrack(), "[2]:[1]:[GENERATE]; [2]:[2]:[HANDLE]; [2]:[3]:[TEST]; [2]:[TERMINATE]:[TERMINATE]")
                
                
if __name__ == '__main__':
    unittest.main(module="test_test")
