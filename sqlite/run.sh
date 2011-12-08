#!/usr/bin/env bash
rm database.db
time ./read_schema.py
time ./read_tweets.py data/tail-tweets2009-06.csv
time ./find_usernames.py
