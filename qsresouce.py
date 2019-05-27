def readQSresouce(path,list1,list2):  # read top n word vectors
    with open(path, errors='ignore',encoding='UTF-8') as f:
        tag=True
        for line in f:
            if tag==True:
                list1.append(line.replace("\n", ""))
                tag=False
            else:
                list2.append(line.replace("\n", ""))
                tag=True
    return 
