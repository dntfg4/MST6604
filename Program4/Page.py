from Constants import *
from ControlIndex import ControlIndex


class Page(object):
    def __init__(self, name, type):
        self.__name = name
        self.__type = type
        self.__control_index = None
        self.__data = ''
        self.__index = None
        self.__data_offset = None

    def get_control_index(self):
        return self.__control_index

    def set_control_index(self, ic):
        self.__control_index = ic

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def set_index(self, index):
        self.__index = index

    def get_index(self):
        return self.__index

    def set_data_offset(self, data_offset):
        self.__data_offset = data_offset

    def get_data_offset(self):
        return self.__data_offset