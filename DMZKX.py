# -*- coding: utf-8 -*-
import os    
import nltk
import string
import re
import sys
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
reload(sys)  
sys.setdefaultencoding('utf8')
 


def tokenization(line):
    line=line.lower()
   # identify = string.maketrans('', '') 
    delEStr = string.punctuation + string.digits  #ASCII 标点符号和数字   
    untokenline=line.translate(None, delEStr)
    untokenline = "".join(re.findall('[a-z ]*',untokenline)) 
    token = nltk.word_tokenize(untokenline)     #分词操作
    return token  
    
def delstopstem(line):#删除停止词和词干提取
    stop = stopwords.words('english')
    line = [i for i in line if not i in stop]    
    stemmer = PorterStemmer()
    stemmed=[]
    for word in line:
        if not word:
            continue   
        if len(word)<=1 :
            line.remove(word)
        else:
            stemmed.append(stemmer.stem_word(word))
    return stemmed

    
    
if __name__ == '__main__': 
    termnum = {}
    dictionary = {}
    tf_list = list()
    print "preporcessing for extracting dictionary..."   
    for dirName in os.listdir('./ICML/'): 
        print dirName
        if os.path.isdir('./ICML/'+dirName):                     
            for fileName in os.listdir('./ICML/'+dirName+'/'):
                #print fileName
                if fileName.find('.txt')==-1:
                    continue
                else:
                    termnum[fileName]=0
                    if not os.path.isdir(fileName):        
                        fr=open('./ICML/'+dirName+'/'+fileName).readlines() 
                        for line in fr:  #遍历该文件的每一行 
                            tokenline=tokenization(line)      
                            linestemmed=delstopstem(tokenline)#预处理完成
                            for word in linestemmed:
                                termnum[fileName] = termnum[fileName] + 1#计算文件字数
                                dictionary[word] = 0#形成字典                    
    print "dictionary extracted, length is：",
    print len(dictionary)

    print '****************************************************************'
    tf_list = list()
    idf = dictionary.copy()
    N=0 
    for dirName in os.listdir('./ICML/'):
        if os.path.isdir('./ICML/'+dirName):                     
            for fileName in os.listdir('./ICML/'+dirName+'/'): 
                if fileName.find('.txt')==-1:
                    continue
                N=N+1
                tf_list.append(dictionary.copy())
                if not os.path.isdir(fileName):        
                    fr=open('./ICML/'+dirName+'/'+fileName).readlines()   
                    for line in fr:  #遍历该文件的每一行  
                        tokenline=tokenization(line)      
                        linestemmed=delstopstem(tokenline)#预处理完成
                        for word in linestemmed:
                            if word in dictionary:
					tf_list[-1][word] = tf_list[-1][word] + 1.0/termnum[fileName]
					if tf_list[-1][word] < 1.1/termnum[fileName]:
    				          idf[word] = idf[word] + 1.0
    print N	
    print '****************************************************************'
    for eachword in dictionary.keys():
        idf[eachword] = math.log(N/(idf[eachword] + 1.0) + 1.0)
    for eachdoc in tf_list:
	  for eachword in eachdoc:
		eachdoc[eachword] = eachdoc[eachword] * idf[eachword]

    index = 0
    for dirName in os.listdir('./ICML/'):
        print("write to file ../result/" + dirName)
        if not os.path.exists('./result/'):
            os.makedirs('./result/')
        output = open('./result/' + dirName, 'w')
        for fileName in os.listdir('./ICML/' + dirName):
            if fileName.find('.txt')==-1:
                continue
            cord = 0
            for tfidf in tf_list[index].values():
                if tfidf != 0:
                    print >> output, str(cord) + ":" + str(round(tfidf, 4)) + " ",
                cord = cord + 1
            print >> output, ""
            index = index + 1 
        print >> output,"/n"

    dictionaryList = sorted(dictionary.keys())
    dictionary = dict(dictionaryList,range(1,len(dictionaryList)+1))

    for dirName in os.listdir('./ICML/'):
        print("write to file ../result/" + dirName)
        if not os.path.exists('./result/'):
            os.makedirs('./result/')
        output = open('./result/' + dirName, 'w')
        for fileName in os.listdir('./ICML/' + dirName):
            if fileName.find('.txt')==-1:
                continue
            cord = 0
            for word in sorted(tf_list[index].keys()):
                if (tfidf == tf_list[index][word]) != 0.0:
                    cord = dictionary[word]
                    print >> output, str(cord) + ":" + str(round(tfidf, 4)) + " ",
                
            # for tfidf in tf_list[index].values():
            #     if tfidf != 0:
            #         cord = dictionary[]
            #         print >> output, str(cord) + ":" + str(round(tfidf, 4)) + " ",
            #     cord = cord + 1
            print >> output, ""
            index = index + 1 
        print >> output,"/n"
            
    print 'over'
            

                    
                
            
            
		 
   
   
   
   
   
   
   
  
 
 

































           
        