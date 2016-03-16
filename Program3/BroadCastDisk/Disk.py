import math


class Disk(object):
    def __init__(self, name):
        self.__values = []
        self.__chunks = []
        self.__q = 0.0
        self.__f = 0
        self.__name = name
        self.__spacing = 0

    def get_name(self):
        return self.__name

    def add_data(self, data, percentage):
        self.__values.append((data, percentage))
        self.__sort()

    def get_number_of_data(self):
        return len(self.__values)

    def determine_q(self):
        total = 0.0
        for i in range(len(self.__values)):
            total += self.__values[i][1]

        self.__q = total/len(self.__values)

    def get_q(self):
        self.determine_q()
        return self.__q

    def get_number_of_chunks(self):
        return len(self.__chunks)

    def get_chunk(self, i):
        try:
            return self.__chunks[i]
        except:
            return None

    def generate_chunks(self, number_of_chunks):
        data_per_chunk = int(math.ceil(float(len(self.__values))/float(number_of_chunks)))
        for i in range(number_of_chunks):
            chunk = []
            for j in range(data_per_chunk):
                if ((i * data_per_chunk) + j) < len(self.__values):
                    chunk.append(self.__values[((i * data_per_chunk) + j)][0])
            self.__chunks.append(chunk)

    def set_frequency(self, f):
        self.__f = f

    def get_frequency(self):
        return self.__f

    def set_spacing(self, spacing):
        self.__spacing = spacing

    def get_spacing(self):
        return self.__spacing

    def print_disk_info(self):
        it = iter(self.__values)
        data = []
        for i in it:
            data.append(i[0])

        print "Disk%d:" % self.__name
        print "     Number of Data:     ", len(self.__values)
        print "     Data Items:         ", data
        print "     Optimal Frequency:  ", self.__f
        print "     Access Percentage:  ", self.get_q()
        #print "     Spacing:            ", self.__spacing
        print "     Number of Chunks:   ", len(self.__chunks)

        for i in range(len(self.__chunks)):
            print "         C(", self.__name, ",", i, "):   ", self.__chunks[i]

    def __sort(self):
        length = len(self.__values)

        for i in range(length):
            j = i + 1
            while j < length:
                if self.__values[i][0] > self.__values[j][0]:
                    tmp = self.__values[i]
                    self.__values[i] = self.__values[j]
                    self.__values[j] = tmp
                else:
                    j += 1


if __name__ == "__main__":
    d = Disk()
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