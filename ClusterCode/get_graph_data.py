#!/usr/bin/env python
import sys
import re

DEFAULT_THRESHOLD = 0.5

def main(argv):
    if len(argv) > 1:
        try:
            threshold = float(argv[1])
        except ValueError:
            print ("Usage: cat clusters.txt | ./get_graph_data.py "
                   "[threshold 0.0 - 0.99, default=0.5] [--mode=final]"
                   " > data.dot")
            exit()
    else:
        threshold = DEFAULT_THRESHOLD
        
    if len(argv) > 2 and argv[2] == '--mode=final':
        final_mode = True
    else:
        final_mode = False
        
    print "graph G\n{"
    
    # looping over input
    cluster_id = 0
    pairs_used = {}
    for line in sys.stdin:
        if line.find(' ') == -1:
            continue
        line = line.strip()
        
        cluster_id += 1
        if final_mode:
            nodes = line.split(' ')
            for node in nodes:
                cleannode = node if re.match('[a-z]', node[0]) else '_' + node
                print '%s--%s' % ('Cluster'+str(cluster_id), cleannode)
#            if line[0] != '#':
#                continue
#            node1, node2, weight = line.split('\t', 2)
#            node1 = node1[1:] # removing hash
#            node2 = node2[1:]
        else:
            node1, node2, weight1, weight2 = line.split(' ', 3)
            weight = float(weight1) / float(weight2)
            print_line = True if weight > threshold else False
            
            if print_line:
                dirtynode1 = re.match('[a-z]', node1[0])
                dirtynode2 = re.match('[a-z]', node2[0])
                cleannode1 = node1 if dirtynode1 else '_' + node1
                cleannode2 = node2 if dirtynode2 else '_' + node2
                id = '%s--%s' % (cleannode1, cleannode2)
                id2 = '%s--%s' % (cleannode2, cleannode1)
                if id not in pairs_used and id2 not in pairs_used:
                    print id
                    pairs_used[id] = True
        
    print "}"
    
    
if __name__ == '__main__':
    main(sys.argv)
