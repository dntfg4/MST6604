import time
import threading
from Tree import *
from Token import Token


class TokenRingThread(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, token_nodes, wait=2):
        super(TokenRingThread, self).__init__()
        self.__token_nodes = token_nodes
        self.__stoprequest = threading.Event()
        self.__token = Token()
        self.__wait = wait

    def set_wait_time(self, wait):
        self.__wait = wait
        if self.__wait < 1:
            self.__wait = 1

    def grant_token(self, node):
        node.receive_token(self.__token)

    def retrieve_token(self, node):
        self.__token = node.return_token()

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so __stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.__stoprequest.isSet():
            try:
                it = iter(self.__token_nodes)
                self.__token.increment_counter()
                print "token counter = %d" % self.__token.get_counter()

                for i in it:
                    print "Token Ring Grant MSS %d" % i.get_name()
                    self.grant_token(i)
                    time.sleep(self.__wait)
                    self.retrieve_token(i)

            except:
                continue

    def join(self, timeout=None):
        self.__stoprequest.set()
        super(TokenRingThread, self).join(timeout)