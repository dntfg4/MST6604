'''Location Management Algorithms:
        This program contains algorithms determining search and updates for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/06 12:00:00 $'
__copyright__ = 'Copyright (c) 2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

from LocationManagementConstants import *
from LocationManagementMisc import *

##################################################################################
#
#  Class Description: This is the base class of alorithms
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
        pass

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
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        return

    ##################################################################################
    #
    #  Description: This prints the dot information for the forwarding list
    #
    ##################################################################################
    def print_dot_forwarding(self, f, search_list, ms1, ms2):
        return


##################################################################################
#
#  Class Description: This the alorithm for Actual Values in the database
#
##################################################################################
class ValueAlgorithm(Algorithm):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, loc_type=VALUE, name="Actual_Value_Algorithm"):
        Algorithm.__init__(self, loc_type, name)
        return


    ##################################################################################
    #
    #  Description: This finds the node with name, searches for the node containing ms
    #
    ##################################################################################
    def find_node_and_query_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
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

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.find_ms(ms, self.get_type()) is not None:
                    found = True
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, self.get_type())
                else:
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()

        return None

    ##################################################################################
    #
    #  Description: This finds the node named name and moves ms to this node
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.move_ms_to_node(ms, node)

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        lca = self.get_tree().get_lca(ms_node, node)

        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        while ms_node is not None:
            ms_node_parent = ms_node.get_parent_node()
            ms_node.add_ms_location(ms, node, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms.set_node(node, self.get_type())
        return

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                f.write(text)
                f.write("\n")


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
        node = self.get_tree().get_node(name)

        return self.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
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

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if node.find_ms(ms, self.get_type()) is not None:
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # Now look down the pointer list
        if found:
            if node is node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                return node

            while node is not node.get_ms_location(ms, self.get_type()):
                node = node.get_ms_location(ms, self.get_type())
                self.get_tree().add_node_search(node)
                self.increment_search_count()

            return node

        return None

    ##################################################################################
    #
    #  Description: This finds the node named name and moves ms to this node
    #
    ##################################################################################
    def find_node_and_move_ms_location_from_node(self, ms, name):
        node = self.get_tree().get_node(name)

        return self.move_ms_to_node(ms, node)

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        lca = self.get_tree().get_lca(ms_node, node)

        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        while (lca is not ms_node) and (lca is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(ms_node_parent)

        lca.set_ms_location(ms, ms_node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(lca)

        node.add_ms_location(ms, node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(node)
        ms.set_node(node, self.get_type())
        return

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                f.write(text)
                f.write("\n")


##################################################################################
#
#  Class Description: This the alorithm for Forwarding Pointers of Pointers in the database
#
##################################################################################
class ForwardingPointerPAlgorithm(PointerAlgorithm):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, max_forwards=2):
        PointerAlgorithm.__init__(self, FORWARDING_P, "Forwarding_Algorithm_For_Pointer")
        self.__forwarding_type = FORWARDING_P_FORWARD
        self.__reverse_type = FORWARDING_P_REVERSE
        self.__max_forwards = max_forwards
        self.__forwarding_level = 0
        return

    ##################################################################################
    #
    #  Description: This sets the maximum number of forwards
    #
    ##################################################################################
    def set_max_forwards(self, max_forwards):
        __max_forwards = max_forwards
        return

    ##################################################################################
    #
    #  Description: This calculates the current number of forwards for the ms
    #
    ##################################################################################
    def get_current_forwards_count(self, ms, ms_node):
        forwards = 0
        while (ms_node is not None) and (not ms_node.is_root()):
            if ms_node.get_ms_location(ms, self.__reverse_type) is not None:
                forwards +=1
            if ms_node.get_ms_location(ms, self.__reverse_type) is None:
                ms_node = ms_node.get_parent_node()
            else:
                ms_node = ms_node.get_ms_location(ms, self.__reverse_type)
        return forwards

    ##################################################################################
    #
    #  Description: This purges the current pointers
    #
    ##################################################################################
    def purge_current_pointers(self, ms, ms_node):
        while not ms_node.is_root():
            prev_node = ms_node.get_ms_location(ms, self.__reverse_type)
            if prev_node is None:
                prev_node = ms_node.get_parent_node()
            ms_node.delete_all_ms_locations(ms)
            self.increment_update_count()
            self.get_tree().add_node_update(prev_node)
            self.get_tree().delete_forwarding_update(ms_node)
            ms_node = prev_node
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
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

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if (node.find_ms(ms, self.__forwarding_type) is not None) or (node.find_ms(ms, self.get_type()) is not None):
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # Now look down the pointer list
        if found:
            if node is node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                return node

            while node is not node.get_ms_location(ms, self.get_type()):
                next_node = node.get_ms_location(ms, self.get_type())
                if next_node is None:
                    next_node = node.get_ms_location(ms, self.__forwarding_type)
                self.get_tree().add_node_search(next_node)
                self.increment_search_count()
                node = next_node

            return node

        return None

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)
        ms_node = ms.get_node(self.get_type())

        if (node is None) or (ms_node is None) or (ms_node is node):
            return

        if self.get_current_forwards_count(ms, ms_node) >= self.__max_forwards:
            self.purge_current_pointers(ms, ms_node)
            node.add_ms_location(ms, node, self.get_type())
            ms.set_node(node, self.get_type())
            self.increment_update_count()
            self.get_tree().add_node_update(node)
            parent_node = node.get_parent_node()
            while node is not None:
                parent_node = node.get_parent_node()
                if parent_node is not None:
                    if parent_node.get_ms_location(ms, self.get_type()) is not node:
                        parent_node.add_ms_location(ms, node, self.get_type())
                        self.increment_update_count()
                        self.get_tree().add_node_update(parent_node)
                node = parent_node
            return

        level_up = self.determine_forwarding_level_up(ms)
        if level_up == 0:
            current_update_count = self.get_update_count()
            super(ForwardingPointerPAlgorithm, self).move_ms_to_node(ms, node)
            self.set_update_count(current_update_count + self.get_update_count())
            return


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
            self.get_tree().add_node_update(ms_node)
            self.increment_update_count()
            ms_node = next_node

        ms_node = node

        while (level_node is not ms_node) and (level_node is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.delete_all_ms_locations(ms)
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(ms_node_parent)

        level_node.delete_all_ms_locations(ms)
        level_node.add_ms_location(ms, ms_node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(level_node)

        if level_node_ms is not level_node:
            level_node_ms.add_ms_location(ms, level_node, self.__forwarding_type)
            level_node_ms.set_ms_location(ms, None, self.get_type())
            self.get_tree().add_forwarding_update(level_node_ms)
            self.increment_update_count()
            self.get_tree().add_node_update(level_node_ms)
            level_node.add_ms_location(ms, level_node_ms, self.__reverse_type)

            node.delete_all_ms_locations(ms)
            node.add_ms_location(ms, node, self.get_type())
            self.increment_update_count()
            self.get_tree().add_node_update(node)

        node.delete_all_ms_locations(ms)
        node.add_ms_location(ms, node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(node)
        ms.set_node(node, self.get_type())
        return

    ##################################################################################
    #
    #  Description: This returns the current forwarding level
    #
    ##################################################################################
    def determine_forwarding_level_up(self, ms):
        return self.__forwarding_level

    ##################################################################################
    #
    #  Description: This sets the forwarding level
    #
    ##################################################################################
    def set_forwarding_level(self, level):
        self.__forwarding_level = level
        return

    ##################################################################################
    #
    #  Description: This gets the tree level distance from ms to node2
    #
    ##################################################################################
    def get_node_level_distance(self, ms, node2):
        distance = 0

        node1 = ms.get_node(self.get_type())

        while node1 is not node2:
            if (node1.get_ms_location(ms, self.get_type()) is not None) or (node1.get_ms_location(ms, self.__forwarding_type)):
                node1 = node1.get_parent_node()
                distance += 1
            else:
                node1 = node1.get_ms_location(ms, self.__reverse_type)

        return distance

    ##################################################################################
    #
    #  Description: This determines the current number of forwards ms has.
    #
    ##################################################################################
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

    ##################################################################################
    #
    #  Description: This returns the node level_up levels from ms
    #
    ##################################################################################
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

    ##################################################################################
    #
    #  Description: This returns the node level_up levels from node
    #
    ##################################################################################
    def get_level_node(self, node, level_up):
        levels = level_up

        while (node is not None) and (levels > 0):
            node = node.get_parent_node()
            levels -= 1

        return node

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                if search_list[i].get_ms_location(ms1, FORWARDING_P_FORWARD) is search_list[j]:
                    text = text + "[style=\"bold,dashed\",color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_ms_location(ms1, FORWARDING_P) is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_parent_node() is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")

    ##################################################################################
    #
    #  Description: This prints the dot information for the forwarding list
    #
    ##################################################################################
    def print_dot_forwarding(self, f, forwarding_list, ms1, ms2):
        for i in range(len(forwarding_list)):
            if forwarding_list[i].get_ms_location(ms1,self.__forwarding_type):
                text = str(forwarding_list[i].get_name()) + " -- " + str(forwarding_list[i].get_ms_location(ms1,self.__forwarding_type).get_name())
                text = text + "[style=\"bold,dashed\",color=blue,label=\"F" + "\"];"
                f.write(text)
                f.write("\n")

            if forwarding_list[i].get_ms_location(ms2,self.__forwarding_type):
                text = str(forwarding_list[i].get_name()) + " -- " + str(forwarding_list[i].get_ms_location(ms2,self.__forwarding_type).get_name())
                text = text + "[style=\"bold,dashed\",color=blue,label=\"F" + "\"];"
                f.write(text)
                f.write("\n")


##################################################################################
#
#  Class Description: This the alorithm for Forwarding Pointers of Actual Values in the database
#
##################################################################################
class ForwardingPointerVAlgorithm(ValueAlgorithm):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, max_forwards=2):
        ValueAlgorithm.__init__(self, FORWARDING_V, "Forwarding_Algorithm_For_Actual_Value")
        self.__forwarding_type = FORWARDING_P_FORWARD
        self.__reverse_type = FORWARDING_P_REVERSE
        self.__max_forwards = max_forwards
        return

    ##################################################################################
    #
    #  Description: This sets the maximum forwards
    #
    ##################################################################################
    def set_max_forwards(self, max_forwards):
        __max_forwards = max_forwards
        return

    ##################################################################################
    #
    #  Description: This calculates the current number of forwards for the ms
    #
    ##################################################################################
    def get_current_forwards_count(self, ms, ms_node):
        forwards = 0
        while ms_node.get_ms_location(ms, self.__reverse_type) is not None:
            forwards +=1
            ms_node = ms_node.get_ms_location(ms, self.__reverse_type)
        return forwards

    ##################################################################################
    #
    #  Description: This purges the current pointers
    #
    ##################################################################################
    def purge_current_pointers(self, ms, ms_node):
        while ms_node.get_ms_location(ms, self.__reverse_type) is not None:
            prev_node = ms_node.get_ms_location(ms, self.__reverse_type)
            lca = self.get_tree().get_lca(prev_node, ms_node)
            while lca is not ms_node:
                ms_node.delete_all_ms_locations(ms)
                ms_node = ms_node.get_parent_node()
                self.increment_update_count()
                self.get_tree().add_node_update(ms_node)
                self.get_tree().delete_forwarding_update(ms_node)
            ms_node = prev_node
        ms.set_node(ms_node,self.get_type())
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if (node.get_ms_location(ms, self.get_type()) is not None) and (node.get_ms_location(ms, self.__forwarding_type) is None):
            return node
        elif (node.get_ms_location(ms, self.get_type()) is not None) and (node.get_ms_location(ms, self.__forwarding_type) is not None):
            self.get_tree().add_node_search(node)
            node = node.get_ms_location(ms, self.__forwarding_type)
            self.increment_search_count()
            while node.get_ms_location(ms, self.__forwarding_type) is not None:
                node = node.get_ms_location(ms, self.__forwarding_type)
                self.increment_search_count()
                self.get_tree().add_node_search(node)
            return node.get_ms_location(ms, self.get_type())
        else:
            # look up the tree
            if node.is_root():
                return None

            found = False

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.get_ms_location(ms, self.get_type()) is not None:
                    self.get_tree().add_node_search(node)
                    found = True
                else:
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()

            self.get_tree().add_node_search(node)
            node = node.get_ms_location(ms, self.get_type())
            self.increment_search_count()
            if node.get_ms_location(ms, self.__forwarding_type) is not None:
                self.get_tree().add_node_search(node)
                node = node.get_ms_location(ms, self.__forwarding_type)
                self.increment_search_count()
                self.get_tree().add_node_search(node)
                while node.get_ms_location(ms, self.__forwarding_type) is not None:
                    self.get_tree().add_node_search(node)
                    node = node.get_ms_location(ms, self.__forwarding_type)
                    self.increment_search_count()

            return node

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        self.set_update_count(0)

        ms_node = ms.get_node(self.get_type())

        if ms_node is node:
            return

        if self.get_current_forwards_count(ms, ms_node) >= self.__max_forwards:
            self.purge_current_pointers(ms, ms_node)
            current_update_count = self.get_update_count()
            super(ForwardingPointerVAlgorithm, self).move_ms_to_node(ms, node)
            self.set_update_count(current_update_count + self.get_update_count())
            return

        if node.get_ms_location(ms, self.__forwarding_type) is not None:
            self.remove_pre_loop_items(ms, node)

        if ms_node.get_ms_location(ms, self.get_type()) is None:
            node.set_ms_location(ms, None, self.__forwarding_type)
            node.set_ms_location(ms, node, self.get_type())
            self.get_tree().delete_forwarding_update(node)
            self.increment_update_count()
            self.get_tree().add_node_update(node)
            ms.set_node(node, self.get_type())
            return

        ms_node.set_ms_location(ms, node, self.get_type())
        ms_node.set_ms_location(ms, node, self.__forwarding_type)
        self.get_tree().add_forwarding_update(ms_node)
        self.increment_update_count()
        self.get_tree().add_node_update(ms_node)
        node.add_ms_location(ms, node, self.get_type())
        node.set_ms_location(ms, ms_node, self.__reverse_type)
        self.increment_update_count()
        self.get_tree().add_node_update(node)

        lca = self.get_tree().get_lca(ms_node, node)

        tmp_node = node

        while (lca is not tmp_node) and (lca is not tmp_node.get_parent_node()):
            node_parent = tmp_node.get_parent_node()
            node_parent.add_ms_location(ms, node, self.get_type())
            tmp_node = node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(node_parent)

        ms.set_node(node, self.get_type())
        return

    ##################################################################################
    #
    #  Description: This removes the pre_loop condition for forwards
    #
    ##################################################################################
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
                self.get_tree().add_node_update(tmp_node)

            tmp_node = prev_node
            prev_node = tmp_node.get_ms_location(ms, self.__reverse_type)

        return

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                if search_list[i].get_ms_location(ms1, FORWARDING_P_FORWARD) is search_list[j]:
                    text = text + "[style=\"bold,dashed\",color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_ms_location(ms1, FORWARDING_V) is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_parent_node() is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")

    ##################################################################################
    #
    #  Description: This prints the dot information for the forwarding list
    #
    ##################################################################################
    def print_dot_forwarding(self, f, forwarding_list, ms1, ms2):
        for i in range(len(forwarding_list)):
            if forwarding_list[i].get_ms_location(ms1,self.__forwarding_type):
                text = str(forwarding_list[i].get_name()) + " -- " + str(forwarding_list[i].get_ms_location(ms1,self.__forwarding_type).get_name())
                text = text + "[style=\"bold,dashed\",color=blue,label=\"F" + "\"];"
                f.write(text)
                f.write("\n")

            if forwarding_list[i].get_ms_location(ms2,self.__forwarding_type):
                text = str(forwarding_list[i].get_name()) + " -- " + str(forwarding_list[i].get_ms_location(ms2,self.__forwarding_type).get_name())
                text = text + "[style=\"bold,dashed\",color=blue,label=\"F" + "\"];"
                f.write(text)
                f.write("\n")


##################################################################################
#
#  Class Description: This the class for replication values
#
##################################################################################
class ReplicationValues(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, mins=.6, maxs=1.2):
        self.__mins = mins
        self.__maxs = maxs
        return

    ##################################################################################
    #
    #  Description: This set mins
    #
    ##################################################################################
    def set_mins(self, mins):
        self.__mins = mins
        return

    ##################################################################################
    #
    #  Description: This returns mins
    #
    ##################################################################################
    def get_mins(self):
        return self.__mins

    ##################################################################################
    #
    #  Description: This sets maxs
    #
    ##################################################################################
    def set_maxs(self, maxs):
        self.__maxs = maxs
        return

    ##################################################################################
    #
    #  Description: This returns maxs
    #
    ##################################################################################
    def get_maxs(self):
        return self.__maxs


##################################################################################
#
#  Class Description: This the alorithm for Replication of Pointer Values in the database
#
##################################################################################
class ReplicationPointerAlgorithm(PointerAlgorithm, ReplicationValues):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self):
        PointerAlgorithm.__init__(self, REPLICATION_P, "Replication_Algorithm_For_Pointer")
        ReplicationValues.__init__(self)
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if node.get_ms_location(ms, self.get_type()) is not None:
            found = True
            if node is node.get_ms_location(ms, self.get_type()):
                return node
        elif node.get_ms_location(ms, REPLICATION) is not None:
            return node.get_ms_location(ms, REPLICATION)

        # look up the tree
        if not found:
            if node.is_root():
                return None

            found = False

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if node.find_ms(ms, self.get_type()) is not None:
                    found = True
                elif node.get_ms_location(ms, REPLICATION) is not None:
                    return node.get_ms_location(ms, REPLICATION)
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # Now look down the pointer list
        if found:
            if node is node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                return node
            elif node.get_ms_location(ms, REPLICATION):
                self.get_tree().add_node_search(node)
                return node.get_ms_location(ms, REPLICATION)

            while node is not node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                if node.get_ms_location(ms, REPLICATION) is not None:
                    return node.get_ms_location(ms, REPLICATION)
                node = node.get_ms_location(ms, self.get_type())
                self.increment_search_count()

            self.get_tree().add_node_search(node)
            return node

        return None

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        super(ReplicationPointerAlgorithm, self).move_ms_to_node(ms, node)
        self.perform_replication(ms)

    ##################################################################################
    #
    #  Description: This performs the replication process
    #
    ##################################################################################
    def perform_replication(self, ms):
        it = iter(self.get_tree().get_leaf_nodes())
        for i in it:
            node = i
            while node is not None:
                lcmr = node.calculate_lcmr()
                rnode = node.get_ms_location(ms, REPLICATION)
                if lcmr < self.get_mins():
                    if rnode is not None:
                        rnode.set_ms_location(ms, None, REPLICATION)
                        if not self.get_tree().has_node_been_updated(rnode):
                            self.increment_update_count()
                            self.get_tree().add_node_update(rnode)
                        if rnode.get_ms_location(ms, REPLICATION_V) is None:
                            rnode.delete_all_ms_locations(ms)
                else: # for our topology, we at each spot if needed
                    if (rnode is None) or (rnode is not ms.get_node(REPLICATION_V)):
                        node.add_ms_location(ms, ms.get_node(REPLICATION_V), REPLICATION)
                        self.get_tree().add_node_update(node)
                        if not self.get_tree().has_node_been_updated(rnode):
                            self.increment_update_count()
                            self.get_tree().add_node_update(rnode)
                node = node.get_parent_node()

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                if search_list[i].get_ms_location(ms1, REPLICATION) is search_list[j]:
                    text = text + "[style=\"bold,dashed\",color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_ms_location(ms1, REPLICATION_P) is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_parent_node() is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")


##################################################################################
#
#  Class Description: This the alorithm for Replication of Actual Values in the database
#
##################################################################################
class ReplicationValueAlgorithm(ValueAlgorithm, ReplicationValues):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self):
        ValueAlgorithm.__init__(self, REPLICATION_V, "Replication_Algorithm_For_Actual_Value")
        ReplicationValues.__init__(self)
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node
        if node.find_ms(ms, self.get_type()) is not None:
            found = True
            return node.get_ms_location(ms, self.get_type())
        elif node.find_ms(ms, REPLICATION_V) is not None:
            return node.get_ms_location(ms, REPLICATION)
        else:
            # look up the tree
            if node.is_root():
                return None

            found = False

            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                if node.find_ms(ms, self.get_type()) is not None:
                    found = True
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, self.get_type())
                elif node.find_ms(ms, REPLICATION) is not None:
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, REPLICATION)
                else:
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()

        return None

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        super(ReplicationValueAlgorithm, self).move_ms_to_node(ms, node)
        self.perform_replication(ms)

    ##################################################################################
    #
    #  Description: This performs the replication process
    #
    ##################################################################################
    def perform_replication(self, ms):
        it = iter(self.get_tree().get_leaf_nodes())
        for i in it:
            node = i
            while node is not None:
                lcmr = node.calculate_lcmr()
                rnode = node.get_ms_location(ms, REPLICATION)
                if lcmr < self.get_mins():
                    if rnode is not None:
                        node.set_ms_location(ms, None, REPLICATION)
                        if not self.get_tree().has_node_been_updated(node):
                            self.increment_update_count()
                            self.get_tree().add_node_update(node)
                        if node.get_ms_location(ms, REPLICATION_V) is None:
                            node.delete_all_ms_locations(ms)
                # for our topology, all nodes with a lcmr between mins <= lcmr < maxs will be replicated
                elif ((lcmr >= self.get_mins()) and (lcmr < self.get_maxs())) or (lcmr >= self.get_maxs()):
                    if (rnode is None) or (rnode is not ms.get_node(REPLICATION_V)):
                        node.add_ms_location(ms, ms.get_node(REPLICATION_V), REPLICATION)
                        if not self.get_tree().has_node_been_updated(node):
                            self.increment_update_count()
                            self.get_tree().add_node_update(node)
                node = node.get_parent_node()

    ##################################################################################
    #
    #  Description: This prints the dot information for the search list
    #
    ##################################################################################
    def print_dot_search(self, f, search_list, ms1, ms2):
        if len(search_list) > 1:
            for i in range(len(search_list)):
                j = i + 1
                if j >= len(search_list):
                    return
                text = str(search_list[i].get_name()) + " -- " + str(search_list[j].get_name())
                if search_list[i].get_ms_location(ms1, REPLICATION) is search_list[j]:
                    text = text + "[style=\"bold,dashed\",color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_ms_location(ms1, REPLICATION_V) is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")
                elif search_list[i].get_parent_node() is search_list[j]:
                    text = text + "[style=bold,color=red,label=\"S" + str(i) + "\"];"
                    f.write(text)
                    f.write("\n")