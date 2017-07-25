#!/usr/bin/env python

import os
import sys
from math import *

print('### project-1 ###')

input = sys.argv
print(len(input[1:]))
nbTotalFiles = len(input[1:])
nbFileWithWord = 1

def getTf(countCurWord, countMostFrequent):
	tf = countCurWord / countMostFrequent
	return tf
	
def getIdf(nbTotalFiles, nbFileWithWord):
	ratio = nbTotalFiles / nbFileWithWord
	print(ratio)
	return (log10(ratio) + 1)
	
#print(str(getIdf(nbTotalFiles, nbFileWithWord) * getTf(countCurWord, countMostFrequent)))