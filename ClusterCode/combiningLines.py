from nltk.corpus import wordnet as wn
import string
import array

#opens document
f = open('./textFiles/realClusters.txt', 'r')


c = open('./textFiles/editedReal.txt', 'w')

firstLineDoc = f.readline()
currentWords = string.split(firstLineDoc)
currentTopWord = currentWords[0]
combinedLine = currentTopWord
#first step creates a list of the top words and prints them to a file
for line in f:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    secondWord = words[1]
    if firstWord == currentTopWord:
        combinedLine = combinedLine + ' ' + secondWord
    else:
        c.write(combinedLine + '\n')
        currentTopWord = firstWord
        combinedLine = currentTopWord + ' ' + secondWord


c.write(combinedLine)
c.close()
