
from itertools import chain
from SE import Wor2Vec
from nltk.util import pr
from SE import basic_crawler, Web_page
from SE.UtilityFunctions import CommonHelpers
from SE.UtilityFunctions import PreprocessHelpers
from SE import Tf_Idf
from SE.pr import Generate_web_graph,Pagerank
import time
import pathlib,os
url ="https://cs.uic.edu/"
import sys
sys.setrecursionlimit(10000)
class Start:
    def __init__(self,URL):
        self.url = URL
        

    def start_crawl(self,n,cache=False):
        self.crawler = basic_crawler.Crawler([self.url])
        if cache == False:
            self.crawler.run(n)
        else:
            self.crawler.init_data_from_pickle()
        self.doc_list = self.crawler.doc_list


    def run_tf_idf(self,cache=False):
        self.tf_idf = Tf_Idf.TF_IDF()
        if cache==False:
            if len(self.doc_list)==0:
                raise Exception
            else:
                self.tf_idf.load_docs(self.doc_list)
                self.tf_idf.generate_inverted_index()
                self.tf_idf.calculate_doc_length()
        else:
            self.tf_idf.init_data_from_pickle()
    
    def query_string_tf_idf(self,query):
        preprocessor = PreprocessHelpers.Preprocessor()
        preprocessor.set_text(query)
        cleaned_query = preprocessor.run_lemma_pipeline(True)
        self.doc_scores = self.tf_idf.query_similarity(cleaned_query)
        return self.doc_scores

    def run_word2vec(self,cache=False):
        self.word2vec = Wor2Vec.Word_2_Vec()
        if cache==False:
            self.word2vec.set_weighted_avg(False)
            self.word2vec.set_model()
            self.word2vec.set_data(self.doc_list)
            self.word2vec.get_avg_feature_vectors()
        else:
            self.word2vec.init_data_from_pickle()

    def query_string_word2vec(self,query):
        docs = self.word2vec.get_top_n_documents(query)
        return docs

    def page_rank(self,cache=False):
        self.pr = Pagerank.Page_rank(20,0.15)
        self.pr.run(os.path.join("SE","data/web_pages.pickle"),
                                   os.path.join("SE","data/web_graph.pickle"),
                                   cache)
                
    
    def start_all(self,pages=30,cache=False):
        start_time = time.time()
        self.start_crawl(pages,True)
        print("Crawl complete")
        print("Crawling %s pages took %s seconds"%(len(self.doc_list),time.time()-start_time))
        self.page_rank(True)
        print("Page rank complete")
        self.run_tf_idf(True)
        print("Tf idf complete")
        self.run_word2vec(cache)
        print("Word2vec complete")   
        end_time = time.time()
        print("Starting all with cache = %s took %s seconds"%(cache,end_time-start_time)) 

    def called_from_flask(self):
        start_time = time.time()
        self.page_rank(True)
        print("Page rank complete")
        self.run_tf_idf(True)
        print("Tf idf complete")
        self.run_word2vec(True)
        print("Word2vec complete")   
        end_time = time.time()
        print("Loading all took %s seconds"%(end_time-start_time)) 

    def query(self,query,type):
        if type==0:
            results = self.query_string_tf_idf(query)
            return results

        elif type==1:
            results1 = self.query_string_word2vec(query)
            return results1

        elif type==2:
            results2 = self.query_string_tf_idf(query)
            search = {}
            for each in results2:
                try:
                    search[each] = (results2[each] * self.pr.page_rank[each])/ (results2[each] + self.pr.page_rank[each])
                except:
                    print(f"Page rank failed for {each}")
            search = {k: v for k, v in sorted(search.items(), key=lambda item: item[1],reverse=True)}
            return search


    def menu_driven(self):
        while True:
            print("\nMenu\nQ to quit\n Any other query")
            choice = input(">>> ").lower().rstrip()
            type=0
            if choice=="q":
                break
            elif choice == "0":
                print("Setting to tfidf")
                type=0
            elif choice=="1":
                print("Setting to pure word2vec")
                type=1
            elif choice=="2":
                print("Setting to word2vec+pagerank")
                type=2
            else:
                query_start = time.time()
                res = self.query(choice,type)
                query_end = time.time()
                print("Results took %s"%(query_end-query_start))
        print("E.N.D")

# start = Start(url)
# s1= time.time()
# start.start_all(pages=3500,cache=False)
# s2=time.time()
# print("Crawling took %s seconds"%(s2-s1))
# start.menu_driven()
