##!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import func_discrete
from pyss.pyss_const import *
from pyss.statisticalseries import StatisticalSeries,approx_equal

class TestFuncDiscrete(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        ss=StatisticalSeries()
        # суммарные частоты
        fd = func_discrete.FuncDiscrete(randomGenerator=random.random, dictValues={.1:2,.3:3,.7:4,.8:5,1.0:6})
        for i in xrange(1,300000):
            x=fd.get()
            ss.append(x, count=1)
        c=ss.count()
        for x,y in ss[DATA].iteritems():
            # относительные частоты
            f=float(y)/c
            print "x=%f, y=%f"%(x,f)
            if approx_equal(x, 2.0, tol=.001):
                self.assertAlmostEqual(f, .1, places=2)
            elif approx_equal(x, 3.0, tol=.001):
                self.assertAlmostEqual(f, .2, places=2)
            elif approx_equal(x, 4.0, tol=.001):
                self.assertAlmostEqual(f, .4, places=2)
            elif approx_equal(x, 5.0, tol=.001):
                self.assertAlmostEqual(f, .1, places=2)
            elif approx_equal(x, 6.0, tol=.001):
                self.assertAlmostEqual(f, .2, places=2)

if __name__ == '__main__':
    unittest.main(module="test_func_discrete")
