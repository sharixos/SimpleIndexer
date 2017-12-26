from bs4 import BeautifulSoup
import re
import os
from collections import OrderedDict

id = 0
wordnum = 0

# doclists = []

worddict = {}

basepath = 'data/shakespeare'
for dirpath,dirnames,filenames in os.walk(basepath):
    for file in filenames:
        fullpath = os.path.join(dirpath,file)
        shakespeare = open(fullpath, 'r')
        soup = BeautifulSoup(shakespeare, 'lxml')

        docs = soup.find_all('doc')
        for doc in docs:
            # document = Document(doc.docno.contents[0],id)
            # if hasattr(doc.title, 'contents'):
            #     document.setTitle(doc.title.contents[0])

            for content in doc.contents:
                if hasattr(content, 'docno') == False:
                    content = re.sub('\W',' ',content).lower()
                    wordlist = content.split()
                    for word in wordlist:
                        wordnum = wordnum + 1
                        # document.appendWord(word)
                        if word not in worddict:
                            worddict[word] = OrderedDict()
                        worddict[word][id] = True

            # doclists.append(document)
            id = id + 1

worddict = sorted(worddict.items(), key=lambda d:d[0])

print("The number of documents is : ", id)
print("The number of terms is :", len(worddict))
print("The number of words is :", wordnum)
print("The average words of documents is: ", wordnum / id)

# write inverted inodes docno and dictionary data
f1 = open('data/index/inverted.txt', 'w')
f2 = open('data/index/dictionary.txt', 'w')
termid = 0
for k,v in worddict:
    for d in v:
        f1.write(str(d) + ' ')
    f1.write('\n')
    strid = str(termid)
    strfq = str(len(v))
    f2.write(k + ' '*(20-len(k)) + ' '+ strid + ' '*(4-len(strid))+ ' ' + strfq + ' '*(4-len(strfq))+'\n')

    termid = termid + 1

