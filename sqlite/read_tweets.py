#!/usr/bin/env python

from os import system
from sys import argv
import twitter_lib

def read_file(filename):
    tweets = []
    for line in open(filename):
        when, username, text = line.split('\t')
        date, time = when.split(' ')
        year, month, day = date.split('-')
        hour, minute, second = time.split(':')
        username = username.decode('utf8')
        text = text.decode('utf8')
        tweets.append(twitter_lib.Tweet(-1, year, month, day, hour, minute, second, username, -1, text))
    twitter_lib.insert_tweets(tweets)

def main():
    if len(argv) < 2:
        print 'Usage: ./read_tweets.py [tweets-file]'
        print 'e.g.: ./read_tweets.py tail-tweets2009-06.csv'
        return
    read_file(argv[1])

if __name__ == '__main__':
    main()
