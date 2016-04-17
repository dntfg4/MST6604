import sys
from Tree import Tree
from PartialReplication import PartialReplication

if __name__ == "__main__":
    tree = Tree()

    if len(sys.argv) == 2:
        fp = open(sys.argv[1])
        for line in fp:
            line = line.strip()
            if len(line) > 0:
                line_split = line.split(':')
                data = line_split[0]
                if line_split[0] == "Node":
                    tree.add_node(line_split[1], line_split[2])
                elif line_split[0] == "DataItem":
                    tree.add_data(int(line_split[1]), line_split[2], line_split[3])
                elif line_split[0] == "ReplicationLevel":
                    tree.set_replication_level(int(line_split[1]))
        tree.complete()
        pr = PartialReplication(tree)
        pr.generate_broadcast()
    else:
        print "Usage: python main.py <input file>"