from nltk.corpus import wordnet as wn
import string
import array

#opens document
f1 = open('./textFiles/prePro.txt', 'r')
f2 = open('./textFiles/topWords.txt', 'r')

name = './textFiles/classes/' + 'newFile.txt'
c = open(name, 'w')

for line in f2:
    f1 = open('./textFiles/prePro.txt', 'r')
    currentLine = line

    words = string.split(currentLine)
    topWord = words[0]
    fileName = './textFiles/classes/' + topWord + '.txt'
    c = open(fileName, 'w')
    for line2 in f1:

        currentLine = line2
        words = string.split(currentLine)
        firstWord = words[0]
        firstWord = firstWord[1:len(firstWord)]

        if firstWord == topWord:
            c.write(line2)

    c.close()
    f1.close()
    
    

    
