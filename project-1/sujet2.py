import shutil
import os
import sys
from math import *

tri = open(input("Input Files: "))

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

ngramList = []
grams = {}
for f in tri:
	data = f.strip()
	data = replace_all(data)
	data = data.lower()
	for r in range(2, 7):
		ngs = ngrams(data, r)
		ngs = [' '.join(x) for x in ngs]
		for g in ngs:
			grams.setdefault(g, 0)
			grams[g] += 1
ngramList.append(grams)
print(ngramList)
