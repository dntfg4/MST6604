from Segment import Segment
from DataItem import DataItem
from Constants import *


class DataSegment(Segment):
    def __init__(self):
        Segment.__init__(self, DATA_SEGMENT)
        self.__data = []

    def add_data(self, data):
        self.__data.append(data)

    def get_data(self):
        return self.__data

    def get_pretty_print(self):
        it = iter(self.__data)
        pretty_print = ""
        for i in it:
            pretty_print = pretty_print + i.get_name() + "->"
        return pretty_print
