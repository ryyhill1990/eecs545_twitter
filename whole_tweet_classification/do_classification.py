#!/usr/bin/env python

import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.lda import LDA
from random import shuffle

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
        LDA
        )

cluster_list_suffix = '_indexed_cluster_list.txt'
cluster_map_suffix = '_cluster_map.txt'
datapoint_suffix = '_datapoints.txt'
terms_suffix = '_terms.txt'

test_ratio = 0.1

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
    print 'Removed', atr(num_removed), 'dimensions'
    return ret, test_ret

def accuracy(predict_y, test_y):
    pass

def do_classification(train_x, train_y, test_x, test_y, classifier_class):
    print 'Doing classification with ', str(classifier_class)
    classifier = classifier_class()
    classifier.fit(train_x, train_y)
    print 'Fit classifier'
    predict_y = classifier.predict(test_x)
    print 'Did prediction'
    predict_accuracy = accuracy(predict_y, test_y)
    print 'Prediction accuracy:', predict_accuracy

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

def learn(cluster_type, x_type, test_ratio, use_cos):
    print 'Learning, cluster type', cluster_type[0], ', x type', x_type, ', cos', use_cos
    cluster_type_name = cluster_type[0] if not use_cos else cluster_type[0] + '_cos'
    clusters = read_clusters(cluster_type_name)
    print 'Read clusters'
    xs, ys = read_datapoints(x_type[0], x_type[1], clusters, cluster_type[1])
    del clusters
    print 'Read datapoints'
    num_datapoints = len(xs)
    num_testing = int(num_datapoints * test_ratio)
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
    for classifier_class in classifier_classes:
        do_classification(train_x, train_y, test_x, test_y, classifier_class)

def main():
    for cluster_type in cluster_types:
        for x_type in x_types:
            learn(cluster_type, x_type, test_ratio, False)
            learn(cluster_type, x_type, test_ratio, True)

if __name__ == '__main__':
    main()
