from nltk.util import pr
import basic_crawler
from UtilityFunctions import CommonHelpers
from UtilityFunctions import PreprocessHelpers
import Tf_Idf
url ="https://cs.uic.edu/"
class Start:
    def __init__(self,URL):
        self.url = URL

    def start_crawl(self):
        crawler = basic_crawler.Crawler([self.url])

        # crawler.run()
        # crawler.dump_data_to_pickle()
        crawler.init_data_from_pickle()
        self.doc_list = crawler.doc_list

    def run_tf_idf(self):
        self.tf_idf = Tf_Idf.TF_IDF()
        '''
        self.tf_idf.load_docs(self.doc_list)
        self.tf_idf.generate_inverted_index()
        self.tf_idf.calculate_doc_length()
        '''
        self.tf_idf.init_data_from_pickle()
    
    def query_string(self,query):
        preprocessor = PreprocessHelpers.Preprocessor()
        preprocessor.set_text(query)
        cleaned_query = preprocessor.run_lemma_pipeline(True)
        self.doc_scores = self.tf_idf.query_similarity(cleaned_query)
        print(self.doc_scores)


start = Start(url)
start.start_crawl()
for each in start.doc_list:
    print(each,len(start.doc_list[each]))

start.run_tf_idf()
start.query_string("computer science")