'''Location Management Algorithms:
        This program contains algorithms determining search and updates for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/17 12:00:00 $'
__copyright__ = '2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

from LocationManagementConstants import *
from Tree import *

##################################################################################
#
#  Class Description: This is the base class of algorithms
#
##################################################################################
class Algorithm(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, algorithm_type, name=""):
        self.__search_count = 0
        self.__update_count = 0
        self.__tree = None
        self.__type = algorithm_type
        self.__name = name
        return

    ##################################################################################
    #
    #  Description: This sets the search value
    #
    ##################################################################################
    def set_search_count(self, value):
        self.__search_count = value
        return

    ##################################################################################
    #
    #  Description: This returns the current search count
    #
    ##################################################################################
    def get_search_count(self):
        return self.__search_count

    ##################################################################################
    #
    #  Description: This increments the search count
    #
    ##################################################################################
    def increment_search_count(self):
        self.__search_count += 1
        return

    ##################################################################################
    #
    #  Description: This set the search count
    #
    ##################################################################################
    def set_update_count(self, value):
        self.__update_count = value
        return

    ##################################################################################
    #
    #  Description: The gets the update count
    #
    ##################################################################################
    def get_update_count(self):
        return self.__update_count

    ##################################################################################
    #
    #  Description: This increments the update count
    #
    ##################################################################################
    def increment_update_count(self):
        self.__update_count += 1
        return

    ##################################################################################
    #
    #  Description: This sets the tree for the algorithm
    #
    ##################################################################################
    def set_tree(self, tree):
        self.__tree = tree
        return

    ##################################################################################
    #
    #  Description: This gets the tree for the algorithm
    #
    ##################################################################################
    def get_tree(self):
        return self.__tree

    ##################################################################################
    #
    #  Description: This returns the algorithm type
    #
    ##################################################################################
    def get_type(self):
        return self.__type

    ##################################################################################
    #
    #  Description: This gets the algorithm name
    #
    ##################################################################################
    def get_name(self):
        return self.__name

    ##################################################################################
    #
    #  Description: This finds the node with name, searches for the node containing ms
    #
    ##################################################################################
    def find_node_and_query_ms_location_from_node(self, ms, name):
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        return None

    ##################################################################################
    #
    #  Description: This finds the node named name and moves ms to this node
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        return

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        return None


##################################################################################
#
#  Class Description: This the alorithm for Node Pointer Values in the database
#
##################################################################################
class PointerAlgorithm(Algorithm):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, loc_type=POINTER, name="Pointer_Algorithm"):
        Algorithm.__init__(self, loc_type, name)
        return

    ##################################################################################
    #
    #  Description: This finds the node with name, searches for the node containing ms
    #
    ##################################################################################
    def find_node_and_query_ms_location_from_node(self, ms, name):
        # get the node named name
        node = self.get_tree().get_node(name)

        # search for ms starting at node
        return self.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        # initialize the search count for this search
        self.set_search_count(0)

        found = False

        # if node is None, search fails and return
        if node is None:
            return node

        # check if the ms in this node
        if node is node.get_ms_location(ms):
            return node

        # look up the tree
        if not found:
            # if node is the root node, return
            if node.is_root():
                return None

            found = False

            # get the parent node
            node.get_gui_node().search_line()
            node = node.get_parent_node()
            self.increment_search_count()

            # while the ms has not been found and we have not passed the root node (should not happen),
            # search up the tree
            while (not found) and (node is not None):
                #self.get_tree().add_node_search(node)
                if node.get_ms_location(ms) is not None:
                    found = True
                else:
                    node.get_gui_node().search_line()
                    node = node.get_parent_node()
                    self.increment_search_count()

        # if we found the node which has ms, search down the tree for ms
        if found:
            # if this node contains ms, return the node
            if node is node.get_ms_location(ms):
                return node

            # while ms is not in the node, follow down the tree until the ms is found
            while node is not node.get_ms_location(ms):
                node = node.get_ms_location(ms)
                node.get_gui_node().search_line()
                self.increment_search_count()

            return node

        return None

    ##################################################################################
    #
    #  Description: This finds the node named name and moves ms to this node
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        # get the node named name
        node = self.get_tree().get_node(name)

        # move ms to node
        return self.move_ms_to_node(ms, node)

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        # initialize the update count
        self.set_update_count(0)

        # get the node where ms is located
        ms_node = ms.get_node()

        # if ms_node is empty, the update failed and return
        if ms_node is node:
            return

        # get the lca of the ms_node and node (where the ms is moving)
        lca = self.get_tree().get_lca(ms_node, node)

        # while the ms_node is not the lca, move up the tree
        while lca is not ms_node:
            ms_node.leave(ms)
            ms_node.get_gui_node().update_node()
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        # while the node (where ms is going) is not the lca and its parent is not lca,
        # add the ms to the node and move up the tree
        while (lca is not ms_node) and (lca is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.add_ms_location(ms, ms_node)
            ms_node = ms_node_parent
            ms_node.get_gui_node().update_node()
            self.increment_update_count()

        # add the last checked node to as the ms pointer node to the lca
        lca.add_ms_location(ms, ms_node)
        self.increment_update_count()
        lca.get_gui_node().update_node()

        # add ms to node (where is the ms is going)
        node.join(ms, node)
        node.get_gui_node().update_node()
        self.increment_update_count()
        # tell ms what node it is in
        ms.set_node(node)
        return
