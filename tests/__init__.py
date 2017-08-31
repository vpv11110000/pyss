# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss import *

def pyss_module_suite():

    #test_files = glob.glob('test_*.py')
    #module_strings = [test_file[0:len(test_file)-3] for test_file in test_files]
    #suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
    #test_suite = unittest.TestSuite(suites)

    testmodules=["test_advance", 
                 "test_assemble", 
                 "test_assign",
                 "test_enter_leave", 
                 "test_generate",
                 "test_pyss_model",
                 "test_queue", 
                 "test_recurrent_statistic",
                 "test_segment", 
                 "test_split",
                 "test_statisticalseries",
                 "test_storage", 
                 "test_table",
                 "test_terminate",
                 "test_transfer",
                 ]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for testMopduleName in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(testMopduleName, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(testMopduleName))
    return suite

if __name__ == '__main__':
    suite=pyss_module_suite()
    unittest.TextTestRunner().run(suite)


