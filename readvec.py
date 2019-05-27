import jieba
import numpy as np

import app


#本代码加入了太多vectors，其实不需要，但由于函数中参数的传递也仅仅为地址，故不影响速度
#词向量字典模型建模
def read_vectors(path, topn, vectors):  # read top n word vectors
    lines_num =  0
    with open(path, encoding='utf-8', errors='ignore') as f:
        first_line = True
        for line in f:
            if first_line:
                first_line = False
                continue
            lines_num += 1
            tokens = line.rstrip().split(' ')
            vectors[tokens[0]] = np.asarray([float(x) for x in tokens[1:]])
            if topn != 0 and lines_num >= topn:
                break
    return 


#print('数据读取完成')

#将句子转化为向量
def sentence_vector(s,vectors):#该函数用于计算句子向量
        words = jieba.lcut(s.replace("能不能",""))
        v = np.zeros(300)
        for word in words:
            if word in app.StopWord_list:
                 continue
            if word in vectors.keys():#如果表中有则加入
                v += vectors[word]
            else:
                for tmp in word:#如果表中没有则分成单个字后加入
                    if tmp in vectors.keys():
                        v+=vectors[tmp]
       # v /= len(words)，不需要，计算向量角度和向量的长度无关
        return v



#用于计算句子相似度，即输入两个句子计算其cos
def vector_similarity(s1, s2,vectors):
    v1, v2 = sentence_vector(s1,vectors), sentence_vector(s2,vectors)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))





def similarityCheck(s,vectors,queList,ansList):
    finalsimiar=0 
    flag=0
    for index in range(len(queList)):
        tmpsimilar=vector_similarity(s,queList[index],vectors)
        if tmpsimilar>finalsimiar:
            finalsimiar=tmpsimilar
            flag=index
            answer=ansList[flag]
    if finalsimiar>0.75:
        return answer.replace("\n","")


def getQA(s,vectors,queList,ansList):
    ##global qastring
    finalsimiar=0
    flag=0
    for index in range(len(queList)):
        tmpsimilar=vector_similarity(s,queList[index],vectors)
        if tmpsimilar>finalsimiar:
            finalsimiar=tmpsimilar
            flag=index
            ##answer=ansList[flag]
            question=queList[flag]
            ##qastring=question.replace("\n","")+"\n"+answer.replace("\n","")
    if finalsimiar>0.6:
        return question.replace("\n", "")
        ##return qastring

    else:
        return  "我也不知道。"
