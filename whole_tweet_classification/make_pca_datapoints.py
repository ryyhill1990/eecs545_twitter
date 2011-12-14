#!/usr/bin/env python
from scipy.sparse import lil_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.lda import LDA
from random import shuffle

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

cluster_map_suffix = '_cluster_map.txt'

cluster_types = (
        ('spectral', 300), # Name, num clusters
        ('norm_spectral', 300),
        ('metis', 281),
        ('spectral_cos', 300), # Name, num clusters
        ('norm_spectral_cos', 300),
        ('metis_cos', 281),
        )

test_ratio = 0.1

classifier_classes = (
#        GaussianNB,
#        MultinomialNB,
        BernoulliNB,
        LDA,
        )


def read_clusters(cluster_type):
    cluster_map = {}
    for line in open(cluster_type + cluster_map_suffix):
        tokens = line.split()
        cluster_map[tokens[0]] = int(tokens[1])
    return cluster_map


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

# Does nothing for now.
def make_pca_datapoints(terms_map, stopwords, clusters):
	new_terms_map = {}
	raw_data = []
	target = []
	for line in open(tweets_file):
		tokens = line.split()
		terms = [terms_map[int(term)] for term in tokens[3].split(',') if terms_map[int(term)] not in stopwords]
		for term in terms:
			if not term in new_terms_map:
				new_terms_map[term] = len(new_terms_map)
		new_term_ids = [new_terms_map[term] for term in terms]
                tags = [terms_map[int(term)] for term in tokens[4].split(',')]
		raw_data.append(new_term_ids)
		target.append(tags)
	data = lil_matrix( (len(raw_data), len(new_terms_map)) )
	count = 0
	for cur_vector in raw_data:
		for point in cur_vector:
			data[(count, point)] += 1
		count += 1
	pca = RandomizedPCA (n_components=100)
	transformed_data = pca.fit_transform(data) 
	
	xs = []
	ys = []
	count = 0
	for datum in transformed_data:
		for tag in target[count]:
			if (len(tag) > 1) and tag[1:] in clusters:
				xs.append(datum)
				ys.append(clusters[tag[1:]])
		count += 1

	del transformed_data
	return xs, ys	

def accuracy(predict_y, test_y):
        correct = sum(1 for i in range(len(predict_y)) if predict_y[i] == test_y[i])
#	print 'Number of accurate items: ', correct
	return correct / float(len(predict_y))

def do_real_classification(train_x, train_y, test_x, test_y, classifier_class):
#    print 'Doing classification with ', str(classifier_class)
    classifier = classifier_class()
    classifier.fit(train_x, train_y)
#    print 'Fit classifier'
    predict_y = classifier.predict(test_x)
#    print 'Did prediction'
    predict_accuracy = accuracy(predict_y, test_y)
#    print 'Prediction accuracy:', predict_accuracy
    return predict_accuracy    

def do_classification(xs, ys, cluster_type):
	num_datapoints = len(xs)
	num_testing = int(num_datapoints * test_ratio)
        test_indexes = range(num_datapoints)
        shuffle(test_indexes)
        test_indexes = test_indexes[:num_testing]
#        print 'Found test indexes'
        train_x, train_y, test_x, test_y = split_data(xs, ys, test_indexes)
        del xs
        del ys
        del test_indexes
#        print 'Split testing and training data'
        for classifier_class in classifier_classes:
            accuracy = do_real_classification(train_x, train_y, test_x, test_y, classifier_class)
	    print 'Classifier ',classifier_class, ' cluster set ', cluster_type, ' accuracy ', accuracy 
 
def split_data(xs, ys, test_indexes):
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    test_ar = [False] * len(xs)
    for test_index in test_indexes:
        test_ar[test_index] = True
    for i in range(len(xs)):
        if test_ar[i]:
            test_x.append(xs[i])
            test_y.append(ys[i])
        else:
            train_x.append(xs[i])
            train_y.append(ys[i])
    return train_x, train_y, test_x, test_y


def main():
	stopwords = make_stopwords()
	terms_map = make_terms_map()
#	print 'Made terms map'
	for cluster_type in cluster_types:
		cluster_type_name = cluster_type[0]
#		print 'Current cluster type: ', cluster_type_name
		clusters = read_clusters(cluster_type_name)
#		print 'Read clusters'
		xs, ys = make_pca_datapoints(terms_map, stopwords, clusters)
#		print 'Reduced data dimensions'
		do_classification(xs, ys, cluster_type)				
	

if __name__ == '__main__':
    main()
