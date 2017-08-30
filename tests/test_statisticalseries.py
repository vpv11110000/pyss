##!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import logger
from pyss.statisticalseries import StatisticalSeries

class TestStatisticalSeries(unittest.TestCase):

    objectForTest=StatisticalSeries()

    def setUp(self):
        self.objectForTest.reset()

    def tearDown(self):
        self.objectForTest.reset()

    def build_001(self):
        t=self.objectForTest
        l=[[150, 8],[250,25],[350,52],[450,7],[550,5],[650,3]]
        map(lambda x:t.append(x[0],count=x[1]),l)

    def test_count_001(self):
        logger.info("--- test_count_001 ----------------------------------")
        #
        t=self.objectForTest
        logger.info("count=%d"%t.count())
        expected=0
        self.assertEqual(t.count(), expected)
        #
        t.append(1.0)
        logger.info("count=%d"%t.count())
        expected=1
        self.assertEqual(t.count(), expected)

    def test_mean_001(self):
        logger.info("--- test_count_001 ----------------------------------")
        #
        t=self.objectForTest
        c=t.count()
        mn=t.mean()
        expected=0
        self.assertEqual(c, expected)
        expected=None
        self.assertEqual(mn, expected)
        #
        t.append(1.0)
        c=t.count()
        mn=t.mean()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=1
        self.assertEqual(c, expected)
        expected=1.0
        self.assertEqual(mn, expected)
        #
        t.append(2.0)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        mn=t.mean()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=1.5
        self.assertEqual(mn, expected)

    def test_mean_002(self):
        logger.info("--- test_mean_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        c=t.count()
        mn=t.mean()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=100
        self.assertEqual(c, expected)
        expected=335.0
        self.assertEqual(mn, expected)

    def test_mean_003(self):
        logger.info("--- test_count_003 ----------------------------------")
        #
        t=self.objectForTest
        listOfValues=[1.0,2.0]
        t.extend(listOfValues)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        mn=t.mean()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=1.5
        self.assertEqual(mn, expected)

    def test_mean_004(self):
        logger.info("--- test_count_004 ----------------------------------")
        #
        t=self.objectForTest
        listOfValues=[0.0,1.0,2.0]
        t.extend(listOfValues)
        c=t.count()
        expected=3
        self.assertEqual(c, expected)
        mn=t.mean()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=1.0
        self.assertEqual(mn, expected)
        # filter
        ss=t.cloneWithFilter(funcFilter=lambda k,v: k!=0.0)
        mn=ss.mean()
        c=ss.count()
        logger.info("count=%d mean=%f"%(c,mn))
        expected=1.5
        self.assertEqual(mn, expected)

    def test_maxmin_001(self):
        logger.info("--- test_maxmin_001 ----------------------------------")
        #
        t=self.objectForTest
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        mx=t.max()
        expected=None
        self.assertEqual(mx, expected)
        mn=t.max()
        expected=None
        self.assertEqual(mn, expected)
        #
        t.append(1.0)
        c=t.count()
        mx=t.max()
        mn=t.max()
        expected=1
        self.assertEqual(c, expected)
        expected=1.0
        self.assertEqual(mx, expected)
        expected=1.0
        self.assertEqual(mn, expected)

        #
        t.append(2.0)
        c=t.count()
        mx=t.max()
        mn=t.min()
        expected=2
        self.assertEqual(c, expected)
        expected=2.0
        self.assertEqual(mx, expected)
        expected=1.0
        self.assertEqual(mn, expected)
        # кеш
        c=t.count()
        mx=t.max()
        mn=t.min()
        expected=2
        self.assertEqual(c, expected)
        expected=2.0
        self.assertEqual(mx, expected)
        expected=1.0
        self.assertEqual(mn, expected)

    def test_variationRange_001(self):
        logger.info("--- test_variationRange_001 ----------------------------------")
        #
        t=self.objectForTest
        c=t.count()
        v=t.variationRange()
        expected=0
        self.assertEqual(c, expected)
        expected=None
        self.assertEqual(v, expected)
        #
        t.append(1.0)
        c=t.count()
        v=t.variationRange()
        expected=1
        self.assertEqual(c, expected)
        expected=0
        self.assertEqual(v, expected)

        #
        t.append(2.0)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.variationRange()
        expected=1.0
        self.assertEqual(v, expected)
        # кеш
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.variationRange()
        expected=1.0
        self.assertEqual(v, expected)

    def test_dispertion_001(self):
        logger.info("--- test_dispertion_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.dispertion()
        expected=None
        self.assertEqual(v, expected)
        #
        t.append(1.0)
        c=t.count()
        v=t.dispertion()
        expected=1
        self.assertEqual(c, expected)
        expected=0.0
        self.assertEqual(v, expected)
        #
        t.append(2.0)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.dispertion()
        expected=0.25
        self.assertEqual(v, expected)
        # кеш
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.dispertion()
        expected=0.25
        self.assertEqual(v, expected)

    def test_sko_001(self):
        logger.info("--- test_sko_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.sko()
        expected=None
        self.assertEqual(v, expected)
        #
        t.append(1.0)
        c=t.count()
        v=t.sko()
        expected=1
        self.assertEqual(c, expected)
        expected=0.0
        self.assertEqual(v, expected)
        #
        t.append(2.0)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.sko()
        expected=0.5
        self.assertEqual(v, expected)
        # кеш
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.sko()
        expected=0.5
        self.assertEqual(v, expected)

    def test_mode_001(self):
        logger.info("--- test_mode_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.mode()
        expected=None
        self.assertEqual(v, expected)
        #
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1]])
        v=t.mode()
        expected=[]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1]])
        v=t.mode()
        expected=[]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1]])
        v=t.mode()
        expected=[1.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2]])
        v=t.mode()
        expected=[2.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,1]])
        v=t.mode()
        expected=[]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,1]])
        v=t.mode()
        expected=[1.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2],[3.0,1]])
        v=t.mode()
        expected=[2.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,2]])
        v=t.mode()
        expected=[3.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2]])
        v=t.mode()
        expected=[1.0,3.0]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2],[4.0,1]])
        v=t.mode()
        expected=[1.0,3.0]
        self.assertEqual(v, expected)

        # кеш
        c=t.count()
        expected=6
        self.assertEqual(c, expected)
        v=t.mode()
        expected=[1.0,3.0]
        self.assertEqual(v, expected)

    def test_variationCoefficient_001(self):
        logger.info("--- test_variationCoefficient_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.variationCoefficient()
        expected=None
        self.assertEqual(v, expected)
        #
        t.append(1.0)
        c=t.count()
        expected=1
        self.assertEqual(c, expected)
        v=t.variationRange()
        expected=0
        self.assertEqual(v, expected)

        #
        t.append(2.0)
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.variationRange()
        expected=1.0
        self.assertEqual(v, expected)
        # кеш
        c=t.count()
        expected=2
        self.assertEqual(c, expected)
        v=t.variationRange()
        expected=1.0
        self.assertEqual(v, expected)

    def test_distributionFunction_001(self):
        logger.info("--- test_distributionFunction_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.distributionFunction()
        expected=None
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1]])
        v=t.distributionFunction()
        logger.info("distributionFunction=%s"%str(v))
        expected=[[1,1]]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1]])
        v=t.distributionFunction()
        logger.info("distributionFunction=%s"%str(v))
        expected=[[1.0, 0.5], [2.0, 1.0]]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2],[4.0,1]])
        v=t.distributionFunction()
        logger.info("distributionFunction=%s"%str(v))
        expected=[[1.0, 0.3333333333333333], [2.0, 0.5], [3.0, 0.8333333333333333], [4.0, 0.9999999999999999]]
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 5],[2.0,2],[3.0,1],[4.0,1]])
        v=t.distributionFunction()
        logger.info("distributionFunction=%s"%str(v))
        expected=[[1.0, 0.5555555555555556], [2.0, 0.7777777777777778], [3.0, 0.8888888888888888], [4.0, 1.0]]
        self.assertEqual(v, expected)

    #
    def test_mediana_001(self):
        logger.info("--- test_mediana_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.mediana()
        expected=None
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1]])
        v=t.mediana()
        logger.info("mediana=%s"%str(v))
        expected=None
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1]])
        v=t.mediana()
        logger.info("mediana=%s"%str(v))
        expected=1.0
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2],[4.0,1]])
        v=t.mediana()
        logger.info("mediana=%s"%str(v))
        expected=2
        self.assertAlmostEqual(v, expected, places=6)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 5],[2.0,2],[3.0,1],[4.0,1]])
        v=t.mediana()
        logger.info("mediana=%s"%str(v))
        expected=0.9  #0.8999999999999999
        self.assertAlmostEqual(v, expected, places=6)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,5],[3.0,1],[4.0,1]])
        v=t.mediana()
        logger.info("mediana=%s"%str(v))
        expected=1.6
        self.assertAlmostEqual(v, expected, places=6)

    def test_skewnessCoefficient_001(self):
        logger.info("--- test_skewnessCoefficient_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=None
        self.assertEqual(v, expected)
        #
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1]])
        v=t.skewnessCoefficient()
        expected=None
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1]])
        v=t.skewnessCoefficient()
        logger.info("sko=%f skewnessCoefficient=%s"%(t.sko(),str(v)))
        expected=0
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0.707106781186548
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=-0.707106781186548
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,1]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,1]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0.49338220021815865
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2],[3.0,1]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,2]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=-0.49338220021815865
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2],[4.0,1]])
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0.05482024446868387
        self.assertAlmostEqual(v, expected,places=4)

        # кеш
        c=t.count()
        expected=6
        self.assertEqual(c, expected)
        v=t.skewnessCoefficient()
        logger.info("skewnessCoefficient=%s"%str(v))
        expected=0.05482024446868387
        self.assertAlmostEqual(v, expected,places=4)

    def test_kurtosis_001(self):
        logger.info("--- test_kurtosis_001 ----------------------------------")
        #
        t=self.objectForTest
        #
        c=t.count()
        expected=0
        self.assertEqual(c, expected)
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=None
        self.assertEqual(v, expected)
        #
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1]])
        v=t.kurtosis()
        expected=None
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1]])
        v=t.kurtosis()
        logger.info("sko=%f kurtosis=%s"%(t.sko(),str(v)))
        expected=-2.0
        self.assertEqual(v, expected)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.4999999999999993
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.4999999999999993
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,1]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.5
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,1]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.371900826446281
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,2],[3.0,1]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 1],[2.0,1],[3.0,2]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.371900826446281
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.7499999999999998
        self.assertAlmostEqual(v, expected,places=4)
        #
        t.reset()
        map(lambda x:t.append(x[0],count=x[1]),[[1.0, 2],[2.0,1],[3.0,2],[4.0,1]])
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.3884297520661164
        self.assertAlmostEqual(v, expected,places=4)

        # кеш
        c=t.count()
        expected=6
        self.assertEqual(c, expected)
        v=t.kurtosis()
        logger.info("kurtosis=%s"%str(v))
        expected=-1.3884297520661164
        self.assertAlmostEqual(v, expected,places=4)

    def test_count_002(self):
        logger.info("--- test_count_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        logger.info("count=%d"%t.count())
        expected=100
        c=t.count()
        self.assertEqual(c, expected)

    def test_dispertion_002(self):
        logger.info("--- test_dispertion_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        c=t.count()
        expected=100
        self.assertEqual(c, expected)
        v=t.dispertion()
        logger.info("count=%d dispertion=%f"%(c,v))
        expected=10875.0
        self.assertEqual(v, expected)

    def test_sko_002(self):
        logger.info("--- test_sko_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        c=t.count()
        expected=100
        self.assertEqual(c, expected)
        v=t.sko()
        logger.info("count=%d sko=%f"%(c,v))
        expected=104.283
        self.assertAlmostEqual(v, expected, places=3, msg=None, delta=None)

    def test_mode_002(self):
        logger.info("--- test_mode_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        v=t.mode()
        expected=[350.0]
        self.assertEqual(v, expected)

    def test_distributionFunction_002(self):
        logger.info("--- test_distributionFunction_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        v=t.distributionFunction()
        logger.info("distributionFunction=%s"%str(v))
        expected=[[150, 0.08], [250, 0.33], [350, 0.8500000000000001], [450, 0.9200000000000002], [550, 0.9700000000000002], [650, 1.0000000000000002]]
        self.assertEqual(v, expected)

    def test_mediana_002(self):
        logger.info("--- test_mediana_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        v=t.mediana()
        expected=282.692308 # 282.6923076923077
        logger.info("mediana=%s"%str(v))
        self.assertAlmostEqual(v, expected,places=6)

    def test_skewnessCoefficient_002(self):
        logger.info("--- test_skewnessCoefficient_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        c=t.count()
        expected=100
        self.assertEqual(c, expected)
        v=t.skewnessCoefficient()
        logger.info("count=%d skewnessCoefficient=%f"%(c,v))
        expected=0.778384
        self.assertAlmostEqual(v, expected, places=2, msg=None, delta=None)

    def test_kurtosis_002(self):
        logger.info("--- test_kurtosis_002 ----------------------------------")
        #
        t=self.objectForTest
        self.build_001()
        #
        c=t.count()
        expected=100
        self.assertEqual(c, expected)
        v=t.kurtosis()
        logger.info("count=%d kurtosis=%f"%(c,v))
        expected=1.41 #1.407309
        self.assertAlmostEqual(v, expected, places=2, msg=None, delta=None)


if __name__ == '__main__':
    unittest.main(module="test_statisticalseries")
