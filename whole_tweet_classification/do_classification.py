#!/usr/bin/env python

import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.lda import LDA
from sklearn.svm.sparse import SVC
from scipy.sparse import coo_matrix
from random import shuffle, random
from types import BooleanType

cluster_types = (
        ('spectral', 300), # Name, num clusters
        ('norm_spectral', 300),
        ('metis', 281),
        )

x_types = (
        ('raw', 9697), # name, num dimensinos
        ('pca', 666),
        )

classifier_classes = (
        GaussianNB,
        MultinomialNB,
        BernoulliNB,
        LDA,
        )

sparse_classifier_classes = (
        (SVC, 'SVC'),
        )

cluster_list_suffix = '_indexed_cluster_list.txt'
cluster_map_suffix = '_cluster_map.txt'
datapoint_suffix = '_datapoints.txt'
terms_suffix = '_terms.txt'

test_fraction = 0.1

def read_clusters(cluster_type):
    cluster_map = {}
    for line in open(cluster_type + cluster_map_suffix):
        tokens = line.split()
        cluster_map[tokens[0]] = int(tokens[1])
    return cluster_map

# Return parallel lists of x and y values.
def read_datapoints(x_type, num_dimensions, cluster_map, num_clusters):
    xs = []
    ys = []
    for line in open(x_type + datapoint_suffix):
        tags = []
        x = [0] * num_dimensions
        for token in line.split():
            if token[0] == '#':
                tags.append(token[1:])
            else:
                word_index = int(token)
                x[word_index] = x[word_index] + 1
        for tag in tags:
            if tag in cluster_map:
                cluster_index = cluster_map[tag]
                xs.append(list(x))
                ys.append(cluster_index)
    return xs, ys

def read_sparse_datapoints(x_type, num_dimensions, cluster_map, num_clusters, test_fraction):

    datapoint_indexes = ([],[]) # Train, test
    dimension_indexes = ([], []) # Train, test
    value_indexes = ([], []) # Train, test
    y_values = ([], []) # Train, test
    tweet_ids = ([], []) # Train, test
    tweet_categories = {} # Maps tweet-id onto map of categories for that tweet.

    line_index = -1
    datapoint_is = [0, 0]
    # print 'Reading sparse datapoints, x type:', x_type
    for line in open(x_type + datapoint_suffix):
        # print line.strip()
        line_index = line_index + 1
        if line_index % 10000 == 0:
            print line_index
        tags = []
        word_indexes = []
        for token in line.split():
            if token[0] == '#':
                tags.append(token[1:])
                #print 'got tag', tags[-1]
            else:
                word_indexes.append(int(token))
        for tag in tags:
            if tag in cluster_map:
                half = 1 if random() < test_fraction else 0
                datapoint_index_list = datapoint_indexes[half]
                dimension_index_list = dimension_indexes[half]
                value_index_list = value_indexes[half]
                y_value_list = y_values[half]
                tweet_id_list = tweet_ids[half]
                for word_index in word_indexes:
                    datapoint_index_list.append(datapoint_is[half])
                    dimension_index_list.append(word_index)
                    value_index_list.append(1)
                cluster_index = cluster_map[tag]
                y_value_list.append(cluster_index)
                tweet_id_list.append(line_index)
                if not line_index in tweet_categories:
                    tweet_categories[line_index] = {}
                tweet_categories[line_index][cluster_index] = True
                datapoint_is[half] = datapoint_is[half] + 1
                #print tag, cluster_map[tag]
            #else:
                #print 'tag not in cluster map:', tag
    train_xs = coo_matrix((value_indexes[0], (datapoint_indexes[0], dimension_indexes[0])), shape=(datapoint_is[0], num_dimensions))
    test_xs = coo_matrix((value_indexes[1], (datapoint_indexes[1], dimension_indexes[1])), shape=(datapoint_is[1], num_dimensions))
    return train_xs, y_values[0], tweet_ids[0], test_xs, y_values[1], tweet_ids[1], tweet_categories

# Removes dimensions that don't have any varience
# Can be called with test_x and train_x.
def remove_redundant_dimensions(x, test_x):
    same = False
    for x_point in x:
        if same == False:
            same = list(x_point)
            continue
        for i in range(len(x_point)):
            if x_point[i] != same[i]:
                same[i] = False
    if not same:
        print 'Removed no redundant dimensions'
        return x, test_x  
    use_indexes = [i for i in range(len(same)) if type(same[i]) == BooleanType and same[i] == False]
    ret =      [list(point[i] for i in use_indexes) for point in x]
    test_ret = [list(point[i] for i in use_indexes) for point in test_x]
    num_removed = len(x) - len(ret)
    print 'Removed', str(num_removed), 'dimensions'
    return ret, test_ret

def accuracy(predict_y, test_y, test_tweet_ids, tweet_categories_map):
    num_points = sum(1 for i in range(len(predict_y)) if i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1])
    return  sum(1 for i in range(len(predict_y)) if predict_y[i] == test_y[i] and (i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1])) / float(num_points), \
            sum(1 for i in range(len(predict_y)) if predict_y[i] in tweet_categories_map[test_tweet_ids[i]] and (i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1])) / float(num_points)

def log_predictions(test_x, test_y, predict_y, prefix):
    num_dimensions = test_x.shape[1]
    dense = test_x.todense()
    print 'Logging, made dense matrix'
    with open(prefix + '_predictions.txt', 'w') as f:
        for i in range(len(test_y)):
            f.write(' '.join((','.join(str(j) for j in range(num_dimensions) if dense[i,j] != 0), str(test_y[i]), str(predict_y[i]))) + '\n')

def do_classification(train_x, train_y, test_x, test_y, classifier_class, classifier_name):
    print 'Doing classification with ', str(classifier_class)
    print 'Num train', str(len(train_y)), ', num test', str(len(test_y))
    classifier = classifier_class()
    classifier.fit(train_x, train_y)
    print 'Fit classifier'
    predict_y = classifier.predict(test_x)
    return predict_y

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

def find_majority(items):
    item_dict = {}
    for item in items:
        if item not in item_dict:
            item_dict[item] = 1
        else:
            item_dict[item] = item_dict[item] + 1
    return max(item_dict.keys(), key=lambda x: item_dict[x])

def learn(cluster_type, x_type, test_fraction, use_cos):
    print 'Learning, cluster type', cluster_type[0], ', x type', x_type, ', cos', use_cos
    cluster_type_name = cluster_type[0] if not use_cos else cluster_type[0] + '_cos'
    clusters = read_clusters(cluster_type_name)
    print 'Read clusters'

    train_x, train_y, train_tweet_ids, test_x, test_y, test_tweet_ids, tweet_categories_map = read_sparse_datapoints(x_type[0], x_type[1], clusters, cluster_type[1], test_fraction)
    print 'Read training datapoints'

    """
    xs, ys = read_datapoints(x_type[0], x_type[1], clusters, cluster_type[1])
    del clusters
    print 'Read datapoints'
    num_datapoints = len(xs)
    num_testing = int(num_datapoints * test_fraction)
    test_indexes = range(num_datapoints)
    shuffle(test_indexes)
    test_indexes = test_indexes[:num_testing]
    print 'Found test indexes'
    train_x, train_y, test_x, test_y = split_data(xs, ys, test_indexes)
    train_x, test_x = remove_redundant_dimensions(train_x, test_x)
    del xs
    del ys
    del test_indexes
    print 'Split testing and training data'
    """
    # Figure out majority vote
    majority_y = find_majority(train_y)
    majority_test_accuracy = sum(1 for i in range(len(test_y)) if test_y[i] == majority_y) / float(len(test_y))
    majority_total_accuracy = (sum(1 for i in range(len(train_y)) if train_y[i] == majority_y) + \
            sum(1 for i in range(len(test_y)) if test_y[i] == majority_y)) / float(len(test_y) + len(train_y))
    print 'Majority class', majority_y, ', majority vote accuracy on testing data', majority_test_accuracy, ', on all data ', majority_total_accuracy
    num_train_points = sum(1 for i in range(len(train_y)) if i == 0 or train_tweet_ids[i] != train_tweet_ids[i-1])
    num_test_points = sum(1 for i in range(len(test_y)) if i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1])
    generous_majority_test_accuracy = sum(1 for i in range(len(test_y)) if majority_y in tweet_categories_map[test_tweet_ids[i]] \
            and (i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1])) / float(num_test_points)
    generous_majority_total_accuracy = (sum(1 for i in range(len(train_y)) if majority_y in tweet_categories_map[train_tweet_ids[i]] \
            and (i == 0 or train_tweet_ids[i] != train_tweet_ids[i-1])) + \
            sum(1 for i in range(len(test_y)) if majority_y in tweet_categories_map[test_tweet_ids[i]] \
            and (i == 0 or test_tweet_ids[i] != test_tweet_ids[i-1]))) / float(num_test_points + num_train_points)
    print 'Generous majority vote accuracy on testing data', generous_majority_test_accuracy, ', on all data', generous_majority_total_accuracy

#    for classifier_class in classifier_classes:
    for classifier_class in sparse_classifier_classes:
        classifier_name = classifier_class[1] + ('_cos' if use_cos else '')
        predict_y = do_classification(train_x, train_y, test_x, test_y, classifier_class[0], classifier_name)
        print 'Did prediction'
        log_predictions(test_x, test_y, predict_y, classifier_name)
        print 'Logged predictions'
        predict_accuracy, generous_predict_accuracy = accuracy(predict_y, test_y, test_tweet_ids, tweet_categories_map)
        print 'Prediction accuracy:', predict_accuracy
        print 'Generous prediction accuracy:', generous_predict_accuracy

def main():
    for cluster_type in cluster_types:
        for x_type in x_types:
            learn(cluster_type, x_type, test_fraction, False)
            learn(cluster_type, x_type, test_fraction, True)

if __name__ == '__main__':
    main()
