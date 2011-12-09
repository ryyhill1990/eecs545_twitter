# Load the wordnet corpus
from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array


#opens document
f = open('./textFiles/newTopWords.txt', 'r')

topWords = []
topCounts = []
listofNum = []
count = 0
for line in f:
    words = string.split(line)
    firstWord = words[0]
    num = int(words[1])

    topWords.append(firstWord)
    topCounts.append(num)

    if count < 100:
        listofNum.append(count+1)
        
    count = count + 1


f.close()

f = open('./textFiles/clusterID.txt', 'r')

for index in listofNum:
    c = open('./textFiles/spectralClusters/' + str(listofNum[index-1]) + '.txt', 'w')

    c.write('')
    c.close()

count = 0
for line in f:
    words = string.split(line)
    ID = int(words[0])

    c = open('./textFiles/spectralClusters/' + str(ID) + '.txt', 'a')

    c.write(topWords[count] + '\n')

    c.close()
    count = count + 1

    
    
