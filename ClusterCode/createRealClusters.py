from __future__ import division
from nltk.corpus import wordnet as wn
import string
import array

#opens document
f1 = open('./textFiles/clusters.txt', 'r')

name = './textFiles/realClusters.txt'
c = open(name, 'w')

for line in f1:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    secondWord = words[1]
    coOccurances = words[2]
    totalCount = words[3]

    if firstWord != secondWord:

        name = './textFiles/classes/' + firstWord + '.txt'
        c1 = open(name, 'r')
        print name
        semiTotalCount = 0
        count = 0
        for line2 in c1:
            
            currentLine = line2
            words = string.split(currentLine)

            compareWord1 = words[1]

            name = './textFiles/classes/' + secondWord + '.txt'
            c2 = open(name, 'r')
            
            for line3 in c2:

                words = string.split(line3)
                compareWord2 = words[1]
                number = int(words[2])

                if compareWord1 == compareWord2:
                    count = count + 1
                    break

            c2.close()
            semiTotalCount = semiTotalCount + 1


        if int(count)/int(semiTotalCount) > .1:
            c.write(firstWord + ' ' + secondWord + ' ' + coOccurances + ' ' + str(totalCount) + '\n')

c.close()

                    

                
