# Load the wordnet corpus
from nltk.corpus import wordnet as wn
import string
 
#opens document
f = open('30.txt', 'r')

rep = 'defined'

total = 0
count = 0
for line in f:
  #reads in each line of the document; stores first/second word
  currentLine = line
  words = string.split(currentLine)
  firstWord = words[0]
  # Get a collection of synsets (synonym sets) for the words
  synsets1 = wn.synsets(rep)
  synsets2 = wn.synsets(firstWord[1:len(firstWord)])
  maximum = 0

  if synsets1 != [] and synsets2 != []:
    for synset1 in synsets1:
      for synset2 in synsets2:
        num = wn.wup_similarity(synset1, synset2, verbose=False, simulate_root=True)
        if num > maximum:
          maximum = num
    total = total + maximum 
    count = count + 1
    
print total
print count
if count != 0:
  print total/count
