# Load the wordnet corpus
from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array


#opens document
f = open('./textFiles/prePro.txt', 'r')

#first step creates a list of the top words and prints them to a file
topWords = []
count = 0
totalCoOccur = 0
totalCoOccurList = []
for line in f:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    firstWord = firstWord[1:len(firstWord)]
    num = int(words[2])

    if count == 0:
        topWords.append(firstWord)
        count = count + 1
        totalCoOccur = num
    elif topWords[count-1] == firstWord:
        totalCoOccur = totalCoOccur + num
    elif topWords[count-1] != firstWord:
        topWords.append(firstWord)
        totalCoOccurList.append(totalCoOccur)
        totalCoOccur = 0
        count = count + 1

totalCoOccurList.append(totalCoOccur)
print topWords
c = open('./textFiles/topWords.txt', 'w')
count = 0
for index in topWords:
    c.write(index + ' ' + str(totalCoOccurList[count]) + '\n')
    count = count + 1
c.close()

print count

f.close()
#reopens document
f = open('./textFiles/prePro.txt', 'r')
c = open('./textFiles/clusters.txt', 'w')
newClusters = []
count = 0
for line in f:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    firstWord = firstWord[1:len(firstWord)]
    secondWord = words[1]
    secondWord = secondWord[1:len(secondWord)]
    num = int(words[2])

    if topWords[count] == firstWord:
        currentTotal = totalCoOccurList[count]
    else:
        count = count + 1
        currentTotal = totalCoOccurList[count]

    for item in topWords:
        if currentTotal == 0:
            None
        elif secondWord == item and int(num)/int(currentTotal) > .01:
            c.write(firstWord + ' ' + item + ' ' + str(num) + ' ' + str(currentTotal) + '\n')
        

c.close()
f.close()
