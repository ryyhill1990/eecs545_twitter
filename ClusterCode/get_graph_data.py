#!/usr/bin/env python
import sys
import re

DEFAULT_THRESHOLD = 0.5

def main(argv):
    if len(argv) > 1:
        try:
            threshold = float(argv[1])
        except ValueError:
            print "Usage: cat clusters.txt | ./get_graph_data.py [threshold 0.0 - 0.99, default=0.5] > data.dot"
            exit()
    else:
        threshold = DEFAULT_THRESHOLD
        
    print "graph G\n{"
    
    # looping over input
    for line in sys.stdin:
        if line.find(' ') == -1:
            continue
        line = line.strip()
        
        node1, node2, weight1, weight2 = line.split(' ', 3)
        weight = float(weight1) / float(weight2)
        if weight > threshold:
            cleannode1 = node1 if re.match('[a-z]', node1[0]) else '_' + node1
            cleannode2 = node2 if re.match('[a-z]', node2[0]) else '_' + node2
            print '%s--%s' % (cleannode1, cleannode2)
    
        
    print "}"
    
    
if __name__ == '__main__':
    main(sys.argv)
