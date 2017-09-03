# #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль блока записи данных (преобразованных в строки) в файл
"""

# pylint: disable=line-too-long
import os

from pyss import pyssobject
from pyss.pyss_const import *
from pyss.block import Block

# pylint: disable=line-too-long

def appendToFile(filename, strData):
    with open(filename, "ab") as f:
        f.write(strData + "\n")

class FileSave(Block):
    r"""Блок записи данных (преобразованных в строки) в файл
    
При входе транзакта в блок FileSave инициируется запись в файл fileName результата вызова функции funcSave.
Перед записью данные преобразуются в текстовый вид (str()).

Проход блока открывает (режим python io "ab"), записывает данные, закрывает файл.

Прочитать данные в список можно:

    with open(filename,'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

Args:
    ownerSegment=None - объект сегмента-владельца 
    label=None - метка блока (см. block.py)  
    fileName="default.dat" - имя файла
    funcSave=None - функция формирования данных для записи. Сигнатура str f(owner,transact)
    mode="write" - режим записи. 
                   "write" - создание или перезапись файла (аналог python io 'wb' ). 
                   "append" - создаёт файл ("wb") если не существует и добавляет данные в существующий файл (аналог python io 'wb' и 'ab').

Например, блок

file_save.FileSave(sgm, fileName="c:\\temp\\model.dat",funcSave=lambda o,t:str(model.getCurTime()),mode="write")

записывает текущее время в файл c:\temp\model.dat.

Атрибуты блока FileSave (в дополнение к атрибутам block.Block):
bl = file_save.FileSave(...)
bl[FILENAME] - имя файла
bl[FUNC_SAVE] - функция формирования данных для записи. Сигнатура str f(owner,transact)

    """
    
    def __init__(self, ownerSegment=None, label=None, fileName="default.dat", funcSave=None, mode=MODE_WRITE):

        # pylint:disable=too-many-arguments

        super(FileSave, self).__init__(FILE_SAVE, label=label, ownerSegment=ownerSegment)
        map(pyssobject.raiseIsTrue, [fileName is None or fileName == "", funcSave is None, mode is None or mode == ""])
        self[FILENAME] = fileName
        self[FUNC_SAVE] = funcSave
        if mode == MODE_WRITE:
            with open(self[FILENAME], 'wb'):
                pass
        elif mode == MODE_APPEND:
            if not os.path.exists(fileName):
                with open(self[FILENAME], 'wb'):
                    pass

    def transactInner(self, currentTime, transact=None):
        # pylint:disable=unused-argument
        appendToFile(self[FILENAME], self[FUNC_SAVE](self, transact))
        return transact

if __name__ == '__main__':
    def main():
        print "?"

    main()
