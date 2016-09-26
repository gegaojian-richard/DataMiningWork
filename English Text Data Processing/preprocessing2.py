#encoding=utf-8
# 2016-9-14
# gegaojian
# english text data processing

from numpy import *
from decimal import *
from os import listdir
import re
import Stemmer
import time
# import nltk


def tokenization(fileName, stopWordList):
    pattern = r'''(?x)\
                ([A-Z]\.)+\
                | \w+(-\w+)*\
                | \$?\d+(\.\d+)?%?\
                | \.\.\.
                | [][.,;"'?():-_`]
                '''
    wordList = []
    content = open(fileName).read()
    wordList.extend([stemming(token.lower()) \
                    for token in re.split(r'\W*', content) \
                    if len(token) > 2 and re.search(r'\w*\d+\w*', token) == None \
                    and token.lower() not in stopWordList])
    return wordList


def stemming(word):
    stemmer = Stemmer.Stemmer('english')
    return stemmer.stemWord(word)

# 计算tfidf
# wtotalList: 每篇文章对应的次数
# tfList: 字典的列表，每个元素为一篇文章对应的字典
# idfList: 每个元素对应词汇表中每个词在多少篇文章中出现过
# vocabDict: 记录词汇表中每个词的顺序（位置）
def computeTFIDF(wtotalList, tfList, idfDict, vocabDict):
    d = len(tfList)
    featSparseMatrix = []
    for i in range(d):
        print "Compute TFIDF : %d/%d" % (i+1, d)
        featSparseVect = [str(vocabDict[word]) + ":" + \
                        str(float(tfList[i][word]) / wtotalList[i] * log(d / idfDict[word])) \
                        for word in sorted(tfList[i].keys()) \
                        if (float(tfList[i][word]) / wtotalList[i] * log(d / idfDict[word])) != 0.0]

        featSparseMatrix.append(featSparseVect)
    return featSparseMatrix

# 读取数据集，并完成分词、词干化，以及相关统计数据的采集
def loadDataSet(dataPath, stopWordPath):
    subFileList = listdir(dataPath) # 子文件夹列表
    classList = []                  # 论文类别列表 classList[0] = 0 表示语料库第一篇论文的类别为0
    class2Int = []                  # 类别映射列表 class2Int[0] = "Active Learning" 表示用0表示类别Active Learning
    paperName2Int = []              # 论文映射列表 paperName2Int[0] = "Active Transfer Learning under Model Shift" 表示语料库中第一篇文章是Active Transfer Learning under Model Shift
    vocab2Int = []                  # 词汇映射表 vocab2Int[0] = "absolute" 表示特征向量第一维元素代表词汇absolute
    tfList = []                     # 语料库，其元素为字典，统计每篇文章中每个词出现的频数
    wtotalList = []                 # 统计每篇文章的字数
    idfDict = {}                    # 统计每个词在多少片文章中出现过

    # 读取停用词列表
    stopWordList = open(stopWordPath).readlines()
    stopWordList = [stopWord.strip("\r\n") for stopWord in stopWordList]

    classCount = len(subFileList) - 1 # 去掉.DS_Store文件
    for i in range(1, classCount+1):  # 第一个元素为隐藏的.DS_Store文件
        class2Int.append(subFileList[i].split(".")[1].strip())
        fileList = listdir(dataPath + subFileList[i])
        paperList = [paper for paper in fileList if paper.split('.')[1] == 'txt']
        paperName2Int.extend([paper.split('.')[0] for paper in fileList if paper.split('.')[1] == 'txt'])

        for j in range(len(paperList)):
            tfDict = {}
            classList.append(i)
            print "Preprocessing paper : " + paperList[j].split('.')[0] # 打印论文名
            wordList = tokenization(dataPath + subFileList[i] + "/" + paperList[j], stopWordList)
            wtotalList.append(len(wordList))
            for word in wordList:
                tfDict[word] = tfDict.get(word,0) + 1
            for word in tfDict.keys():
                idfDict[word] = idfDict.get(word,0) + 1
            tfList.append(tfDict)
            vocab2Int.extend(set(wordList))
    vocab2Int = sorted(list(set(vocab2Int)), reverse=False)

    return paperName2Int, class2Int, classList, vocab2Int, wtotalList, tfList, idfDict


def main():

    dataPath = raw_input("请输入训练数据集的绝对路径(例：/Users/gegaojian/Sources/Code/DataMiningWork/ICML) ： ")
    stopWordPath = raw_input("请输入停用词文件的路径(例：stop-word-list.txt) ： ")

    paperName2Int, class2Int, classList, vocab2Int, wtotalList, tfList, idfDict = loadDataSet(dataPath, stopWordPath)

    # print len(paperName2Int)
    # print len(vocab2Int)
    # print len(idfDict)
    # print len(tfList)
    # print tfList[0]
    # print wtotalList

    vocabDict = dict(zip(vocab2Int,range(1,len(vocab2Int)+1)))

    f=open('vocabulary.txt','a')
    for i in range(len(vocab2Int)):
        f.write(str(i) + ": " + vocab2Int[i])
        f.write("\n")
    f.close()

    featSparseMatrix = computeTFIDF(wtotalList, tfList, idfDict, vocabDict)

    f=open('featSparseMatrix.txt','a')
    for i in range(len(featSparseMatrix)):
        f.write(paperName2Int[i])
        f.write(' :\n')
        for feat in featSparseMatrix[i]:
            f.write(str(feat))
            f.write('\t')
        f.write('\n')
    f.close()

def test():
    dict = {"c":5,"a":1,"b":3}
    print dict
    print sorted(dict)
    print dict.get("d",0)
    stopWordList = open("stop-word-list.txt").readlines()
    print stopWordList




if __name__ == '__main__':
    startTime = time.clock()
    main()
    # test()
    endTime = time.clock()
    print 'Running time: %f Seconds' % (endTime-startTime)
