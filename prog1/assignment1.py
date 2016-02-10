'''Location Management: This program contains algorithms determining search and updates
                        for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/06 12:00:00 $'
__copyright__ = 'Copyright (c) 2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

POINTER = "pointer"
VALUE = "value"
FORWARDING_P = "forwarding_p"
FORWARDING_V = "forwarding_v"
FORWARDING_P_FORWARD = "forwarding_p_forward"
FORWARDING_P_REVERSE = "forwarding_p_reverse"
MOBILE_STATION = "mobile station"
LOCATION = "location"

algorithm_list = [POINTER, VALUE, FORWARDING_P, FORWARDING_V]
location_list = [FORWARDING_P_FORWARD, FORWARDING_P_REVERSE]
location_list[len(location_list):] = algorithm_list


class Tree:
    def __init__(self, algorithm):
        self.__root_node = None
        self.__algorithm = algorithm
        if self.__algorithm is not None:
            self.__algorithm.set_tree(self)
        return

    def add_node(self, node):
        if node.is_root():
            self.__root_node = node
        return

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

        if (self.__algorithm.get_type() == VALUE) or (self.__algorithm.get_type() == FORWARDING_V):
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        else:
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        ms.set_node(node, self.__algorithm.get_type())

        #print node.get_name()

        while not node.is_root():
            node_parent = node.get_parent_node()
            if (self.__algorithm.get_type() == VALUE) or (self.__algorithm.get_type() == FORWARDING_V):
                node_parent.add_ms_location(ms, ms.get_node(self.__algorithm.get_type()), self.__algorithm.get_type())
            else:
                node_parent.add_ms_location(ms, node, self.__algorithm.get_type())
            node = node_parent
            #print node.get_name()

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
        return

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
        return

    def add_parent_node(self, parent):
        self.__parent_node = parent
        return

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
            #print self.__ms_list.__len__()
            #print self.__ms_list
        return

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
            #print self.__ms_list
            return True
        else:
            return self.set_ms_location(ms, loc, loc_type)

    def set_ms_location(self, ms, loc, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            self.__ms_list[i][LOCATION][loc_type] = loc
            #print self.__ms_list
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
                #print self.__ms_list
                return True
            else:
                return False
        return True

    def delete_all_ms_locations(self, ms):
        i = self.find_ms(ms)
        if i is not None:
            del self.__ms_list[i]
            #print self.__ms_list
        return


class MS:
    def __init__(self, name, max_forwards=5):
        self.__name = name
        self.__node_list = {}
        self.__max_forwards = max_forwards
        it = iter(algorithm_list)
        for node_type in it:
            self.__node_list[node_type] = None
        return

    def set_ms_name(self, name):
        self.__name = name
        return

    def get_ms_name(self):
        return self.__name

    def set_node(self, node, loc_type):
        self.__node_list[loc_type] = node
        return

    def get_node(self, loc_type):
        return self.__node_list[loc_type]

    def get_max_forwards(self):
        return self.__max_forwards


class Algorithm:
    def __init__(self, algorithm_type):
        self.__search_count = 0
        self.__update_count = 0
        self.__tree = None
        self.__type = algorithm_type
        return

    def set_search_count(self, value):
        self.__search_count = value
        return

    def get_search_count(self):
        return self.__search_count

    def increment_search_count(self):
        self.__search_count += 1
        return

    def set_update_count(self, value):
        self.__update_count = value
        return

    def get_update_count(self):
        return self.__update_count

    def increment_update_count(self):
        self.__update_count += 1
        return

    def set_tree(self, tree):
        self.__tree = tree
        return

    def get_tree(self):
        return self.__tree

    def get_type(self):
        return self.__type

    def find_node_and_query_ms_location_from_node(self, ms, name):
        return

    def query_ms_location_from_node(self, ms, node):
        return None

    def find_node_and_move_ms_location_from_node(self, ms, name):
        return

    def move_ms_to_node(self, ms, node):
        return None


class ValueAlgorithm(Algorithm):
    def __init__(self, loc_type=VALUE):
        Algorithm.__init__(self, loc_type)
        return

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
            return node.get_ms_location(ms, self.get_type())
        else:
            # look up the tree
            if node.is_root():
                return None

            found = False

            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.find_ms(ms, self.get_type()) is not None:
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
        return


class PointerAlgorithm(Algorithm):
    def __init__(self, loc_type=POINTER):
        Algorithm.__init__(self, loc_type)
        return

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

            while (not found) and (node is not None):
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

        # if lca is not ms_node:
        #     ms_node.add_ms_location(ms, ms_node, self.get_type())
        #     self.increment_update_count()

        node.add_ms_location(ms, node, self.get_type())
        self.increment_update_count()
        ms.set_node(node, self.get_type())
        return


class ForwardingPointerPAlgorithm(PointerAlgorithm):
    def __init__(self):
        PointerAlgorithm.__init__(self, FORWARDING_P)
        self.__forwarding_type = FORWARDING_P_FORWARD
        self.__reverse_type = FORWARDING_P_REVERSE
        return

    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if node.find_ms(ms) is not None:
            found = True
            if node is ms.get_node(self.get_type()):
                return node

        # look up the tree
        if not found:
            if node.is_root():
                return None

            node = node.get_parent_node()
            self.increment_search_count()

            while (not found) and (node is not None):
                if node.find_ms(ms, self.__forwarding_type) is not None:
                    found = True
                if (node.find_ms(ms, self.get_type()) is not None) and (node.find_ms(ms, self.__reverse_type) is None):
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # Now look down the pointer list
        if found:
            if node is node.get_ms_location(ms, self.get_type()):
                return node

            while node is not node.get_ms_location(ms, self.get_type()):
                next_node = node.get_ms_location(ms, self.__forwarding_type)
                if next_node is None:
                    next_node = node.get_ms_location(ms, self.get_type())
                self.increment_search_count()
                node = next_node

            return node

        return None

    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)
        ms_node = ms.get_node(self.get_type())
        if ms_node is node:
            return

        level_up = self.determine_forwarding_level_up(ms)

        lca = self.get_tree().get_lca(ms_node, node)
        level_distance = self.get_node_level_distance(ms, lca)
        if level_up < level_distance:
            level_node_ms = self.get_ms_level_node(ms, level_up)
            level_node = self.get_level_node(node, level_up)
        else:
            level_node_ms = lca
            level_node = lca

        while level_node_ms is not ms_node:
            next_node = ms_node.get_ms_location(ms, self.get_type())
            if next_node is None:
                next_node = ms_node.get_ms_location(ms, self.__reverse_type)
            else:
                next_node = ms_node.get_parent_node()

            ms_node.delete_all_ms_locations(ms)

            ms_node = next_node
            self.increment_update_count()

        ms_node = node

        while (level_node is not ms_node) and (level_node is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()

        if level_node_ms is level_node:
            level_node_ms.set_ms_location(ms, ms_node, self.get_type())
            self.increment_update_count()

            if level_node_ms is not ms_node:
                node.add_ms_location(ms, node, self.get_type())
                self.increment_update_count()
        else:
            level_node_ms.delete_all_ms_locations(ms)
            level_node_ms.add_ms_location(ms, level_node, self.__forwarding_type)
            level_node_ms.set_ms_location(ms, level_node, self.get_type())
            self.increment_update_count()
            level_node.delete_all_ms_locations(ms)
            level_node.add_ms_location(ms, level_node_ms, self.__reverse_type)
            level_node.set_ms_location(ms, ms_node, self.get_type())
            self.increment_update_count()
            node.add_ms_location(ms, node, self.get_type())
            self.increment_update_count()

        ms.set_node(node, self.get_type())
        return

    def determine_forwarding_level_up(self, ms):
        return 0

    def get_node_level_distance(self, ms, node2):
        distance = 0

        node1 = ms.get_node(self.get_type())

        while node1 is not node2:
            if node1.get_ms_location(ms, self.get_type()) is not None:
                node1 = node1.get_parent_node()
                distance += 1
            else:
                node1 = node1.get_ms_location(ms, self.__reverse_type)

        return distance

    def determine_number_of_forwards(self,ms):
        forwards = 0
        node = ms.get_node(self.get_type())

        while not node.is_root():
            if node.get_ms_location(ms, self.get_type()) is not None:
                node = node.get_parent()
            else:
                node = node.get_ms_location(ms, self.__reverse_type)
                forwards += 1

        return forwards

    def get_ms_level_node(self, ms, level_up):
        node = ms.get_node(self.get_type())
        levels = level_up

        while (not node.is_root()) and (levels > 0):
            if node.get_ms_location(ms, self.get_type()) is not None:
                node = node.get_parent_node()
                levels -= 1
            else:
                node = node.get_ms_location(ms, self.__reverse_type)

        return node

    def get_level_node(self, node, level_up):
        levels = level_up

        while (node is not None) and (levels > 0):
            node = node.get_parent_node()
            levels -= 1

        return node

class ForwardingPointerVAlgorithm(ValueAlgorithm):
    def __init__(self):
        ValueAlgorithm.__init__(self, FORWARDING_V)
        self.__forwarding_type = FORWARDING_P_FORWARD
        self.__reverse_type = FORWARDING_P_REVERSE
        return

    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if (node.get_ms_location(ms, self.get_type()) is not None) and (node.get_ms_location(ms, self.__forwarding_type) is None):
            return node
        elif (node.get_ms_location(ms, self.get_type()) is not None) and (node.get_ms_location(ms, self.__forwarding_type) is not None):
            node = node.get_ms_location(ms, self.__forwarding_type)
            self.increment_search_count()
            while node.get_ms_location(ms, self.__forwarding_type) is not None:
                node = node.get_ms_location(ms, self.__forwarding_type)
                self.increment_search_count()
            return node.get_ms_location(ms, self.get_type())
        else:
            # look up the tree
            if node.is_root():
                return None

            found = False

            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.get_ms_location(ms, self.get_type()) is not None:
                    found = True
                else:
                    if not node.is_root():
                        node = node.get_parent_node()
                        self.increment_search_count()

            node = node.get_ms_location(ms, self.get_type())
            self.increment_search_count()
            if node.get_ms_location(ms, self.__forwarding_type) is not None:
                node = node.get_ms_location(ms, self.__forwarding_type)
                self.increment_search_count()
                while node.get_ms_location(ms, self.__forwarding_type) is not None:
                    node = node.get_ms_location(ms, self.__forwarding_type)
                    self.increment_search_count()

            return node

    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        if node.get_ms_location(ms, self.__forwarding_type) is not None:
            self.remove_pre_loop_items(ms, node)

        if ms_node.get_ms_location(ms, self.get_type()) is None:
            node.set_ms_location(ms, None, self.__forwarding_type)
            node.set_ms_location(ms, node, self.get_type())
            self.increment_update_count()
            ms.set_node(node, self.get_type())
            return

        ms_node.set_ms_location(ms, node, self.get_type())
        ms_node.set_ms_location(ms, node, self.__forwarding_type)
        self.increment_update_count()
        node.add_ms_location(ms, node, self.get_type())
        node.set_ms_location(ms, ms_node, self.__reverse_type)
        self.increment_update_count()

        lca = self.get_tree().get_lca(ms_node, node)

        tmp_node = node

        while (lca is not tmp_node) and (lca is not tmp_node.get_parent_node()):
            node_parent = tmp_node.get_parent_node()
            node_parent.add_ms_location(ms, node, self.get_type())
            tmp_node = node_parent
            self.increment_update_count()

        ms.set_node(node, self.get_type())
        return

    def remove_pre_loop_items(self, ms, node):
        ms_node = ms.get_node(self.get_type())

        tmp_node = ms_node
        prev_node = tmp_node.get_ms_location(ms, self.__reverse_type)

        while tmp_node is not node:
            lca = self.get_tree().get_lca(prev_node, tmp_node)

            while lca is not tmp_node:
                tmp_node.delete_all_ms_locations(ms)
                tmp_node = tmp_node.get_parent_node()
                self.increment_update_count()

            tmp_node = prev_node
            prev_node = tmp_node.get_ms_location(ms, self.__reverse_type)

        return


def fill_tree(tree):
    node0 = Node(0)
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)
    node8 = Node(8)
    node9 = Node(9)
    node10 = Node(10)
    node11= Node(11)
    node12 = Node(12)
    node13 = Node(13)
    node14 = Node(14)
    node15 = Node(15)
    node16 = Node(16)
    node17 = Node(17)
    node18 = Node(18)

    node0.add_child_node(node1)
    node0.add_child_node(node2)
    node1.add_parent_node(node0)
    node2.add_parent_node(node0)

    node1.add_child_node(node3)
    node1.add_child_node(node4)
    node3.add_parent_node(node1)
    node4.add_parent_node(node1)

    node2.add_child_node(node5)
    node2.add_child_node(node6)
    node5.add_parent_node(node2)
    node6.add_parent_node(node2)

    node3.add_child_node(node7)
    node3.add_child_node(node8)
    node3.add_child_node(node9)
    node7.add_parent_node(node3)
    node8.add_parent_node(node3)
    node9.add_parent_node(node3)

    node4.add_child_node(node10)
    node4.add_child_node(node11)
    node4.add_child_node(node12)
    node10.add_parent_node(node4)
    node11.add_parent_node(node4)
    node12.add_parent_node(node4)

    node5.add_child_node(node13)
    node5.add_child_node(node14)
    node5.add_child_node(node15)
    node13.add_parent_node(node5)
    node14.add_parent_node(node5)
    node15.add_parent_node(node5)

    node6.add_child_node(node16)
    node6.add_child_node(node17)
    node6.add_child_node(node18)
    node16.add_parent_node(node6)
    node17.add_parent_node(node6)
    node18.add_parent_node(node6)

    tree.add_node(node0)

    return


if __name__ == "__main__":
    tpa = Tree(PointerAlgorithm())
    tfppa = Tree(ForwardingPointerPAlgorithm())
    tva = Tree(ValueAlgorithm())
    tfpva = Tree(ForwardingPointerVAlgorithm())
    fill_tree(tpa)
    fill_tree(tva)
    fill_tree(tfppa)
    fill_tree(tfpva)

    ms1 = MS(1)

    tpa.put_ms_into_node_name(ms1, 8)
    tva.put_ms_into_node_name(ms1, 8)
    tfppa.put_ms_into_node_name(ms1, 8)
    tfpva.put_ms_into_node_name(ms1, 8)

    ms2 = MS(2)

    tpa.put_ms_into_node_name(ms2, 17)
    tva.put_ms_into_node_name(ms2, 17)
    tfppa.put_ms_into_node_name(ms2, 17)
    tfpva.put_ms_into_node_name(ms2, 17)

    #tpa.find_node_and_move_ms_location_from_node(ms1, 13)
    #print "PA Update Count  = %d" % tpa.get_update_count()
    tpa.find_node_and_move_ms_location_from_node(ms1, 13)
    p = tpa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(POINTER).get_name())
    #tva.find_node_and_move_ms_location_from_node(ms1, 13)
    #print "VA Update Count  = %d" % tva.get_update_count()
    tva.find_node_and_move_ms_location_from_node(ms1, 13)
    v = tva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(VALUE).get_name())
    #tfppa.find_node_and_move_ms_location_from_node(ms1, 13)
    #print "FPP Update Count = %d" % tfppa.get_update_count()
    tfppa.find_node_and_move_ms_location_from_node(ms1, 13)
    fpp = tfppa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_P).get_name())
    #tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    #print "FPV Update Count = %d" % tfpva.get_update_count()
    tfpva.find_node_and_move_ms_location_from_node(ms1, 11)
    fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    print "FPV Search Count = %d" % tfpva.get_search_count()
    print "FPV Update Count = %d" % tfpva.get_update_count()
    tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    print "FPV Search Count = %d" % tfpva.get_search_count()
    print "FPV Update Count = %d" % tfpva.get_update_count()
    tfpva.find_node_and_move_ms_location_from_node(ms1, 8)
    fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    print "FPV Search Count = %d" % tfpva.get_search_count()
    print "FPV Update Count = %d" % tfpva.get_update_count()
    tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    print
    print
    print "PA Search Count  = %d" % tpa.get_search_count()
    print "PA Update Count  = %d" % tpa.get_update_count()
    print "VA Search Count  = %d" % tva.get_search_count()
    print "VA Update Count  = %d" % tva.get_update_count()
    print "FPP Search Count = %d" % tfppa.get_search_count()
    print "FPP Update Count = %d" % tfppa.get_update_count()
    print "FPV Search Count = %d" % tfpva.get_search_count()
    print "FPV Update Count = %d" % tfpva.get_update_count()
    print
    print

    if (p.get_name() == v.get_name()) and (p.get_name() == fpp.get_name()) and (p.get_name() == fpv.get_name()):
        print "All search results are the same."
    else:
        print "All search results are NOT the same!!"
        print "p    = %d" % p.get_name()
        print "v    = %d" % v.get_name()
        print "fpp  = %d" % fpp.get_name()
        print "fpv  = %d" % fpv.get_name()

