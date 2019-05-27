import pickle
import os
from flask import Flask, request
from flask import render_template
from flask_cors import CORS

import tulingbot
from manage import *
from qsresouce import *

Ecommerce_queList=[]
Ecommerce_ansList=[]
Logistics_queList=[]
Logistics_ansList=[]
Hotel_queList=[]
Hotel_ansList=[]

#电商
Smartguide_queList=[]
Smartguide_ansList=[]
#酒店
Smartguide_hotel_queList = []
Smartguide_hotel_ansList = []


#######################单轮语料列表声明#################################
root=""
with open("corpus/Multi_dia.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    root=ChangeDictToTree(load_dict)
multi_round_start=root.child_list  #多轮对话开始列表
#multi_round_start.append(root)  #将root加入到开始列表
multi_round_process=[]   #多轮对话中间列表

###########################多轮语料列表声明##########################

readQSresouce('corpus/ecommerce.txt',Ecommerce_queList,Ecommerce_ansList)#读取电商沙盘语料库
readQSresouce('corpus/logistics.txt',Logistics_queList,Logistics_ansList)#读取物流沙盘语料库
readQSresouce('corpus/hotel.txt',Hotel_queList,Hotel_ansList)#读取物流沙盘语料库

readQSresouce('corpus/smartguide.txt',Smartguide_queList,Smartguide_ansList)#读取物流沙盘语料库
readQSresouce('corpus/smartguide_hotel.txt', Smartguide_hotel_queList, Smartguide_hotel_ansList)  # 读取物流沙盘语料库

#语料读取

StopWord_list=[]
readQSresouce('corpus/stopword.txt',StopWord_list,StopWord_list)
#停用词读取

with open('newembedding.pickle', 'rb') as handle:
    vectors = pickle.load(handle)
# 用vectors从embedding.pickle中读取全部词向量

app = Flask(__name__)
CORS(app)

@app.route("/",methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/check",methods=['post'])
def check():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='password':
        return render_template('qsSystem.html')
    return render_template("login.html",answer="wrong")

@app.route("/question",methods=['post'])
def add():
    ques=request.form['question'].replace('\n','')#去除回车
    ans=request.form['answer'].replace('\n','')
    Ecommerce_queList.append(ques)
    Ecommerce_ansList.append(ans)
    file1=open("ecommerce.txt","a")
    file1.write('\n')
    file1.write(ques)
    file1.write('\n')
    file1.write(ans)
    file1.close()
    return render_template('qsSystem.html',answer="success")


#电商沙盘机器人接口
@app.route("/chatbot")
def chat():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=Multi_round_check(content,multi_round_start,multi_round_process,vectors)  #多轮
    if answer==None:  #单轮
        answer=readvec.similarityCheck(content,vectors,Ecommerce_queList,Ecommerce_ansList) 
    if answer==None:  #其他
        #answer="这里为您展示互联网的搜索结果"
        answer=tulingbot.get_answer(content)
#######Log日志记录#####
    file1=open("Log/HistoryEcommerce.txt","a")
    file1.write(content)
    file1.write('\n')
    file1.write(answer)
    file1.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer})



#####################电商智能导读接口######################
@app.route("/smartguide")
def smartguide():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=readvec.getQA(content,vectors,Smartguide_queList,Smartguide_ansList)
    ##Log##
    Logfile = open("Log/HistorySmartguide.txt", "a")
    Logfile.write(content)
    Logfile.write("\n")
    Logfile.write(answer)
    Logfile.write("\n")
    Logfile.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer})

#####################酒店沙盘智能导读接口######################
@app.route("/smartguide_hotel")
def smartguide_hotel():
    tmpcontent = request.args.get('content')
    content = tmpcontent.replace('\n', '')
    answer = readvec.getQA(content, vectors, Smartguide_hotel_queList, Smartguide_hotel_ansList)
    ##Log##
    Logfile = open("Log/HistorySmartguide_hotel.txt", "a")
    Logfile.write(content)
    Logfile.write("\n")
    Logfile.write(answer)
    Logfile.write("\n")
    Logfile.close()
    print(content)
    print(answer)
    print("#####################")
    return json.dumps({'as': answer})

#########################酒店沙盘机器人接口#####################################
@app.route("/hotel")
def hotel():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=Multi_round_check(content,multi_round_start,multi_round_process,vectors)  #多轮
    if answer==None:  #单轮
        answer=readvec.similarityCheck(content,vectors,Hotel_queList,Hotel_ansList)
    if answer==None:
        answer="你的问题小智不知道哦( *>.<* )，点击下方按钮，可以选择查阅参考文档或选用互联网检索"
        # answer=tulingbot.get_answer(content)
    file2=open("Log/HistoryHotel.txt","a")
    file2.write(content)
    file2.write('\n')
    file2.write(answer)
    file2.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer}) 

#物流沙盘机器人接入口
@app.route("/logistics")
def logistics():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=readvec.similarityCheck(content,vectors,Logistics_queList,Logistics_ansList)
    if answer==None:
        answer=tulingbot.get_answer(content)
    file3=open("Log/HistoryLogistics.txt","a")
    file3.write(content)
    file3.write('\n')
    file3.write(answer)
    file3.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer}) 



# if __name__ == '__main__':
#     # app.run()
#     app.run(debug=True)
#    # debug=True,debug模式会产生双倍的内存消耗

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=False)

