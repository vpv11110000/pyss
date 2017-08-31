# #!/usr/bin/python
# -*- coding: utf-8 -*-

# test_queue_depart.py

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
from pyss.pyss_const import *


# DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))+"/"
# sys.path.append(DIRNAME_MODULE)


class TestQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("testing skipping test_001")
    def test_001(self):
        """Тест Queue - Depart

        Очередь инициализирована значением 7.
        Формируются транзакты в моменты времени 1, 2, 3.

        Проходят в очередь. Длина очереди увеличивается на значение атрибута NUM транзакта.
        7+1,7+2,7+3
        Выходят из очереди. Длина очереди уменьшается на значение атрибута NUM транзакта.
        7,7,7
        Выходят из модели в моменты времени 1, 2, 3 без задержек.

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
        #
        Q_1 = "Q_1"
        D_1 = "D_1"

        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)
        def testBlockBefore(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()

            if b[LABEL] == Q_1:
                q = b.getQueueObject()
                # проверка перед входом транзакта в блоки (block.transactHandle)
                # проверка атрибутов блока Queue
                if t[NUM] == 1:
                    # проверка перед входом транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 7)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0)
                elif t[NUM] == 2:
                    # проверка перед входом транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 8)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 1)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
                elif t[NUM] == 3:
                    # проверка перед входом транзакта в Queue
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 9)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 3)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 3)
            elif b[LABEL] == D_1:
                q = b.getQueueObject()
                # проверка атрибутов блока Depart
                if t[NUM] == 1:
                    # проверка перед входом транзакта в Depart

                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 8)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 8)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    # список номеров транзактов и времени постановки в очередь
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "len(q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # первый транзакт поставлен во время 1
                    self.assertEqual(q[LISTTRANSACT][1], 1, "q[LISTTRANSACT][1], 1")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    # список времён нахождения в очереди
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0)
                elif t[NUM] == 2:
                    # проверка перед входом транзакта в Depart

                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 9)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 9)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 1)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1)
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # второй транзакт поставлен во время 2
                    self.assertEqual(q[LISTTRANSACT][2], 2, "q[LISTTRANSACT][2], 2")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
                elif t[NUM] == 3:
                    # проверка перед входом транзакта в Depart

                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 10)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 10)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 1 + 2)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1)
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # третий транзакт поставлен во время 3
                    self.assertEqual(q[LISTTRANSACT][3], 3, "q[LISTTRANSACT][3], 3")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 3)


        # проверка после обработки транзакта в блоки (block.transactHandle)
        def testBlockAfter(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()

            if b[LABEL] == Q_1:
                q = b.getQueueObject()
                # проверка атрибутов блока Queue
                q = b.getQueueObject()
                if t[NUM] == 1:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 8, "q[QUEUE_LENGTH], 8")
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 8, "q[QUEUE_LENGTH_MAX], 8")
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0, "q[ENTRY_ZERO], 0")
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0, "q[STATISTICAL_SERIES].count(), 1")
                elif t[NUM] == 2:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 9)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 9)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 1)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "len(q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
                elif t[NUM] == 3:
                    # проверка после обработки транзакта в Queue
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 10)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 10)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 1 + 2, "q[ENTRY_ZERO], 2")
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "len(q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 3)
            elif b[LABEL] == D_1:
                # блок Depart
                q = b.getQueueObject()
                if t[NUM] == 1:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # блок Depart
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 8)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    # +1 !!! (by t[NUM])
                    self.assertEqual(q[ENTRY_ZERO], 1)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
                elif t[NUM] == 2:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # блок Depart
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 9)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    # +2 !!! (by t[NUM])
                    self.assertEqual(q[ENTRY_ZERO], 1 + 2)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 3)
                elif t[NUM] == 3:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # блок Depart
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1, "q[QUEUE_NAME], Q_1")
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 7, "q[QUEUE_LENGTH], 7")
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 10, "q[QUEUE_LENGTH_MAX], 10")
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    # +3 !!! (by t[NUM])
                    self.assertEqual(q[ENTRY_ZERO], 1 + 2 + 3, "q[ENTRY_ZERO], 1+2+3")
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 0, "q[TIME_MEAN], 0")
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None, "q[TIME_MEAN_WITHOUT_ZERO], None")
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0, "len(q[LISTTRANSACT].keys()), 0")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 6, "q[STATISTICAL_SERIES].count(), 6")

        ### MODEL ----------------------------
        # Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Generate(sgm, med_value=None, modificatorFunc=[1, 2, 3], max_amount=None)
        # test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        def deltaByNUM(o, t):
            return t[NUM]
        Queue(sgm, queueName=Q_1, deltaIncrease=deltaByNUM, initLength=7, label=Q_1)
        #
        Depart(sgm, queueName=Q_1, deltaDecrease=deltaByNUM, label=D_1)
        Terminate(sgm, deltaTerminate=1)

        # test
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)

        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=MAX_TIME)

        ### ТЕСТЫ ----------------------
        for t in list_all_transact:
            if t[NUM] == 1:
                pass

    def test_002(self):
        """Тест Queue - Depart с обработкой

        Очередь инициализирована значением 0.
        Формируются транзакты в моменты времени 1, 2.

        Проходят в очередь. Длина очереди увеличивается на значение атрибута NUM транзакта.
        1,2
        Обрабатываются 1 и 2 соответственно.
        Выходят из очереди. Длина очереди уменьшается на значение атрибута NUM транзакта.
        0,0
        Выходят из модели в моменты времени 2, 4 соответственно.

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
        #
        Q_1 = "Q_1"
        D_1 = "D_1"
        #
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)
        def testBlockBefore(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()

            if b[LABEL] == Q_1:
                q = b.getQueueObject()
                # проверка перед входом транзакта в блоки (block.transactHandle)
                # проверка атрибутов блока Queue
                if t[NUM] == 1:
                    # проверка перед входом транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 0)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 0)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0)
                elif t[NUM] == 2:
                    # проверка перед входом транзакта в Queue
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 0)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 1)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 1.0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], 1.0)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
            elif b[LABEL] == D_1:
                q = b.getQueueObject()
                # проверка атрибутов блока Depart
                if t[NUM] == 1:
                    # проверка перед входом транзакта в Depart

                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 1)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    # список номеров транзактов и времени постановки в очередь
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "len(q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # первый транзакт поставлен во время 1
                    self.assertEqual(q[LISTTRANSACT][1], 1, "q[LISTTRANSACT][1], 1")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    # список времён нахождения в очереди
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0)
                elif t[NUM] == 2:
                    # проверка перед входом транзакта в Depart

                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 2)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 2)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 1.0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], 1.0)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1)
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # второй транзакт поставлен во время 2
                    self.assertEqual(q[LISTTRANSACT][2], 2, "q[LISTTRANSACT][2], 2")
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)


        # проверка после обработки транзакта в блоки (block.transactHandle)
        def testBlockAfter(b):
            d = m.getCurTime()
            t = m.getCurrentTransact()

            if b[LABEL] == Q_1:
                q = b.getQueueObject()
                # проверка атрибутов блока Queue
                q = b.getQueueObject()
                if t[NUM] == 1:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # проверка атрибутов блока Queue
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 1, "q[QUEUE_LENGTH], 1")
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 1, "q[QUEUE_LENGTH_MAX], 1")
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0, "q[ENTRY_ZERO], 0")
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], None)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], None)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 0, "q[STATISTICAL_SERIES].count(), 1")
                elif t[NUM] == 2:
                    # проверка после обработки транзакта в Queue
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 2, "q[QUEUE_LENGTH], 2")
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 2, "q[QUEUE_LENGTH_MAX], 2")
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 1.0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], 1.0)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 1, "len(q[LISTTRANSACT].keys()), 1")
                    self.assertTrue(t[NUM] in q[LISTTRANSACT])
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)

            elif b[LABEL] == D_1:
                # блок Depart
                q = b.getQueueObject()
                if t[NUM] == 1:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # блок Depart
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 0)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 1)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    # +1 !!! (by t[NUM])
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    self.assertEqual(q[TIME_MEAN], 1.0)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertEqual(q[TIME_MEAN_WITHOUT_ZERO], 1.0)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 1)
                elif t[NUM] == 2:
                    # проверка после обработки транзакта в блоки (block.transactHandle)
                    # блок Depart
                    # bl[QUEUE_OBJECT][QUEUE_NAME] - имя объекта (queue.Queue) очереди
                    self.assertEqual(q[QUEUE_NAME], Q_1)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH] - Текущая длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH], 0)
                    # bl[QUEUE_OBJECT][QUEUE_LENGTH_MAX] - Максимальная длина очереди.
                    self.assertEqual(q[QUEUE_LENGTH_MAX], 2)
                    # bl[QUEUE_OBJECT][ENTRY_ZERO] - NOT_IMPLEMENT Число нулевых входов в очередь, при котором время нахождения в очереди равно нулю.
                    # +2 !!! (by t[NUM])
                    self.assertEqual(q[ENTRY_ZERO], 0)
                    # bl[QUEUE_OBJECT][TIME_MEAN] - NOT_IMPLEMENT Среднее время пребывания транзактов в очереди (включая нулевые входы).
                    # (1+2*2) / 3
                    self.assertAlmostEqual(q[TIME_MEAN], float(1 + 2 * 2) / 3, 3)
                    # bl[QUEUE_OBJECT][TIME_MEAN_WITHOUT_ZERO] - NOT_IMPLEMENT Среднее время пребывания сообщения в очереди (без нулевых входов).
                    self.assertAlmostEqual(q[TIME_MEAN_WITHOUT_ZERO], float(1 + 2 * 2) / 3, 3)
                    # bl[QUEUE_OBJECT][QUEUE_MEAN_LENGTH_BY_TIME] - NOT_IMPLEMENT
                    # bl[QUEUE_OBJECT][LISTTRANSACT]
                    self.assertEqual(len(q[LISTTRANSACT].keys()), 0)
                    # bl[QUEUE_OBJECT][STATISTICAL_SERIES] - NOT_IMPLEMENT
                    self.assertEqual(q[STATISTICAL_SERIES].count(), 3)

        ### MODEL ----------------------------
        # Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Generate(sgm, med_value=None, modificatorFunc=[1, 2], max_amount=None)
        # test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        def deltaByNUM(o, t):
            return t[NUM]
        Queue(sgm, queueName=Q_1, deltaIncrease=deltaByNUM, initLength=0, label=Q_1)
        # задержка

        Advance(sgm, meanTime=0, modificatorFunc=lambda o, c: m.getCurrentTransact()[NUM])
        #
        Depart(sgm, queueName=Q_1, deltaDecrease=deltaByNUM, label=D_1)
        Terminate(sgm, deltaTerminate=1)

        # test
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)

        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=50)

        ### ТЕСТЫ ----------------------
        for t in list_all_transact:
            if t[NUM] == 1:
                pass

    def test_003(self):
        """Тест Queue - Depart с обработкой 2,4

        Очередь инициализирована значением 0.
        Формируются транзакты в моменты времени 1, 2, 3, 4, 5, 6.

        Проходят в очередь. Длина очереди увеличивается 1.
        Обрабатываются 4,4,4,2,2,2
        Выходят из очереди. Длина очереди уменьшается на 1.
        Выходят из модели в моменты времени 5,6,7,6,7,8 соответственно.

        Среднее время обработки (4+4+4+2+2+2)/6 = 3

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
        #
        Q_1 = "Q_1"
        D_1 = "D_1"
        #
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)
        def testBlockBefore(b):
            pass

        # проверка после обработки транзакта в блоки (block.transactHandle)
        def testBlockAfter(b):
            pass

        ### MODEL ----------------------------
        # Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Generate(sgm, med_value=None, modificatorFunc=[1, 2, 3, 4, 5, 6], max_amount=None)
        # test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        q = Queue(sgm, queueName=Q_1, deltaIncrease=1, initLength=0, label=Q_1)
        # задержка
        def funcAdv(o, c):
            if m.getCurrentTransact()[NUM] < 4:
                return 4
            else:
                return 2
        Advance(sgm, meanTime=0, modificatorFunc=funcAdv)
        #
        Depart(sgm, queueName=Q_1, deltaDecrease=1, label=D_1)
        Terminate(sgm, deltaTerminate=1)

        # test
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)

        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=MAX_TIME)

        ### ТЕСТЫ ----------------------
        self.assertAlmostEqual(q.getQueueObject()[TIME_MEAN], 3, 3)
        self.assertAlmostEqual(q.getQueueObject()[TIME_MEAN_WITHOUT_ZERO], 3, 3)

        for t in list_all_transact:
            if t[NUM] == 1:
                pass

    def test_004(self):
        """Тест Queue - Depart с обработкой 2,4,0

        Очередь инициализирована значением 0.
        Формируются транзакты в моменты времени 1, 2, 3, 4, 5, 6,7.

        Проходят в очередь. Длина очереди увеличивается 1.
        Обрабатываются 4,4,4,2,2,2,0
        Выходят из очереди. Длина очереди уменьшается на 1.
        Выходят из модели в моменты времени 5,6,7,6,7,8,7 соответственно.

        Среднее время обработки (4+4+4+2+2+2+0)/7 = 2.571
        Среднее время обработки без 0 - (4+4+4+2+2+2)/6 = 3

        """

        logger.info("--- test_001 ----------------------------------")

        # MODEL ----------------------
        ### MODEL ----------------------------------
        m = PyssModel()
        sgm = Segment(m)
        #
        m[OPTIONS].setAllFalse()

        MAX_TIME = 20
        #
        list_all_transact = []
        #
        Q_1 = "Q_1"
        D_1 = "D_1"
        #
        #
        def funcTransactTo_list_all_transact(owner, transact):
            # складируем транзакты в список
            list_all_transact.append(transact)

        # FOR TEST -----------------------------------------------------
        # проверка перед входом транзакта в блоки (block.transactHandle)
        def testBlockBefore(b):
            pass

        # проверка после обработки транзакта в блоки (block.transactHandle)
        def testBlockAfter(b):
            pass

        ### MODEL ----------------------------
        # Формируются транзакты (атрибут NUM [1,2,3]) во времена [1,2,3]
        Generate(sgm, med_value=None, modificatorFunc=[1, 2, 3, 4, 5, 6, 7], max_amount=None)
        # test
        Handle(sgm, handlerFunc=funcTransactTo_list_all_transact)
        #
        q=Queue(sgm, queueName=Q_1, deltaIncrease=1, initLength=0, label=Q_1)
        # задержка
        def funcAdv(o, c):
            if m.getCurrentTransact()[NUM] < 4:
                return 4
            elif m.getCurrentTransact()[NUM] < 7:
                return 2
            else:
                return 0

        Advance(sgm, meanTime=0, modificatorFunc=funcAdv)
        #
        Depart(sgm, queueName=Q_1, deltaDecrease=1, label=D_1)
        Terminate(sgm, deltaTerminate=1)

        # test
        sgm.setOnBeforeBlock(testBlockBefore)
        sgm.setOnAfterBlock(testBlockAfter)

        ### ЗАПУСК ----------------------
        m.start(terminationCount=20, maxTime=50)

        ### ТЕСТЫ ----------------------
        self.assertAlmostEqual(q.getQueueObject()[TIME_MEAN], 2.571, 3)
        self.assertAlmostEqual(q.getQueueObject()[TIME_MEAN_WITHOUT_ZERO], 3, 3)

        for t in list_all_transact:
            if t[NUM] == 1:
                pass


if __name__ == '__main__':
    unittest.main(module="test_queue_depart")
