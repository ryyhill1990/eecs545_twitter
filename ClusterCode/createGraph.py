# Load the wordnet corpus
from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array


#opens document
#f = open('./textFiles/topWords.txt', 'r')
f = open('./textFiles/newTopWords.txt', 'r')

topWords = []
topCounts = []
count = 0
for line in f:
    words = string.split(line)
    firstWord = words[0]
    num = int(words[1])

    topWords.append(firstWord)
    topCounts.append(num)

    count = count + 1

print count

f.close()

#f = open('./textFiles/clusters.txt', 'r')
f = open('./textFiles/realClusters.txt', 'r')

c = open('./textFiles/graph.txt','w')

for line in f:
    words = string.split(line)
    firstWord = words[0]
    secondWord = words[1]
    num1 = int(words[2])
    num2 = int(words[3])

    index1 = topWords.index(firstWord)

    if topWords.count(secondWord) != 0:
        index2 = topWords.index(secondWord)

    c.write(str(index1+1) + ' ' + str(index2+1) + ' ' + str(num1) + ' ' + str(num2) + '\n')



c.close()
