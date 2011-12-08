import sys
import array
import numpy
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle
from sklearn.cross_validation import KFold

f = open(sys.argv[1], 'r')

data = []
target = []
count = 0
for line in f:
	count = count + 1
	if count % 1000 == 0:
		print count
	parts = line.split()
	if len(parts) != 2:
		continue
	data_part = parts[0]
	target_part = parts[1]
	
	x_items = data_part.split(",")
	cur_data = numpy.zeros( (60) )
	for x_item in x_items:
		x_item_parts = x_item.split("=")
		index = int(x_item_parts[0])
                value = int(x_item_parts[1])
		cur_data[index] = value
	
	targets = target_part.split(",")
	for cur_target in targets:
		data.append(cur_data)
		target.append(int(cur_target))

print "created data"

shuffle(data, target)

corrects = []

cv = KFold(len(data), 10)
clf = MultinomialNB()
for train, test in cv:
	print train
	print test
	X_train = [data[i] for i in range(len(data)) if train[i]]
	X_test = [data[i] for i in range(len(data)) if test[i]]
	Y_train = [target[i] for i in range(len(target)) if train[i]]
	Y_test = [target[i] for i in range(len(target)) if test[i]]

	print "fitting" 
	clf.fit(X_train, Y_train)
	print "fitted"

	predictions =  clf.predict(X_test)

	correct = sum(1 for i in range(len(predictions)) if predictions[i] == Y_test[i])
	correct_pc = correct/float(len(X_test))
	print correct_pc
	corrects.append(correct_pc)

print corrects
print sum(corrects)/len(corrects)
