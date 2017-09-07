# #!/usr/bin/python
# -*- coding: utf-8 -*-

# test_preempt_return.py

# pylint: disable=line-too-long,missing-docstring,bad-whitespace, unused-argument, too-many-locals

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
from pyss.storage import Storage
from pyss.advance import Advance
from pyss.preempt import Preempt
from pyss.g_return import GReturn
from pyss.facility import Facility
from pyss.seize import Seize
from pyss.release import Release
from pyss.transfer import Transfer
from pyss.test import Test
from pyss.pyss_const import *

class TestPreemptReturn(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("testing skipping test_preempt_return_001")
    def test_preempt_return_001(self):
        """Тест Preempt - Return

        Формируется один транзакт в момент времени 1.
        Прерывает работу устройства F_1 на 5 единиц времени.
        Выходит из модели в момент времени 6.
        """

        logger.info("--- test_preempt_return_001 ----------------------------------")

        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20

        #
        list_all_transact = []
        #
        MAX_TIME = 20
        #
        F_1 = "F_1"
        # ОКУ
        Facility(m, facilityName=F_1)
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)
        ### SEGMENT ----------------------------

        # формируется одна заявка в момент времени 1
        Generate(sgm, med_value=None,
                 modificatorFunc=None,
                 first_tx=1,
                 max_amount=1)
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(F_1, t[FACILITY]))
        #
        Preempt(sgm, facilityName=F_1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertIn(F_1, t[FACILITY]))
        #
        Advance(sgm, meanTime=5, modificatorFunc=None)
        GReturn(sgm, facilityName=F_1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:not self.assertNotIn(F_1, t[FACILITY]))
        #
        Terminate(sgm, deltaTerminate=0)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)

        # ТЕСТЫ ----------------------
        for t in list_all_transact:
            self.assertEqual(t[TIME_CREATED], 1)
            self.assertEqual(t[TERMINATED_TIME], 6)
            print str(["%s:%s" % (k, t[k])
                       for k in t.keys() if k
                       in [TIME_CREATED, TERMINATED_TIME]])

    # @unittest.skip("testing skipping test_preempt_return_002")
    def test_preempt_return_002(self):
        """Тест Preempt - Return

        Формируется транзакт A в момент времени 1.
        Идёт на обработку устройством F_1 в течение 3 единиц времени.
        Формируется транзакт B в момент времени 2.
        Прерывает работу устройства на 5 единиц времени.
        Транзакт B выходит из модели в момент времени 7.
        Транзакт А выходит из модели в момент времени 9.
        Обработка транзакта А была прервана с 2 по 7.

        """

        logger.info("--- test_preempt_return_002 ----------------------------------")
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20

        # CONSTS
        TRANSACT_A = "A"
        TRANSACT_B = "B"
        #
        list_all_transact = []
        tA = []
        tB = []
        #
        F_1 = "F_1"
        # ОКУ
        facility_1 = Facility(m, facilityName=F_1)
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        def setTransactLabel(owner, transact):
            if transact[NUM] == 1:
                transact[LABEL] = TRANSACT_A
                tA.append(transact)
            elif transact[NUM] == 2:
                transact[LABEL] = TRANSACT_B
                tB.append(transact)

        # функция проверки условия
        def checkTest(o):
            t=m.getCurrentTransact()
            if t[LABEL] == TRANSACT_B:
                return False
            return True

        def printAllTransact(owner, transact):
            print "Time=%s" % str(m.getCurTime())
            print "\n".join([str(t) for t in list_all_transact])
            print "tA=%s" % str(tA[0])
            print "tB=%s" % str(tB[0])

        ### SEGMENT ----------------------------
        # формируется одна заявка в момент времени 1
        Generate(sgm,
                 med_value=1,
                 modificatorFunc=None,
                 first_tx=1,
                 max_amount=2)
        # вспомогательные операции
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        Handle(sgm, handlerFunc=setTransactLabel)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(F_1, t[FACILITY]))
        #
        # первый транзакт проходит, второй направляется к метке "to_preempt"
        Test(sgm, funcCondition=checkTest, move2block="to_preempt")
        # только первый транзакт
        Seize(sgm, facilityName=F_1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertIn(F_1, t[FACILITY]))
        #
        Advance(sgm, meanTime=3, modificatorFunc=None)
        Release(sgm, facilityName=F_1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(F_1, t[FACILITY]))
        #
        Transfer(sgm, funcTransfer=lambda o, t: o.findBlockByLabel("to_term"))
        #---
        # только второй транзакт
        Preempt(sgm, facilityName=F_1, label="to_preempt")
        # test
        # .addBlock(handle.Handle(handlerFunc=lambda o,t:self.assertEqual(tA[0][REMAIND_TIME], None)))
        Handle(sgm, handlerFunc=printAllTransact)
        Handle(sgm, handlerFunc=lambda o, t:self.assertIn(F_1, t[FACILITY]))
        #
        Handle(sgm, handlerFunc=printAllTransact)
        Advance(sgm, meanTime=5, modificatorFunc=None)
        GReturn(sgm, facilityName=F_1)
        # test
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(tA[0][REMAIND_TIME], 2))
        Handle(sgm, handlerFunc=lambda o, t:self.assertEqual(tA[0][SCHEDULED_TIME], 9))
        Handle(sgm, handlerFunc=lambda o, t:self.assertNotIn(F_1, t[FACILITY]))
        #
        Handle(sgm, handlerFunc=printAllTransact)
        # все транзакты
        Terminate(sgm, label="to_term", deltaTerminate=0)

        # ЗАПУСК ----------------------
        m.start(terminationCount=MAX_TIME, maxTime=MAX_TIME)
        # ТЕСТЫ ----------------------
        for t in list_all_transact:
            # Формируется транзакт A в момент времени 1.
            # Идёт на обработку устройством F_1 в течение 3 единиц времени.
            # Формируется транзакт B в момент времени 2.
            # Прерывает работу устройства на 5 единиц времени.
            # Транзакт B выходит из модели в момент времени 7.
            # Транзакт А выходит из модели в момент времени 9.
            # Обработка транзакта А была прервана с 2 по 7.
            print str(["%s:%s" % (k, t[k])
                       for k in t.keys() if k
                       in [TIME_CREATED, TERMINATED_TIME, LIFE_TIME_LIST]])
            if t[LABEL] == TRANSACT_A:
                self.assertEqual(t[TIME_CREATED], 1)
                self.assertEqual(t[REMAIND_TIME], 2)
                self.assertEqual(t[TERMINATED_TIME], 9)
                self.assertListEqual(t[LIFE_TIME_LIST], [
                    {'start': 1, 'state': 'actived'},
                    {'start': 2, 'state': 'preempted'},
                    {'start': 7, 'state': 'actived'},
                    {'start': 9, 'state': 'deleted'}])


            elif t[LABEL] == TRANSACT_B:
                self.assertEqual(t[TIME_CREATED], 2)
                self.assertEqual(t[TERMINATED_TIME], 7)
                self.assertListEqual(t[LIFE_TIME_LIST], [
                    {'start': 2, 'state': 'actived'},
                    {'start': 7, 'state': 'deleted'}])

if __name__ == '__main__':
    unittest.main(module="test_preempt_return")
