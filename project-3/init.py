#!/usr/bin/env python

import shutil
import os
import sys
from math import *
import operator

MIN_NGRAM = 2
MAX_NGRAM = 5
print('### project-3 ###')
DEMO_MODE = False
demoInput = input('Demo mode (y/n)')
if (demoInput.lower() == 'y' or demoInput.lower() == 'yes'):
    DEMO_MODE = True

if (not DEMO_MODE):
    ###### Get thematics from User ######

    thematicsList = []
    print('Enter thematics you want to identify : ')
    print('Enter Q to quit')
    i = 0
    while True:
        themes = input('Thematic number ' + str(i) + ' -> ')
        i += 1
        if (themes.lower() == 'Quit' or themes.lower() == 'q'):
            break;
        thematicsList.append(themes)
    print() # Graphic separators
    if (len(thematicsList) < 2):
        print("You must specify at least 2 themes")
        sys.exit()

### SANITIZE
if (os.path.isdir("tmp")):
    shutil.rmtree('tmp')
print('Sanitize work place')
os.makedirs("tmp")

def copyfiles():
  for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    if ('file' in path):
        for file in files:
            full_file_name = os.path.join(root, file)
            if (os.path.isfile(full_file_name)):
                if (not os.path.isdir("tmp/" + os.path.basename(root))):
                    os.makedirs("tmp/" + os.path.basename(root))
                try:
                    shutil.copy(full_file_name, "tmp/" + os.path.basename(root))
                except:
                    continue

if (DEMO_MODE):
    copyfiles()
else:
    for elt in thematicsList:
        os.makedirs('tmp/' + elt + '/')
    os.makedirs('tmp/submit/')
    print() # Graphic separators
    print('Please move files in the temporary directories created')
    print('The submit directory is a special directory for the files you want to classify')
    print('Example : Place file ' + thematicsList[0] + '.txt in tmp/' + thematicsList[0] + '/')
    input('Press Enter When done ...')

def getThemes():
    tmp = []
    for root, dirs, files in os.walk('.'):
      path = root.split(os.sep)
      if ('tmp' in path and os.path.basename(root) != 'tmp' and 'submit' not in path):
          tmp.append(os.path.basename(root))
    return tmp

if (DEMO_MODE):
    print('Theme choosed for you :')
else:
    print('You chose the following themes :')
thematicsList = getThemes()

i = 0
for index, elt in enumerate(thematicsList):
    print('\r#\r' + str(index) + '| ' + elt)

### Extracting n-grams
print()
print()
print('##### Extracting n-gramms #######')
print()
print()

def getFilesPath(theme):
    tmp = []
    for root, dirs, files in os.walk("."):
      path = root.split(os.sep)
      if (theme in path and 'tmp' in path):
          for file in files:
            full_file_name = os.path.join(root, file)
            tmp.append(full_file_name)
    return tmp

def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input) - n + 1):
    output.append(input[i:i + n])
  return output

def replace_all(text):
    sanitize = ['\n', ',', '(', ')', '-', '.', '\r', '\'', '"', '?', '!']
    text = text.lower()
    for i in sanitize:
        text = text.replace(i, '')
    text = ' '.join(text.split())
    return text

ngramList = []
for index, elt in enumerate(thematicsList):
    print('#' + str(index) + '| analyse ' + elt)
    files = getFilesPath(elt)
    grams = {}
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as myfile:
            data = myfile.read().strip()
            data = replace_all(data)
            for r in range(MIN_NGRAM, MAX_NGRAM):
                ngs = ngrams(data, r)
                ngs = [' '.join(x) for x in ngs]
                for g in ngs:
                    grams.setdefault(g, 0)
                    grams[g] += 1
    ngramList.append(grams)

def getReport(dico):
    tmp = {}
    for key, value in dico.items():
        tmp.setdefault(value, 0)
        tmp[value] += 1
    print(tmp)

def jaccard_similarity(set1, set2):
    intersection_cardinality = len(set.intersection(*[set1, set2]))
    union_cardinality = len(set.union(*[set1, set2]))
    return ((intersection_cardinality / float(union_cardinality)) * 100)

def loadSetByFile(file):
    with open(file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return set(content)

def dictToSet(dico, name, path, submitText):
    if (os.path.isfile(os.path.join(os.path.dirname(path), "_demo_ngrams.txt"))):
        return loadSetByFile(os.path.join(os.path.dirname(path), "_demo_ngrams.txt"))
    mySet = set()
    sorted_x = sorted(dico.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    print('-------------' + name + '-------------')
    for i in range(0, min(20, len(sorted_x))):
        isCoherent = True if input("Is revelant for " + name + " y/n ? -> : " + str(sorted_x[i])) == 'y' else False
        if (isCoherent):
            mySet.add(sorted_x[i][0])
    if (not submitText and not os.path.isfile(os.path.join(os.path.dirname(path), "_demo_ngrams.txt"))):
        with open(os.path.join(os.path.dirname(path), "_demo_ngrams.txt"), 'a') as out:
            for elt in mySet:
                out.write(elt + os.linesep)
    return mySet;

ngramSetsList = []
for i, elt in enumerate(thematicsList):
    if len(os.listdir('tmp/' + elt)) <= 0:
        print('Directories cannot be empty')
        sys.exit(1)

for i, elt in enumerate(ngramList):
    ngramSetsList.append(dictToSet(elt, getFilesPath(thematicsList[i])[0], getFilesPath(thematicsList[i])[0], False))

print('#########' + str(index) + '| analyse submited Texts')
submitedTextNGrams = []
submitedTextNames = []
files = getFilesPath('submit')
for f in files:
    submitedTextNames.append(os.path.basename(f))
    grams = {}
    with open(f, 'r', encoding='utf-8', errors='ignore') as myfile:
        data = myfile.read().strip()
        data = replace_all(data)
        for r in range(MIN_NGRAM, MAX_NGRAM):
                ngs = ngrams(data, r)
                ngs = [' '.join(x) for x in ngs]
                for g in ngs:
                    grams.setdefault(g, 0)
                    grams[g] += 1
    submitedTextNGrams.append(dictToSet(grams, os.path.basename(f), '', True))

print("###############    CONCLUSION    ###############")
for i, elt in enumerate(submitedTextNGrams):
    maxVal = 0
    index = -1
    for j, sections in enumerate(ngramList):
        percent = jaccard_similarity(submitedTextNGrams[i], ngramSetsList[j])
        if (max(maxVal, percent) > maxVal):
            maxVal = max(maxVal, percent)
            index = j
        print("#   -> " + submitedTextNames[i] + " over " + thematicsList[j] + " = " + str(percent) + " %")
    print("### BILAN  ### -> " + submitedTextNames[i] + " belongs to " + (" NO ONE " if index == -1 else thematicsList[index]) + " with " + str(maxVal) + "%")
print("##################################################")
