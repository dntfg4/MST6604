'''Location Management: This program contains algorithms determining search and updates
                        for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/06 12:00:00 $'
__copyright__ = 'Copyright (c) 2016 James Soehlke and David N. Taylor'
__license__ = 'Python'



POINTER_VALUE = "pointer"
ACTUAL_VALUE = "value"
FORWARDING_POINTER = "forwarding"
MOBILE_STATION = "mobile station"
LOCATION = "location"

location_list = [POINTER_VALUE, ACTUAL_VALUE, FORWARDING_POINTER]


class Tree:
    def __init__(self, algorithm):
        self.__node_list = []
        self.__root_node = None
        self.__algorithm = algorithm
        if self.__algorithm is not None:
            self.__algorithm.set_tree(self)

    def add_node(self,n):
        if self.__node_list.count(n) == 0:
            self.__node_list.append(n)
            if n.is_root():
                self.__root_node = n

    def get_root_node(self):
        return self.__root_node

    def get_node(self, name):
        if self.__root_node is not None:
            return self.__root_node.get_child_with_name(name)

        return None

    @staticmethod
    def get_lca(node1, node2):
        n1 = node1
        n2 = node2

        while n1 is not n2:
            while not n2.is_root():
                n2 = n2.get_parent_node()
                if n1 is n2:
                    return n2

            if n1.is_root():
                break
            else:
                n1 = n1.get_parent_node()
                n2 = node2

        if n1 is n2:
            return n2
        else:
            return None

    def put_ms_into_node_name(self, ms, name):
        node = self.get_node(name)
        if node is None:
            return False

        if self.__algorithm.get_type() == ACTUAL_VALUE:
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        else:
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        ms.set_node(node, self.__algorithm.get_type())

        print node.get_name()

        while not node.is_root():
            node_parent = node.get_parent_node()
            if self.__algorithm.get_type() == ACTUAL_VALUE:
                node_parent.add_ms_location(ms, ms.get_node(self.__algorithm.get_type()), self.__algorithm.get_type())
            else:
                node_parent.add_ms_location(ms, node, self.__algorithm.get_type())
            node = node_parent
            print node.get_name()

        return True

    def get_update_count(self):
        return self.__algorithm.get_update_count()

    def get_search_count(self):
        return self.__algorithm.get_search_count()

    def find_node_and_query_ms_location_from_node(self, ms, name):
        return self.__algorithm.find_node_and_query_ms_location_from_node(ms, name)

    def query_ms_location_from_node(self, ms, node):
        return self.__algorithm.query_ms_location_from_node(self, ms, node)

    def find_node_and_move_ms_location_from_node(self, ms, name):
        return self.__algorithm.find_node_and_move_ms_location_from_node(ms, name)

    def move_ms_to_node(self, ms, node):
        return self.__algorithm.move_ms_to_node(ms, node)


class Node:
    def __init__(self, name):
        self.__name = name
        self.__parent_node = None
        self.__children_node = []
        self.__ms_list = {}

    def get_name(self):
        return self.__name

    def get_children_nodes(self):
        return self.__children_node

    def get_child_with_name(self, name):
        if self.get_name() == name:
            return self

        for i in range(self.__children_node.__len__()):
            n = self.__children_node[i].get_child_with_name(name)
            if n is not None:
                return n

        return None

    def add_child_node(self, node):
        if self.__children_node.count(node) == 0:
            self.__children_node.append(node)

    def add_parent_node(self, parent):
        self.__parent_node = parent

    def get_parent_node(self):
        return self.__parent_node

    def find_ms(self, ms, loc=None):
        it = iter(self.__ms_list)
        for i in it:
            if ms is self.__ms_list[i][MOBILE_STATION]:
                if loc is not None:
                    if self.__ms_list[i][LOCATION][loc] is not None:
                        return i
                else:
                    return i

        return None

    def get_new_ms_list_index(self):
        i = 0
        it = iter(self.__ms_list)
        for j in it:
            if i <= j:
                i = j + 1
        return i

    def add_ms(self, ms):
        if self.find_ms(ms) is None:
            l = self.get_new_ms_list_index()
            self.__ms_list[l] = {}
            self.__ms_list[l][MOBILE_STATION] = ms
            self.__ms_list[l][LOCATION] = {}
            it = iter(location_list)
            for loc in it:
                self.__ms_list[l][LOCATION][loc] = None
            print self.__ms_list.__len__()
            print self.__ms_list

    def contains_ms(self, ms):
        return self.find_ms(ms) is None

    def is_root(self):
        return self.__parent_node is None

    def is_leaf(self):
        return self.__children_node.__len__() == 0

    def add_ms_location(self, ms, loc, loc_type):
        if self.find_ms(ms) is None:
            self.add_ms(ms)
            i = self.find_ms(ms)
            self.__ms_list[i][LOCATION][loc_type] = loc
            print self.__ms_list
            return True
        else:
            return self.set_ms_location(ms, loc, loc_type)

    def set_ms_location(self, ms, loc, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            self.__ms_list[i][LOCATION][loc_type] = loc
            print self.__ms_list
            return True

        return False

    def get_ms_location(self, ms, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            return self.__ms_list[i][LOCATION][loc_type]

        return None

    def delete_ms_location(self, ms, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            self.__ms_list[i][LOCATION][loc_type] = None
            empty = True
            it = iter(location_list)
            for loc in it:
                if self.__ms_list[i][LOCATION][loc] is not None:
                    empty = False
            if empty:
                del self.__ms_list[i]
                print self.__ms_list


class MS:
    def __init__(self, name):
        self.__name = name
        self.__node_list = {}
        self.__node_list[POINTER_VALUE] = None
        self.__node_list[ACTUAL_VALUE] = None

    def set_ms_name(self, name):
        self.__name = name

    def get_ms_name(self):
        return self.__name

    def set_node(self, node, loc_type):
        self.__node_list[loc_type] = node

    def get_node(self, loc_type):
        return self.__node_list[loc_type]


class Algorithm:
    def __init__(self, algorithm_type):
        self.__search_count = 0
        self.__update_count = 0
        self.__tree = None
        self.__type = algorithm_type

    def set_search_count(self, value):
        self.__search_count = value

    def get_search_count(self):
        return self.__search_count

    def increment_search_count(self):
        self.__search_count += 1

    def set_update_count(self, value):
        self.__update_count = value

    def get_update_count(self):
        return self.__update_count

    def increment_update_count(self):
        self.__update_count += 1

    def set_tree(self, tree):
        self.__tree = tree

    def get_tree(self):
        return self.__tree

    def get_type(self):
        return self.__type

    def find_node_and_query_ms_location_from_node(self, ms, name):
        pass

    def query_ms_location_from_node(self, ms, node):
        return None

    def find_node_and_move_ms_location_from_node(self, ms, name):
        pass

    def move_ms_to_node(self, ms, node):
        return None


class ValueAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self, ACTUAL_VALUE)

    def find_node_and_query_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.query_ms_location_from_node(ms, node)

    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if node.find_ms(ms, ACTUAL_VALUE) is not None:
            found = True
            if node is node.get_ms_actual_location(ms):
                return node

        # look up the tree
        if not found:
            if node.is_root():
                return None

            found = False

            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.find_ms(ms, ACTUAL_VALUE) is not None:
                    found = True
                    return node.get_ms_location(ms, self.get_type())
                else:
                    if not node.is_root():
                        node = node.get_parent_node()
                        self.increment_search_count()

        return None

    def find_node_and_move_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.move_ms_to_node(ms, node)

    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        lca = self.get_tree().get_lca(ms_node, node)

        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        while ms_node is not None:
            ms_node_parent = ms_node.get_parent_node()
            ms_node.add_ms_location(ms, node, self.get_type())
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms.set_node(node, self.get_type())


class PointerAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self, POINTER_VALUE)

    def find_node_and_query_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.query_ms_location_from_node(ms, node)

    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if node.find_ms(ms, self.get_type()) is not None:
            found = True
            if node is node.get_ms_location(ms, self.get_type()):
                return node

        # look up the tree
        if not found:
            if node.is_root():
                return None

            found = False

            node = node.get_parent_node()
            self.increment_search_count()

            while (not found) and (not node.is_root()):
                if node.find_ms(ms, self.get_type()) is not None:
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

            # Now look down the pointer list
            if found:
                if node is node.get_ms_location(ms, self.get_type()):
                    return node

            while node is not node.get_ms_location(ms, self.get_type()):
                node = node.get_ms_location(ms, self.get_type())
                self.increment_search_count()

            return node

        return None

    def find_node_and_move_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.move_ms_to_node(ms, node)

    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        lca = self.get_tree().get_lca(ms_node, node)

        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        while (lca is not ms_node) and (lca is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()

        lca.set_ms_location(ms, ms_node, self.get_type())
        self.increment_update_count()
        ms_node.add_ms_location(ms, ms_node, self.get_type())
        self.increment_update_count()

        ms.set_node(node, self.get_type())


def fill_tree(tree):
    root_node = Node(0)
    tree.add_node(root_node)

    node_count = 0
    for i in range(2):
        node_count += 1
        inode = Node(node_count)
        inode.add_parent_node(root_node)
        root_node.add_child_node(inode)
        tree.add_node(inode)

        for j in range(3):
            node_count += 1
            jnode = Node(node_count)
            jnode.add_parent_node(inode)
            inode.add_child_node(jnode)
            tree.add_node(jnode)

            for k in range(2):
                node_count += 1
                knode = Node(node_count)
                knode.add_parent_node(jnode)
                jnode.add_child_node(knode)
                tree.add_node(knode)
    return


if __name__ == "__main__":
    tpa = Tree(PointerAlgorithm())
    tva = Tree(ValueAlgorithm())
    fill_tree(tpa)
    fill_tree(tva)

    ms1 = MS(1)

    tpa.put_ms_into_node_name(ms1, 6)
    tva.put_ms_into_node_name(ms1, 6)

    ms2 = MS(2)

    tpa.put_ms_into_node_name(ms2, 17)
    tva.put_ms_into_node_name(ms2, 17)

    b = tpa.find_node_and_query_ms_location_from_node(ms1, 20)
    tpa.find_node_and_move_ms_location_from_node(ms1, 20)
    c = tva.find_node_and_query_ms_location_from_node(ms1, 20)
    tva.find_node_and_move_ms_location_from_node(ms1, 20)
    print
    print
    print "PA Search Count = %d" % tpa.get_search_count()
    print "PA Update Count = %d" % tpa.get_update_count()
    print "VA Search Count = %d" % tva.get_search_count()
    print "VA Update Count = %d" % tva.get_update_count()
    if b.get_name() == c.get_name():
        print "B is C"
    else:
        print "B is NOT C"

