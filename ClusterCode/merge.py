# Load the wordnet corpus
from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array


#opens document
f = open('./textFiles/newTopWords.txt', 'r')
clusters = 100

#first step creates a list of the top words and prints them to a file
topWords = []
count = 0
listOfNum = []
for line in f:
    currentLine = line
    words = string.split(currentLine)
    firstWord = words[0]

    topWords.append(firstWord)

    if count < 100:
        listOfNum.append(count + 1)
        count = count + 1

f.close

c = open('./textFiles/merge.txt', 'w')

c.write('')
c.close()

c = open('./textFiles/merge.txt', 'a')

for index in listOfNum:

    number = listOfNum[index-1]

    f = open('./textFiles/finalClusters/Cluster' + str(number) + '.txt')

    #we don't need first line
    f.readline()

    for line in f:
        c.write(line)

c.close()



             
