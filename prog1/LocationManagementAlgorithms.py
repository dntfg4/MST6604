'''Location Management Algorithms:
        This program contains algorithms determining search and updates for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/17 12:00:00 $'
__copyright__ = '2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

from LocationManagementConstants import *
from LocationManagementMisc import *

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
        # get the node
        node = self.get_tree().get_node(name)

        # query the find the ms location
        return self.query_ms_location_from_node(ms, node)

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        # init the search count for this search
        self.set_search_count(0)

        found = False

        # if node is None, return
        if node is None:
            return node

        # check the node to see if the ms is in it
        if node.get_ms_location(ms, self.get_type()) is not None:
            found = True
            return node.get_ms_location(ms, self.get_type())
        else:
            # if this is the root node return node as ms is not in it, but this should never happen
            if node.is_root():
                return None

            found = False

            # get the parent and increment the search count
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            # Go up the tree until the ms node is found in the tree
            while not found:
                if node.get_ms_location(ms, self.get_type()) is not None:
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, self.get_type())
                else:
                    # if not the root node, get the parent
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()
                    else:
                        return None

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
        # initialize the update count for this move
        self.set_update_count(0)

        # get the ms node for this algorithm
        ms_node = ms.get_node(self.get_type())

        # check if the ms is in node
        if ms_node is node:
            return

        # find the lca of ms_node and node
        lca = self.get_tree().get_lca(ms_node, node)

        # while ms_node is not the lca, go up the tree and remove ms from the node
        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()


        ms_node = node

        # from the node to where ms is being moved, add the ms up the tree including the root node
        while ms_node is not None:
            ms_node_parent = ms_node.get_parent_node()
            ms_node.add_ms_location(ms, node, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        # tell ms about its current node
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
        if node is node.get_ms_location(ms, self.get_type()):
            return node

        # look up the tree
        if not found:
            # if node is the root node, return
            if node.is_root():
                return None

            found = False

            # get the parent node
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            # while the ms has not been found and we have not passed the root node (should not happen),
            # search up the tree
            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if node.get_ms_location(ms, self.get_type()) is not None:
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # if we found the node which has ms, search down the tree for ms
        if found:
            # if this node contains ms, return the node
            if node is node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                return node

            # while ms is not in the node, follow down the tree until the ms is found
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
        ms_node = ms.get_node(self.get_type())

        # if ms_node is empty, the update failed and return
        if ms_node is node:
            return

        # get the lca of the ms_node and node (where the ms is moving)
        lca = self.get_tree().get_lca(ms_node, node)

        # while the ms_node is not the lca, move up the tree
        while lca is not ms_node:
            ms_node.delete_ms_location(ms, self.get_type())
            self.get_tree().add_node_update(ms_node)
            ms_node = ms_node.get_parent_node()
            self.increment_update_count()

        ms_node = node

        # while the node (where ms is going) is not the lca and its parent is not lca,
        # add the ms to the node and move up the tree
        while (lca is not ms_node) and (lca is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(ms_node_parent)

        # add the last checked node to as the ms pointer node to the lca
        lca.set_ms_location(ms, ms_node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(lca)

        # add ms to node (where is the ms is going)
        node.add_ms_location(ms, node, self.get_type())
        self.increment_update_count()
        self.get_tree().add_node_update(node)
        # tell ms what node it is in
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

        # starting a ms_node, determine how many forward pointers have been created
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
        # from ms_node, re-trace the path to the root node and remove the ms from the nodes
        # do not adjust the root node
        while not ms_node.is_root():
            prev_node = ms_node.get_ms_location(ms, self.__reverse_type)
            if prev_node is None:
                prev_node = ms_node.get_parent_node()
            ms_node.delete_all_ms_locations(ms)
            self.increment_update_count()
            self.get_tree().add_node_update(prev_node)
            self.get_tree().delete_forwarding_update(ms_node)
            ms_node = prev_node

        # remove the forwarding type and put the ms in this location
        ms_node.add_ms_location(ms, None, self.__forwarding_type)
        ms_node.add_ms_location(ms, ms_node, self.get_type())
        self.get_tree().add_node_update(ms_node)
        self.get_tree().delete_forwarding_update(ms_node)
        ms.set_node(ms_node,self.get_type())
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        # initialize the search count for this search
        self.set_search_count(0)

        found = False

        # if node is None, search failed and return
        if node is None:
            return node

        # check if the ms is in this node
        # if it is, return the node
        if node is node.get_ms_location(ms, self.get_type()):
            return node

        # look up the tree
        if not found:
            # if this is the root node, return None
            if node.is_root():
                return None

            # get the parent node
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            # while the ms is not found and node is not None, search up the tree
            # if the node points or forward points to the ms, we have found the node
            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if (node.get_ms_location(ms, self.__forwarding_type) is not None) or (node.get_ms_location(ms, self.get_type()) is not None):
                    found = True
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # If we found the node on the search up, now search down to find ms
        if found:
            # if ms is contained in the node, return the node
            if node is node.get_ms_location(ms, self.get_type()):
                self.get_tree().add_node_search(node)
                return node

            # while ms is not in the node, follow the pointers and forwarding pointers to find the node with ms
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
        # initialize the update count
        self.set_update_count(0)

        # get the ms node
        ms_node = ms.get_node(self.get_type())

        # if error condition, return
        if (node is None) or (ms_node is None) or (ms_node is node):
            return

        # determine if the number of maximum forwards are reached
        if self.get_current_forwards_count(ms, ms_node) >= self.__max_forwards:
            # purge the pointers
            self.purge_current_pointers(ms, ms_node)
            current_update_count = self.get_update_count()
            # move using the Pointer Algorithm
            super(ForwardingPointerPAlgorithm, self).move_ms_to_node(ms, node)
            self.set_update_count(current_update_count + self.get_update_count())
            return

        # get the lca
        lca = self.get_tree().get_lca(ms_node, node)
        # determine the tree level node for the ms
        level_node_ms = self.determine_forwarding_level_node(ms_node, lca)
        # determine the tree level node for the destination node
        level_node = self.determine_forwarding_level_node(node, lca)

        # if level node is ms node or a loop will occur,
        # purge the pointers and perform the Pointer Algorithm
        if (level_node_ms is ms_node) or (level_node_ms.get_ms_location(ms, self.__reverse_type) is not None) or (level_node.get_ms_location(ms,self.__forwarding_type) is not None):
            self.purge_current_pointers(ms, ms_node)
            current_update_count = self.get_update_count()
            super(ForwardingPointerPAlgorithm, self).move_ms_to_node(ms, node)
            self.set_update_count(current_update_count + self.get_update_count())
            return

        # determine the tree level node for the destination node
        level_node = self.determine_forwarding_level_node(node, lca)

        # from ms node upto the tree level node for the ms
        # remove ms from the node
        while level_node_ms is not ms_node:
            next_node = ms_node.get_ms_location(ms, self.__reverse_type)
            if next_node is None:
                next_node = ms_node.get_parent_node()

            ms_node.delete_all_ms_locations(ms)
            self.get_tree().add_node_update(ms_node)
            self.increment_update_count()
            ms_node = next_node

        ms_node = node

        # for the nodes between the tree level node for the destination node and the destination node,
        # add the ms into the node
        while (level_node is not ms_node) and (level_node is not ms_node.get_parent_node()):
            ms_node_parent = ms_node.get_parent_node()
            ms_node_parent.delete_all_ms_locations(ms)
            ms_node_parent.add_ms_location(ms, ms_node, self.get_type())
            ms_node = ms_node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(ms_node_parent)

        # add the ms in to the tree level node for the destination node
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

        if node is not level_node:
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
    def determine_forwarding_level_node(self, node, lca):
        # set the initial threshold lcmr to determine the forwarding node
        tcmr = 1

        # initialize the forwarding node
        fnode = node

        # while not the lca, check the lcmr versus the tcmr and set the fnode if needed
        while node is not lca:
            lcmr = node.calculate_lcmr()

            # if the lcmr is greater than the current threshold, update the forwarding node
            if lcmr > tcmr:
                fnode = node

            # get the parent node
            node = node.get_parent_node()

            # increment the threshold lcmr for the next level
            tcmr += 1

        # return the forwarding node
        return fnode

    ##################################################################################
    #
    #  Description: This determines the current number of forwards ms has.
    #
    ##################################################################################
    def determine_number_of_forwards(self,ms):
        forwards = 0
        node = ms.get_node(self.get_type())

        # from node, re-trace the route to determine the number of forwards
        while not node.is_root():
            if node.get_ms_location(ms, self.get_type()) is not None:
                node = node.get_parent()
            else:
                node = node.get_ms_location(ms, self.__reverse_type)
                forwards += 1

        return forwards

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

        # re-trace the route to determine the current number of forwards for ms
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

        # from ms_node, retrace the route to delete all of the forwarding pointers
        while ms_node.get_ms_location(ms, self.__reverse_type) is not None:
            prev_node = ms_node.get_ms_location(ms, self.__reverse_type)

            # get lca between ms_node and the previous node
            lca = self.get_tree().get_lca(prev_node, ms_node)

            # remove ms from ms_node upto the lca
            while lca is not ms_node:
                ms_node.delete_all_ms_locations(ms)
                ms_node = ms_node.get_parent_node()
                self.increment_update_count()
                self.get_tree().add_node_update(ms_node)
                self.get_tree().delete_forwarding_update(ms_node)
            ms_node = prev_node

        # remove the forwarding type and put the ms in this location
        ms_node.add_ms_location(ms, None, self.__forwarding_type)
        ms_node.add_ms_location(ms, ms_node, self.get_type())
        self.get_tree().add_node_update(ms_node)
        self.get_tree().delete_forwarding_update(ms_node)
        ms.set_node(ms_node,self.get_type())
        return

    ##################################################################################
    #
    #  Description: This searches for the node which contains the ms starting from node and returns the node
    #
    ##################################################################################
    def query_ms_location_from_node(self, ms, node):
        # initialize this search count
        self.set_search_count(0)

        found = False

        # if node is None, return
        if node is None:
            return node

        # check if ms is in the current node
        if (node.get_ms_location(ms, self.get_type()) is not None) and (node.get_ms_location(ms, self.__forwarding_type) is None):
            return node
        # if the node contains a forwarding pointer for ms, follow the forwarding pointers until the
        # node which contains the ms is found
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
            # look up the tree for ms
            # if this is the root node, return
            if node.is_root():
                return None

            found = False

            # get this parent node
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            # look up the tree until we find the ms
            while not found:
                # check if ms is in the node
                if node.get_ms_location(ms, self.get_type()) is not None:
                    self.get_tree().add_node_search(node)
                    found = True
                else:
                    # if not the root node, get the parent
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()

            self.get_tree().add_node_search(node)
            node = node.get_ms_location(ms, self.get_type())
            self.increment_search_count()

            # if this node has a forwarding pointer, follow it until we find the node with ms in it
            if node.get_ms_location(ms, self.__forwarding_type) is not None:
                self.get_tree().add_node_search(node)
                node = node.get_ms_location(ms, self.__forwarding_type)
                self.increment_search_count()
                self.get_tree().add_node_search(node)
                # if this node has a forwarding pointer, follow it until we find the node with ms in it
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
        # initialize the update count
        self.set_update_count(0)

        # get the ms ndoe
        ms_node = ms.get_node(self.get_type())

        # if the ms node is the node, return
        if ms_node is node:
            return

        # if the ms has greater than or equal to the maximum number of forwards,
        # purge the pointers move using the Actual Value Algorithms
        if self.get_current_forwards_count(ms, ms_node) >= self.__max_forwards:
            self.purge_current_pointers(ms, ms_node)
            current_update_count = self.get_update_count()
            super(ForwardingPointerVAlgorithm, self).move_ms_to_node(ms, node)
            self.set_update_count(current_update_count + self.get_update_count())
            return

        # if we have a loop, remove enough forwarding pointers to continue
        if node.get_ms_location(ms, self.__forwarding_type) is not None:
            self.remove_pre_loop_items(ms, node)

        # ms node has a forwarding pointer, remove the forwarding pointer and update the ms location in node
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
        level_node = self.determine_forwarding_level_node(node, lca)

        tmp_node = node

        while (level_node is not tmp_node):
            node_parent = tmp_node.get_parent_node()
            node_parent.add_ms_location(ms, node, self.get_type())
            tmp_node = node_parent
            self.increment_update_count()
            self.get_tree().add_node_update(node_parent)

        ms.set_node(node, self.get_type())
        return

    ##################################################################################
    #
    #  Description: This returns the current forwarding level
    #
    ##################################################################################
    def determine_forwarding_level_node(self, node, lca):
        # set the initial threshold lcmr to determine the forwarding node
        tcmr = 1

        # initialize the forwarding node
        fnode = node

        # while not the lca, check the lcmr versus the tcmr and set the fnode if needed
        while node is not lca:
            lcmr = node.calculate_lcmr()

            # if the lcmr is greater than the current threshold, update the forwarding node
            if lcmr > tcmr:
                fnode = node

            # get the parent node
            node = node.get_parent_node()

            # increment the threshold lcmr for the next level
            tcmr += 1

        # return the forwarding node
        return fnode

    ##################################################################################
    #
    #  Description: This removes the pre_loop condition for forwards
    #
    ##################################################################################
    def remove_pre_loop_items(self, ms, node):
        # get the ms node
        ms_node = ms.get_node(self.get_type())

        tmp_node = ms_node
        prev_node = tmp_node.get_ms_location(ms, self.__reverse_type)

        # follow the reverse pointers to remove the loop condition
        while tmp_node is not node:
            lca = self.get_tree().get_lca(prev_node, tmp_node)

            # remove ms from the neccessary nodes up the tree
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
        # initialize the search count
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node for a replication
        if node.get_ms_location(ms, REPLICATION) is not None:
            return node.get_ms_location(ms, REPLICATION)
        elif node.get_ms_location(ms, self.get_type()) is not None:
            found = True

            # if this node has the ms, return it
            if node is node.get_ms_location(ms, self.get_type()):
                return node

        # look up the tree
        if not found:
            if node.is_root():
                return None

            found = False

            # get the parent
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            # search up the tree for a replication or the node which has the ms node value
            while (not found) and (node is not None):
                self.get_tree().add_node_search(node)
                if node.get_ms_location(ms, REPLICATION) is not None:
                    return node.get_ms_location(ms, REPLICATION)
                elif node.get_ms_location(ms, self.get_type()) is not None:
                    found = True
                    if node is node.get_ms_location(ms, self.get_type()):
                        self.get_tree().add_node_search(node)
                        return node
                else:
                    node = node.get_parent_node()
                    self.increment_search_count()

        # if we did not find it, look down the tree for a replication or the node which contains the ms
        if found:
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
        # move the ms to node using the Pointer Algorithm
        super(ReplicationPointerAlgorithm, self).move_ms_to_node(ms, node)
        # replicate where neccessary
        self.perform_replication(ms)

    ##################################################################################
    #
    #  Description: This performs the replication process
    #
    ##################################################################################
    def perform_replication(self, ms):
        # for each leaf node, look up the tree to determine which node will contain the replication
        it = iter(self.get_tree().get_leaf_nodes())
        for i in it:
            node = i
            while node is not None:
                # calculate the lcmr for this node
                lcmr = node.calculate_lcmr()
                rnode = node.get_ms_location(ms, REPLICATION)
                # if lcrm is less than mins
                if lcmr < self.get_mins():
                    # if the node has a replication remove it
                    if rnode is not None:
                        # remove any replication
                        node.set_ms_location(ms, None, REPLICATION)
                        if not self.get_tree().has_node_been_updated(node):
                            self.increment_update_count()
                            self.get_tree().add_node_update(node)
                        # if this node does not have a pointer, remove any trace of ms from the node
                        if node.get_ms_location(ms, REPLICATION_P) is None:
                            node.delete_all_ms_locations(ms)
                # for our topology, all nodes with a lcmr between mins <= lcmr < maxs will be replicated
                elif ((lcmr >= self.get_mins()) and (lcmr < self.get_maxs())) or (lcmr >= self.get_maxs()):
                    if (rnode is None) or (rnode is not ms.get_node(REPLICATION_P)):
                        node.add_ms_location(ms, ms.get_node(REPLICATION_P), REPLICATION)
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
        # initialize the search count
        self.set_search_count(0)

        found = False

        if node is None:
            return node

        # check the node for replication or the node containing the ms
        if node.get_ms_location(ms, REPLICATION) is not None:
            return node.get_ms_location(ms, REPLICATION)
        elif node.get_ms_location(ms, self.get_type()) is not None:
            return node.get_ms_location(ms, self.get_type())
        else:
            # search for the ms
            # look up the tree
            if node.is_root():
                return None

            found = False

            # get the parent node
            self.get_tree().add_node_search(node)
            node = node.get_parent_node()
            self.increment_search_count()

            while not found:
                # look for a replication
                if node.get_ms_location(ms, REPLICATION) is not None:
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, REPLICATION)
                # check the node to see if it contains the ms
                elif node.get_ms_location(ms, self.get_type()) is not None:
                    self.get_tree().add_node_search(node)
                    return node.get_ms_location(ms, self.get_type())
                else:
                    if not node.is_root():
                        self.get_tree().add_node_search(node)
                        node = node.get_parent_node()
                        self.increment_search_count()
                    else:
                        return None

        return None

    ##################################################################################
    #
    #  Description: This moves ms to node
    #
    ##################################################################################
    def move_ms_to_node(self, ms, node):
        # move the node based on the Value Algorithms
        super(ReplicationValueAlgorithm, self).move_ms_to_node(ms, node)
        # replicate as neccessary
        self.perform_replication(ms)

    ##################################################################################
    #
    #  Description: This performs the replication process
    #
    ##################################################################################
    def perform_replication(self, ms):
        # for each leaf node, go up the tree to determine which nodes contain a replication
        it = iter(self.get_tree().get_leaf_nodes())
        for i in it:
            node = i
            while node is not None:
                # calculate the lcmr
                lcmr = node.calculate_lcmr()
                rnode = node.get_ms_location(ms, REPLICATION)
                # if the lcmr is less than mins, remove any replication
                if lcmr < self.get_mins():
                    # if the node contains a replication
                    if rnode is not None:
                        # remove the replication
                        node.set_ms_location(ms, None, REPLICATION)
                        if not self.get_tree().has_node_been_updated(node):
                            self.increment_update_count()
                            self.get_tree().add_node_update(node)
                        # if the node only had a replication, remove any trace of ms in the node
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