#!/usr/bin/env python

import twitter_lib
from re import match

def find_users():
    usernames = {}
    all_tweets = twitter_lib.all_tweets()
    tweets_list = []
    for tweet in all_tweets:  
        tweets_list.append(tweet)
        usernames[tweet.username] = True
        for username in twitter_lib.find_mentions(tweet.text):
            usernames[username] = True
    twitter_lib.insert_users(usernames.keys())
    return tweets_list

def find_tweet_userids(all_tweets):
    all_tweets = twitter_lib.all_tweets()
    users = twitter_lib.all_users()
    users_map = {}
    tweet_updates = []
    for user in users:
        users_map[user.username] = user.sqlid
    for tweet in all_tweets:
        tweet.userid = users_map[tweet.username]
        tweet_updates.append(tweet)
    print 'size of all_tweets', len(tweet_updates)
    twitter_lib.update_tweet_userids(tweet_updates)
    return users_map

def find_mentions(users_map):
    print 'Finding mentions...'
    mentions = []
    all_tweets = twitter_lib.all_tweets()
    tweets_list = []
    for tweet in all_tweets:
        tweets_list.append(tweet)
        for mention in twitter_lib.find_mentions(tweet.text):
            # print 'found mention', tweet.sqlid, tweet.userid, mention
            mentions.append(twitter_lib.Mention(-1, tweet.sqlid, tweet.userid, mention))
    print 'mentions found', str(len(mentions))
    i = 0
    for mention in mentions:
        if not mention.mentioned in users_map:
            #print 'Error, user not found, name', mention.mentioned
            pass
        else:
            mention.mentioned = users_map[mention.mentioned]
    twitter_lib.insert_mentions(mentions)
    return tweets_list

def find_hashtags(all_tweets):
    hashtags = {}
    for tweet in all_tweets:
        for hashtag in twitter_lib.find_hashtags(tweet.text):
            hashtags[hashtag] = True
    twitter_lib.insert_hashtags(hashtags.keys())

def find_hashtag_uses(users, all_tweets):
    hashtag_uses = []
    hashtag_map = twitter_lib.hashtag_map()
    for tweet in all_tweets:
        for hashtag in twitter_lib.find_hashtags(tweet.text):
            if not hashtag in hashtag_map:
                print 'Error, hashtag not found,', hashtag
            else:
                hashtag_sqlid = hashtag_map[hashtag]
                hashtag_uses.append(twitter_lib.HashtagUse(-1, hashtag_sqlid, tweet.sqlid))
    twitter_lib.insert_hashtag_uses(hashtag_uses)
    return hashtag_map

if __name__ == '__main__':
    all_tweets = find_users()
    users_map = find_tweet_userids(all_tweets)
    all_tweets = find_mentions(users_map)
    find_hashtags(all_tweets)
    find_hashtag_uses(users_map, all_tweets)
