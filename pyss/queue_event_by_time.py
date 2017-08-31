# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль с классом очереди транзактов, упорядоченной по времени
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *

class QueueEventByTime(object):
    """Очередь транзактов, упорядоченная по времени

    Фактор упорядочивания определяется значением transact[SCHEDULED_TIME]

    """

    def __init__(self, reverse=False):
        if reverse not in [True, False]:
            raise Exception("reverse must in [True, False]")
        self.transactList = []
        self.reverse = reverse

    def isEmpty(self):
        return len(self.transactList) == 0

    def put(self, transact):
        if transact[SCHEDULED_TIME] is None:
            raise Exception("transact[SCHEDULED_TIME] is None")
        self.transactList.append(transact)

    def _keyFunc(self,t):
        return t[SCHEDULED_TIME]
    
    def clear(self):
        self.transactList[:] = []        

    def first(self):
        if self.transactList:
            if self.reverse is False:
                return min(self.transactList, key=self._keyFunc)
            else:
                return max(self.transactList, key=self._keyFunc)
        else:
            return None

    def remove(self, transact):
        if transact in self.transactList:
            self.transactList.remove(transact)

    def findByTime(self, currentTime):
        rv = None
        t = self.first()
        if t:
            if t[SCHEDULED_TIME] <= currentTime:
                rv = t
        return rv

    def extractByTime(self, currentTime):
        rv = self.first()
        if rv:
            if rv[SCHEDULED_TIME] <= currentTime:
                self.remove(rv)
            else:
                rv = None
        return rv

    def __str__(self):
        so = sorted(self.transactList,
                    cmp=lambda a, b:(-1 if a[SCHEDULED_TIME] < b[SCHEDULED_TIME] 
                                     else 1 if a[SCHEDULED_TIME] < b[SCHEDULED_TIME] else 0))
        s = "\n".join([str(t) for t in so])
        return s

if __name__ == '__main__':
    def main():
        print "?"

    main()
