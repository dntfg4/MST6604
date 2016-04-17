from DataItem import DataItem
from Node import Node


class Tree(object):
    def __init__(self):
        self.__root_node = None
        self.__nodes = []
        self.__replication_level = 0
        self.__tree_levels = 0

    def add_node(self, name, parent_name):
        n = Node(name, parent_name)
        self.__nodes.append(n)

    def add_data(self, attribute, data, node_name):
        d = DataItem(int(attribute), data)
        it = iter(self.__nodes)
        for i in it:
            if node_name == i.get_name():
                i.add_data(d)
                break

    def complete(self):
        print "Creating Tree:                 Started"
        it = iter(self.__nodes)
        for i in it:
            jt = iter(self.__nodes)
            if i.get_parent_name() == 'None':
                self.__root_node = i
            for j in jt:
                if i.get_parent_name() == j.get_name():
                    i.set_parent_node(j)
                    j.add_child(i)
                    break

        r = self.__root_node
        while len(r.get_children()) > 0:
            self.__tree_levels += 1
            r = r.get_children()[0]

        print "Creating Tree:                 Finished"

    def get_root(self):
        return self.__root_node

    def get_tree_levels(self):
        return self.__tree_levels

    def print_tree(self):
        self.__root_node.print_node()

    def set_replication_level(self, level):
        self.__replication_level = level

    def get_replication_level(self):
        return self.__replication_level
