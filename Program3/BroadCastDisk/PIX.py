class PIX(object):
    def __init__(self, broadcast, client_data, cache_size):
        self.__broadcast = broadcast.split(',')
        self.__client_data = client_data.split(',')
        self.__broadcast_frequencies = []
        self.__client_data_access_probabilities = []
        self.__pix_values = []
        self.__cache_size = cache_size
        self.__cache = []
        for i in range(self.__cache_size):
            self.__cache.append('')
        self.__pix_step = 0

    def perform(self):
        print "\nPerforming PIX:                                    Started"
        print "     broadcast   : [ %s ]" % " | ".join(self.__broadcast)
        print "     client data : [ %s ]" % " | ".join(self.__client_data)

        self.__calculate_broadcast_frequencies()
        self.__calculate_client_data_access_probabilities()
        self.__calculate_pix_values()
        self.__perform()
        print "Performing PIX:                                    Finished"

    def __calculate_broadcast_frequencies(self):
        print "\nCalculating Broadcast Frequencies                  Started"
        it = iter(self.__client_data)
        for i in it:
            if self.__new_client_data_item(i):
                self.__broadcast_frequencies.append((i, self.__broadcast.count(i)))

        print self.__broadcast_frequencies
        print "Calculating Broadcast Frequencies                  Finished"

    def __calculate_client_data_access_probabilities(self):
        print "\nCalculating Client Data Access Probabilities        Started"
        it = iter(self.__client_data)
        for i in it:
            if self.__new_client_data_access_probability(i):
                self.__client_data_access_probabilities.append((i, float(self.__client_data.count(i))/float(len(self.__client_data))))

        print self.__client_data_access_probabilities
        print "Calculating Client Data Access Probabilities       Finished"

    def __calculate_pix_values(self):
        print "\nCalculating PIX values                             Started"
        it = iter(self.__client_data_access_probabilities)

        for i in it:
            jt = iter(self.__broadcast_frequencies)

            for j in jt:
                if i[0] == j[0]:
                    self.__pix_values.append((i[0], i[1]/j[1]))
                    break

        print self.__pix_values
        print "Calculating PIX values                             Finished"

    def __new_client_data_item(self, data_item):
        it = iter(self.__broadcast_frequencies)
        for i in it:
            if i[0] == data_item:
                return False

        return True

    def __new_client_data_access_probability(self, data_item):
        it = iter(self.__client_data_access_probabilities)
        for i in it:
            if i[0] == data_item:
                return False

        return True

    def __perform(self):
        b = 0
        i = 0
        while i < len(self.__client_data):
            while True:
                if self.__client_data[i] == self.__broadcast[b]:
                    self.__client_data[i] = '[' + self.__client_data[i] + ']'
                    while (i + 1) < (len(self.__client_data)) and (self.__broadcast[b] == self.__client_data[i+1]):
                        i += 1
                        self.__client_data[i] = '[' + self.__client_data[i] + ']'
                    while ((i + 1) < len(self.__client_data)) and self.__in_cache(self.__client_data[i+1]):
                        i += 1
                        self.__cache_move_to_top(self.__client_data[i])
                        self.__client_data[i] = '[' + self.__client_data[i] + ']'
                    i += 1
                    self.__print_info(b)
                    self.__add_to_cache(self.__broadcast[b])
                    b = self.__increment(b)
                    break

                self.__print_info(b)
                b = self.__increment(b)

    def __add_to_cache(self, data):
        if self.__cache.count('') == 0:
            if self.__cache_remove_by_pix(data):
                self.__add_to_cache(data)
        else:
            i = 0
            tmp = self.__cache[i]
            while (tmp != '') and (i < (len(self.__cache) - 1)):
                tmp1 = self.__cache[i + 1]
                self.__cache[i + 1] = tmp
                tmp = tmp1
                i += 1
            self.__cache[0] = data

    def __increment(self, b):
        b += 1
        b %= len(self.__broadcast)

        return b

    def __in_cache(self, data):
        for i in range(len(self.__cache)):
            if data == self.__cache[i]:
                return True

        return False

    def __cache_move_to_top(self, data):
        if data == self.__cache[0]:
            return

        i = 0
        found = False

        for i in range(len(self.__cache)):
            if self.__cache[i] == data:
                found = True
                break

        if found:
            while i > 0:
                self.__cache[i] = self.__cache[i - 1]
                i -= 1

            self.__cache[0] = data

    def __cache_remove_by_pix(self, data):
        pix_value = self.__get_pix_value(data)
        pix_loc = self.__cache_size + 1

        for i in range(len(self.__cache)):
            if self.__get_pix_value(self.__cache[i]) < pix_value:
                pix_value = self.__get_pix_value(self.__cache[i])
                pix_loc = i

        while pix_loc < (len(self.__cache) - 1):
            self.__cache[pix_loc] = self.__cache[pix_loc + 1]
            pix_loc += 1

        if pix_loc < (self.__cache_size + 1):
            self.__cache[pix_loc]=''
            return True
        else:
            return False

    def __get_pix_value(self, data):
        it = iter(self.__pix_values)
        for i in it:
            if data == i[0]:
                return i[1]

        return 0.0

    def __print_info(self, b):
        self.__pix_step += 1
        print "\nPIX Step:             %d" % self.__pix_step
        print "PIX Value:            %s" % self.__pix_values
        self.__broadcast[b] = '[' + self.__broadcast[b] + ']'
        print "PIX Broadcast:        [ %s ]" % " | ".join(self.__broadcast)
        self.__broadcast[b] = self.__broadcast[b].strip('[]')
        print "PIX Cache(%d):         [ %s ]" % (self.__cache_size, " | ".join(self.__cache))
        print "PIX Client Data:      [ %s ]" % " | ".join(self.__client_data)

        raw_input('\nPress Enter Key to Continue:')
        print "\n"
