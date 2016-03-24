import sys
import __future__
from BroadCastDisk import BroadCastDisk
from LIX import LIX
from PIX import PIX

if __name__ == "__main__":
    bdisk = BroadCastDisk()
    lix_client_data = ""
    lix_broadcast = ""
    lix_disks = []
    lix_disks_frequency = []
    lix_cache_size = 1
    pix_client_data = ""
    pix_broadcast = ""
    pix_cache_size = 1

    if len(sys.argv) == 2:
        fp = open(sys.argv[1])
        for line in fp:
            line = line.strip()
            if len(line) > 0:
                line_split = line.split(':')
                data = line_split[0]
                if line_split[0] == "LIXClient":
                    lix_client_data = line_split[1]
                elif line_split[0] == "LIXBroadcast":
                    lix_broadcast = line_split[1]
                elif line_split[0] == "LIXDisk":
                    lix_disks.append(line_split[1])
                    lix_disks_frequency.append(int(line_split[2]))
                elif line_split[0] == "LIXCacheSize":
                    lix_cache_size = int(line_split[1])
                    if lix_cache_size < 1:
                        lix_cache_size = 1
                elif line_split[0] == "PIXClient":
                    pix_client_data = line_split[1]
                elif line_split[0] == "PIXBroadcast":
                    pix_broadcast = line_split[1]
                elif line_split[0] == "PIXCacheSize":
                    pix_cache_size = int(line_split[1])
                    if pix_cache_size < 1:
                        pix_cache_size = 1
                elif line_split[0] == "BroadCastDisk":
                    percentage = eval(compile(line_split[2], '<string>', 'eval', __future__.division.compiler_flag))
                    bdisk.add_data(line_split[1], percentage)
    else:
        print "Usage: python main.py <input file>"

    if bdisk.get_number_of_data() > 0:
        broadcast = bdisk.generate_schedule()

    if (len(pix_broadcast) > 0) and (len(pix_client_data) > 0):
        pix = PIX(pix_broadcast, pix_client_data, pix_cache_size)
        pix.perform()
    elif (len(pix_broadcast) > 0) or (len(pix_client_data) > 0):
        print "\nPIX File Entries must have the following:"
        print "     1. A line which has something like \'PIXClient:a,b,c,b,a,a\'"
        print "     2. A line which has something like \'PIXBroadcast:a,b,a,c,a,d\'"
        print "\n The PIX Entry similar to \'PIXCacheSize:2\' is optional. \'PIXCacheSize:1\' is default"

    if (len(lix_broadcast) > 0) and (len(lix_client_data) > 0) and (len(lix_disks) > 0):
        lix = LIX(lix_broadcast, lix_client_data, lix_disks, lix_disks_frequency, lix_cache_size)
        lix.perform()
    elif (len(lix_broadcast) > 0) or (len(lix_client_data) > 0) or (len(lix_disks) > 0):
        print "\nLIX File Entries must have the following:"
        print "     1. A line which has something like \'LIXClient:a,b,c,b,a,a\'"
        print "     2. A line which has something like \'LIXBroadcast:a,b,a,c,a,d\'"
        print "     3. At least one line which has something similar to \'LIXDisk:b,c,d:1\'"
        print "        where \'b,c,d\' are the elements in the disk and 1 is the frequency."
        print "        The disks entries, as a whole, must contain all of the proper elements in the broadcast;"
        print "        otherwise, program may crash."
        print "\n The LIX Entry similar to \'LIXCacheSize:2\' is optional. \'LIXCacheSize:1\' is default"
