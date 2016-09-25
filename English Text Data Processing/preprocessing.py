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


def tokenization(fileName, stopWordList):
    wordList = []
    contentOfLines = open(fileName).readlines()
    for contentInLen in contentOfLines:
        wordList.extend([stemming(token.lower()) for token in re.split(r'\W*', contentInLen) if len(token) > 2 and re.search(r'\w*\d+\w*', token) == None and token.lower() not in stopWordList])
    return wordList

def stemming(word):
    stemmer = Stemmer.Stemmer('english')
    return stemmer.stemWord(word)


def computeTFIDF(wtotalList, tfList, idfDict, vocab2Int):
    getcontext().prec = 50
    d = len(tfList)
    w = len(vocab2Int)
    # featMatrix = zeros((d, w))
    featMatrix = []
    featSparseMatrix = []
    for i in range(d):
        print "%d/%d" % (i+1, d)
        featSparseVect = []

        featVect = [float(tfList[i].get(word, 0)) / wtotalList[i] * log(d / idfDict[word]) for word in vocab2Int]
        featMatrix.append(featVect)
        # for word in sorted(tfList[i].keys()):
        #     # index = vocab2Int.index(word)
        #     tfidf = float(tfList[i][word]) / wtotalList[i] * log(d / idfDict[word])
        #     # print tfidf
        #     if tfidf != 0.0:
        #         index = vocab2Int.index(word)
        #         featSparseVect.append(str(index) + ":" + str(tfidf))

        # featSparseMatrix.append(featSparseVect)
    return featMatrix

def saveVect(fileName, vect):
    f=open(fileName,'a')
    for i in range(len(vect)):
        f.write(str(i) + ": ")
        f.write(str(vect[i]))
        f.write("\n")
    f.close()

def saveMatrix(fileName, matrix):

    d = len(matrix)
    w = len(matrix[0])

    f=open(fileName,'a')
    for i in range(d):
        f.write(str(i) + ": ")
        for j in range(w):
            f.write(str(matrix[i][j]))
            f.write("\t")
        f.write("\n")
    f.close()


# 读取原始数据集
def loadDataSet(fileName):
    subFileList = listdir(fileName) # 子文件夹列表
    classList = []                  # 论文类别列表 classList[0] = 0 表示语料库第一篇论文的类别为0
    class2Int = []                  # 类别映射列表 class2Int[0] = "Active Learning" 表示用0表示类别Active Learning
    paperName2Int = []              # 论文映射列表 paperName2Int[0] = "Active Transfer Learning under Model Shift" 表示语料库中第一篇文章是Active Transfer Learning under Model Shift
    # corpus = []
    vocab2Int = []                  # 词汇映射表 vocab2Int[0] = "absolute" 表示特征向量第一维元素代表词汇absolute
    tfList = []                     # 统计每篇文章中每个词出现的频数
    wtotalList = []                 # 统计每篇文章的字数
    idfDict = {}                    # 统计每个词在多少片文章中出现过

    # 读取停用词
    stopWordList = open("stop-word-list.txt").readlines()
    stopWordList = [stopWord.strip("\r\n") for stopWord in stopWordList]

    classCount = len(subFileList) - 1 # 去掉.DS_Store文件
    for i in range(1, classCount+1):
        class2Int.append(subFileList[i].split(".")[1].strip())
        fileList = listdir("/Users/gegaojian/Sources/Code/DataMiningWork/ICML/" + subFileList[i])
        paperList = [paper for paper in fileList if paper.split('.')[1] == 'txt']
        paperName2Int.extend([paper.split('.')[0] for paper in fileList if paper.split('.')[1] == 'txt'])

        print subFileList[i] # 打印类

        for j in range(len(paperList)):
            tfDict = {}
            classList.append(i)
            print paperList[j] # 打印论文名
            wordList = tokenization("/Users/gegaojian/Sources/Code/DataMiningWork/ICML/" + subFileList[i] + "/" + paperList[j], stopWordList)
            wtotalList.append(len(wordList))
            for word in wordList:
                tfDict[word] = tfDict.get(word,0) + 1
            for word in tfDict.keys():
                idfDict[word] = idfDict.get(word,0) + 1
            tfList.append(tfDict)
            vocab2Int.extend(set(wordList))
            # corpus.append(wordList)
    vocab2Int = sorted(list(set(vocab2Int)), reverse=False)

    return paperName2Int, class2Int, classList, vocab2Int, wtotalList, tfList, idfDict


def main():

    paperName2Int, class2Int, classList, vocab2Int, wtotalList, tfList, idfDict = loadDataSet("/Users/gegaojian/Sources/Code/DataMiningWork/ICML")

    print len(paperName2Int)
    print len(vocab2Int)
    print len(idfDict)
    print len(tfList)
    print tfList[0]
    print wtotalList

    f=open('vocabulary.txt','a')
    for i in range(len(vocab2Int)):
        f.write(str(i) + ": " + vocab2Int[i])
        f.write("\n")
    f.close()

    featSparseMatrix = computeTFIDF(wtotalList, tfList, idfDict, vocab2Int)
    # saveMatrix('featMatrix.txt', featMatrix)
    # print featSparseMatrix[0]
    saveMatrix("featMatrix.txt", featSparseMatrix)

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
    # main()
    test()
    endTime = time.clock()
    print 'Running time: %f Seconds' % (endTime-startTime)
    # test()
