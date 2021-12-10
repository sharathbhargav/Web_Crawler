from SE.pr.Graph import Graph,Node
import os,sys
sys.path.append( os.path.join(".."))
from SE.UtilityFunctions import CommonHelpers
class Generate_web_graph:
    def __init__(self):
        pass

    def run(self,path,save_path,cache=False):
        print(f"In Generate web graph with input path = {path}, save path ={save_path}")
        if cache==False:
            self.web_pages = CommonHelpers.load_pickle(path)
            print(type(self.web_pages))
            crawled_pages = self.web_pages.keys()
            self.graph = Graph()
            for each in self.web_pages:
                # print(" url = ",each,"  outgoing = ",len(self.web_pages[each].out_going_urls),"  incoming = ",len(self.web_pages[each].incoming_urls))
                for each_out in self.web_pages[each].out_going_urls:
                    if each_out in crawled_pages:
                        self.graph.add_edge(each,each_out)
                for each_in in self.web_pages[each].incoming_urls:
                    if each_in in crawled_pages:
                        self.graph.add_edge(each_in,each)
            CommonHelpers.dump_pickle(save_path,self.graph)
        else:
            self.graph = CommonHelpers.load_pickle(save_path)
        print("Generating graph done")
        return self.graph

    

