import sys
import __future__
from BroadCastDisk import BroadCastDisk
from LIX import LIX
from PIX import PIX

if __name__ == "__main__":
    bdisk = BroadCastDisk()
    lix_data = ""
    pix_client_data = ""
    pix_broadcast = ""
    pix_cache_size = 1
    perform_lix = False
    perform_pix = False
    user_input = []
    i = 0

    if len(sys.argv) == 2:
        fp = open(sys.argv[1])
        for line in fp:
            line = line.strip()
            if len(line) > 0:
                line_split = line.split(':')
                data = line_split[0]
                if line_split[0] == "LIX":
                    perform_lix = True
                    lix_data = line_split[1]
                elif line_split[0] == "PIXClient":
                    perform_pix = True
                    pix_client_data = line_split[1]
                elif line_split[0] == "PIXBroadcast":
                    perform_pix = True
                    pix_broadcast = line_split[1]
                elif line_split[0] == "PIXCacheSize":
                    pix_cache_size = int(line_split[1])
                    if pix_cache_size < 1:
                        pix_cache_size = 1
                else:
                    percentage = eval(compile(line_split[1], '<string>', 'eval', __future__.division.compiler_flag))
                    user_input.append((line_split[0], percentage))
                    bdisk.add_data(line_split[0], percentage)
    else:
        print "Usage: python main.py <input file>"

    broadcast = bdisk.generate_schedule()

    if perform_pix:
        pix = PIX(pix_broadcast, pix_client_data, pix_cache_size)
        pix.perform()

    if perform_lix:
        lix = LIX(user_input, broadcast, lix_data)
        lix.perform()
