class DataItem(object):
    def __init__(self, attribute, data):
        self.__attribute = attribute
        self.__data = int(data)
        self.__name = data

    def get_attribute(self):
        return self.__attribute

    def get_data(self):
        return self.__data

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def print_data(self):
        print "Name = %s" % self.get_name()
        print "Search Attribute = %d" % self.get_attribute()
        print "Data = %s" % self.get_data()


if __name__ == "__main__":
    d = DataItem(1, "A")
    d.set_name("A1")
    d.print_data()
