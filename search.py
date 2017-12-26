import os
from collections import OrderedDict

f1 = open('data/index/inverted.txt')
f2 = open('data/index/dictionary.txt')

worddict = {}
for line in f2:
    term = line.split()[0]
    worddict[term] = OrderedDict()
    docnos = f1.readline().split()
    for id in docnos:
        worddict[term][id] = True

print('please input the key word to search')
while True:
    key = input("key:")
    if key in worddict:
        print("docno is:  ", end='')
        for d in worddict[key]:
            print(d,' ',end='')
        print()
    else:
        print('not found')