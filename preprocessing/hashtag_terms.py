#!/usr/bin/env python
import sys
from nltk.tokenize import WhitespaceTokenizer

BLOCKED_TAGS = ('#fb', '#ff')
MIN_HASHTAG_LEN = 2

def main(argv):
    # looping over input
    for line in sys.stdin:
        if line.find('\t') == -1:
            continue
        line = line.strip()
        date, user, post = line.split('\t', 2)
        
        tokens = WhitespaceTokenizer().tokenize(post)
        
        """
        token_freq = {}
        for token in tokens:
            if token not in token_freq:
                token_freq[token] = 0
            token_freq[token] += 1
        utokens = keys(token_freq)
        """
        # getting unique terms
        utokens = list(set(tokens))
        
        num_tokens = len(utokens)
        for i in range(num_tokens):
            if (utokens[i][0] == '#' and utokens[i] not in BLOCKED_TAGS
                    and len(utokens[i]) >= (MIN_HASHTAG_LEN+1)):
                for j in range(num_tokens):
                    # not pairings w/ self, or blocked tags
                    if i == j or utokens[j] in BLOCKED_TAGS:
                        continue
                    
                    # not pairing w/ hashtags missing min length
                    if utokens[j][0] == '#' and len(utokens[j]) < (MIN_HASHTAG_LEN+1):
                        continue
                
                    # including hashtag 
                    print "\t".join((utokens[i], utokens[j], date, user))
    
if __name__ == '__main__':
    main(sys.argv)
