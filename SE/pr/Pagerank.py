import os,sys
import pathlib
sys.path.append( os.path.join(".."))
from SE.pr import Generate_web_graph
from SE.UtilityFunctions import CommonHelpers
class Page_rank:
    def __init__(self,iterations,random_prob):
        self.iter = iterations
        self.prob = random_prob
        self.gen_web_graph = Generate_web_graph.Generate_web_graph()
        self.pickle_path = os.path.join(pathlib.Path(__file__).parent.resolve(),
            "..","data","page_rank.pickle")

    def print_stats(self):
        for each in self.graph.nodes:
            print(each)



    
    def run(self,load_path,save_path,cache=True):
        if cache==False:
            self.graph = self.gen_web_graph.run(load_path,save_path,cache)
            for i in range(self.iter):
                self.run_each()
            self.page_rank={}
            for each in self.graph.nodes:
                self.page_rank[each.name]=each.pagerank
            CommonHelpers.dump_pickle(self.pickle_path,self.page_rank)
        else:
            self.page_rank=CommonHelpers.load_pickle(self.pickle_path)

    def run_each(self):
        nodes = self.graph.nodes
        for node in nodes:
            node.update_page_rank(self.prob,len(nodes))
        self.graph.normalize_pagerank()
