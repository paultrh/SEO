#!/usr/bin/env python

import shutil
import os
import sys
import operator
from math import *

files = sys.argv[1:]
nbTotalFiles = len(files)
nbFileWithWord = 1
nbGrams = int(input('Please enter the number of representative ngram you want to see: \n'))

def getTf(countCurWord, countMostFrequent):
	tf = countCurWord / countMostFrequent
	return tf
	
def getIdf(nbTotalFiles, nbFileWithWord):
	ratio = nbTotalFiles / nbFileWithWord
	return (log10(ratio) + 1)

def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output

def replace_all(text):
    sanitize = ['\n', ',', '(', ')', '-']
    for i in sanitize:
        text = text.replace(i, '')
    return text
	
gramsOccurence = {}
gramsFile = {}
resultString = ''
countMostFrequent = 0

print('processing...')

for file in files:
	tmpSet = {}
	f = open(file)
	data = f.read().strip()
	data = replace_all(data)
	data = data.lower()
	for r in range(2, 7):
		ngs = ngrams(data, r)
		ngs = [' '.join(x) for x in ngs]
		for g in ngs:
			gramsOccurence.setdefault(g, 0)
			gramsOccurence[g] += 1
			countMostFrequent = max(gramsOccurence[g], countMostFrequent)
			if not g in tmpSet:
				gramsFile.setdefault(g, 0)
				gramsFile[g] += 1;
				tmpSet.setdefault(g, 0)
				tmpSet[g] += 1;


print('finalize')
tfIdfSet = {}
for gram in gramsOccurence:
	tfIdf = getTf(gramsOccurence[gram], countMostFrequent) * getIdf(nbTotalFiles, gramsFile[gram])
	tfIdfSet[gram] = tfIdf

resultList = sorted(tfIdfSet.items(), key=operator.itemgetter(1), reverse=True)[:nbGrams]
for res in resultList:
	resultString += str(res) + '\n'

f = open('result.txt', 'w+')
print('please check generated result.txt file')
f.write(resultString)
