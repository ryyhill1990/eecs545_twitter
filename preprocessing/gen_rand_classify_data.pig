-- Usage:
-- pig gen_rand_classify_data.pig


-- loading random id adder
DEFINE rand_id_adder `add_rand_id_to_tweet.py`
    SHIP('/home/dol/eecs545_twitter/preprocessing/add_rand_id_to_tweet.py');

-- grabbing full ngram signal results
tweets = LOAD '/user/dol/output/julyAug/TaggedTweetsClean/part*' 
         AS (date:chararray, user:chararray, post:chararray);

-- search results through streaming job
tweets_w_id = STREAM tweets THROUGH rand_id_adder 
          AS (id:chararray, date:chararray, user:chararray, post:chararray);
          
-- sorting results and returning just ngram and correlation
all_rand_tweets = ORDER tweets_w_id by id;
limit_rand_tweets = LIMIT all_rand_tweets 100000;
rand_tweets = FOREACH limit_rand_tweets GENERATE date, user, post;


-- list of distinct terms in first 100k tweets
tokened_tweets = FOREACH rand_tweets GENERATE FLATTEN(TOKENIZE(post)) as token;
unique_terms = DISTINCT tokened_tweets;
STORE unique_terms INTO 'output/julyAug/uniqueTermsRand';


-- loading tweet-terms-mapper
DEFINE tweet_terms_mapper `tweet_terms_mapper.py`
    SHIP('/home/dol/eecs545_twitter/preprocessing/tweet_terms_mapper.py')
    CACHE('/user/dol/output/julyAug/uniqueTermsRand/part-r-00000#tweet_terms.txt'); 

-- storing tweet terms data
final = STREAM rand_tweets THROUGH tweet_terms_mapper 
        AS (date:chararray, user:chararray, term_ids:chararray, hashtag_ids:chararray);
STORE final INTO 'output/julyAug/100kTweetTermsRand';