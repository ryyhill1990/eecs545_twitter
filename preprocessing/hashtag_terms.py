#!/usr/bin/env python
import sys
from nltk.tokenize import WhitespaceTokenizer

BLOCKED_TAGS = ('#fb',)

def main(argv):
    # looping over input
    for line in sys.stdin:
        if line.find('\t') == -1:
            continue
        line = line.strip()
        date, user, post = line.split('\t', 2)
        
        post = post.replace('#', ' #')
        
        tokens = WhitespaceTokenizer().tokenize(post)
        for i in range(len(tokens)):
            if tokens[i][0] == '#' and tokens[i] not in BLOCKED_TAGS:
                for j in range(len(tokens)):
                    if i != j and tokens[j] not in BLOCKED_TAGS:
                        print "\t".join((tokens[i], tokens[j], date, user))
    
if __name__ == '__main__':
    main(sys.argv)
