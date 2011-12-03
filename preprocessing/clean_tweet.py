#!/usr/bin/env python
import sys
import re


"""
hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar \
     -D mapred.reduce.tasks=0 \
     -file clean_tweet.py \
     -mapper clean_tweet.py \
     -input output/julyTaggedTweets/part* \
     -output output/julyTaggedTweetsClean
"""

def main(argv):
    # looping over input
    for line in sys.stdin:
        if line.find('\t') == -1:
            continue
        line = line.strip()
        date, user, post = line.split('\t', 2)
        
        # skipping non-english tweets
        try:
            post.decode('ascii')
        except UnicodeDecodeError:
            continue
        
        s = post.lower()
        
        # removing URLs
        s = re.sub(r"((http://|www)[^\s]+)|(\w+(\.com|\.edu|\.net)([^\s]+)?)|(\w+\.\w+/\w+([^\s]+)?)", '', s)
        
        # preserving replies and hashes before removing non-alphanumeric characters
        s = re.sub("[^a-z0-9@# ]", '', s)
        s = s.strip()
        if s:
            print "%s\t%s\t%s" % (date, user, s)

    
if __name__ == '__main__':
    main(sys.argv)
