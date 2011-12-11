#!/usr/bin/env python

import sys
import numpy

def read_vocabulary(filename):
	id = 0
	id_to_word = {}
	for word in open(filename):
		id_to_word[id] = word
		id += 1
	return id_to_word

def read_hashtag_mapping(filename):
	hashtag_to_cluster_id = {}
	for line in open(filename):
		tokens = line.split()
		if len(tokens) == 2:
			hashtag_to_cluster_id[tokens[0]] = tokens[1]
	return hashtag_to_cluster_id

def read_stopwords(filename):
	stopwords = set([])
	for line in open(filename):
		stopwords.add(line.strip())
	return stopwords

def create_data(filename, hashtag_to_cluster_map, id_to_token, stop_words):
	X = []
	Y = []

	# count no. of words in vocabulary
        total_no_words = sum ([1 for key, val in id_to_token.iteritems() if not val.startswith('#')])

	# go over each tweet
	for line in open(filename):
		tokens = line.split()
		cur_Y = set([])
		cur_X = numpy.sparse.csr_matrix(zeros( total_no_words ))
		
		# tweet_date, tweet_time, tweet_user are ignored
		tweet_date = tokens[0]
		tweet_time = tokens[1]
		tweet_user = tokens[2]
		
		# tweet_words
		tweet_words = tokens[3].split(',')	
		for word_id in tweet_words:
			word = id_to_token[int(word_id)]
			if word not in stop_words:
				cur_X[int(word)] += 1

		# iterate over all hashtags and input the relevant clusters
		tweet_tags = tokens[4].split(',')
		for tag in tweet_tags:
			hash_tag = id_to_token[int(tag)]
	
			# note that the hash_tags in the vocabulary have '#' in front to
			# denote a hash, but the hashtag cluster files don't have that. 
			hash_tag_cluster_id = hashtag_to_cluster_map[hash_tag[1:]]
			if hash_tag_cluster_id != -1:
				X.append(cur_X)
				Y.append(hash_tag_cluster_id)
	return X, Y	

if __name__ == '__main__':
	if len(sys.argv) != 4 and  len(sys.argv) != 3:
		print 'Please run using the following format: python ', sys.argv[0], ' <tweets file> <vocabulary_file> <hashtag_mapping_file> [<stop_words>]' 
		sys.exit()

	# read all stop words
	if len (sys.argv) == 4:
		stop_words = read_stopwords(sys.argv[3])
	else:
		stop_words = set([])
	
	# read all words in the vocabulary - should include both hashtags and the words themselves
	id_to_token = read_vocabulary(sys.argv[2])

	# read all hashtag clusters. file format - each line: <hashtag>\t<cluster it belongs to>
	hashtag_cluster_map = read_hashtag_mapping (sys.argv[3])
	
	X, Y = create_data(sys.argv[1], id_to_token, hashtag_cluster_map, stop_words)
