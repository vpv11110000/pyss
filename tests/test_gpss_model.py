# #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import unittest

DIRNAME_MODULE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) + os.sep
sys.path.append(DIRNAME_MODULE)
sys.path.append(DIRNAME_MODULE + "pyss" + os.sep)

from pyss.pyss_const import *
from pyss import pyssobject
from pyss.pyss_model import PyssModel

class TestPyssModel(unittest.TestCase):

    def test_init_001(self):
        #
        m = PyssModel(optionz=None)
        self.assertEqual(m[NUM], None)
        #sl=dir(m)
        #print sl
        l=[OPTIONS, CURRENT_TIME, QUEUE_OBJECTS, CURRENT_EVENT_LIST,
           BLOCKS, DELAYED_LIST, TRANSACT_FAMILIES,
           SEGMENTS, ENTITY_TYPE, FUTURE_EVENT_LIST, CURRENT_SEGMENT,
           LABEL, FACILITIES, NUM, END_TIME, MAX_TIME_STR,
           PLOT_MODULES, CURRENT_TRANSACT, STORAGES, START_TIME]
        for key in l: 
            self.assertTrue(key in m)
        
#         ['__class__', '__cmp__', '__contains__', '__delattr__', 
#          '__delitem__', '__dict__', '__doc__', '__eq__', '__format__', 
#          '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', 
#          '__init__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', 
#          '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
#          '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
#          '_firstTx', 'addFacility', 'addPlotModule', 'addQtable', 
#          'addQueueObject', 'addSegment', 'addStorage', 'addTable', 
#          'appendToDelayedList', 'clear', 'commonInfo', 'copy', 'entitytypeWithLabel', 
#          'extractFromDelayedListFirst', 'findBlockByLabel', 'findFacility', 'findMinTime', 
#          'findMinTimeFromGenerates', 'fromkeys', 'generates', 'get', 'getCel', 
#          'getCurTime', 'getCurrentSegment', 'getCurrentTransact', 'getDelayedList', 
#          'getFacilities', 'getFel', 'getOptionForCurrentSegment', 'getOptions', 
#          'getPlotSubsystem', 'getQueueList', 'getStorages', 'has_key', 
#          'initBlocksFromSegments', 'initDelayedListForKey', 'initPlotFacilityLifeLine', 
#          'initPlotStorageLifeLine', 'initPlotTable', 'initPlotTransactLifeLine', 
#          'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'logTransactTrace', 
#          'moveFromDelayedListForKey_toCel', 
#          'moveTransactFromFelToCel', 'plotSubsystem', 'pop', 'popitem', 
#          'printHeader', 'printResult', 'qtableList', 'run', 'setCurrentSegment', 
#          'setCurrentTime', 'setCurrentTransact', 'setdefault', 'setlabel', 'start', 
#          'strBlocksHandle', 'strCel', 'strFacilities', 'strQtables', 'strQueueHandle', 
#          'strStorages', 'strTables', 'strTransactFamilies', 'tableList', 
#          'terminateCounter', 'update', 'values', 'variables', 'viewitems', 
#          'viewkeys', 'viewvalues']

if __name__ == '__main__':
    unittest.main(module="test_pyss_model")
