from Segment import Segment
from DataSegment import DataSegment
from ControlIndex import ControlIndex
from Constants import *

class IndexSegment(Segment):
    def __init__(self):
        Segment.__init__(self, INDEX_SEGMENT)
        self.__nodes = []
        self.__data_segment = DataSegment()
        self.__control_index = ControlIndex()

    def add_index_item(self, node):
        self.__nodes.append(node)

    def complete_data(self):
        it = iter(self.__nodes)
        for i in it:
            if len(i.get_data()) > 0:
                dt = iter(i.get_data())
                for d in dt:
                    self.__data_segment.add_data(d)

    def reverse(self):
        self.__nodes.reverse()

    def print_index_segment(self):
        it = iter(self.__nodes)
        pretty_print = ""
        for i in it:
            pretty_print = pretty_print + i.get_name() + "->"
        pretty_print = pretty_print + self.__data_segment.get_pretty_print()
        print "%s" % pretty_print
        return pretty_print

    def get_nodes(self):
        return self.__nodes

    def get_data_segment(self):
        return self.__data_segment
