## Introduction
This is a simple indexer, and can be used to index the xml format documents.

## Structure
* index
* compress
    + inverted index
    + dictionary
* search

## Tools
* BeautifulSoup

## Run
```shell
bash run.sh
```

### 附
* [博客站内搜索](http://www.sharix.site/blogs/categories&nlp&blog-search-engine)

对于大量数据搜索的话，就需要用到Lucene这样的开源搜索引擎了，附上之前写的针对trec-cds2015检索竞赛数据的例子，效果不太好，但功能基本完整
* https://github.com/sharixos/InformationRetrieve
