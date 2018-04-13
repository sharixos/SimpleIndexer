import re
import os
from collections import OrderedDict
import jieba
import jieba.analyse

class Document(object):
    """docstring for Document."""
    def __init__(self, docid, filepath, wordlist, tags):
        super(Document, self).__init__()
        self.docid = docid
        self.filepath = filepath
        self.tags = tags
        self.wordlist = wordlist


class BlogSearch(object):
    """docstring for BlogSearch."""
    def __init__(self, basepath):
        self.basepath = basepath
        self.documents = []
        self.paths = []
        self.worddoc = {}
        self.index()

    def index(self):
        for dirpath,dirnames,filenames in os.walk(self.basepath):
            for file in filenames:
                if len(file.split('.')) == 1:
                    fullpath = os.path.join(dirpath,file)
                    self.add_document(fullpath)

    def flush(self):
        count = 0
        for dirpath,dirnames,filenames in os.walk(self.basepath):
            for file in filenames:
                if len(file.split('.')) == 1:
                    fullpath = os.path.join(dirpath,file)
                    if fullpath not in self.paths:
                        self.add_document(fullpath)
                        count += 1
        return count

    def add_document(self,fullpath):
        f = open(fullpath, 'r', encoding='utf-8')
        content = ''
        iscode = False
        for line in f:
            if line[0:3] == '```':
                iscode = not iscode
            elif iscode == True or line[0] == '!':
                pass
            else:
                content += line

        content = re.sub('\W',' ',content).lower().replace('__','')
        tags = jieba.analyse.extract_tags(content, topK=20)

        wordlist = jieba.lcut_for_search(content)
        while ' ' in wordlist:
            wordlist.remove(' ')

        docid = len(self.paths)
        self.documents.append(Document(docid, fullpath, wordlist, tags))
        self.paths.append(fullpath)

        for word in wordlist:
            if word not in self.worddoc:
                self.worddoc[word] = []
            if docid not in self.worddoc[word]:
                self.worddoc[word].append(docid)

    def search(self,q):
        result = None
        content = re.sub('\W',' ',q).lower()
        keywords = jieba.analyse.extract_tags(content, topK=3)
        for k in keywords:
            if k in self.worddoc:
                if result == None:
                    result = self.worddoc[k]
                else:
                    result = list(set(result).intersection(set(self.worddoc[k])))
        resultdict = {}
        if result == None:
            return []
        for docid in result:
            resultdict[docid] = 0
            for k in keywords:
                tags = self.documents[docid].tags
                if k in tags:
                    resultdict[docid] += (len(tags) - tags.index(k))
        result = [k for k,v in sorted(resultdict.items(), key=lambda d: d[1], reverse=True)]
        return result


    def get_tags_topk(self,path,k):
        tag = ''
        if path in self.paths:
            docid = self.paths.index(path)
            tag = self.documents[docid].tags[0:k]
        return tag

    def get_path(self,docid):
        if docid < len(self.paths):
            return self.paths[docid]
        return ''

bs = BlogSearch('static/blogs/')
