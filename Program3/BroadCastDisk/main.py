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
                page = int(line_split[0])
                percentage = eval(compile(line_split[1], '<string>', 'eval', __future__.division.compiler_flag))
                bdisk.add_data(page, percentage)
    else:
        while True:
            try:
                user_input = raw_input("Please enter data number: ")
                if user_input == "":
                    break
                data = int(user_input)
                print "you entered %d" % data
                bp = False
                while not bp:
                    try:
                        percentage = raw_input("Please enter percentage: ")
                        percentage = eval(compile(percentage, '<string>', 'eval', __future__.division.compiler_flag))
                        print "percentage %f" % percentage
                        bp = True
                        bdisk.add_data(data, percentage)
                    except:
                        print "Enter a percentage between 0.0 and 1.0"

            except:
                print "Invalid value...must be integer"

    bdisk.generate_schedule()
