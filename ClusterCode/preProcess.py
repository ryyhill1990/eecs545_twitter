# Load the wordnet corpus
from nltk.corpus import wordnet as wn
import string
import array

#opens document
f = open('./textFiles/CoCounts.txt', 'r')
c = open('./textFiles/prePro.txt', 'w')
#first step creates a list of the top words and prints them to a file
topWords = []
count = 0
for line in f:
    currentLine = line

    words = string.split(currentLine)
    firstWord = words[0]
    firstWord = firstWord[1:len(firstWord)]
    secondWord = words[1]
    secondWord = secondWord[1:len(secondWord)]

    if firstWord == 'fb' or secondWord == 'fb':
        None
    elif firstWord == 'twitter' or secondWord == 'twitter':
        None
    elif firstWord == 'ff' or secondWord == 'ff':
        None
    elif firstWord == 'news' or secondWord == 'news':
        None
    elif firstWord == 'fact' or secondWord == 'fact':
        None
    elif firstWord == 'followfriday' or secondWord == 'followfriday':
        None
    elif firstWord == 'digg' or secondWord == 'digg':
        None
    else:
        c.write(currentLine)
        

c.close()
