class LIXTable(object):
    def __init__(self, broadcast):
        self.__broadcast = broadcast.split(',')
        self.__lix_table = []
        self.__lix_values = []
        self.__lix_column = 0
        it = iter(self.__broadcast)
        for i in it:
            found = False
            jt = iter(self.__lix_table)
            for j in jt:
                if j[0] == i:
                    found = True
                    break
            if not found:
                self.__lix_table.append((i, []))
                self.__lix_values.append((i, [int(0), float(0.0), float(0.5)]))

    def update(self, data):
        it = iter(self.__lix_table)
        for i in it:
            if data == i[0]:
                i[1].append(self.__calculate_lix_value(data, len(i[1]) + 1))
            else:
                if len(i[1]) == 0:
                    i[1].append(float(0.0))
                else:
                    i[1].append(i[1][len(i[1]) - 1])

    def get_last_value(self, data):
        it = iter(self.__lix_table)
        for i in it:
            if i[0] == data:
                if len(i[1]) > 0:
                    return i[1][len(i[1]) - 1]
                else:
                    return 0.0

        return 0.0

    def __calculate_lix_value(self, data, time):
        it = iter(self.__lix_values)
        for i in it:
            if i[0] == data:
                i[1][1] = (i[1][2]/float(time - i[1][0])) + ((1.0 - i[1][2]) * i[1][1])
                i[1][0] = time
                return i[1][1]

    def print_info(self):
        if len(self.__lix_table[0][1]) == 0:
            return

        top_row = ["                      pi"]
        for i in range(len(self.__lix_table[0][1])):
            top_row.append("|   " + str(i + 1))
            if (i + 1) < 10:
                top_row.append("    ")
            else:
                top_row.append("   ")
        print "LIX Table:"
        print "%s" % ''.join(top_row)
        it = iter(self.__lix_table)
        for i in it:
            next_row = [i[0]]
            jt = iter(i[1])
            for j in jt:
                tmp = str(j)
                if len(tmp) > 6:
                    tmp = tmp[:6]
                else:
                    tmp = tmp + (' '*(6 - len(tmp)))
                next_row.append(tmp)
            print "                      %s" % " | ".join(next_row)



class LIX(object):
    def __init__(self, broadcast, client_data, disks, disks_frequency,  cache_size):
        self.__lix_table = LIXTable(broadcast)
        self.__broadcast = broadcast.split(',')
        self.__client_data = client_data.split(',')
        self.__disks = []
        self.__disks_frequency = []
        it = iter(disks)
        for i in it:
            self.__disks.append(i.split(','))
        it = iter(disks_frequency)
        for i in it:
            self.__disks_frequency.append(i)
        self.__cache_size = cache_size
        self.__cache = []
        for i in range(self.__cache_size):
            cache_row = []
            for j in range(len(self.__disks)):
                cache_row.append(' ')
            self.__cache.append(cache_row)
        self.__lix_step = 0

    def perform(self):
        print "\nPerforming LIX:                                    Started"
        print "     broadcast   : [ %s ]" % " | ".join(self.__broadcast)
        print "     client data : [ %s ]" % " | ".join(self.__client_data)
        self.__perform()
        print "Performing LIX:                                    Finished"

    def __perform(self):
        b = 0
        i = 0
        while i < len(self.__client_data):
            while True:
                self.__lix_table.update(self.__broadcast[b])
                if self.__client_data[i] == self.__broadcast[b]:
                    self.__client_data[i] = '[' + self.__client_data[i] + ']'
                    while (i + 1) < (len(self.__client_data)) and (self.__broadcast[b] == self.__client_data[i+1]):
                        i += 1
                        self.__client_data[i] = '[' + self.__client_data[i] + ']'
                    while ((i + 1) < len(self.__client_data)) and self.__data_in_cache(self.__client_data[i+1]):
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
        self.__lix_table.update(self.__broadcast[b])
        self.__print_info(b)

    def __increment(self, b):
        b += 1
        b %= len(self.__broadcast)

        return b

    def __add_to_cache(self, data):
        disk_number = self.__which_disk_contains(data)
        if self.__cache_is_full():
            self.__cache_remove_by_lix()
            self.__add_to_cache(data)
        else:
            i = 0
            tmp = self.__cache[i][disk_number]
            while (tmp != ' ') and (i < (self.__cache_size - 1)):
                tmp1 = self.__cache[i + 1][disk_number]
                self.__cache[i + 1][disk_number] = tmp
                tmp = tmp1
                i += 1
            self.__cache[0][disk_number] = data
            self.__sort_cache_disk(disk_number)

    def __sort_cache_disk(self, disk_number):
        if disk_number < len(self.__disks):
            for i in range(self.__cache_size - 1):
                for j in range(i+1, self.__cache_size):
                    if self.__lix_table.get_last_value(self.__cache[i][disk_number]) < self.__lix_table.get_last_value(self.__cache[j][disk_number]):
                        tmp = self.__cache[j][disk_number]
                        self.__cache[j][disk_number] = self.__cache[i][disk_number]
                        self.__cache[i][disk_number] = tmp

    def __which_disk_contains(self, data):
        for i in range(len(self.__disks)):
            if self.__disks[i].count(data) > 0:
                return i

    def __cache_is_full(self):
        count = 0
        it = iter(self.__cache)
        for i in it:
            jt = iter(i)
            for j in jt:
                if j != ' ':
                    count += 1

        return count >= self.__cache_size

    def __cache_move_to_top(self, data):
        disk_number = self.__which_disk_contains(data)
        if data == self.__cache[0][disk_number]:
            return

        i = 0
        found = False

        for i in range(self.__cache_size):
            if self.__cache[i][disk_number] == data:
                found = True
                break

        if found:
            while i > 0:
                self.__cache[i][disk_number] = self.__cache[i - 1][disk_number]
                i -= 1

            self.__cache[0][disk_number] = data

    def __data_in_cache(self, data):
        disk_number = self.__which_disk_contains(data)
        for i in range(self.__cache_size):
            if self.__cache[i][disk_number] == data:
                return True

        return False

    def __cache_remove_by_lix(self):
        if self.__cache_is_full():
            lix_value = 1.0
            disk_number = len(self.__disks)
            row_value = self.__cache_size + 1
            for i in range(len(self.__disks)):
                for j in range(self.__cache_size - 1, -1, -1):
                    if self.__cache[j][i] != ' ':
                        val = (self.__lix_table.get_last_value(self.__cache[j][i]))/self.__disks_frequency[i]
                        if val < lix_value:
                            disk_number = i
                            row_value = j
                            lix_value = val
                            break

            if disk_number != len(self.__disks):
                self.__cache[row_value][disk_number] = ' '

    def __print_info(self, b):
        self.__lix_step += 1
        print "\n\n\nLIX Step:             %d" % self.__lix_step
        disk_frequencies_print = []
        for i in range(1, len(self.__disks) + 1):
            disk_frequencies_print.append('D' + str(i) + ':' + str(self.__disks_frequency[i - 1]))
        print "LIX Disk Frequencies: %s" % "   ".join(disk_frequencies_print)
        self.__lix_table.print_info()
        self.__broadcast[b] = '[' + self.__broadcast[b] + ']'
        print "LIX Broadcast:        [ %s ]" % " | ".join(self.__broadcast)
        disk_print = []
        for i in range(1, len(self.__disks) + 1):
            disk_print.append('D' + str(i))
        self.__broadcast[b] = self.__broadcast[b].strip('[]')
        print "LIX Cache(%d):           %s" % (self.__cache_size, "  ".join(disk_print))
        for i in range(len(self.__cache)):
            print "                      [ %s ]" % " | ".join(self.__cache[i])
        print "LIX Client Data:      [ %s ]" % " | ".join(self.__client_data)

        raw_input('\nPress Enter Key to Continue:')
        print "\n"
