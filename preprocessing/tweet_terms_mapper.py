#!/usr/bin/env python
import sys
import os
from itertools import imap

"""
hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar \
     -D mapred.reduce.tasks=0 \
     -file tweet_terms.txt \
     -file tweet_terms_mapper.py \
     -mapper tweet_terms_mapper.py \
     -input output/julyAug/100kTweets/part* \
     -output output/julyAug/100kTweetTerms
"""

def main(argv):
    # load top terms into dict
    TERM_IDS = {}
    dir = os.path.abspath(os.path.dirname(__file__)) 
    with open(dir + "/tweet_terms.txt") as f:
        id = 0
        for line in f:
            term = line.strip()
            TERM_IDS[term] = id
            id += 1
    
    # for each tweet, get terms, lookup ids, and output
    for line in sys.stdin:
        if line.find('\t') == -1:
            continue
        line = line.strip()
        date, user, post = line.split('\t', 2)
        
        # convert terms to IDs
        tokens = set(post.split(' '))
        term_ids = []
        hashtag_ids = []
        for t in tokens:
            try:
                tid = TERM_IDS[t]
            except:
                continue
            if t[0] == '#':
                hashtag_ids.append(tid)
            else:
                term_ids.append(tid)
        
        # only outputting if has terms and hashtags
        if term_ids and hashtag_ids:
            # output <user, date, terms, hashtags>
            term_ids_str = ','.join(imap(str, term_ids))
            hashtag_ids_str = ','.join(imap(str, hashtag_ids))
            print '\t'.join([date, user, term_ids_str, hashtag_ids_str])

    
if __name__ == '__main__':
    main(sys.argv)




