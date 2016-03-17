import sys
import __future__
from BroadCastDisk import BroadCastDisk

if __name__ == "__main__":
    bdisk = BroadCastDisk()
    i = 0

    if len(sys.argv) == 2:
        fp = open(sys.argv[1])
        for line in fp:
            line = line.strip()
            if len(line) > 0:
                line_split = line.split(':')
                data = line_split[0]
                percentage = eval(compile(line_split[1], '<string>', 'eval', __future__.division.compiler_flag))
                bdisk.add_data(data, percentage)
    else:
        print "Usage: python main.py <input file>"

    bdisk.generate_schedule()
