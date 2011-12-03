#!/usr/bin/env python
import re
import sys

#outputSchema("word:chararray")
for line in sys.stdin:
    if line.find('\t') == -1:
        continue
    date, user, hashtag = line.split('\t', 2)
    hashtag = re.sub(r"[^A-Za-z0-9]", '', hashtag.lower())
    hashtag = hashtag[:20] if len(hashtag) > 20 else hashtag
    print '%s\t%s\t%s' % (date, user, hashtag)

