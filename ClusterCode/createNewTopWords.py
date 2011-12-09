# Load the wordnet corpus
from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array


#opens document
f = open('./textFiles/realClusters.txt', 'r')

#first step creates a list of the top words and prints them to a file
topWords = []
count = 0
totalCoOccur = 0
totalCoOccurList = []
for line in f:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    num = int(words[2])

    if count == 0:
        topWords.append(firstWord)
        count = count + 1
    elif topWords[count-1] == firstWord:
        totalCoOccur = totalCoOccur + num
    elif topWords[count-1] != firstWord:
        topWords.append(firstWord)
        totalCoOccurList.append(totalCoOccur)
        totalCoOccur = 0
        count = count + 1

totalCoOccurList.append(totalCoOccur)
print topWords
c = open('./textFiles/newTopWords.txt', 'w')
count = 0
for index in topWords:
    c.write(index + ' ' + str(totalCoOccurList[count]) + '\n')
    count = count + 1
c.close()
