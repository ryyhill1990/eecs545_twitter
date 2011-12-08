#!/usr/bin/env python

from os import system
import sqlite3
import re

schema_file = 'schema.sql'
database_file = 'database.db'
command_delimiter = ';'
command_template = 'sqlite3 {0} \'{1}\''
touch_command = 'touch'

class Tweet:
    def __init__(self, sqlid, year, month, day, hour, minute, second, username, userid, text):
        self.sqlid = sqlid
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.username = username
        self.userid = userid
        self.text = text

class User:
    def __init__(self, sqlid, username):
        self.sqlid = sqlid
        self.username = username

class Mention:
    def __init__(self, sqlid, tweetid, mentioner, mentioned):
        self.sqlid = sqlid
        self.tweetid = tweetid
        self.mentioner = mentioner
        self.mentioned = mentioned

class Hashtag:
    def __init__(self, sqlid, text):
        self.sqlid = sqlid
        sqlf.text = text

class HashtagUse:
    def __init__(self, sqlid, hashtagid, tweetid):
        self.sqlid = sqlid
        self.hashtagid = hashtagid
        self.tweetid = tweetid

_insert_tweet_template = 'insert into tweets (year, month, day, hour, minute, second, username, userid, text) values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
_update_tweet_userids_template = 'update tweets set userid=? where id=?'
_insert_user_template = 'insert into users (username) values (?)'
_insert_mention_template = 'insert into mentions (tweetid, mentionerid, mentionedid) values (?, ?, ?)'
_insert_hashtag_template = 'insert into hashtags (text) values (?)'
_insert_hashtag_use_template = 'insert into hashtag_uses (hashtagid, tweetid) values (?, ?)'
_all_tweets_template = 'select id, year, month, day, hour, minute, second, username, userid, text from tweets'
_all_hashtags_template = 'select id, text from hashtags'
_all_users_template = 'select id, username from users'
_find_user_template = 'select id, username from users where username=?'
_db_connection = sqlite3.connect(database_file)
_mention_regex = re.compile('@(\S+)')
_hashtag_regex = re.compile('#(\S+)')

def find_mentions(text):
    return _mention_regex.findall(text)

def find_hashtags(text):
    return _hashtag_regex.findall(text)

def insert_tweets(tweets):
    db_cursor = _db_connection.cursor()
    for tweet in tweets:
        db_cursor.execute(_insert_tweet_template, (tweet.year, tweet.month, tweet.day, tweet.hour, tweet.minute, tweet.second, tweet.username, tweet.userid, tweet.text))
    _db_connection.commit()
    db_cursor.close()

def update_tweet_userids(tweets):
    print 'UDATING TWEET USERIDS'
    db_cursor = _db_connection.cursor()
    for tweet in tweets:
        db_cursor.execute(_update_tweet_userids_template, (tweet.userid, tweet.sqlid))
    _db_connection.commit()
    db_cursor.close()

def insert_users(usernames):
    db_cursor = _db_connection.cursor()
    for username in usernames:
        db_cursor.execute(_insert_user_template, (username,))
    _db_connection.commit()
    db_cursor.close()

def insert_mentions(mentions):
    db_cursor = _db_connection.cursor()
    for mention in mentions:
        db_cursor.execute(_insert_mention_template, (mention.tweetid, mention.mentioner, mention.mentioned))
    _db_connection.commit()
    db_cursor.close()

def insert_hashtags(hashtags):
    db_cursor = _db_connection.cursor()
    for hashtag in hashtags:
        db_cursor.execute(_insert_hashtag_template, (hashtag,))
    _db_connection.commit()
    db_cursor.close()

def insert_hashtag_uses(hashtags):
    db_cursor = _db_connection.cursor()
    for hashtag in hashtags:
        db_cursor.execute(_insert_hashtag_use_template, (hashtag.hashtagid, hashtag.tweetid))
    _db_connection.commit()
    db_cursor.close()

def all_users():
    # TODO implement
    # return a list of all users as objects
    db_cursor = _db_connection.cursor()
    db_cursor.execute(_all_users_template)
    users = []
    for row in db_cursor:
        sqlid = row[0]
        username = row[1]
        users.append(User(sqlid, username))
    db_cursor.close()
    return users

def all_tweets():
    db_cursor = _db_connection.cursor()
    db_cursor.execute(_all_tweets_template)
    for row in db_cursor:
        sqlid = row[0]
        year = row[1]
        month = row[2]
        day = row[3]
        hour = row[4]
        minute = row[5]
        second = row[6]
        username = row[7]
        userid = row[8]
        text = row[9]
        yield Tweet(sqlid, year, month, day, hour, minute, second, username, userid, text)
    db_cursor.close()

def hashtag_map():
    ret = {}
    db_cursor = _db_connection.cursor()
    db_cursor.execute(_all_hashtags_template)
    for row in db_cursor:
        sqlid = row[0]
        text = row[1]
        ret[text] = sqlid
    db_cursor.close()
    return ret

def find_user(username):
    db_cursor = _db_connection.cursor()
    db_cursor.execute(_find_user_template, (username,))
    for row in db_cursor:
        sqlid = row[0]
        username = row[1]
        yield User(sqlid, username)
    db_cursor.close()
