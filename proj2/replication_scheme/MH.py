from Algorithms import *
from AppCircle import *
from Queue import *
import time

##################################################################################
#
#  Class Description: This class represent a mobile subscribe
#
##################################################################################
class MH(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, name):
        self.__name = name
        self.__mss = None
        self.__gui = None
        self.__mode = "DOZE"
        self.set_mode("DOZE", "Initialization")
        self.__request_count = 0
        self.__request_q = Queue()

    ##################################################################################
    #
    #  Description: Set the name
    #
    ##################################################################################
    def set_name(self, name):
        self.__name = name

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
    def set_node(self, mss):
        self.set_mode("ACTIVE", "Moving")
        self.__mss = mss
        self.move_gui(self.get_node().get_gui_node())
        self.set_mode("DOZE", "Finished Move")
        return

    ##################################################################################
    #
    #  Description: Get the node of location type
    #
    ##################################################################################
    def get_node(self):
        return self.__mss

    def add_gui(self, gui):
        self.__gui = gui

    def get_gui(self):
        return self.__gui

    def move_gui(self, node):
        self.__gui.move(node)
        return

    def set_mode(self, mode, reason):
        self.__mode = mode
        print "MH %d is in %s Mode: %s" % (self.get_name(), self.__mode, reason)

    def get_mode(self):
        return self.__mode

    def request_token(self, mh, message=""):
        if self.get_node() is not None:
            #if self.__request_q.empty():
            self.__request_count += 1
            self.__request_q.put((self.get_node(), mh, message, self.__request_count))
            self.get_node().request_token(self, self.__request_count)
            #else:
            #    print "MH %d cannot request again until previous request is satisfied" % self.__name

    def send_message(self, mh, message="Happy Default Message from me"):
        self.set_mode("ACTIVE", "Request Token")
        self.request_token(mh, message)
        self.set_mode("DOZE", "Requested Token")

    def process_token(self, token):
        self.set_mode("ACTIVE", "Processing Token")
        self.__gui.token_node()
        self.__request_count = token.get_counter()
        q = Queue()
        service = True
        while not self.__request_q.empty():
            request = self.__request_q.get(False)
            if service and (request[3] <= token.get_counter()):
                self.__gui.search_line("green")
                self.get_node().send_message(request[1], request[2])
                time.sleep(1)
                self.get_node().release(self, request[3])
                service = False
            else:
                q.put(request)

        if not q.empty():
            del self.__request_q
            self.__request_q = q
        else:
            del q

        self.__gui.untoken_node()
        self.set_mode("DOZE", "Returned Token")

    def process_message(self, message):
        self.set_mode("ACTIVE", "Processing Message")
        self.__gui.search_line("green")
        self.__gui.message_node()
        print "MH %d - Received Message: %s" % (self.__name, message)
        time.sleep(1)
        self.__gui.unmessage_node()
        self.set_mode("DOZE", "Processed Message")

    def join(self, mss):
        if not self.__request_q.empty():
            q = Queue()
            while not self.__request_q.empty():
                request = self.__request_q.get(False)
                print "MH %d - Joining MSS %d" % (self.__name, mss.get_name())
                mss.inform_mss(self)
                q.put(request)

            del self.__request_q
            self.__request_q = q
