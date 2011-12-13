#!/usr/bin/env python
import sys
import uuid

def main(argv):
    # looping over input
    for line in sys.stdin:
        if line.find('\t') == -1:
            continue
        line = line.strip()
        date, user, post = line.split('\t', 2)
        
        id = uuid.uuid4()
        
        print "\t".join((str(id), date, user, post))
    
if __name__ == '__main__':
    main(sys.argv)
