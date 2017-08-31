# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль объекта очереди с приоритетом
"""

# pylint: disable=line-too-long

from pyss.pyss_const import *

class QueueEventPriorities(object):
    def __init__(self, reverse=True):
        # # reverse = True - в порядке убывания
        self.keys = []
        self.items = {}
        self.reverse = reverse

    def isEmpty(self):
        return not bool(self.items)

    def put(self, transact):
        
#         if transact is None:
#             return
        p = transact[PR]
        if p not in self.keys:
            self.keys.append(p)
            self.keys = sorted(self.keys, reverse=self.reverse)
        if p not in self.items:
            self.items[p] = []
        self.items[p].append(transact)
        # self.items[p]=sorted(self.items[p], key = lambda t:t[NUM])

    def insertFirst(self, transact):
        # # в ставка на первое место с учётом приоритета
        p = transact[PR]
        if p not in self.keys:
            self.keys.append(p)
            self.keys = sorted(self.keys, reverse=self.reverse)
        if p not in self.items:
            self.items[p] = []
        self.items[p].insert(0, transact)
        # self.items[p]=sorted(self.items[p], key = lambda t:t[NUM])

    def first(self):
        rv = None
        if self.keys:
            for priority in self.keys:
                l = self.items[priority]
                if l:
                    return l[0]
        return rv

    def extractFirst(self):
        rv = None
        forRemove = []
        if self.keys:
            for priority in self.keys:
                l = self.items[priority]
                if l:
                    t = l[0]
                    self.items[priority].remove(t)
                    if not self.items[priority]:
                        forRemove.append(priority)
                    rv = t
                    break
        for k in forRemove:
            self.keys.remove(k)
        return rv

    def remove(self, transact):
        p = transact[PR]
        if p in self.items:
            if self.items[p]:
                if transact in self.items[p]: 
                    self.items[p].remove(transact)
                    if not self.items[p]:
                        self.keys.remove(p)

    def toString(self):
        s = ''
        for p in self.keys:
            l = self.items[p]
            if l:
                tl = [t.toString() for t in l]
                s += "\n".join(tl)

    def findByTime(self, currentTime):
        for p in self.keys:
            l = self.items[p]
            for t in l:
                if t[SCHEDULED_TIME] < currentTime:
                    return t

    def extractByTime(self, currentTime):
        forRemove = []
        rv = None
        for p in self.keys:
            l = self.items[p]
            for t in l:
                if t[SCHEDULED_TIME] < currentTime:
                    self.items[p].remove(t)
                    if not self.items[p]:
                        forRemove.append(p)
                    rv = t
        for k in forRemove:
            self.keys.remove(k)
        return rv

    def __str__(self):
        s = ''
        for p in self.keys:
            l = self.items[p]
            if l:
                s += "\n".join([str(t) for t in l])
            else:
                pass
        return s

if __name__ == '__main__':
    def main():
        print "?"
    main()





