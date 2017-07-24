#!/usr/bin/env python

import shutil
import os
import sys

print('### project-3 ###')
DEMO_MODE = False
demoInput = input('Demo mode (y/n)')
if (demoInput.lower() == 'y' or demoInput.lower() == 'yes'):
    DEMO_MODE = True

if (not DEMO_MODE):
    ###### Get thematics from User ######

    thematicsList = []
    print('Enter thematics you want to identifies : ')
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
            print(full_file_name)
            if (os.path.isfile(full_file_name)):
                os.makedirs("tmp/"+os.path.basename(root))
                shutil.copy(full_file_name, "tmp/"+os.path.basename(root))

if (DEMO_MODE):
    copyfiles()
else:
    for elt in thematicsList:
        os.makedirs('tmp/'+elt+'/')
    print() # Graphic separators
    print('Please move files in the temporary directories created')
    print('Example : Place file '+thematicsList[0]+'.txt in tmp/'+thematicsList[0]+'/')
    input("Press Enter When done ...")
    
def getThemes():
    tmp = []
    for root, dirs, files in os.walk("."):
      path = root.split(os.sep)
      if ('tmp' in path and os.path.basename(root) != 'tmp'):
          tmp.append(os.path.basename(root))
    return tmp

if (DEMO_MODE):
    print('Theme choosed for you :')
else:
    print('You choosed the following themes :')
thematicsList = getThemes()

i = 0
for index, elt in enumerate(thematicsList):
    print('\r#\r' + str(index) + '| ' + elt)

### Extracting n-grams
print()
print()
print('#####  Extracting n-gramms #######')
print()
print()

def getFilesPath(theme):
    tmp = []
    for root, dirs, files in os.walk("."):
      path = root.split(os.sep)
      if (theme in path and "tmp" in path):
          for file in files:
            full_file_name = os.path.join(root, file)
            print(full_file_name)
            tmp.append(full_file_name)
    return tmp

def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output

for index, elt in enumerate(thematicsList):
    print('  ' + str(index) + '| analyse ' + elt)
    files = getFilesPath(elt)
    grams = {}
    for f in files:
        with open(f, 'r') as myfile:
            data=myfile.read().replace('\n', '')
            ngs = ngrams(data, 3)
            ngs = [' '.join(x) for x in ngs]
            for g in ngs:
               grams.setdefault(g, 0)
               grams[g] += 1
            print(grams)
            sys.exit()
            

