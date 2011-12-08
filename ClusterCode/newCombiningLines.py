# Load the wordnet corpus
from nltk.corpus import wordnet as wn
import string

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

c = open('./textFiles/combinedLines.txt', 'w')

for index in listofNum:
    #reads in each line of the document; stores first/second word

    f = open('./textFiles/spectralClusters/' + str(listofNum[index-1]) + '.txt', 'r')

    name = ''
    for line in f:
        words = string.split(line)
        word = words[0]
        name = name + ' ' + word
        
    c.write(name + '\n') 
        
    
c.close()
