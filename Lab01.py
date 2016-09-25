#-*- coding=utf-8 -*-
#!/usr/bin/env python

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import re
from collections import defaultdict
import  math
import pandas as pd
import time

allFileNum = 0
allFiles = []
tfDict = {}
idfDict = defaultdict(int)
allTfidf = {}
wordsNum = defaultdict(int)

#获取所有文件的名字
def printPath(level, path):
    global allFileNum

    #打印一个目录下的所有文件夹和文件

    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if(f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if(f[0] == '.'):
            pass
        elif(os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(path + '/' + f)
    # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if(i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            #print '-' * (int(dirList[0])), dl
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
       # print '-' * (int(dirList[0])), fl
        allFiles.append(fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1

if __name__ == '__main__':
    startTime = time.clock()
    path = os.path.join(os.path.abspath('.'), 'ICML')
    printPath(1,path)

    english_stopwords = stopwords.words('english')

    for fs in allFiles:
        st = LancasterStemmer()
        re_word = re.compile(r'^[a-z]+$')
        with open(fs, 'r') as f:
            texts_filtered_stopwords = [st.stem(word.lower()) for word in word_tokenize(f.read().decode('utf-8')) if re_word.match(word.lower()) and len(word) > 2 and word.lower() not in english_stopwords]

        tfDoc = defaultdict(int)

        for w in texts_filtered_stopwords:
            # wordsNum[fs] += 1
            tfDoc[w] += 1

        tfDict[fs] = tfDoc

        # wordsNoDuplication = list(set(texts_filtered_stopwords))
        #for w in wordsNoDuplication:
        for w in tfDoc.keys():
            idfDict[w] += 1

    allWords = idfDict.keys()
    allWords.sort()

    print idfDict.values()

    for f in tfDict:
        doc = tfDict.get(f)
        print 'wordsNum : %d' % wordsNum.get(f)
        tfidf = [((doc.get(wd,0) + 0.0 )/ wordsNum.get(f)) * math.log((allFileNum/idfDict.get(wd))) for wd in allWords]
        allTfidf[f] = tfidf


    print allTfidf.values()[0]

    endTime = time.clock()
    print 'Running time: %f Seconds' % (endTime-startTime)
    # result = pd.DataFrame(allTfidf)
    # print result.T







