class LIX(object):
    def __init__(self, user_input, broadcast, client_data):
        self.__user_input = user_input
        self.__broadcast = broadcast
        self.__client_data = client_data.split(',')

    def perform(self):
        # print "LIX:"
        # print "     broadcast   : [ %s ]" % " | ".join(self.__broadcast)
        # print "     client data : [ %s ]" % " | ".join(self.__client_data)
        # print "User Input:"
        # it = iter(self.__user_input)
        # for i in it:
        #     print "(%s, %0.6f)" % (i[0], i[1])
        print "\nPerforming LIX:                                    Started"
        print "Performing LIX:                                    Finished"