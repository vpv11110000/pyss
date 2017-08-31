##!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import func_exponential
from pyss.pyss_const import *
from pyss.statisticalseries import StatisticalSeries,approx_equal



class TestFuncExponential(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        ss=StatisticalSeries()
        # суммарные частоты
        fd = func_exponential.Exponential(timeForEvent=2, scale=1.0)
        for i in xrange(1,100000):
            x=fd.get()
            ss.append(x, count=1)
        c=ss.count()
        for x,y in ss[DATA].iteritems():
            # относительные частоты
            f=float(y)/c
            print "x=%f, y=%f"%(x,f)


if __name__ == '__main__':
    unittest.main(module="test_func_exponential")
