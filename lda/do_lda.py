#!/usr/bin/env python

import numpy as np
from sklearn.lda import LDA
from random import shuffle
from types import BooleanType

num_dimensions = 50
from math import isnan, isinf

def read_data(filename):
    x = []
    y = []
    index = 0
    for line in open(filename):
        index = index + 1
        if index % 100000 == 0:
            print index
        (x_tok, y_tok) = line.split('\t')
        x_toks = x_tok.split(',')
        x_item = [0] * 50
        for x_token in x_toks:
            if len(x_token) == 0:
                continue
            (dim_tok, val_tok) = x_token.split('=')
            dim = int(dim_tok)
            val = int(val_tok)
            x_item[dim] = val
            if isnan(val) or isinf(val):
                print 'error, line', index
        y_toks = y_tok.split(',')
        for y_token in y_toks:
            x.append(list(x_item))
            y.append(int(y_token))
    return x, y

def do_majority(x, y):
    correct = 0
    count = 0
    for x_item, y_item in [(x[i], y[i]) for i in range(len(x))]:
        count = count + 1
        if count % 100000 == 0:
            print count, correct
        majority_x = max((i for i in range(len(x_item))), key=lambda i:x_item[i])
        if majority_x == y_item:
            correct += 1
    return correct

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
    return ret, test_ret

def do_lda(x, y, folds):
    indexes = list(range(len(x)))
    shuffle(indexes)
    x = list(x[i] for i in indexes)
    y = list(y[i] for i in indexes)
    fold_size = len(x) / folds
    corrects = []
    for fold in range(folds):
        test_x = []
        train_x = []
        test_y = []
        train_y = []
        for i in range(len(x)):
            fold_index = i / fold_size
            if fold == fold_index:
                test_x.append(x[i])
                test_y.append(y[i])
            else:
                train_x.append(x[i])
                train_y.append(y[i])
        print 'Partitioned data into fold'
        test_x, train_x = remove_redundant_dimensions(test_x, train_x)
        print 'Removed redundant dimensions'
        lda = LDA()
        lda.fit(train_x, train_y)
        print 'Fit lda'
        predictions = lda.predict(test_x)
        correct = sum(1 for i in range(len(predictions)) if predictions[i] == test_y[i])
        print 'Did fold, correct:', correct
        corrects.append(correct)
    return corrects

if __name__ == '__main__':
    filename = 'write_training_data.txt'
    # filename = 'short_training_data.txt'
    x, y = read_data(filename)
    print 'read data, size', len(x)
    majority_correct = do_majority(x, y)
    print 'majority correct:', majority_correct, majority_correct / float(len(x))
    lda_corrects = do_lda(x, y, 10)
    print 'lda corrects:', lda_corrects, sum(lda_corrects) / (len(lda_corrects) * float(len(x)))
