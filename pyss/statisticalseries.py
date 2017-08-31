# #!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=bad-whitespace, missing-docstring

# TODO from collections import Counter
# from collections import Counter
import math
from pyss.pyss_const import *

def approx_equal(a, b, tol=0.001):
    
    # # tol=0.001
    return abs(a - b) <= (abs(a) + abs(b)) / 2 * tol

class StatisticalSeries(dict):
    """Статистический ряд (группированные данные)"""
    
    def __init__(self, owner=None, label=None):
        super(StatisticalSeries, self).__init__()
        self[LABEL] = label
        self[OWNER] = owner
        self[DATA] = {}
        # кеш
        self[DATA_1] = {}

    def __hash__(self):
        return hash((self[LABEL], self[OWNER]))

    def append(self, value, count=1):
        """Добавить элемент value в количестве count раз"""
        if value in self[DATA]:
            self[DATA][value] += count
        else:
            self[DATA][value] = count
        self[DATA_1] = {}
        return self

    def extend(self, listOfValues):
        if listOfValues:
            map(lambda x:self.append(x, count=1), listOfValues)
        return self

    def reset(self):
        self[DATA] = {}
        # кеш
        self[DATA_1] = {}

    def count(self):
        """Число элементов в выборке"""
        if not self[DATA]:
            return int(0)
        if self.count not in self[DATA_1]:
            self[DATA_1][self.count] = reduce(lambda x, y:x + y, [self[DATA][x] for x in self[DATA]])
        return int(self[DATA_1][self.count])

    def maxAndMin(self):
        """Максимальное и минимальное значения"""
        
        if not self[DATA]:
            return None, None
        if self.maxAndMin not in self[DATA_1]:
            mx = None
            mn = None
            for v in self[DATA]:
                if mx is None:
                    mx = v
                    mn = v
                else:
                    mx = max(mx, v)
                    mn = min(mn, v)
            self[DATA_1][self.maxAndMin] = (mx, mn)
        return self[DATA_1][self.maxAndMin]

    def max(self):
        mx, mn = self.maxAndMin()
        return mx

    def min(self):
        mx, mn = self.maxAndMin()
        return mn

    def variationRange(self):
        if not self[DATA]:
            return None
        if self.variationRange not in self[DATA_1]:
            self[DATA_1][self.variationRange] = reduce(lambda x, y: x - y, list(self.maxAndMin()))
        return self[DATA_1][self.variationRange]


    def variationCoefficient(self):
        if not self[DATA]:
            return None
        if self.variationCoefficient not in self[DATA_1]:
            self[DATA_1][self.variationCoefficient] = self.sko() / self.mean()
        return self[DATA_1][self.variationCoefficient]

    def mean(self):
        """ Среднее от статистической последовательности"""
        if not self[DATA]:
            return None
        if self.mean not in self[DATA_1]:
            n = self.count()
            self[DATA_1][self.mean] = reduce(lambda x, y:x + y, [float(x) * float(self[DATA][x]) for x in self[DATA]]) / n
        return self[DATA_1][self.mean]
    
    def cloneWithFilter(self, funcFilter=None):
        """ Копирование элементов в новую статистическую последовательность, содержащую отфильтрованные элементы
        
        Args:
            funcFilter - функция фильтрации значений. Возвращает True/False. 
                         Если True, то элемент учитывается при вычислении среднего значения.
                         bool f(key, value)
                         Например: lambda key, value: key != 0
                         Пропустить все элементы последовательности, ключ которыхт равен нулю.
                         См. атрибут TIME_MEAN_WITHOUT_ZERO.
            
        """        
        
        r = StatisticalSeries(owner=None, label=None)
        map(lambda t: r.append(t[0], count=t[1]), [(x, self[DATA][x]) for x in self[DATA] if funcFilter(x, self[DATA][x])])
        return r
        

    def dispertion(self):
        if not self[DATA]:
            return None
        mn = self.mean()
        if self.dispertion not in self[DATA_1]:
            self[DATA_1][self.dispertion] = reduce(lambda x, y:x + y, [float(self[DATA][x]) * float(x - mn) ** 2 for x in self[DATA]]) / self.count()
        return self[DATA_1][self.dispertion]

    def distributionFunction(self):
        if not self[DATA]:
            return None
        if self.distributionFunction not in self[DATA_1]:
            n = self.count()
            values = sorted(self[DATA])
            f = 0.0
            r = []
            for v in values:
                f += float(self[DATA][v]) / n
                r.append([v, f])
            self[DATA_1][self.distributionFunction] = r
        return self[DATA_1][self.distributionFunction]

    def mediana(self):
        if not self[DATA]:
            return None
        if self.mediana not in self[DATA_1]:
            self[DATA_1][self.mediana] = self.quantile(alfa=0.5)
        return self[DATA_1][self.mediana]

    def mode(self):
        """Мода"""
        
        if not self[DATA]:
            return None
        if self.mode not in self[DATA_1]:
            values = sorted(self[DATA])
            rv = []
            if len(values) > 1:
                mx = self[DATA][values[0]]
                mn = self[DATA][values[0]]
                for v in values[1:]:
                    mx = max(mx, self[DATA][v])
                    mn = min(mn, self[DATA][v])
                if mx != mn:
                    for v in values:
                        if mx == self[DATA][v]:
                            rv.append(v)
            self[DATA_1][self.mode] = rv
        return self[DATA_1][self.mode]

    def sko(self):
        """Cтандартное отклонение"""
        
        if not self[DATA]:
            return None
        return math.sqrt(self.dispertion())

    def quantile(self, alfa=0.5):
        if not self[DATA]:
            return None
        rv = None
        r = self.distributionFunction()
        vn1 = None
        fn1 = None
        for v, f in r:
            if f <= alfa:
                rv = v
                vn1 = v
                fn1 = f
            else:
                if not fn1:
                    if len(r) > 1:
                        vn1 = r[0][0] + r[0][0] - r[1][0]
                        fn1 = 0
                if fn1 is not None:
                    k = (fn1 - f) / (vn1 - v)
                    rv = v + (alfa - f) / k
                break
        return rv

    def skewnessCoefficient(self):
        """Показатель асимметрии через отношение центрального момента третьего порядка к среднему квадратическому отклонению ряда в кубе"""
        if not self[DATA]:
            return None
        if self.skewnessCoefficient not in self[DATA_1]:
            z = self.sko()
            if z == 0.0:
                return None
            mn = self.mean()
            n = self.count()
            sk = z ** 3
            rv = 0
            for v in self[DATA]:
                c = self[DATA][v]
                rv += float(c) * ((v - mn) ** 3)
            rv = rv / n / sk
            self[DATA_1][self.skewnessCoefficient] = rv
        return self[DATA_1][self.skewnessCoefficient]

    def kurtosis(self):
        """Показатель эксцесса 
        
представляет собой отклонение вершины эмпирического
распределения вверх или вниз («крутость»)
от вершины кривой нормального распределения
эксцесс для нормального закона равен 3
        
        """
        
        if not self[DATA]:
            return None
        if self.kurtosis not in self[DATA_1]:
            z = self.sko()
            if z == 0.0:
                return None
            mn = self.mean()
            n = self.count()
            sk = z ** 4
            rv = 0
            for v in self[DATA]:
                c = self[DATA][v]
                rv += float(c) * ((v - mn) ** 4)
            rv = rv / n / sk
            self[DATA_1][self.kurtosis] = rv - 3.0
        return self[DATA_1][self.kurtosis]


    def quantile25(self):
        return self.quantile(alfa=0.25)

    def quantile75(self):
        return self.quantile(alfa=0.75)

if __name__ == '__main__':
    def main():
        print "?"

    main()
