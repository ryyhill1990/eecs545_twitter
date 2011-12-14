#!/usr/bin/env python

#tweets_file = '100k_tweets.txt'
#terms_file = 'tweet_terms.txt'
tweets_file = '100kTweetTermsRand.txt'
terms_file = 'uniqueTermsRand.txt'
stopwords_file = 'stopwords.txt'

long_datapoint_file = 'raw_datapoints.txt'
long_mapping_file = 'raw_terms.txt'
pca_datapoint_file = 'pca_datapoints.txt'
pca_mapping_file = 'pca_terms.txt'

log_file = 'make_datapoints_log.txt'

# Makes a map with an entry for each english stopword, from the nltk corpus
def make_stopwords():
    stopwords = {}
    for line in open(stopwords_file):
        stopwords[line.strip()] = True
    return stopwords

# Makes a list of all the terms in the long terms list,
# including hashtags and stopwords.
def make_terms_map():
    terms_map = []
    for line in open(terms_file):
        terms_map.append(line.strip())
    return terms_map

# Reads each line form the tweets file and
# writes a line to the long datapoint file.
# Writes using a new mapping, also writing
# a new index file.
def make_long_datapoints(terms_map, stopwords):
    # Maps strings onto new term indexes
    new_terms_map = {}
    with open(log_file, 'w') as log:
        with open(long_datapoint_file, 'w') as f:
            with open(long_mapping_file, 'w') as m:
                for line in open(tweets_file):
                    tokens = line.split()
                    terms = [terms_map[int(term)] for term in tokens[3].split(',') if terms_map[int(term)] not in stopwords]
                    tags = [terms_map[int(term)] for term in tokens[4].split(',')]
                    for term in terms:
                        if not term in new_terms_map:
                            new_terms_map[term] = len(new_terms_map)
                            m.write(term + '\n')
                            # For debugging
                            log.write(str(len(new_terms_map) - 1) + ' ' + term + '\n')
                    write_line = ' '.join([str(new_terms_map[term]) for term in terms] + tags)
                    f.write(write_line + '\n')
                    # For debugging
                    log.write(line)
                    log.write(' '.join(terms) + ' ')
                    log.write(' '.join(tags) + '\n')
                    log.write(write_line + '\n\n')

# Does nothing for now.
def make_pca_datapoints(terms_map, stopwords):
    pass

def main():
    stopwords = make_stopwords()
    terms_map = make_terms_map()
    print 'Made terms map'
    make_long_datapoints(terms_map, stopwords)
    make_pca_datapoints(terms_map, stopwords)

if __name__ == '__main__':
    main()
