import json
class Node(object):
    def __init__(self,question = None,response=None):
        self.question = question  #用户发出的问题
        self.response=response
        self.child_list = []      #用户待选的问题的节点
    # 添加一个孩子节点
    def add_child(self,node):
        self.child_list.append(node)

# 递归将字典变成树 ，实际上也可以递归建图，再设置一个flag，用来记录是否建立过该节点
def ChangeDictToTree(dict):
        root=Node(dict["question"],dict["answer"])
        children=dict["children"]
        for member in children:
            root.add_child(ChangeDictToTree(member))
        return root


