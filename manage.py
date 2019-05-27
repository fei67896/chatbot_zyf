from DiaTree import *
import readvec
import numpy as np
import argparse
import random
import jieba
import qsresouce
import app




def Multi_round_check(content,multi_round_start,multi_round_process,vectors):
######################如果中间列表非空的话######################
    if len(multi_round_process): 
        for member in multi_round_process:
            if readvec.vector_similarity(content,member.question,vectors)>0.8:
                response=member.response 
                multi_round_process[:]=member.child_list #更新给用户选择的列表
                return response 

######################中间列表空###############################        
    for member in multi_round_start:
        if readvec.vector_similarity(content,member.question,vectors)>0.75: #如果用户问题出现在开始列表当中 
            response=member.response
            multi_round_process[:]=member.child_list#更新给用户选择的列表
            return response
            
######################中间列表只要没有更新则滞空,进入单轮###############################  
    del multi_round_process[:]




# content=input('请输入')
# while content is not '0':
#     print(check(content,multi_round_start,multi_round_process))
#     content=input('请')



