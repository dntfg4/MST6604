'''Location Management Misc:
        This contains the MH, Tree, and Node classes for the algorithms.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/17 12:00:00 $'
__copyright__ = '2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

import subprocess
from LocationManagementConstants import *
from LocationManagementAlgorithms import *
from LMCircle import *
from TokenRing import *
from MH import *
from Node import *

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
        self.__thread = None
        return

    def start_token_thread(self):
        self.__thread = TokenRingThread(self.__leaf_nodes)
        self.__thread.start()

    def set_token_ring_wait_time(self, wait_time):
        self.__thread.set_wait_time(wait_time)

    def clean(self):
        self.__thread.join()

    ##################################################################################
    #
    #  Description: Add the root node to the tree and hold the leaf nodes in a list
    #
    ##################################################################################
    def add_node(self, node):
        node.set_tree(self)
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

        node.add_ms_location(ms, node)
        ms.set_node(node)

        while not node.is_root():
            node_parent = node.get_parent_node()
            node_parent.add_ms_location(ms, node)
            node = node_parent

        return True

    ##################################################################################
    #
    #  Description: Remove ms from tree starting at snode
    #
    ##################################################################################
    @staticmethod
    def remove_ms_from_tree(ms, snode):
        while snode is not None:
            snode.delete_ms(ms)
            snode = snode.get_parent_node()

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
        self.__root_node.clear_node_gui_search()
        return self.__algorithm.find_node_and_query_ms_location_from_node(ms, name)


    ##################################################################################
    #
    #  Description: Find the ms node starting at node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        self.__root_node.clear_node_gui_search()
        return self.__algorithm.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: Find the node named name and move ms to it
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        self.__root_node.clear_node_gui_search()
        self.__root_node.clear_node_gui_update()
        return self.__algorithm.find_node_and_move_ms_location_from_node(ms, name)

    ##################################################################################
    #
    #  Description: Move ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        self.__root_node.clear_node_gui_search()
        self.__root_node.clear_node_gui_update()
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
#  Description: Creates the nodes and organizes the structure and adds to the tree
#
##################################################################################
def fill_tree(tree, canvas):
    radius = 30
    level0 = radius
    level1 = level0 + 100
    level2 = level1 + 100
    level3 = level2 + 100
    node0 = Node(0)
    c0 = canvas.add_circle(canvas.get_width()/2, level0, radius, fill="white", outline="black", width=2, name="0")
    node0.add_gui_node(c0)
    node1 = Node(1)
    c1 = canvas.add_circle(canvas.get_width()/4, level1, radius, fill="white", outline="black", width=2, name="1")
    node1.add_gui_node(c1)
    node2 = Node(2)
    c2 = canvas.add_circle((canvas.get_width()/4)*3, level1, radius, fill="white", outline="black", width=2, name="2")
    node2.add_gui_node(c2)
    node3 = Node(3)
    c3 = canvas.add_circle(canvas.get_width()/8, level2, radius, fill="white", outline="black", width=2, name="3")
    node3.add_gui_node(c3)
    node4 = Node(4)
    c4 = canvas.add_circle((canvas.get_width()/8)*3, level2, radius, fill="white", outline="black", width=2, name="4")
    node4.add_gui_node(c4)
    node5 = Node(5)
    c5 = canvas.add_circle((canvas.get_width()/8)*5, level2, radius, fill="white", outline="black", width=2, name="5")
    node5.add_gui_node(c5)
    node6 = Node(6)
    c6 = canvas.add_circle((canvas.get_width()/8)*7, level2, radius, fill="white", outline="black", width=2, name="6")
    node6.add_gui_node(c6)
    node7 = Node(7)
    c7 = canvas.add_circle(canvas.get_width()/16, level3, radius, fill="white", outline="black", width=2, name="7")
    node7.add_gui_node(c7)
    node8 = Node(8)
    c8 = canvas.add_circle((canvas.get_width()/16)*2, level3, radius, fill="white", outline="black", width=2, name="8")
    node8.add_gui_node(c8)
    node9 = Node(9)
    c9 = canvas.add_circle((canvas.get_width()/16)*3, level3, radius, fill="white", outline="black", width=2, name="9")
    node9.add_gui_node(c9)
    node10 = Node(10)
    c10 = canvas.add_circle((canvas.get_width()/16)*5, level3, radius, fill="white", outline="black", width=2, name="10")
    node10.add_gui_node(c10)
    node11= Node(11)
    c11 = canvas.add_circle((canvas.get_width()/16)*6, level3, radius, fill="white", outline="black", width=2, name="11")
    node11.add_gui_node(c11)
    node12 = Node(12)
    c12 = canvas.add_circle((canvas.get_width()/16)*7, level3, radius, fill="white", outline="black", width=2, name="12")
    node12.add_gui_node(c12)
    node13 = Node(13)
    c13 = canvas.add_circle((canvas.get_width()/16)*9, level3, radius, fill="white", outline="black", width=2, name="13")
    node13.add_gui_node(c13)
    node14 = Node(14)
    c14 = canvas.add_circle((canvas.get_width()/16)*10, level3, radius, fill="white", outline="black", width=2, name="14")
    node14.add_gui_node(c14)
    node15 = Node(15)
    c15 = canvas.add_circle((canvas.get_width()/16)*11, level3, radius, fill="white", outline="black", width=2, name="15")
    node15.add_gui_node(c15)
    node16 = Node(16)
    c16 = canvas.add_circle((canvas.get_width()/16)*13, level3, radius, fill="white", outline="black", width=2, name="16")
    node16.add_gui_node(c16)
    node17 = Node(17)
    c17 = canvas.add_circle((canvas.get_width()/16)*14, level3, radius, fill="white", outline="black", width=2, name="17")
    node17.add_gui_node(c17)
    node18 = Node(18)
    c18 = canvas.add_circle((canvas.get_width()/16)*15, level3, radius, fill="white", outline="black", width=2, name="18")
    node18.add_gui_node(c18)
    canvas.pack()

    canvas.add_line(c0, c1)
    canvas.add_line(c0, c2)
    canvas.add_line(c1, c3)
    canvas.add_line(c1, c4)
    canvas.add_line(c2, c5)
    canvas.add_line(c2, c6)
    canvas.add_line(c3, c7)
    canvas.add_line(c3, c8)
    canvas.add_line(c3, c9)
    canvas.add_line(c4, c10)
    canvas.add_line(c4, c11)
    canvas.add_line(c4, c12)
    canvas.add_line(c5, c13)
    canvas.add_line(c5, c14)
    canvas.add_line(c5, c15)
    canvas.add_line(c6, c16)
    canvas.add_line(c6, c17)
    canvas.add_line(c6, c18)

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

    tree.start_token_thread()
