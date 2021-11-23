import numpy as np

class Node:
    def __init__(self,url):
        self.name = url
        self.outgoing = []
        self.incoming = []
        self.pagerank = 1.0

    def link_outgoing(self,out):
        for each in self.outgoing:
            if(each.name == out.name):
                return None
        self.outgoing.append(out)

    def link_incoming(self,income):
        for each in self.incoming:
            if(each.name == income.name):
                return None
        self.incoming.append(income)

    def update_page_rank(self,random_prob,n):
        pr_sum = sum((node.pagerank/ len(node.outgoing)) for node in self.incoming)
        random_jump = random_prob/n
        self.pagerank = random_jump+ (1-random_prob)*pr_sum

    def __str__(self):
        return str(self.name) + ", outgoing count="+str(len(self.outgoing))+ \
        " incoming count ="+str(len(self.incoming)) \
            + " page rank ="+str(self.pagerank)
class Graph:
    def __init__(self):
        self.nodes = []
    
    def has(self,name):
        for node in self.nodes:
            if node.name == name:
                return True
        return False

    def find(self,name):
        if not self.has(name):
            new_node  = Node(name)
            self.nodes.append(new_node)
            return new_node
        else:
            ret_node =None
            for node in self.nodes:
                if node.name == name:
                    ret_node = node
                    break
            return ret_node

    def add_edge(self,first,second):
        first_node = self.find(first)
        second_node = self.find(second)
        first_node.link_outgoing(second_node)
        second_node.link_incoming(first_node)

    def display(self):
        for node in self.nodes:
            if len(node.outgoing)>0:
                print(f'{node.name} links to {[out.name for out in node.outgoing]}')
                print("\n\n\n\n")


    def normalize_pagerank(self):
        pagerank_sum = sum(node.pagerank for node in self.nodes)

        for node in self.nodes:
            node.pagerank /= pagerank_sum

    def get_pagerank_list(self):
        pagerank_list = np.asarray([node.pagerank for node in self.nodes], dtype='float32')
        return np.round(pagerank_list, 10)