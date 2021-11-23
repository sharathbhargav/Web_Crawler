import os,sys
import pathlib
sys.path.append( os.path.join(".."))
from pr import Generate_web_graph
from UtilityFunctions import CommonHelpers
class Page_rank:
    def __init__(self,iterations,random_prob):
        self.iter = iterations
        self.prob = random_prob
        self.gen_web_graph = Generate_web_graph.Generate_web_graph()
    
    def generate_graph(self,load_path,save_path):
        self.graph = self.gen_web_graph.run(load_path,save_path)

    def load_graph(self,path):
        self.graph = self.gen_web_graph.load_from_pickles(path)

    def print_stats(self):
        for each in self.graph.nodes:
            print(each)

    def run(self):
        for i in range(self.iter):
            self.run_each()
        self.page_rank={}
        for each in self.graph.nodes:
            self.page_rank[each.name]=each.pagerank
        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),
        "..","data","page_rank.pickle"),self.page_rank)

    def load_from_pickle(self):
        self.page_rank=CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),
        "..","data","page_rank.pickle"))

    def run_each(self):
        nodes = self.graph.nodes
        for node in nodes:
            node.update_page_rank(self.prob,len(nodes))
        self.graph.normalize_pagerank()
