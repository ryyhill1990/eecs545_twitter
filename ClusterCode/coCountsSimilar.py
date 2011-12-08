# Load the wordnet corpus
from nltk.corpus import wordnet as wn
import string
 
# Get a collection of synsets (synonym sets) for a word
synsets1 = wn.synsets( '1' )
synsets2 = wn.synsets( '2' )

maximum = 0
for synset1 in synsets1:
  for synset2 in synsets2:
    num = wn.wup_similarity(synset1, synset2, verbose=False, simulate_root=True)
    if num > maximum:
      maximum = num

#opens document
#f = open('./textFiles/CoCounts.txt', 'r')
f = open('./textFiles/merge.txt', 'r')

total = 0
count = 0
for line in f:
  #reads in each line of the document; stores first/second word
  currentLine = line
  words = string.split(currentLine)
  firstWord = words[0]
  secondWord = words[1]
  num = int(words[2])
  # Get a collection of synsets (synonym sets) for the words
  synsets1 = wn.synsets(firstWord[1:len(firstWord)])
  synsets2 = wn.synsets(secondWord[1:len(secondWord)])
  maximum = 0

  if synsets1 != [] and synsets2 != [] and num > 5:
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
 	
