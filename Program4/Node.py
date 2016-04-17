from DataItem import DataItem

class Node(object):
    def __init__(self, name, parent_name):
        self.__name = name
        self.__parent_name = parent_name
        self.__parent_node = None
        self.__childern = []
        self.__data = []

    def get_name(self):
        return self.__name

    def get_parent_name(self):
        return self.__parent_name

    def get_children(self):
        return self.__childern

    def get_data(self):
        return self.__data

    def add_child(self, child):
        self.__childern.append(child)

    def add_data(self, data):
        self.__data.append(data)

    def set_parent_node(self, node):
        self.__parent_node = node

    def get_parent_node(self):
        return self.__parent_node

    def are_children_leafs(self):
        it = iter(self.get_children())
        for i in it:
            if len(i.get_children()) > 0:
                return False
        return True

    def print_node(self):
        print "Node: %s" % self.__name
        print "Node Parent: %s" % self.__parent_name
        if len(self.__childern) > 0:
            it = iter(self.__childern)
            for i in it:
                i.print_node()
        if len(self.__data):
            it = iter(self.__data)
            for i in it:
                i.print_data()
