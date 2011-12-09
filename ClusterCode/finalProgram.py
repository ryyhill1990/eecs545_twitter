# Load the wordnet corpus
from nltk.corpus import wordnet as wn
import string
 
#opens document
f = open('./textFiles/editedReal.txt', 'r')

count = 1
for line in f:
    #reads in each line of the document; stores first/second word
    currentLine = line
    words = string.split(currentLine)

    c = open('./textFiles/finalClusters/Cluster' + str(count) + '.txt', 'w')

    name = ''
    for word in words:
        name = name + ' ' + word

    c.write(name + '\n')              

    for word in words:
        f2 = open('./textFiles/topWords.txt', 'r')

        #isTop = False
        #for line2 in f2:
#            currentTop = string.split(line2)
#            if currentTop[0] == word:
#                  isTop = True
        isTop = True
        if isTop == True:                         
            f1 = open('./textFiles/classes/' + word + '.txt', 'r')
            for line1 in f1:
                current = string.split(line1)
                num = current[2]
                #if int(num) > 50:
#                    c.write(line1)
                c.write(line1)
        f2.close()        
    count = count + 1

    c.close()
