
from itertools import chain
import Wor2Vec
from nltk.util import pr
import basic_crawler
from UtilityFunctions import CommonHelpers
from UtilityFunctions import PreprocessHelpers
import Tf_Idf
from pr import Generate_web_graph,Pagerank
import time
url ="https://cs.uic.edu/"
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
            self.word2vec.set_weighted_avg(True)
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
        if cache==False:
            self.pr.generate_graph("data/web_pages.pickle","data/web_graph.pickle")
            self.pr.run()

        else:
            self.pr.load_from_pickle()

    
    def start_all(self,pages=30,cache=False):
        start_time = time.time()
        self.start_crawl(pages,cache)
        print("Crawl complete")
        self.page_rank(cache)
        print("Page rank complete")
        self.run_tf_idf(cache)
        print("Tf idf complete")
        self.run_word2vec(cache)
        print("Word2vec complete")   
        end_time = time.time()
        print("Starting all with cache = %s took %s seconds"%(cache,end_time-start_time)) 

    def query(self,query,type):
        if type==0:
            results = self.query_string_tf_idf(query)
            # return list(results.keys())[:10]
            i=0
            for each in results:
                i+=1
                if i>11:
                    break
                print(each,results[each])
        elif type==1:
            results1 = self.query_string_word2vec(query)
            # return list(results1.keys())[:10]
            i=0
            for each in results1:
                i+=1
                if i>11:
                    break
                print(each,results1[each])
        elif type==2:
            results2 = self.query_string_word2vec(query)
            search = {}
            for each in results2:
                search[each] = results2[each] * self.pr.page_rank[each]
            search = {k: v for k, v in sorted(search.items(), key=lambda item: item[1],reverse=True)}
            # return list(search.keys())[:10]
            i=0
            for each in search:
                i+=1
                if i>11:
                    break
                print(each,search[each])

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
                res = start.query(choice,type)
                query_end = time.time()
                print(res)
                print("Results took %s"%(query_end-query_start))
        print("E.N.D")

start = Start(url)

start.start_all(pages=100,cache=True)
start.menu_driven()
