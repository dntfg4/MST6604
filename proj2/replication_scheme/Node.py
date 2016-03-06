from Constants import *
from Tree import *
from Token import *
from Queue import *


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
        self.__mh_list = {}
        self.__gui_node = None
        self.__token = None
        self.__request = Queue()
        self.__tree = None
        self.__undeliverable = Queue()

    def set_tree(self, tree):
        self.__tree = tree

    def add_gui_node(self, gn):
        self.__gui_node = gn

    def get_gui_node(self):
        return self.__gui_node

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

    ##################################################################################
    #
    #  Description: Add the parent node
    #
    ##################################################################################
    def add_parent_node(self, parent):
        self.__parent_node = parent

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
    def __find_ms(self, ms):
        it = iter(self.__mh_list)
        for i in it:
            if ms is self.__mh_list[i][MOBILE_STATION]:
                return i

        return None

    ##################################################################################
    #
    #  Description: Create a new index for ms in the list
    #
    ##################################################################################
    def __get_new_ms_list_index(self):
        i = 0
        it = iter(self.__mh_list)
        for j in it:
            if i <= j:
                i = j + 1
        return i

    ##################################################################################
    #
    #  Description: Add an ms to the node
    #
    ##################################################################################
    def __add_ms(self, ms):
        if self.__find_ms(ms) is None:
            l = self.__get_new_ms_list_index()
            self.__mh_list[l] = {}
            self.__mh_list[l][MOBILE_STATION] = ms
            self.__mh_list[l][LOCATION] = None

    ##################################################################################
    #
    #  Description: Does the node contain ms
    #
    ##################################################################################
    def contains_ms(self, ms):
        return self.__find_ms(ms) is None

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
    def add_ms_location(self, ms, loc):
        if self.__find_ms(ms) is None:
            self.__add_ms(ms)
            i = self.__find_ms(ms)
            self.__mh_list[i][LOCATION] = loc
            return True
        else:
            return self.set_ms_location(ms, loc)

    ##################################################################################
    #
    #  Description: The ms joins the Node
    #
    ##################################################################################
    def join(self, ms, loc):
        node = self.add_ms_location(ms, loc)
        ms.join(self)

    ##################################################################################
    #
    #  Description: Set the ms location type
    #
    ##################################################################################
    def set_ms_location(self, ms, loc):
        i = self.__find_ms(ms)
        if i is not None:
            self.__mh_list[i][LOCATION] = loc
            return True

        return False

    ##################################################################################
    #
    #  Description: The the ms location type
    #
    ##################################################################################
    def get_ms_location(self, ms):
        i = self.__find_ms(ms)
        if i is not None:
            return self.__mh_list[i][LOCATION]

        return None

    ##################################################################################
    #
    #  Description: Delete the ms from the node
    #
    ##################################################################################
    def delete_ms(self, ms):
        i = self.__find_ms(ms)
        if i is not None:
            del self.__mh_list[i]
        return True

    ##################################################################################
    #
    #  Description: The ms leaves the node
    #
    ##################################################################################
    def leave(self, ms):
        i = self.__find_ms(ms)
        if i is not None:
            del self.__mh_list[i]
        return True

    def clear_node_gui_search(self):
        if self.is_leaf():
            if self.__gui_node is not None:
                self.__gui_node.clear_line()
            return

        it = iter(self.__children_node)
        for i in it:
            i.clear_node_gui_search()

        if self.__gui_node is not None:
            self.__gui_node.clear_line()

        return

    def clear_node_gui_update(self):
        if self.is_leaf():
            if self.__gui_node is not None:
                self.clear_node()
            return

        it = iter(self.__children_node)
        for i in it:
            i.clear_node_gui_update()

        if self.__gui_node is not None:
            self.clear_node()
        return

    def token_node(self):
        if self.__gui_node is not None:
            self.__gui_node.token_node()

    def untoken_node(self):
        if self.__gui_node is not None:
            self.__gui_node.untoken_node()

    def clear_node(self):
        if self.__gui_node is not None:
            self.__gui_node.clear_node()

    def receive_token(self, token):
        self.__token = token
        self.token_node()
        q = Queue()
        while not self.__request.empty():
            request = self.__request.get(False)
            if (self.__find_ms(request[1]) is not None) and (request[2] <= self.__token.get_counter()):
                print "Token MSS %d grants token to MH %d" % (self.__name, request[1].get_name())
                self.grant_process_token(self.__token, request[1])
            else:
                q.put(request)

        if not q.empty():
            del self.__request
            self.__request = q
        else:
            del q

    def release(self, mh, count):
        it = self.__tree.get_ring_nodes()

        for i in it:
            if i is not self:
                i.delete_request(mh, count)

    def delete_request(self, mh, count):
        q = Queue()
        while not self.__request.empty():
            request = self.__request.get(False)
            if not ((request[1] is mh) and (request[3] == count)):
                q.put(request)
                print "MSS %d deleting request: mh=%d, count=%d" % (self.__name, mh.get_name(), count)

        if not q.empty():
            del self.__request
            self.__request = q
        else:
            del q

    def grant_process_token(self, token, mh):
        if self.__token is None:
            self.token_node()
        mh.process_token(token)
        if self.__token is None:
            self.untoken_node()

    def return_token(self):
        token = self.__token
        self.__token = None
        self.untoken_node()
        return token

    def request_token(self, mh, count):
        self.__perform_phase1(mh, count)
        self.__request.put((self, mh, count, 0))

    def send_message(self, ms, message):
        node = self.__tree.query_ms_location_from_node(ms, self)
        if node is not None:
            node.receive_message(ms, message)

    def __perform_phase1(self, mh, count):
        it = self.__tree.get_ring_nodes()
        priority = -1

        for i in it:
            if i is not self:
                pr = i.receive_remote_request(mh, count)
                if pr > priority:
                    priority = pr

        it = self.__tree.get_ring_nodes()
        for i in it:
            if i is not self:
                pr = i.receive_remote_priority_request(mh, count, pr)

        return

    def perform_phase2(self, mh, count):
        return

    def receive_remote_request(self, mh, count):
        print "MSS %d got remote request of MH %d with count=%d" % (self.__name, mh.get_name(), count)
        self.__undeliverable.put((mh, count))
        return self.__determine_priority()

    def __determine_priority(self):
        q = Queue()
        priority = -1
        while not self.__request.empty():
            request = self.__request.get(False)
            if request[3] > priority:
                priority = request[3]
            q.put(request)
        del self.__request
        self.__request = q
        return priority + 1

    def receive_remote_priority_request(self, mh, count, priority):
        print "MSS %d moving undeliverable request to deliverable" % self.__name
        q = Queue()

        while not self.__undeliverable.empty():
            request = self.__undeliverable.get(False)
            if (request[0] is mh) and (request[1] == count):
                self.__request.put((self,request[0], request[1], priority))
                break
            else:
                q.put(request)

        while not q.empty():
            request = q.get(False)
            self.__undeliverable.put(request)

        del q

        self.__sort_requests()

    def __sort_requests(self):
        print "MSS %d resorting requests based on priority" % self.__name
        requests = {}
        i = 0
        while not self.__request.empty():
            requests[i] = self.__request.get(False)

        i = 0
        for i in range(len(requests)):
            j = i + 1
            while j < len(requests):
                print requests[i][3]
                if requests[i][3] < requests[j][3]:
                    tr = requests[i]
                    requests[i] = requests[j]
                    requests[j] = tr
                else:
                    j += 1

        for i in range(len(requests)):
            self.__request.put(requests[i])

        return

    def receive_message(self, ms, message):
        i = self.__find_ms(ms)
        if i is not None:
            self.__mh_list[i][MOBILE_STATION].process_message(message)

    def inform_mss(self, mh):
        print "MSS %d - MH %d joined" % (self.__name, mh.get_name())
