create table if not exists tweets (
    id integer primary key,
    year integer,
    month integer,
    day integer,
    hour integer,
    minute integer,
    second integer,
    username text,
    userid integer,
    text text
);
create table if not exists users (
    id integer primary key,
    username text
);
create table if not exists follows (
    id integer primary key,
    followerid integer,
    followedid integer
);
create table if not exists mentions (
    id integer primary key,
    tweetid integer,
    mentionerid integer,
    mentionedid integer
);
create table if not exists hashtags (
    id integer primary key,
    text text
);
create table if not exists hashtag_uses (
    id integer primary key,
    hashtagid integer,
    tweetid integer
);
