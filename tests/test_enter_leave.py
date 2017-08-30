# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=line-too-long,missing-docstring,bad-whitespace

import sys
import os
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.generate import Generate
from pyss.terminate import Terminate
from pyss import logger
from pyss.pyss_model import PyssModel
from pyss.segment import Segment 
from pyss.table import Table
from pyss.handle import Handle
from pyss.enter import Enter
from pyss.leave import Leave
from pyss.storage import Storage
from pyss import pyssobject
from pyss.advance import Advance
from pyss.pyss_const import *

class TestEnterLeave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_enter_leave_001(self):
        """
        Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Захват 2-х канального устройства (МКУ)
        Обработка 4 единицы времени
        
        Состояния транзактов:
            t[NUM]==1:
                [{START:1.0, STATE=ACTIVED},
                 {START:5.0, STATE=TRANSACT_DELETED}]
            
            t[NUM]==2:
                [{START:2.0, STATE=ACTIVED},
                 {START:6.0, STATE=TRANSACT_DELETED}]

            t[NUM]==3:
                [{START:3.0, STATE=ACTIVED},
                 {START:3.0, STATE=DELAYED},
                 {START:5.0, STATE=ACTIVED},
                 {START:9.0, STATE=TRANSACT_DELETED}]
        
        Состояния МКУ:
            [{START:0.0, STATE=0},
            {START:0.0, STATE=1}, захват первый 
            {START:1.0, STATE=2}, захват второй 
            {START:4.0, STATE=1}, освобождение первый 
            {START:4.0, STATE=2}, захват третий 
            {START:5.0, STATE=1}, освобождение второй
            {START:8.0, STATE=0}
            ]
          
        """
        
        logger.info("--- test_enter_leave_001 ----------------------------------")
        
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        
        # storage, 2 канала
        S_1 = "S_1"
        storage_1 = Storage(m, storageName=S_1, storageSize=2)

        ### FOR TEST -----------------------------------------------------
        list_all_transact = []
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        ### MODEL ----------------------------
        # Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Generate(sgm, med_value=None, modificatorFunc=[1, 2, 3], max_amount=None)
        # test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        Enter(sgm, storageName=S_1, funcBusySize=1)
        Advance(sgm, meanTime=4, modificatorFunc=None)
        Leave(sgm, storageName=S_1, funcBusySize=1)
        Terminate(sgm, deltaTerminate=1)

        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=MAX_TIME)

        ### ТЕСТЫ ----------------------
        for t in list_all_transact: 
            if t[NUM] == 1:
                print "--- 1"
                print t[LIFE_TIME_LIST]
                expected = [{'start': 1, 'state': 'actived'},
                           {'start': 5, 'state': 'deleted'}]
                self.assertListEqual(expected,
                                     t[LIFE_TIME_LIST])
            elif t[NUM] == 2:
                print "--- 2"
                print t[LIFE_TIME_LIST]
                expected = [{'start': 2, 'state': 'actived'},
                            {'start': 6, 'state': 'deleted'}]
                self.assertListEqual(expected,
                                     t[LIFE_TIME_LIST])
            elif t[NUM] == 3:
                print "--- 3"
                print t[LIFE_TIME_LIST]
                expected = [{'start': 3, 'state': 'actived'},
                            {'start': 3, 'state': 'delayed'},
                            {'start': 5, 'state': 'actived'},
                            {'start': 9, 'state': 'deleted'}]

                self.assertListEqual(expected,
                                     t[LIFE_TIME_LIST])
        # состояния МКУ
        logger.info(str(storage_1[LIFE_TIME_LIST]))
        expected = [{'start': 0, 'state': 0},
                    {'start': 1, 'state': 1},  # захват 1
                    {'start': 2, 'state': 2},  # захват 2
                    {'start': 5, 'state': 1},  # освоб 1
                    {'start': 5, 'state': 2},  # захват 3
                    {'start': 6, 'state': 1},  # освоб 2
                    {'start': 9, 'state': 0}]


        self.assertListEqual(expected,
                             storage_1[LIFE_TIME_LIST])
        
        s=sgm.strBlocks()
        self.assertEqual(s, "[1]:[GENERATE]; [2]:[HANDLE]; [3]:[ENTER]; [4]:[ADVANCE]; [5]:[LEAVE]; [6]:[TERMINATE]")
        
if __name__ == '__main__':
    unittest.main(module="test_enter_leave")
