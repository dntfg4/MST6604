'''Location Management Misc:
        This contains the MS, Tree, and Node classes for the algorithms.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/06 12:00:00 $'
__copyright__ = 'Copyright (c) 2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

import subprocess
from LocationManagementConstants import *
from LocationManagementAlgorithms import *

algorithm_list = [POINTER, VALUE, FORWARDING_P, FORWARDING_V, REPLICATION_P, REPLICATION_V]
location_list = [FORWARDING_P_FORWARD, FORWARDING_P_REVERSE, REPLICATION]
location_list[len(location_list):] = algorithm_list


##################################################################################
#
#  Class Description: This class is the tree. It contains nodes and allows an
#                     algorithm to help move and search between nodes
#
##################################################################################
class Tree(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, algorithm):
        self.__root_node = None
        self.__leaf_nodes = []
        self.__algorithm = algorithm
        if self.__algorithm is not None:
            self.__algorithm.set_tree(self)
        self.__node_update_list = []
        self.__node_search_list = []
        self.__forwarding_list = []
        self.__tree_draw_count = 0
        return

    ##################################################################################
    #
    #  Description: Add the root node to the tree and hold the leaf nodes in a list
    #
    ##################################################################################
    def add_node(self, node):
        if node.is_root():
            self.__root_node = node
        elif node.is_leaf():
            self.__leaf_nodes.append(node)
        return

    ##################################################################################
    #
    #  Description: Get the root node
    #
    ##################################################################################
    def get_root_node(self):
        return self.__root_node

    ##################################################################################
    #
    #  Description: Get the leaf node list
    #
    ##################################################################################
    def get_leaf_nodes(self):
        return self.__leaf_nodes

    ##################################################################################
    #
    #  Description: Get the node named name
    #
    ##################################################################################
    def get_node(self, name):
        if self.__root_node is not None:
            return self.__root_node.get_child_with_name(name)

        return None

    ##################################################################################
    #
    #  Description: Find the lca of 2 nodes
    #
    ##################################################################################
    @staticmethod
    def get_lca(node1, node2):
        n1 = node1
        n2 = node2

        if (n1 is None) or (n2 is None):
            return None

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

    ##################################################################################
    #
    #  Description: Put the ms into a node named name. This is to initialize the ms in a node.
    #
    ##################################################################################
    def put_ms_into_node_name(self, ms, name):
        node = self.get_node(name)
        if node is None:
            return False

        if (self.__algorithm.get_type() == VALUE) or (self.__algorithm.get_type() == FORWARDING_V) or (self.__algorithm.get_type() == REPLICATION_V):
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        else:
            node.add_ms_location(ms, node, self.__algorithm.get_type())
        ms.set_node(node, self.__algorithm.get_type())

        while not node.is_root():
            node_parent = node.get_parent_node()
            if (self.__algorithm.get_type() == VALUE) or (self.__algorithm.get_type() == FORWARDING_V) or (self.__algorithm.get_type() == REPLICATION_V):
                node_parent.add_ms_location(ms, ms.get_node(self.__algorithm.get_type()), self.__algorithm.get_type())
            else:
                node_parent.add_ms_location(ms, node, self.__algorithm.get_type())
            node = node_parent

        return True

    ##################################################################################
    #
    #  Description: Get the update count
    #
    ##################################################################################
    def get_update_count(self):
        return self.__algorithm.get_update_count()

    ##################################################################################
    #
    #  Description: Get the search count
    #
    ##################################################################################
    def get_search_count(self):
        return self.__algorithm.get_search_count()

    ##################################################################################
    #
    #  Description: Find a node named name and search for ms
    #
    ##################################################################################
    def find_node_and_query_ms_location_from_node(self, ms, name):
        del self.__node_search_list[:]
        return self.__algorithm.find_node_and_query_ms_location_from_node(ms, name)

    ##################################################################################
    #
    #  Description: Find the ms node starting at node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        del self.__node_search_list[:]
        return self.__algorithm.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: Find the node named name and move ms to it
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        del self.__node_update_list[:]
        del self.__node_search_list[:]
        return self.__algorithm.find_node_and_move_ms_location_from_node(ms, name)

    ##################################################################################
    #
    #  Description: Move ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        del self.__node_update_list[:]
        del self.__node_search_list[:]
        return self.__algorithm.move_ms_to_node(ms, node)

    ##################################################################################
    #
    #  Description: Get the tree algorithm
    #
    ##################################################################################
    def get_algorithm(self):
        return self.__algorithm

    ##################################################################################
    #
    #  Description: Add a node to the search list if it is not already there
    #
    ##################################################################################
    def add_node_search(self, node):
        if self.__node_search_list.count(node) == 0:
            self.__node_search_list.append(node)

    ##################################################################################
    #
    #  Description: Add a node to the update list if it is not already there
    #
    ##################################################################################
    def add_node_update(self, node):
        if self.__node_update_list.count(node) == 0:
            self.__node_update_list.append(node)

    ##################################################################################
    #
    #  Description: Is the node in the update list
    #
    ##################################################################################
    def has_node_been_updated(self, node):
        return self.__node_update_list.count(node) > 0

    ##################################################################################
    #
    #  Description: Add a node to the forwarding list if it is not already there
    #
    ##################################################################################
    def add_forwarding_update(self, node):
        if self.__forwarding_list.count(node) == 0:
            self.__forwarding_list.append(node)

    ##################################################################################
    #
    #  Description: Delete a node from the forwarding list
    #
    ##################################################################################
    def delete_forwarding_update(self, node):
        if self.__forwarding_list.count(node) > 0:
            self.__forwarding_list.remove(node)

    ##################################################################################
    #
    #  Description: Draw the tree in a dot file and display it
    #
    ##################################################################################
    def draw_tree(self, ms1, ms2):
        self.__tree_draw_count += 1
        directoryname = "dot\\"
        graphtitle = self.get_algorithm().get_name() + "-" + str(self.__tree_draw_count)
        dotfilename = directoryname + self.get_algorithm().get_name() + "-" + str(self.__tree_draw_count) + ".dot"
        pngfilename = directoryname + self.get_algorithm().get_name() + "-" + str(self.__tree_draw_count) + ".png"
        oscommand = "dot -Tpng " + dotfilename + " > " + pngfilename

        f = open(dotfilename, 'w')
        text = "strict graph G{label=\"" + graphtitle + "\\n"
        text = text + "Search = " + str(self.get_search_count()) + ", "
        text = text + "Update = " + str(self.get_update_count()) + "\""
        f.write(text)
        f.write("\n")
        self.draw_nodes(f, self.__root_node, ms1, ms2)
        self.draw_edges(f, self.__root_node)
        self.draw_update(f, self.__forwarding_list, ms1, ms2)
        self.draw_search_edges(f, self.__node_search_list, ms1, ms2)
        f.write('}')
        f.close()

        subprocess.call(oscommand, shell=True)
        subprocess.call(pngfilename, shell=True)

        return

    ##################################################################################
    #
    #  Description: Draw the nodes in dot
    #
    ##################################################################################
    def draw_nodes(self, f, node, ms1, ms2):
        it = node.get_children_nodes()
        for i in it:
            self.draw_nodes(f, i, ms1, ms2)
        self.draw_node(f, node, ms1, ms2)

    ##################################################################################
    #
    #  Description: Draw a node in dot
    #
    ##################################################################################
    def draw_node(self, f, node, ms1, ms2):
        text = str(node.get_name()) + "[label=\"" + str(node.get_name())
        if ms1.get_node(self.get_algorithm().get_type()) is node:
            text = text + "\\nMS" + str(ms1.get_name())
        elif ms2.get_node(self.get_algorithm().get_type()) is node:
            text = text + "\\nMS" + str(ms2.get_name())
        text = text + "\""
        if self.__node_update_list.count(node) > 0:
            text = text + ",color = lightblue,style = filled"
        text = text + "];"
        f.write(text)
        f.write("\n")

    ##################################################################################
    #
    #  Description: Draw the edges in dot
    #
    ##################################################################################
    def draw_edges(self, f, node):
        it = node.get_children_nodes()
        for i in it:
            self.draw_edges(f, i)

        if not node.is_root():
            self.draw_edge(f, node)

    ##################################################################################
    #
    #  Description: Draw the edge in dot
    #
    ##################################################################################
    def draw_edge(self, f, node):
        text = str(node.get_parent_node().get_name()) + " -- " + str(node.get_name()) + ";"
        f.write(text)
        f.write("\n")

    ##################################################################################
    #
    #  Description: Draw the search edges in dot
    #
    ##################################################################################
    def draw_search_edges(self, f, search_list, ms1, ms2):
        self.get_algorithm().print_dot_search(f, search_list, ms1, ms2)

    ##################################################################################
    #
    #  Description: Draw the search edge in dot
    #
    ##################################################################################
    def draw_update(self, f, forwarding_list, ms1, ms2):
        self.get_algorithm().print_dot_forwarding(f, forwarding_list, ms1, ms2)


##################################################################################
#
#  Class Description: This class represents a node in the tree
#
##################################################################################
class Node(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, name):
        self.__name = name
        self.__parent_node = None
        self.__children_node = []
        self.__ms_list = {}
        self.__lcmr = 0.0
        return

    ##################################################################################
    #
    #  Description: Gets the name
    #
    ##################################################################################
    def get_name(self):
        return self.__name

    ##################################################################################
    #
    #  Description: Get the child nodes
    #
    ##################################################################################
    def get_children_nodes(self):
        return self.__children_node

    ##################################################################################
    #
    #  Description: Get the child node named name
    #
    ##################################################################################
    def get_child_with_name(self, name):
        if self.get_name() == name:
            return self

        for i in range(len(self.__children_node)):
            n = self.__children_node[i].get_child_with_name(name)
            if n is not None:
                return n

        return None

    ##################################################################################
    #
    #  Description: Add a child node
    #
    ##################################################################################
    def add_child_node(self, node):
        if self.__children_node.count(node) == 0:
            self.__children_node.append(node)
        return

    ##################################################################################
    #
    #  Description: Add the parent node
    #
    ##################################################################################
    def add_parent_node(self, parent):
        self.__parent_node = parent
        return

    ##################################################################################
    #
    #  Description: Get the parent node
    #
    ##################################################################################
    def get_parent_node(self):
        return self.__parent_node

    ##################################################################################
    #
    #  Description: Find the ms of location type
    #
    ##################################################################################
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

    ##################################################################################
    #
    #  Description: Create a new index for ms in the list
    #
    ##################################################################################
    def get_new_ms_list_index(self):
        i = 0
        it = iter(self.__ms_list)
        for j in it:
            if i <= j:
                i = j + 1
        return i

    ##################################################################################
    #
    #  Description: Add an ms to the node
    #
    ##################################################################################
    def add_ms(self, ms):
        if self.find_ms(ms) is None:
            l = self.get_new_ms_list_index()
            self.__ms_list[l] = {}
            self.__ms_list[l][MOBILE_STATION] = ms
            self.__ms_list[l][LOCATION] = {}
            it = iter(location_list)
            for loc in it:
                self.__ms_list[l][LOCATION][loc] = None
        return

    ##################################################################################
    #
    #  Description: Does the node contain ms
    #
    ##################################################################################
    def contains_ms(self, ms):
        return self.find_ms(ms) is None

    ##################################################################################
    #
    #  Description: Is it the root node
    #
    ##################################################################################
    def is_root(self):
        return self.__parent_node is None

    ##################################################################################
    #
    #  Description: Is it a leaf node
    #
    ##################################################################################
    def is_leaf(self):
        return len(self.__children_node) == 0

    ##################################################################################
    #
    #  Description: Add a ms and location type
    #
    ##################################################################################
    def add_ms_location(self, ms, loc, loc_type):
        if self.find_ms(ms) is None:
            self.add_ms(ms)
            i = self.find_ms(ms)
            self.__ms_list[i][LOCATION][loc_type] = loc
            return True
        else:
            return self.set_ms_location(ms, loc, loc_type)

    ##################################################################################
    #
    #  Description: Set the ms location type
    #
    ##################################################################################
    def set_ms_location(self, ms, loc, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            self.__ms_list[i][LOCATION][loc_type] = loc
            return True

        return False

    ##################################################################################
    #
    #  Description: The the ms location type
    #
    ##################################################################################
    def get_ms_location(self, ms, loc_type):
        i = self.find_ms(ms)
        if i is not None:
            return self.__ms_list[i][LOCATION][loc_type]

        return None

    ##################################################################################
    #
    #  Description: Delete the ms location type
    #
    ##################################################################################
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
                return True
            else:
                return False
        return True

    ##################################################################################
    #
    #  Description: Delete the ms from the node
    #
    ##################################################################################
    def delete_all_ms_locations(self, ms):
        i = self.find_ms(ms)
        if i is not None:
            del self.__ms_list[i]
        return

    ##################################################################################
    #
    #  Description: Set the lcmr
    #
    ##################################################################################
    def set_lcmr(self, lcmr):
        self.__lcmr = lcmr
        return

    ##################################################################################
    #
    #  Description: Get the lcmr
    #
    ##################################################################################
    def get_lcmr(self):
        return self.__lcmr

    ##################################################################################
    #
    #  Description: Calcuate the lcmr
    #
    ##################################################################################
    def calculate_lcmr(self):
        if self.is_leaf():
            return self.__lcmr

        self.__lcmr = 0

        it = iter(self.__children_node)
        for i in it:
            self.__lcmr += i.calculate_lcmr()

        return self.__lcmr


##################################################################################
#
#  Class Description: This class represent a mobile subscribe
#
##################################################################################
class MS(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, name, max_forwards=5):
        self.__name = name
        self.__node_list = {}
        self.__max_forwards = max_forwards
        it = iter(algorithm_list)
        for node_type in it:
            self.__node_list[node_type] = None
        return

    ##################################################################################
    #
    #  Description: Set the name
    #
    ##################################################################################
    def set_name(self, name):
        self.__name = name
        return

    ##################################################################################
    #
    #  Description: Get the name
    #
    ##################################################################################
    def get_name(self):
        return self.__name

    ##################################################################################
    #
    #  Description: Set the node of location type
    #
    ##################################################################################
    def set_node(self, node, loc_type):
        self.__node_list[loc_type] = node
        return

    ##################################################################################
    #
    #  Description: Get the node of location type
    #
    ##################################################################################
    def get_node(self, loc_type):
        return self.__node_list[loc_type]

    ##################################################################################
    #
    #  Description: Get the maximum number of forwards
    #
    ##################################################################################
    def get_max_forwards(self):
        return self.__max_forwards


##################################################################################
#
#  Description: Creates the nodes and organizes the structure and adds to the tree
#
##################################################################################
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

    node7.set_lcmr(.2)
    node8.set_lcmr(.2)
    node9.set_lcmr(.2)
    node10.set_lcmr(.2)
    node11.set_lcmr(.2)
    node12.set_lcmr(.2)
    node13.set_lcmr(.2)
    node14.set_lcmr(.2)
    node15.set_lcmr(.2)
    node16.set_lcmr(.2)
    node17.set_lcmr(.2)
    node18.set_lcmr(.2)

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
    for i in range(19):
        tree.add_node(tree.get_node(i))

    return


if __name__ == "__main__":
    tpa = Tree(PointerAlgorithm())
    tfppa = Tree(ForwardingPointerPAlgorithm())
    tva = Tree(ValueAlgorithm())
    tfpva = Tree(ForwardingPointerVAlgorithm())
    trva = Tree(ReplicationValueAlgorithm())
    trpa = Tree(ReplicationPointerAlgorithm())
    fill_tree(tpa)
    fill_tree(tva)
    fill_tree(tfppa)
    fill_tree(tfpva)
    fill_tree(trva)
    fill_tree(trpa)

    ms1 = MS(1)

    tpa.put_ms_into_node_name(ms1, 7)
    tva.put_ms_into_node_name(ms1, 7)
    tfppa.put_ms_into_node_name(ms1, 7)
    tfpva.put_ms_into_node_name(ms1, 7)
    trpa.put_ms_into_node_name(ms1, 7)
    trva.put_ms_into_node_name(ms1, 7)

    ms2 = MS(2)

    tpa.put_ms_into_node_name(ms2, 18)
    tva.put_ms_into_node_name(ms2, 18)
    tfppa.put_ms_into_node_name(ms2, 18)
    tfpva.put_ms_into_node_name(ms2, 18)
    trpa.put_ms_into_node_name(ms2, 18)
    trva.put_ms_into_node_name(ms2, 18)

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
    tfppa.find_node_and_move_ms_location_from_node(ms1, 11)
    fpp = tfppa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_P).get_name())
    print "FPP Search Count = %d" % tfppa.get_search_count()
    print "FPP Update Count = %d" % tfppa.get_update_count()
    tfppa.find_node_and_move_ms_location_from_node(ms1, 13)
    fpp = tfppa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_P).get_name())
    print "FPP Search Count = %d" % tfppa.get_search_count()
    print "FPP Update Count = %d" % tfppa.get_update_count()
    tfppa.find_node_and_move_ms_location_from_node(ms1, 15)
    fpp = tfppa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_P).get_name())
    print "FPP Search Count = %d" % tfppa.get_search_count()
    print "FPP Update Count = %d" % tfppa.get_update_count()
    tfppa.find_node_and_move_ms_location_from_node(ms1, 13)
    fpp = tfppa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_P).get_name())
    #tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    #print "FPV Update Count = %d" % tfpva.get_update_count()
    #tfpva.find_node_and_move_ms_location_from_node(ms1, 11)
    #fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    #print "FPV Search Count = %d" % tfpva.get_search_count()
    #print "FPV Update Count = %d" % tfpva.get_update_count()
    #tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    #fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    #print "FPV Search Count = %d" % tfpva.get_search_count()
    #print "FPV Update Count = %d" % tfpva.get_update_count()
    #tfpva.find_node_and_move_ms_location_from_node(ms1, 12)
    #fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    #print "FPV Search Count = %d" % tfpva.get_search_count()
    #print "FPV Update Count = %d" % tfpva.get_update_count()
    tfpva.find_node_and_move_ms_location_from_node(ms1, 13)
    fpv = tfpva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(FORWARDING_V).get_name())
    trpa.find_node_and_move_ms_location_from_node(ms1, 13)
    p = trpa.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(POINTER).get_name())
    trva.find_node_and_move_ms_location_from_node(ms1, 13)
    p = trva.find_node_and_query_ms_location_from_node(ms1, ms2.get_node(POINTER).get_name())
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
    print "RPA Search Count  = %d" % trpa.get_search_count()
    print "RPA Update Count  = %d" % trpa.get_update_count()
    print "RVA Search Count  = %d" % trva.get_search_count()
    print "RVA Update Count  = %d" % trva.get_update_count()
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

    tpa.draw_tree(ms1, ms2)
    tva.draw_tree(ms1, ms2)
    tfppa.draw_tree(ms1, ms2)