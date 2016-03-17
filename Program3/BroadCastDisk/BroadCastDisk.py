import math
from Disk import Disk


class BroadCastDisk(object):
    def __init__(self):
        self.__values = []
        self.__disks = []
        self.__length = 0

    def add_data(self, data, percentage):
        self.__values.append((data, percentage))

    def get_number_of_data(self):
        return len(self.__values)

    def get_data_index(self, p):
        if p < len(self.__values):
            return self.__values[p]

    def generate_schedule(self):
        print "Input Data and Percentages (%d items):" % len(self.__values)
        it = iter(self.__values)
        for i in it:
            print " (%s:%f)" % (i[0], i[1])

        self.__sort()
        self.__generate_disks()
        self.__generate_frequencies()
        length = self.__determine_length()
        self.__determine_spacing(length)
        max_chunks = self.__generate_chunks()
        broadcast = self.__generate_broadcast(max_chunks)
        self.__print_info(max_chunks, broadcast)

        return broadcast

    def __gcd(self, a, b):
        if b == 0:
            return a
        else:
            return self.__gcd(b, a % b)

    def __lcm(self, a, b):
        return (a * b)/self.__gcd(a, b)

    def __calculate_lcm(self):
        llcm = 0
        print "\nCalculating LCM:                                   Started"
        if len(self.__disks) > 1:
            llcm = self.__lcm(self.__disks[0].get_frequency(), self.__disks[1].get_frequency())

            for i in range(2, len(self.__disks)):
                llcm = self.__lcm(self.__disks[i].get_frequency(), llcm)
        elif len(self.__disks) > 0:
            llcm = self.__disks[0].get_frequency()

        print "Calculating LCM:                                   Finished"
        print "LCM: %d" % llcm
        return llcm

    def __generate_broadcast(self, max_chunks):
        print "\nGenerating broadcast:                                Started"
        broadcast = []
        for i in range(max_chunks):
            for j in range(len(self.__disks)):
                k = i % self.__disks[j].get_number_of_chunks()
                chunk = self.__disks[j].get_chunk(k)
                if chunk is not None:
                    for l in range(len(chunk)):
                        broadcast.append(chunk[l])
        print "Generating broadcast:                                Finished"
        return broadcast

    def __determine_length(self):
        print "\nDetermining broadcast length:                      Started"
        length = 0
        it = iter(self.__disks)
        for i in it:
            length += (i.get_number_of_data() * i.get_frequency())

        print "Determining broadcast length:                      Finished"
        print "Broadcast length: %d" % length
        return length

    def __determine_spacing(self, length):
        it = iter(self.__disks)
        for i in it:
            i.set_spacing(length/i.get_frequency())

    def __generate_chunks(self):
        max_chunks = self.__calculate_lcm()
        print "\nGenerating chunks:                                 Started"
        print "Maximum number of chunks on a disk: %d" % max_chunks
        it = iter(self.__disks)

        for i in it:
            i.generate_chunks(max_chunks/i.get_frequency())

        print "Generating chunks:                                 Finished"
        return max_chunks

    def __generate_disks(self):
        print "\nGenerating Disks by grouping access percentages:   Started"
        if len(self.__values) > 0:
            starting_point = self.__values[0][1]
            name = 1
            disk = Disk(name)
            self.__disks.append(disk)
            for i in range(len(self.__values)):
                if math.fabs(self.__values[i][1] - starting_point) < 0.01:
                    disk.add_data(self.__values[i][0], self.__values[i][1])
                else:
                    starting_point = self.__values[i][1]
                    name += 1
                    disk = Disk(name)
                    self.__disks.append(disk)
                    disk.add_data(self.__values[i][0], self.__values[i][1])
        print "Generating Disks by grouping access percentages:   Finished"
        print "There are %d Disks" % len(self.__disks)

    def __generate_frequencies(self):
        print "\nGenerating Disk frequencies:                       Started"
        self.__disks.reverse()

        if len(self.__disks) > 0:
            lowest_disk = self.__disks[0]
            it = iter(self.__disks)
            for i in it:
                freq = math.sqrt(i.get_q()/lowest_disk.get_q())
                freq_int = int(math.floor(freq))
                print "Disk%d q = %f" % (i.get_name(), i.get_q())
                print "Disk%d raw frequency = %f" % (i.get_name(), freq)
                print "Disk%d floor frequency = %f" % (i.get_name(), freq_int)
                i.set_frequency(freq_int)
                print "Disk%d frequency = %d" % (i.get_name(), i.get_frequency())
        self.__disks.reverse()
        print "Generating Disk frequencies:                       Finished"

    def __sort(self):
        length = len(self.__values)
        print "\nSorting input values by access percentage:         Started"

        for i in range(length):
            j = i + 1
            while j < length:
                if self.__values[i][1] < self.__values[j][1]:
                    tmp = self.__values[i]
                    self.__values[i] = self.__values[j]
                    self.__values[j] = tmp
                else:
                    j += 1
        print "Sorting input values by access percentage:         Finished"

    def __print_info(self, max_chunks, broadcast):
        it = iter(self.__disks)
        for i in it:
            print ""
            i.print_disk_info()

        print "\nBroadcast will have %d data items" % len(broadcast)
        print "Broadcast : [", " | ".join(broadcast), "]"
        broadcast_stack = []
        for i in range(3):
            broadcast_stack.append("|")

        for i in range(len(broadcast)):
            if len(broadcast[i]) < 2:
                broadcast_stack[i % len(broadcast_stack)] = broadcast_stack[i % len(broadcast_stack)] + "  " + broadcast[i] + " |"
            else:
                broadcast_stack[i % len(broadcast_stack)] = broadcast_stack[i % len(broadcast_stack)] +  " " + broadcast[i] + " |"

        print "\nBroadcast Column view :"
        for i in range(len(broadcast_stack)):
            print "     ", broadcast_stack[i]

if __name__ == "__main__":
    bdisk = BroadCastDisk()
    bdisk.add_data(5, 0.2)
    bdisk.add_data(4, .3)
    bdisk.add_data(6, .2)
    bdisk.add_data(1, .1)
    bdisk.add_data(2, .1)
    bdisk.add_data(3, .05)
    bdisk.add_data(7, .05)

    for i in range(bdisk.get_number_of_data()):
        print "Data: %s, Percentage: %f" % bdisk.get_data_index(i)

    d = Disk(1)
    d.add_data(5, 0.2)
    d.add_data(4, .3)
    d.add_data(6, .2)
    d.add_data(1, .1)
    d.add_data(2, .1)
    d.add_data(3, .05)
    d.add_data(7, .05)
    d.determine_q()
    d.set_frequency(3)
    print "Number of data = %d" % d.get_number_of_data()
    print "Q = %f" % d.get_q()
    print "Frequency = %d" % d.get_frequency()
